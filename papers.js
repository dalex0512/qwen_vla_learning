/**
 * papers.js - Danh sách paper VLA Modeling
 * Đây là nơi duy nhất bạn cần sửa khi cập nhật trạng thái hoặc thêm paper mới.
 *
 * Các trường dữ liệu:
 * - id: định danh duy nhất (dùng trong url ?id=...)
 * - ten: tên hiển thị của paper
 * - arxiv: mã arXiv (ví dụ '2306.03310')
 * - nhom: 'Đọc rộng' | 'Đọc sâu' | 'Mở rộng'
 * - bia: định danh loại bìa SVG trong assets/covers.js ('libero' | 'groot' | 'qwen' | 'rtc-infer' | 'rtc-train' | 'moe')
 * - moTa: tóm tắt 1 câu ngắn
 * - trangThai: 'chua-doc' | 'dang-doc' | 'da-present'
 * - files: đường dẫn tương đối tới các file (để null nếu chưa có)
 *   + docHieu: trang HTML phân tích/đọc hiểu
 *   + slide: trang HTML slide trình bày
 *   + pdfGoc: file PDF gốc
 *   + pdfViet: file PDF bản dịch tiếng Việt
 */

const PAPERS = [
  // --- NHÓM 1: ĐỌC RỘNG ---
  {
    id: "libero",
    ten: "LIBERO",
    arxiv: "2306.03310",
    nhom: "Đọc rộng",
    bia: "libero",
    moTa: "Bộ bài kiểm tra chuẩn để chấm điểm mô hình VLA",
    trangThai: "da-present",
    files: {
      docHieu: "LIBERO/LIBERO · Đọc hiểu paper.html",
      slide: "LIBERO/LIBERO · Slide trình bày.html",
      pdfGoc: "Docs/LIBERO.pdf",
      pdfViet: "Docs/translated/LIBERO-vi.pdf"
    }
  },
  {
    id: "gr00t-n1",
    ten: "GR00T N1",
    arxiv: "2503.14734",
    nhom: "Đọc rộng",
    bia: "groot",
    moTa: "Mô hình nền tảng cho robot hình người của NVIDIA",
    trangThai: "da-present",
    files: {
      docHieu: "Groot/GR00T N1 · Đọc hiểu paper.html",
      slide: "Groot/GR00T N1 · Slide trình bày.html",
      pdfGoc: "Docs/Groot.pdf",
      pdfViet: "Docs/translated/Groot-vi.pdf"
    }
  },
  {
    id: "qwen-vla",
    ten: "Qwen-VLA",
    arxiv: "2605.30280",
    nhom: "Đọc rộng",
    bia: "qwen",
    moTa: "Mô hình VLA của Qwen",
    trangThai: "da-present",
    files: {
      docHieu: "Qwen-VLA/Qwen-VLA · Đọc hiểu paper.html",
      slide: "Qwen-VLA/Qwen-VLA · Slide trình bày.html",
      pdfGoc: "Docs/QwenVLA.pdf",
      pdfViet: "Docs/translated/QwenVLA-vi.pdf"
    }
  },

  // --- NHÓM 2: ĐỌC SÂU ---
  {
    id: "rtc-inference",
    ten: "RTC inference-time",
    arxiv: "2506.07339",
    nhom: "Đọc sâu",
    cap: "RTC",
    thuTuCap: 1,
    bia: "rtc-infer",
    moTa: "Chạy action chunk mượt khi suy luận",
    trangThai: "dang-doc",
    files: {
      docHieu: "RTC/RTC-Inference · Đọc hiểu paper.html",
      slide: "RTC/RTC · Slide trình bày.html",
      pdfGoc: "Docs/RTC inference time.pdf",
      pdfViet: "Docs/translated/RTC inference time-vi.pdf"
    }
  },
  {
    id: "rtc-training",
    ten: "RTC training-time",
    arxiv: "2512.05964",
    nhom: "Đọc sâu",
    cap: "RTC",
    thuTuCap: 2,
    bia: "rtc-train",
    moTa: "Đưa RTC vào lúc huấn luyện",
    trangThai: "dang-doc",
    files: {
      docHieu: "RTC/RTC-Training · Đọc hiểu paper.html",
      slide: "RTC/RTC · Slide trình bày.html",
      pdfGoc: "Docs/RTC training Time.pdf",
      pdfViet: "Docs/translated/RTC training Time-vi.pdf"
    }
  },
  {
    id: "lingbot-vla",
    ten: "LingBot-VLA 2.0",
    arxiv: "2607.06403",
    nhom: "Đọc sâu",
    bia: "moe",
    moTa: "MoE trong action expert",
    trangThai: "dang-doc",
    files: {
      docHieu: "LingBot/LingBot · Đọc hiểu paper.html",
      slide: "LingBot/LingBot · Slide trình bày.html",
      pdfGoc: "Docs/Moe.pdf",
      pdfViet: "Docs/translated/Moe-vi.pdf"
    }
  },

  // --- NHÓM 3: MỞ RỘNG (SmolVLA: mentor gợi ý, kèm thử LeRobot) ---
  {
    id: "smolvla",
    ten: "SmolVLA",
    arxiv: "2506.01844",
    nhom: "Mở rộng",
    bia: "smolvla",
    moTa: "VLA nhỏ 0,45B, dữ liệu cộng đồng, chạy bất đồng bộ",
    trangThai: "dang-doc",
    files: {
      docHieu: "SmolVLA/SmolVLA · Đọc hiểu paper.html",
      slide: null,
      pdfGoc: "Docs/smolVLA.pdf",
      pdfViet: null
    }
  }
];

// Gắn vào window (trình duyệt) hoặc module.exports (Node.js test)
if (typeof window !== "undefined") {
  window.PAPERS = PAPERS;
}
if (typeof module !== "undefined" && module.exports) {
  module.exports = { PAPERS };
}
