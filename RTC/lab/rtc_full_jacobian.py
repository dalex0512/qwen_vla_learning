"""RTC lúc suy luận (paper 1) với gradient đi QUA mô hình, cắm thẳng vào LeRobot.

Vì sao cần file này: trong RTCProcessor.denoise_step của LeRobot (đã kiểm ở commit b9cb121c
và ae2b57f), v_t được tính TRƯỚC khi x_t bật requires_grad, nên
    correction = d(x1_t)/d(x_t)^T * err = err
tức Jacobian của mô hình bị coi là ma trận đơn vị. Paper 1 (công thức ΠGDM) lấy gradient
qua mô hình bằng một lần backward (vector-Jacobian product). Lớp dưới đây làm đúng như paper,
giữ nguyên mọi phần khác (mask, kẹp trọng số, đệm chiều) của LeRobot.

Dùng: policy.rtc_processor.__class__ = FullJacobianRTC   (sau policy.init_rtc_processor())
"""
import torch

from lerobot.policies.rtc.modeling_rtc import RTCProcessor


class FullJacobianRTC(RTCProcessor):
    def denoise_step(self, x_t, prev_chunk_left_over, inference_delay, time,
                     original_denoise_step_partial, execution_horizon=None):
        if prev_chunk_left_over is None:
            return original_denoise_step_partial(x_t)
        squeezed = x_t.ndim < 3
        if squeezed:
            x_t = x_t.unsqueeze(0)
        prev_in = prev_chunk_left_over if prev_chunk_left_over.ndim == 3 else prev_chunk_left_over.unsqueeze(0)
        eh = self.rtc_config.execution_horizon if execution_horizon is None else execution_horizon
        eh = min(eh, prev_in.shape[1])
        B, Hh, Ad = x_t.shape
        prev = torch.zeros(B, Hh, Ad, device=x_t.device, dtype=x_t.dtype)
        L, Ap = min(prev_in.shape[1], Hh), min(prev_in.shape[2], Ad)
        prev[:, :L, :Ap] = prev_in[:, :L, :Ap].to(x_t.dtype)
        w_mask = self.get_prefix_weights(inference_delay, eh, Hh).to(x_t.device, x_t.dtype)[None, :, None]
        with torch.enable_grad():
            x = x_t.detach().clone().requires_grad_(True)
            v = original_denoise_step_partial(x)                 # lần này v phụ thuộc x
            x1 = x - time * v                                    # đoán chunk sạch (time = 1 là nhiễu)
            err = ((prev - x1) * w_mask).detach()
            corr = torch.autograd.grad(x1, x, err)[0]            # một lần backward
        tau = 1 - float(time)                                    # đổi sang quy ước paper (tau = 1 sạch)
        beta = float(self.rtc_config.max_guidance_weight)
        w = beta if tau <= 0 else min(beta, ((1 - tau) ** 2 + tau**2) / (tau * (1 - tau)))
        out = v.detach() - w * corr
        self.track(time=time, x1_t=x1.detach(), correction=corr, err=err, weights=w_mask,
                   guidance_weight=w, inference_delay=inference_delay, execution_horizon=eh)
        return out.squeeze(0) if squeezed else out
