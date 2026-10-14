"""Lab 0: sinh dữ liệu và huấn luyện 2 mô hình đồ chơi (thường + RTC lúc huấn luyện)."""
import time
from common import get_models

t0 = time.time()
get_models()
print(f"Xong sau {time.time() - t0:.0f} giây. Đã lưu toy_models.pt")
