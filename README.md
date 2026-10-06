# VLA Modeling · Sổ tay học tập

Web học tập tĩnh (HTML/CSS/JS thuần, không framework, không build) phục vụ theo dõi lộ trình đọc 6 paper VLA (Vision-Language-Action) và mở nhanh 4 loại tài liệu: trang đọc hiểu, slide trình bày, PDF gốc và PDF bản dịch tiếng Việt.

---

## 1. Cách chạy với extension Live Server

1. Trong VS Code, mở thư mục dự án `d:\VLA Modeling`.
2. Chuột phải vào file `index.html` và chọn **Open with Live Server** (hoặc bấm nút **Go Live** ở góc dưới bên phải).
3. Trình duyệt sẽ tự động mở địa chỉ `http://127.0.0.1:5500/index.html` (hoặc chạy qua python: `python -m http.server 8000`).
4. Web cũng có thể mở trực tiếp bằng cách nhấp đúp file `index.html` (`file://`).

---

## 2. Cách đổi trạng thái bài học

Mở file `papers.js`, tìm phần tử paper tương ứng và sửa thuộc tính `trangThai`:

- `"chua-doc"`: Paper chưa bắt đầu học (bìa mờ nhẹ, hover sẽ rõ nét).
- `"dang-doc"`: Paper đang học (nổi bật viền cam, có nhãn "ĐANG HỌC" / "Tiếp theo", trạm trên bản đồ tàu điện nhấp nháy phát sáng).
- `"da-present"`: Paper đã đọc và báo cáo xong (nút trạm Metro có dấu tích, thanh tiến độ "Đã hoàn thành X/6" tự động tăng lên).

Ví dụ chuyển GR00T N1 sang trạng thái đang đọc:
```javascript
{
  id: "gr00t-n1",
  ten: "GR00T N1",
  arxiv: "2503.14734",
  nhom: "Đọc rộng",
  bia: "groot",
  moTa: "Mô hình nền tảng cho robot hình người của NVIDIA",
  trangThai: "dang-doc", // <-- Đổi ở đây
  files: { ... }
}
```

---

## 3. Cách thêm Bìa SVG cho Paper mới

Mỗi bìa paper là một hàm vector SVG độc lập nằm trong `assets/covers.js`.

### Bước 1: Khai báo trường `bia` trong `papers.js`
```javascript
{
  id: "ten-paper-moi",
  ten: "Tên Paper Mới",
  arxiv: "2601.12345",
  nhom: "Đọc rộng", // hoặc "Đọc sâu"
  bia: "ten-bia-moi", // <-- Khai báo tên định danh bìa ở đây
  moTa: "Mô tả ngắn 1 câu.",
  trangThai: "chua-doc",
  files: { ... }
}
```

### Bước 2: Thêm `case` vẽ SVG trong `assets/covers.js`
Mở `assets/covers.js`, tìm lệnh `switch (biaType)` và thêm một case mới:
```javascript
case 'ten-bia-moi':
  keywords = ['từ khoá 1', 'từ khoá 2', 'từ khoá 3'];
  innerContent = `
    <!-- Khối đồ hoạ vector SVG của paper mới -->
    <rect x="30" y="30" width="220" height="130" rx="8" class="cv-plate cv-stroke" />
    <text x="140" y="95" class="cv-system-text">Minh hoạ ý chính</text>
  `;
  break;
```

---

## 4. Các tính năng nổi bật của giao diện
- **Cánh tay Robot Động học nghịch (2-Link IK):**
  - Cánh tay 2 khớp tính toán góc xoay liên tục bằng công thức giải tích động học nghịch trong `requestAnimationFrame`, gắp khối vật thể từ Bát đặt sang Đĩa chuẩn xác và mượt mà.
- **Dải bản đồ tàu điện (Subway Line Map):**
  - Tuyến "Đọc rộng" màu Teal (Ga 1–3) và tuyến "Đọc sâu" màu Chàm `#5B5BD6` (Ga 4–6).
  - Trạm đang học nhấp nháy phát sáng (Pulse ring).
  - Đoàn tàu chạy trên ray tới trạm hiện tại.
  - Hover hiển thị tooltip mô tả; Click vào trạm sẽ cuộn mượt xuống thẻ sách và nháy sáng viền thẻ đó.
- **Kệ sách (Bookshelf Grid):**
  - Lưới thẻ dựng đứng 3 cột trên máy tính, 2 cột trên điện thoại.
  - Bìa SVG tỉ lệ 4:3 tích hợp watermark số thứ tự to mờ, từ khoá kỹ thuật và hoạt ảnh khi hover.
  - Hiệu ứng nghiêng 3D (3D Mouse Tilt) tối đa 4 độ theo vị trí con trỏ chuột.
  - Hàng nút tài liệu icon nhỏ tinh tế kèm chú thích.
- **Trình đọc Paper (`paper.html`):**
  - Chuyển tab mượt mà kèm thanh gạch chân trượt (`tab-indicator-bar`).
  - Khung xương tải trang (Skeleton Shimmer).
  - Chế độ **Song song** (Dual Split View) đối chiếu bản dịch tiếng Việt và PDF gốc tiếng Anh.
- **Theme Sáng / Tối:** Tự động phát hiện cài đặt hệ thống và lưu vào `localStorage`.
