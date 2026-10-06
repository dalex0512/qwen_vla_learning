/**
 * papers.js - Danh sách paper VLA Modeling
 * Đây là nơi duy nhất bạn cần sửa khi cập nhật trạng thái hoặc thêm paper mới.
 * 
 * Các trường dữ liệu:
 * - id: định danh duy nhất (dùng trong url ?id=...)
 * - ten: tên hiển thị của paper
 * - arxiv: mã arXiv (ví dụ '2306.03310')
 * - nhom: 'Đọc rộng' | 'Đọc sâu'
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
    trangThai: "chua-doc",
    files: {
      docHieu: null,
      slide: null,
      pdfGoc: null,
      pdfViet: null
    }
  },
  {
    id: "qwen-vla",
    ten: "Qwen-VLA",
    arxiv: "2605.30280",
    nhom: "Đọc rộng",
    bia: "qwen",
    moTa: "Mô hình VLA của Qwen",
    trangThai: "chua-doc",
    files: {
      docHieu: null,
      slide: null,
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
    bia: "rtc-infer",
    moTa: "Chạy action chunk mượt khi suy luận",
    trangThai: "chua-doc",
    files: {
      docHieu: null,
      slide: null,
      pdfGoc: null,
      pdfViet: null
    }
  },
  {
    id: "rtc-training",
    ten: "RTC training-time",
    arxiv: "2512.05964",
    nhom: "Đọc sâu",
    bia: "rtc-train",
    moTa: "Đưa RTC vào lúc huấn luyện",
    trangThai: "chua-doc",
    files: {
      docHieu: null,
      slide: null,
      pdfGoc: null,
      pdfViet: null
    }
  },
  {
    id: "lingbot-vla",
    ten: "LingBot-VLA 2.0",
    arxiv: "2607.06403",
    nhom: "Đọc sâu",
    bia: "moe",
    moTa: "MoE trong action expert",
    trangThai: "chua-doc",
    files: {
      docHieu: null,
      slide: null,
      pdfGoc: null,
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
