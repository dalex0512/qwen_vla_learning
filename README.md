# VLA Modeling · Sổ tay học tập

Web học tập tĩnh (HTML/CSS/JS thuần, không framework, không build) phục vụ theo dõi lộ trình đọc 6 paper và mở nhanh 4 loại tài liệu: trang đọc hiểu, slide trình bày, PDF gốc và PDF bản dịch tiếng Việt.

---

## 1. Cách chạy với extension Live Server

1. Trong VS Code, mở thư mục dự án `d:\VLA Modeling`.
2. Chuột phải vào file `index.html` và chọn **Open with Live Server** (hoặc bấm nút **Go Live** ở thanh trạng thái góc dưới bên phải).
3. Trình duyệt sẽ tự động mở địa chỉ `http://127.0.0.1:5500/index.html`.
4. *Lưu ý:* Web cũng có thể mở trực tiếp bằng cách nhấp đúp file `index.html` (giao thức `file://`) do danh sách paper được nạp qua `papers.js`, hoàn toàn không bị chặn CORS.

---

## 2. Cách đổi trạng thái bài học

Mở file `papers.js`, tìm phần tử paper tương ứng và sửa thuộc tính `trangThai`:

- `"chua-doc"`: Paper chưa bắt đầu học.
- `"dang-doc"`: Paper đang học (sẽ được làm nổi bật nhẹ trên giao diện trang chủ).
- `"da-present"`: Paper đã đọc và báo cáo xong (tiến độ trên thanh header "Đã xong X/6" sẽ tự động tăng lên).

Ví dụ chuyển Qwen-VLA sang trạng thái đang đọc:
```javascript
{
  id: "qwen-vla",
  ten: "Qwen-VLA",
  arxiv: "2605.30280",
  nhom: "Đọc rộng",
  moTa: "Mô hình VLA của Qwen",
  trangThai: "dang-doc", // <-- Đổi ở đây
  files: {
    docHieu: null,
    slide: null,
    pdfGoc: "Docs/QwenVLA.pdf",
    pdfViet: "Docs/translated/QwenVLA-vi.pdf"
  }
}
```

---

## 3. Cách thêm tài liệu hoặc thêm một paper mới

### A. Bổ sung file cho paper có sẵn
Khi bạn có thêm file đọc hiểu, slide hoặc PDF cho một paper:
1. Đặt file vào thư mục:
   - File PDF gốc: thư mục `Docs/` (ví dụ: `Docs/GR00T.pdf`)
   - File PDF bản dịch: thư mục `Docs/translated/` (ví dụ: `Docs/translated/GR00T-vi.pdf`)
   - File Đọc hiểu / Slide: tạo thư mục tương ứng (ví dụ: `GR00T/GR00T · Đọc hiểu paper.html`)
2. Mở `papers.js`, thay giá trị `null` thành đường dẫn file:
   ```javascript
   files: {
     docHieu: "GR00T/GR00T · Đọc hiểu paper.html",
     slide: null,
     pdfGoc: "Docs/GR00T.pdf",
     pdfViet: "Docs/translated/GR00T-vi.pdf"
   }
   ```
*(Hệ thống đã tự động dùng `encodeURI`, bạn có thể đặt tên file có dấu cách và tiếng Việt thoải mái).*

### B. Thêm paper mới vào danh sách
Mở `papers.js` và thêm một object mới vào mảng `PAPERS`:
```javascript
{
  id: "dinh-danh-duy-nhat",          // Dùng trên URL ?id=... (không dấu, viết thường, gạch nối)
  ten: "Tên paper",                 // Tên hiển thị
  arxiv: "YYMM.NNNNN",              // Mã số trên arXiv (để tự tạo link arXiv)
  nhom: "Đọc rộng",                 // "Đọc rộng" hoặc "Đọc sâu"
  moTa: "Tóm tắt ngắn gọn 1 câu.",   // Mô tả nội dung chính
  trangThai: "chua-doc",            // "chua-doc" | "dang-doc" | "da-present"
  files: {
    docHieu: null,                  // Đường dẫn file HTML đọc hiểu hoặc null
    slide: null,                    // Đường dẫn file HTML slide hoặc null
    pdfGoc: null,                   // Đường dẫn file PDF gốc hoặc null
    pdfViet: null                   // Đường dẫn file PDF bản dịch hoặc null
  }
}
```

---

## 4. Các tính năng nổi bật của web
- **Trang chủ (`index.html`):**
  - Thanh tiến độ động "Đã xong X/6" tính từ các paper có trạng thái `da-present`.
  - Dải kết nối dọc (spine 1–6) phân 2 nhóm "Đọc rộng" và "Đọc sâu".
  - Mỗi thẻ paper có 4 nút tài liệu. Nút chưa có file tự động mờ và hiện nhãn "Sắp có".
- **Trang xem paper (`paper.html`):**
  - Chuyển đổi mượt giữa các tab `Đọc hiểu`, `Slide`, `PDF gốc`, `Bản dịch`.
  - Tab **Song song** tự động bật khi có đủ cả PDF gốc và PDF bản dịch (hiển thị 2 tài liệu cạnh nhau, cuộn độc lập). Trên màn hình nhỏ (< 900px), tự chuyển thành nút gạt 2 chế độ Gốc / Tiếng Việt.
  - Tự lưu tab vào hash URL (`#doc-hieu`, `#slide`, `#pdf-goc`, `#ban-dich`, `#song-song`) để tải lại trang vẫn đúng tab.
  - Phím điều hướng nhanh "‹ Paper trước" và "Paper sau ›".
  - Nút chuyển giao diện **Sáng / Tối**, tự nhận diện theo hệ thống và lưu cấu hình vào `localStorage`.
