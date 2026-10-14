"""Thành phần dùng chung cho các bài lab RTC (chạy trên CPU, không cần GPU).

Môi trường đồ chơi "vòng qua vật cản":
- Một điểm đi từ trái (x = 0) sang phải (x = 1), mỗi bước x tăng 0,025 (40 bước).
- Giữa đường có vật cản tròn tâm (0,5; 0), bán kính 0,14. Đi vòng TRÊN hoặc DƯỚI đều được
  (dữ liệu có 2 kiểu, giống dữ liệu người thu thật).
- Đích ở x = 1 nhưng độ cao y của đích dao động theo thời gian, nên phải phản ứng.
- Hành động = vận tốc mỗi bước (vx, vy), giống hành động "delta" của LIBERO.
Thành công = không chạm vật cản và tới x = 1 cách đích theo y dưới 0,08.

Mô hình: flow matching nhỏ (MLP) theo ĐÚNG quy ước của SmolVLA/LeRobot:
time = 1 là nhiễu, time = 0 là sạch, mô hình học vận tốc u = nhiễu - hành động.
Lấy mẫu và RTC đều gọi thẳng hàm của LeRobot (euler_integrate, RTCProcessor),
nên những gì thấy ở đây chuyển nguyên sang SmolVLA.
"""
import math

import torch
from torch import nn

from lerobot.configs import RTCAttentionSchedule
from lerobot.policies.common.flow_matching import FlowConvention, euler_integrate, make_flow_matching_inputs
from lerobot.policies.rtc import RTCConfig
from lerobot.policies.rtc.modeling_rtc import RTCProcessor

from rtc_full_jacobian import FullJacobianRTC

# ---------------------------------------------------------------- môi trường
H = 16            # độ dài chunk (SmolVLA: 50)
A = 2             # số chiều hành động
T = 40            # số bước mỗi episode
VX = 0.025        # vận tốc x cố định
VY_MAX = 0.05     # giới hạn vận tốc y của "động cơ"
OBS_C, OBS_R = (0.5, 0.0), 0.14
NUM_STEPS = 10    # số bước khử nhiễu (SmolVLA: 10)
GOAL_TOL = 0.08    # tới đích nếu lệch y dưới ngưỡng này


def goal_y(g0, phase, t):
    return g0 + 0.08 * torch.sin(2 * math.pi * t / 60 + phase)


class ToyEnv:
    """B episode chạy song song. step(a) nhận vận tốc (B, 2)."""

    def __init__(self, B, seed=0):
        g = torch.Generator().manual_seed(seed)
        self.B = B
        self.pos = torch.stack([torch.zeros(B), (torch.rand(B, generator=g) - 0.5) * 0.06], 1)
        self.g0 = (torch.rand(B, generator=g) - 0.5) * 0.4
        self.phase = torch.rand(B, generator=g) * 2 * math.pi
        self.t = 0
        self.hit = torch.zeros(B, dtype=torch.bool)
        self.path = [self.pos.clone()]
        self.actions = []

    def goal(self, t=None):
        return goal_y(self.g0, self.phase, self.t if t is None else t)

    def obs(self):
        gv = (self.goal(self.t + 1) - self.goal()) * 10
        return torch.stack([self.pos[:, 0], self.pos[:, 1], self.goal(), gv], 1)

    def step(self, a):
        a = a.clone()
        a[:, 1] = a[:, 1].clamp(-VY_MAX, VY_MAX)
        a[:, 0] = VX                      # x luôn tiến đều, chỉ y do chính sách quyết định
        new = self.pos + a
        self.hit |= seg_hits_circle(self.pos, new)
        self.pos = new
        self.t += 1
        self.path.append(self.pos.clone())
        self.actions.append(a)

    def done(self):
        return self.t >= T

    def success(self):
        return (~self.hit) & ((self.pos[:, 1] - self.goal()).abs() < GOAL_TOL)

    def max_jerk(self):
        """|thay đổi vận tốc y| lớn nhất giữa 2 bước liền nhau (đơn vị: bước)."""
        a = torch.stack(self.actions, 1)[..., 1]
        return (a[:, 1:] - a[:, :-1]).abs().max(1).values


def seg_hits_circle(p, q):
    c = torch.tensor(OBS_C)
    d = q - p
    t = ((c - p) * d).sum(1) / (d * d).sum(1).clamp(min=1e-12)
    closest = p + t.clamp(0, 1)[:, None] * d
    return (closest - c).norm(dim=1) < OBS_R


# ---------------------------------------------------------------- chuyên gia (sinh dữ liệu)
def smooth(u):
    u = u.clamp(0, 1)
    return 3 * u**2 - 2 * u**3


def y_ref(x, mode, g, gv, k):
    """Đường tham chiếu cố định cho mỗi kiểu: lên/xuống tới y = +-0,24 ở x = 0,5 rồi về đích.
    Đích được ngoại suy theo vận tốc gv (gv = độ đổi mỗi bước x 10)."""
    yw = mode * 0.24
    g_k = g + gv / 10 * k
    seg1 = yw * smooth(x / 0.5)
    seg2 = yw + (g_k - yw) * smooth((x - 0.5) / 0.4)
    return torch.where(x <= 0.5, seg1, seg2)


def expert_chunk(obs, mode):
    """Kế hoạch H bước vận tốc từ trạng thái obs: bám đường tham chiếu của kiểu mode (+1 trên, -1 dưới)."""
    px, py, g, gv = (obs[:, i:i + 1] for i in range(4))
    m = mode[:, None]
    y, out = py, []
    for k in range(1, H + 1):
        x_prev = (px + VX * (k - 1)).clamp(max=1.0)
        x = (px + VX * k).clamp(max=1.0)
        ff = y_ref(x, m, g, gv, k) - y_ref(x_prev, m, g, gv, k - 1)
        vy = (ff + 0.3 * (y_ref(x_prev, m, g, gv, k - 1) - y)).clamp(-VY_MAX, VY_MAX)
        y = y + vy
        out.append(vy)
    vy = torch.cat(out, 1)
    return torch.stack([torch.full_like(vy, VX), vy], -1)       # (B, H, 2)


def expert_mode(obs, gen):
    """Trước x = 0,25 cả hai kiểu đều hợp lệ (chọn ngẫu nhiên, dữ liệu 2 mode);
    sau đó đi theo phía đang đứng."""
    px, py = obs[:, 0], obs[:, 1]
    rnd = torch.where(torch.rand(len(obs), generator=gen) < 0.5, 1.0, -1.0)
    side = torch.where(py >= 0, 1.0, -1.0)
    return torch.where(px < 0.25, rnd, side)


def make_dataset(n_episodes=4096, seed=0):
    """Cho chuyên gia chạy (có nhiễu nhỏ để phủ trạng thái lệch), ghi (obs, chunk)."""
    gen = torch.Generator().manual_seed(seed)
    env = ToyEnv(n_episodes, seed=seed + 1)
    mode = torch.where(torch.rand(n_episodes, generator=gen) < 0.5, 1.0, -1.0)
    O, C = [], []
    while not env.done():
        o = env.obs()
        # Nhãn: khi còn ở vùng mơ hồ (x < 0,25), chunk ghi vào dữ liệu đi lên hay đi xuống là
        # ngẫu nhiên 50/50, bất kể đang lệch về phía nào. Như dữ liệu người thu: cùng một cảnh,
        # người này vòng trên, người kia vòng dưới. Chính sách học được sẽ có 2 mode thật sự.
        label = torch.where(o[:, 0] < 0.25, expert_mode(o, gen), mode)
        O.append(o)
        C.append(expert_chunk(o, label))
        a = expert_chunk(o, mode)[:, 0].clone()
        a[:, 1] += torch.randn(n_episodes, generator=gen) * 0.006
        env.step(a)
    return torch.cat(O), torch.cat(C)


# ---------------------------------------------------------------- mô hình flow matching
class Normalizer:
    def __init__(self, chunks):
        self.mean = chunks.reshape(-1, A).mean(0)
        self.std = chunks.reshape(-1, A).std(0).clamp(min=1e-3)

    def norm(self, a):
        return (a - self.mean) / self.std

    def unnorm(self, a):
        return a * self.std + self.mean


class VelocityMLP(nn.Module):
    """v(x_t, time, obs). time có thể là (B,) (mọi token cùng mức nhiễu)
    hoặc (B, H) (mỗi token một mức nhiễu, cần cho RTC lúc huấn luyện)."""

    def __init__(self, hidden=512):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(H * A + H + 4, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, hidden), nn.SiLU(),
            nn.Linear(hidden, H * A),
        )

    def forward(self, x_t, time, obs):
        B = x_t.shape[0]
        tt = time[:, None].expand(B, H) if time.ndim == 1 else time
        h = torch.cat([x_t.reshape(B, -1), tt, obs], 1)
        return self.net(h).reshape(B, H, A)


def sample_time(B, gen=None):
    """Giống SmolVLA: Beta(1.5, 1) * 0.999 + 0.001 (nghiêng về phía nhiều nhiễu)."""
    return torch.distributions.Beta(1.5, 1.0).sample((B,)) * 0.999 + 0.001


def train(obs, chunks, normalizer, steps=4000, batch=1024, max_delay=0, seed=0, log=True):
    """max_delay = 0: huấn luyện thường. max_delay > 0: RTC lúc huấn luyện (paper 2):
    d ngẫu nhiên trong {0..max_delay} (như _sample_training_rtc_prefix_mask của Pi05 trong LeRobot),
    d token đầu giữ sạch (time = 0), loss chỉ tính trên phần sau."""
    torch.manual_seed(seed)
    model = VelocityMLP()
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps)
    target_all = normalizer.norm(chunks)
    for it in range(steps):
        idx = torch.randint(0, len(obs), (batch,))
        a, o = target_all[idx], obs[idx]
        noise = torch.randn_like(a)
        time = sample_time(batch)
        prefix_mask = None
        if max_delay > 0:
            d = torch.randint(0, max_delay + 1, (batch,))
            prefix_mask = torch.arange(H)[None] < d[:, None]
        x_t, u_t, model_time = make_flow_matching_inputs(
            a, noise, time, convention=FlowConvention.NOISE_AT_ONE, prefix_mask=prefix_mask
        )
        loss = (model(x_t, model_time, o) - u_t) ** 2
        if prefix_mask is not None:
            post = (~prefix_mask)[..., None].float()
            loss = (loss * post).sum() / (post.sum() * A)
        else:
            loss = loss.mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        if log and (it % 1000 == 0 or it == steps - 1):
            print(f"  bước {it:5d}  loss {loss.item():.4f}")
    return model.eval()


def get_models(cache="toy_models.pt", max_delay=6):
    """Huấn luyện 1 lần (khoảng 1-2 phút CPU) rồi lưu, các lab sau dùng lại."""
    import os
    if os.path.exists(cache):
        ck = torch.load(cache, weights_only=False)
        return ck["plain"], ck["trained"], ck["norm"]
    print("Sinh dữ liệu chuyên gia...")
    O, C = make_dataset()
    norm = Normalizer(C)
    print(f"  {len(O)} mẫu (obs, chunk)")
    print("Huấn luyện mô hình thường:")
    plain = train(O, C, norm)
    print(f"Huấn luyện mô hình RTC lúc huấn luyện (max_delay = {max_delay}):")
    trained = train(O, C, norm, max_delay=max_delay, seed=1)
    torch.save({"plain": plain, "trained": trained, "norm": norm}, cache)
    return plain, trained, norm


# ---------------------------------------------------------------- lấy mẫu: thường / RTC 1 / RTC 2
def make_rtc(kind, execution_horizon, beta=10.0):
    sched = {"hard": RTCAttentionSchedule.ZEROS, "soft": RTCAttentionSchedule.EXP,
             "linear": RTCAttentionSchedule.LINEAR, "soft_full": RTCAttentionSchedule.EXP}[kind]
    cfg = RTCConfig(enabled=True, execution_horizon=execution_horizon, max_guidance_weight=beta,
                    prefix_attention_schedule=sched)
    return FullJacobianRTC(cfg) if kind == "soft_full" else RTCProcessor(cfg)


@torch.no_grad()
def sample_chunk(model, obs, *, method="naive", leftover=None, d=0, rtc=None, gen=None):
    """Trả chunk đã chuẩn hóa (B, H, A).
    method: naive | guided (paper 1, cần rtc) | trained (paper 2, model phải huấn luyện với prefix)."""
    B = obs.shape[0]
    noise = torch.randn(B, H, A, generator=gen)
    fn = lambda x_t, time: model(x_t, time, obs)
    if method == "naive" or leftover is None:
        return euler_integrate(fn, noise, NUM_STEPS)
    if method == "guided":
        return euler_integrate(fn, noise, NUM_STEPS, rtc_processor=rtc, rtc_enabled=True,
                               inference_delay=d, prev_chunk_left_over=leftover,
                               execution_horizon=rtc.rtc_config.execution_horizon)
    if method == "trained":
        if d == 0:
            return euler_integrate(fn, noise, NUM_STEPS)
        prefix = torch.zeros(B, H, A)
        prefix[:, :d] = leftover[:, :d]
        mask = (torch.arange(H) < d)[None, :, None].expand(B, H, A)
        return euler_integrate(fn, noise, NUM_STEPS, hard_prefix=prefix, hard_prefix_mask=mask)
    raise ValueError(method)


# ---------------------------------------------------------------- chạy bất đồng bộ có độ trễ
def run_async(model, norm, *, method="naive", d=0, s=8, rtc=None, B=200, seed=0):
    """Giả lập độ trễ d bước: chunk mới tính từ quan sát lúc bắt đầu hỏi, nhưng chỉ dùng được
    sau d bước; trong d bước đó robot vẫn chạy tiếp chunk cũ (như Algorithm 1 của paper 1).
    Với d = 0 đây chính là chạy đồng bộ, chạy s hành động rồi hỏi lại."""
    assert d <= s <= H - d, f"cần d <= s <= H - d, đang có d={d}, s={s}, H={H}"
    gen = torch.Generator().manual_seed(seed + 1000)
    env = ToyEnv(B, seed=seed)
    chunk = sample_chunk(model, env.obs(), gen=gen)          # chunk đầu: đồng bộ
    i, switches = 0, []
    while not env.done():
        while i < s and not env.done():
            env.step(norm.unnorm(chunk[:, i]))
            i += 1
        if env.done():
            break
        leftover = chunk[:, s:]                                 # phần CHƯA chạy (H - s bước)
        new = sample_chunk(model, env.obs(), method=method, leftover=leftover, d=d, rtc=rtc, gen=gen)
        switches.append((chunk[:, s:s + d], new[:, :d]))
        for j in range(d):                                      # mô hình "đang nghĩ" ...
            if env.done():
                break
            env.step(norm.unnorm(chunk[:, s + j]))
        chunk, i = new, d                                       # đổi chunk, chạy tiếp từ ô d
    return env, switches
