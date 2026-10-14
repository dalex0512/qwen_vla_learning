"""Lab 2: mở RTCProcessor của LeRobot ra xem từng con số, đối chiếu với công thức paper 1.
Chạy: python lab2_ben_trong_rtc.py   Ra: results/lab2_weights.png, results/lab2_denoise.png"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from common import H, NUM_STEPS, ToyEnv, get_models, make_rtc
from lerobot.configs import RTCAttentionSchedule
from lerobot.policies.common.flow_matching import euler_integrate
from lerobot.policies.rtc import RTCConfig
from lerobot.policies.rtc.modeling_rtc import RTCProcessor
from rtc_full_jacobian import FullJacobianRTC

os.makedirs("results", exist_ok=True)
torch.set_printoptions(precision=3, sci_mode=False)

# --- 2a. Mặt nạ trọng số theo vị trí trong chunk
d, eh = 3, 10
print(f"2a) Trọng số W_i theo vị trí i (H = {H}, inference_delay d = {d}, execution_horizon = {eh})")
fig, ax = plt.subplots(1, 2, figsize=(12, 3.6))
for sch in RTCAttentionSchedule:
    w = RTCProcessor(RTCConfig(execution_horizon=eh, prefix_attention_schedule=sch)).get_prefix_weights(d, eh, H)
    print(f"   {sch.value:7s}", [round(x, 3) for x in w.tolist()])
    ax[0].plot(w, marker="o", label=sch.value)
# công thức (5) của paper 1, với H - s = execution_horizon
paper = []
for i in range(H):
    if i < d:
        paper.append(1.0)
    elif i < eh:
        c = (eh - i) / (eh - d + 1)
        paper.append(c * (math.exp(c) - 1) / (math.e - 1))
    else:
        paper.append(0.0)
print("   paper(5)", [round(x, 3) for x in paper], " <- trùng EXP khi execution_horizon = H - s")
ax[0].plot(paper, "k--", lw=1, label="paper Eq.5")
ax[0].axvline(d - 0.5, color="0.6", ls=":"); ax[0].axvline(eh - 0.5, color="0.6", ls=":")
ax[0].set_title("Mặt nạ W_i: 1 = đóng băng, 0 = tự do"); ax[0].set_xlabel("vị trí i trong chunk mới"); ax[0].legend()

# --- 2b. Trọng số guidance theo bước khử nhiễu
print(f"\n2b) Trọng số guidance mỗi bước Euler (LeRobot: time đi 1 -> 0, paper: tau = 1 - time)")
for n, beta in [(10, 10.0), (5, 5.0)]:
    ws = []
    for k in range(n):
        time = 1.0 - k / n
        tau = 1 - time
        ws.append(beta if tau == 0 else min(beta, ((1 - tau) ** 2 + tau**2) / (tau * (1 - tau))))
    print(f"   n = {n:2d}, beta = {beta:4.1f}:", [round(x, 2) for x in ws])
    ax[1].plot(range(n), ws, marker="o", label=f"n={n}, β={beta}")
ax[1].set_title("Trọng số guidance (bị kẹp ở β)"); ax[1].set_xlabel("bước khử nhiễu k"); ax[1].legend()
fig.tight_layout(); fig.savefig("results/lab2_weights.png", dpi=110)

# --- 2c. Jacobian: LeRobot bỏ qua, paper thì không
plain, _, norm = get_models()
env = ToyEnv(1, seed=3)
obs = env.obs()
fn = lambda x, t: plain(x, t if torch.is_tensor(t) else torch.full((1,), t), obs)
torch.manual_seed(0)
prev = torch.randn(1, H - 6, 2)
x = torch.randn(1, H, 2)
p_lr = RTCProcessor(RTCConfig(execution_horizon=10, prefix_attention_schedule=RTCAttentionSchedule.EXP, debug=True))
p_full = FullJacobianRTC(RTCConfig(execution_horizon=10, prefix_attention_schedule=RTCAttentionSchedule.EXP, debug=True))
for name, p in [("LeRobot RTCProcessor", p_lr), ("FullJacobianRTC     ", p_full)]:
    p.denoise_step(x, prev, inference_delay=3, time=0.6, original_denoise_step_partial=lambda z: fn(z, 0.6))
    st = p.get_all_debug_steps()[-1]
    cos = torch.nn.functional.cosine_similarity(st.correction.flatten(), st.err.flatten(), dim=0)
    print(f"\n2c) {name}: correction == err ? {torch.allclose(st.correction, st.err)}"
          f" | cos(correction, err) = {cos:.3f} | |correction| / |err| = {st.correction.norm() / st.err.norm():.3f}")

# --- 2d. Theo dõi 10 bước khử nhiễu: đoán chunk sạch x1 bị kéo về chunk cũ thế nào
torch.manual_seed(0)
noise = torch.randn(1, H, 2)
s = 6
with torch.no_grad():
    old = euler_integrate(fn, torch.randn(1, H, 2), NUM_STEPS)      # "chunk cũ"
leftover = old[:, s:] + 0.8                                          # dời lên để thấy rõ lực kéo
fig, axes = plt.subplots(1, 2, figsize=(12, 3.8), sharey=True)
for ax, (title, rtc) in zip(axes, [("Không RTC", None), ("RTC (LeRobot, EXP, β=10)", make_rtc("soft", H - s))]):
    trace = []
    def fn_trace(x_t, t):
        v = fn(x_t, t)
        tt = float(t[0]) if torch.is_tensor(t) else float(t)
        trace.append((x_t - tt * v).detach()[0, :, 1])               # đoán chunk sạch, chiều y
        return v
    euler_integrate(fn_trace, noise.clone(), NUM_STEPS, rtc_processor=rtc, rtc_enabled=rtc is not None,
                    inference_delay=3, prev_chunk_left_over=leftover, execution_horizon=H - s)
    for k, tr in enumerate(trace):
        ax.plot(tr, color=plt.cm.viridis(k / (len(trace) - 1)), lw=1.2)
    ax.plot(range(H - s), leftover[0, :, 1], "r--", lw=2, label="phần còn lại của chunk cũ")
    ax.axvspan(-0.5, 2.5, color="orange", alpha=0.12)
    ax.set_title(title + "  (màu: bước 1 tím → bước 10 vàng)"); ax.set_xlabel("vị trí trong chunk"); ax.legend()
axes[0].set_ylabel("đoán chunk sạch, chiều y (chuẩn hóa)")
fig.tight_layout(); fig.savefig("results/lab2_denoise.png", dpi=110)
print("\nĐã lưu results/lab2_weights.png, results/lab2_denoise.png")
