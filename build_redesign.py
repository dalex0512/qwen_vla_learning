# -*- coding: utf-8 -*-
"""
Script to apply the complete frontend redesign:
0. Hero 2-Link IK Robot Arm (mathematical inverse kinematics in requestAnimationFrame)
1. Subway Line Map (Metro Map: Teal line & Indigo line with train dot & tooltips & click-to-scroll)
2. Bookshelf Grid (2 shelves, 3-column upright book cards with 3D mouse tilt)
3. 6 Dedicated SVG Covers in assets/covers.js (watermark numbers, hover animations, keywords)
4. Updated papers.js with 'bia' field
5. Updated index.html, assets/style.css, assets/app.js, and README.md
"""

import os

PAPERS_JS = """/**
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
"""

COVERS_JS = """/**
 * covers.js - Trình vẽ Bìa SVG Minh hoạ Ý chính từng Paper
 * Thiết kế theo phong cách Vector nét phẳng, đồng bộ độ dày nét, thích ứng Sáng/Tối.
 * Có watermark số thứ tự to mờ góc trên, 2-3 từ khoá góc dưới và hoạt ảnh khi hover.
 */

(function () {
  'use strict';

  const Covers = {
    /**
     * Hàm chính xuất chuỗi SVG cho bìa sách
     * @param {string} biaType - Mã bìa ('libero', 'groot', 'qwen', 'rtc-infer', 'rtc-train', 'moe')
     * @param {object} paper - Dữ liệu paper từ PAPERS
     * @param {number} index - Số thứ tự 1-6
     * @returns {string} SVG markup string
     */
    render: function (biaType, paper, index) {
      const idxStr = String(index).padStart(2, '0');
      const isDeep = paper.nhom === 'Đọc sâu';
      const bgClass = isDeep ? 'cover-bg--indigo' : 'cover-bg--teal';

      let innerContent = '';
      let keywords = [];

      switch (biaType) {
        case 'libero':
          keywords = ['benchmark', '130 bài', '4 bộ'];
          innerContent = `
            <!-- Mặt bàn bếp & Bồn / Kệ -->
            <rect x="25" y="30" width="230" height="130" rx="8" class="cv-plate cv-stroke" />
            <rect x="35" y="40" width="80" height="24" rx="4" class="cv-box cv-stroke" />
            <text x="75" y="56" class="cv-tag-text">Cabinet</text>

            <!-- 4 ô bộ dữ liệu chuẩn -->
            <g class="cv-libero-grid" transform="translate(130, 40)">
              <rect x="0" y="0" width="55" height="16" rx="3" class="cv-pill" />
              <text x="27" y="12" class="cv-mini-text">Spatial</text>
              <rect x="62" y="0" width="55" height="16" rx="3" class="cv-pill" />
              <text x="89" y="12" class="cv-mini-text">Object</text>
              <rect x="0" y="20" width="55" height="16" rx="3" class="cv-pill" />
              <text x="27" y="32" class="cv-mini-text">Goal</text>
              <rect x="62" y="20" width="55" height="16" rx="3" class="cv-pill" />
              <text x="89" y="32" class="cv-mini-text">Long</text>
            </g>

            <!-- Đĩa đích (Target Plate) bên phải -->
            <g class="cv-plate-group" transform="translate(200, 115)">
              <ellipse cx="0" cy="0" rx="28" ry="16" class="cv-plate-outer cv-stroke" />
              <ellipse cx="0" cy="0" rx="18" ry="10" class="cv-plate-inner cv-stroke" />
              <text x="0" y="4" class="cv-tag-text">Đích</text>
            </g>

            <!-- Bát vật thể (Source Bowl) trượt sang đĩa khi hover -->
            <g class="cv-anim-bowl-slide" transform="translate(80, 115)">
              <ellipse cx="0" cy="0" rx="22" ry="13" class="cv-bowl-body cv-stroke" />
              <circle cx="0" cy="0" r="6" class="cv-cube-item" />
              <text x="0" y="3" class="cv-tag-text">Bát</text>
            </g>
          `;
          break;

        case 'groot':
          keywords = ['humanoid', 'dual-system', 'flow matching'];
          innerContent = `
            <!-- Robot hình người đơn giản hoá -->
            <!-- Khối đầu: Hệ 2 · VLM -->
            <g class="cv-groot-head" transform="translate(140, 42)">
              <rect x="-48" y="-18" width="96" height="36" rx="8" class="cv-block-system2 cv-stroke" />
              <text x="0" y="4" class="cv-system-text">Hệ 2 · VLM</text>
              <!-- Mắt cảm biến -->
              <circle cx="-24" cy="-6" r="3" class="cv-accent-dot" />
              <circle cx="24" cy="-6" r="3" class="cv-accent-dot" />
            </g>

            <!-- Đường dẫn tín hiệu thần kinh từ đầu xuống thân -->
            <line x1="140" y1="60" x2="140" y2="85" class="cv-neural-line cv-stroke" />
            <circle cx="140" cy="72" r="3.5" class="cv-signal-pulse" />

            <!-- Khối thân: Hệ 1 · Action -->
            <g class="cv-groot-body" transform="translate(140, 108)">
              <rect x="-56" y="-22" width="112" height="44" rx="10" class="cv-block-system1 cv-stroke" />
              <text x="0" y="4" class="cv-system-text">Hệ 1 · Action</text>
            </g>

            <!-- Cánh tay và bàn tay robot -->
            <path d="M 84 96 L 50 115 L 45 145" class="cv-limb-line cv-stroke" />
            <circle cx="45" cy="145" r="5" class="cv-hand-dot cv-stroke" />
            
            <path d="M 196 96 L 230 115 L 235 145" class="cv-limb-line cv-stroke" />
            <circle cx="235" cy="145" r="5" class="cv-hand-dot cv-stroke" />

            <!-- Chân -->
            <line x1="115" y1="130" x2="105" y2="162" class="cv-limb-line cv-stroke" />
            <line x1="165" y1="130" x2="175" y2="162" class="cv-limb-line cv-stroke" />
          `;
          break;

        case 'qwen':
          keywords = ['VLM', 'action expert', 'multi-modal'];
          innerContent = `
            <!-- Bên trái: Mắt (Vision) + Bong bóng thoại (Language) -->
            <g class="cv-input-group" transform="translate(48, 70)">
              <!-- Icon Mắt -->
              <ellipse cx="0" cy="0" rx="16" ry="10" class="cv-eye-outline cv-stroke" />
              <circle cx="0" cy="0" r="5" class="cv-eye-pupil" />
              <text x="0" y="20" class="cv-mini-label">Vision</text>
            </g>

            <g class="cv-input-group" transform="translate(48, 125)">
              <!-- Icon Chat Bubble -->
              <path d="M -14 -10 L 14 -10 Q 18 -10 18 -6 L 18 6 Q 18 10 14 10 L -4 10 L -12 16 L -10 10 L -14 10 Q -18 10 -18 6 L -18 -6 Q -18 -10 -14 -10 Z" class="cv-chat-bubble cv-stroke" />
              <text x="0" y="28" class="cv-mini-label">Prompt</text>
            </g>

            <!-- Mũi tên dẫn vào khối VLM -->
            <path d="M 72 70 L 102 92" class="cv-flow-arrow cv-stroke" marker-end="url(#arrowhead-teal)" />
            <path d="M 72 125 L 102 104" class="cv-flow-arrow cv-stroke" marker-end="url(#arrowhead-teal)" />

            <!-- Khối VLM trung tâm -->
            <g class="cv-vlm-core" transform="translate(138, 98)">
              <rect x="-32" y="-30" width="64" height="60" rx="10" class="cv-core-block cv-stroke" />
              <text x="0" y="-4" class="cv-core-title">Qwen</text>
              <text x="0" y="14" class="cv-core-sub">VLM</text>
            </g>

            <!-- 3 Mũi tên hành động bắn ra bên phải -->
            <g class="cv-action-arrows">
              <g class="cv-arrow-row cv-arrow-1" transform="translate(178, 78)">
                <line x1="0" y1="0" x2="52" y2="-12" class="cv-action-path cv-stroke" />
                <polygon points="52,-12 42,-18 45,-10" class="cv-arrow-head" />
                <text x="62" y="-9" class="cv-act-label">a₁</text>
              </g>
              <g class="cv-arrow-row cv-arrow-2" transform="translate(178, 98)">
                <line x1="0" y1="0" x2="56" y2="0" class="cv-action-path cv-stroke" />
                <polygon points="56,0 46,-4 46,4" class="cv-arrow-head" />
                <text x="64" y="4" class="cv-act-label">a₂</text>
              </g>
              <g class="cv-arrow-row cv-arrow-3" transform="translate(178, 118)">
                <line x1="0" y1="0" x2="52" y2="12" class="cv-action-path cv-stroke" />
                <polygon points="52,12 45,10 42,18" class="cv-arrow-head" />
                <text x="62" y="16" class="cv-act-label">a₃</text>
              </g>
            </g>
          `;
          break;

        case 'rtc-infer':
          keywords = ['inference', 'action chunk', 'real-time'];
          innerContent = `
            <!-- Trục thời gian t -->
            <line x1="30" y1="140" x2="250" y2="140" class="cv-axis-line cv-stroke" />
            <polygon points="250,140 242,136 242,144" class="cv-arrow-head" />
            <text x="245" y="156" class="cv-axis-label">t (thời gian)</text>

            <!-- 3 Action Chunk nối nhau với vùng chồng lấn -->
            <g class="cv-chunk-seq" transform="translate(40, 50)">
              <!-- Chunk 1 -->
              <g class="cv-chunk-item cv-chunk-1" transform="translate(0, 0)">
                <rect x="0" y="0" width="70" height="30" rx="5" class="cv-chunk-box cv-stroke" />
                <text x="35" y="18" class="cv-chunk-text">Chunk k-1</text>
              </g>

              <!-- Vùng Overlap 1-2 -->
              <rect x="52" y="18" width="22" height="30" rx="3" class="cv-overlap-box" />

              <!-- Chunk 2 -->
              <g class="cv-chunk-item cv-chunk-2" transform="translate(56, 24)">
                <rect x="0" y="0" width="70" height="30" rx="5" class="cv-chunk-box cv-chunk-active cv-stroke" />
                <text x="35" y="18" class="cv-chunk-text">Chunk k</text>
              </g>

              <!-- Vùng Overlap 2-3 -->
              <rect x="108" y="42" width="22" height="30" rx="3" class="cv-overlap-box" />

              <!-- Chunk 3 -->
              <g class="cv-chunk-item cv-chunk-3" transform="translate(112, 48)">
                <rect x="0" y="0" width="70" height="30" rx="5" class="cv-chunk-box cv-stroke" />
                <text x="35" y="18" class="cv-chunk-text">Chunk k+1</text>
              </g>
            </g>

            <!-- Nhãn mượt mà suy luận -->
            <text x="140" y="34" class="cv-rtc-pill">Smooth Stitching</text>
          `;
          break;

        case 'rtc-train':
          keywords = ['training', 'chunk', 'feedback loop'];
          innerContent = `
            <!-- Vòng lặp huấn luyện xoay quanh (Training Feedback Loop) -->
            <g class="cv-loop-group" transform="translate(140, 92)">
              <circle cx="0" cy="0" r="58" class="cv-train-loop-bg cv-stroke" />
              <path d="M 0 -58 A 58 58 0 0 1 58 0 A 58 58 0 0 1 0 58 A 58 58 0 0 1 -58 0" fill="none" class="cv-train-loop cv-stroke" />
              <polygon points="0,-58 10,-64 10,-52" class="cv-arrow-head cv-loop-arrow" />
              <polygon points="0,58 -10,52 -10,64" class="cv-arrow-head cv-loop-arrow" />
            </g>

            <!-- Trung tâm: Action Chunks -->
            <g class="cv-train-center" transform="translate(105, 74)">
              <rect x="0" y="0" width="70" height="36" rx="6" class="cv-train-block cv-stroke" />
              <text x="35" y="16" class="cv-chunk-text">RTC Loss</text>
              <text x="35" y="28" class="cv-mini-text">Gradient</text>
            </g>

            <text x="140" y="24" class="cv-rtc-pill">Training-time Flow</text>
          `;
          break;

        case 'moe':
          keywords = ['MoE', 'FFN', 'action expert'];
          innerContent = `
            <!-- Khối Router trên đỉnh -->
            <g class="cv-router-block" transform="translate(140, 40)">
              <rect x="-42" y="-16" width="84" height="32" rx="6" class="cv-router-box cv-stroke" />
              <text x="0" y="4" class="cv-system-text">Router</text>
            </g>

            <!-- 4 Mũi tên phân phối tới 4 Expert -->
            <path d="M 115 56 L 45 92" class="cv-expert-line cv-stroke" />
            <path d="M 130 56 L 105 92" class="cv-expert-line cv-stroke" />
            <path d="M 150 56 L 175 92" class="cv-expert-line cv-stroke" />
            <path d="M 165 56 L 235 92" class="cv-expert-line cv-stroke" />

            <!-- 4 Khối Expert bên dưới -->
            <g class="cv-experts-row">
              <g class="cv-exp-item cv-exp-1" transform="translate(45, 114)">
                <rect x="-20" y="-18" width="40" height="36" rx="6" class="cv-expert-box cv-stroke" />
                <text x="0" y="-2" class="cv-mini-text">Exp 1</text>
                <circle cx="0" cy="9" r="3" class="cv-exp-led" />
              </g>

              <g class="cv-exp-item cv-exp-2" transform="translate(105, 114)">
                <rect x="-20" y="-18" width="40" height="36" rx="6" class="cv-expert-box cv-stroke" />
                <text x="0" y="-2" class="cv-mini-text">Exp 2</text>
                <circle cx="0" cy="9" r="3" class="cv-exp-led" />
              </g>

              <g class="cv-exp-item cv-exp-3" transform="translate(175, 114)">
                <rect x="-20" y="-18" width="40" height="36" rx="6" class="cv-expert-box cv-stroke" />
                <text x="0" y="-2" class="cv-mini-text">Exp 3</text>
                <circle cx="0" cy="9" r="3" class="cv-exp-led" />
              </g>

              <g class="cv-exp-item cv-exp-4" transform="translate(235, 114)">
                <rect x="-20" y="-18" width="40" height="36" rx="6" class="cv-expert-box cv-stroke" />
                <text x="0" y="-2" class="cv-mini-text">Exp 4</text>
                <circle cx="0" cy="9" r="3" class="cv-exp-led" />
              </g>
            </g>
          `;
          break;

        default:
          keywords = ['research', 'modeling', 'VLA'];
          innerContent = `
            <rect x="40" y="40" width="200" height="100" rx="8" class="cv-plate cv-stroke" />
            <text x="140" y="95" class="cv-system-text">${paper.ten}</text>
          `;
      }

      const keywordsMarkup = keywords.map(kw => `<span class="cv-kw-tag">${kw}</span>`).join('');

      return `
        <div class="book-cover-inner ${bgClass}">
          <svg class="book-cover-svg" viewBox="0 0 280 190" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
            <defs>
              <marker id="arrowhead-teal" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
                <polygon points="0 0, 6 3, 0 6" fill="var(--teal-500)" />
              </marker>
            </defs>

            <!-- Số thứ tự Watermark to mờ góc trên -->
            <text x="260" y="46" text-anchor="end" class="cv-watermark-num">${idxStr}</text>

            <!-- Nội dung SVG chính -->
            ${innerContent}
          </svg>

          <!-- 2-3 Từ khoá nhỏ góc dưới -->
          <div class="cv-keywords-row">
            ${keywordsMarkup}
          </div>
        </div>
      `;
    }
  };

  if (typeof window !== 'undefined') {
    window.Covers = Covers;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Covers };
  }
})();
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>VLA Modeling · Sổ tay học tập</title>
  <meta name="description" content="Sổ tay học tập và theo dõi lộ trình đọc paper VLA (Vision-Language-Action) modeling.">
  
  <!-- Typography Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/style.css?v=30.0">
  <script>
    (function () {
      try {
        var saved = localStorage.getItem('vla_theme_pref');
        if (saved === 'dark' || saved === 'light') {
          document.documentElement.setAttribute('data-theme', saved);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          document.documentElement.setAttribute('data-theme', 'dark');
        } else {
          document.documentElement.setAttribute('data-theme', 'light');
        }
      } catch (e) {}
    })();
  </script>
</head>
<body class="page-home">
  <!-- Mảng màu tròn mờ nền (Ambient Glow Orbs) -->
  <div class="ambient-glow ambient-glow--teal" aria-hidden="true"></div>
  <div class="ambient-glow ambient-glow--indigo" aria-hidden="true"></div>
  <div class="ambient-glow ambient-glow--orange" aria-hidden="true"></div>

  <div class="container main-layout">
    <!-- Header thương hiệu & Nút đổi theme -->
    <header class="site-header">
      <div class="brand-group">
        <a href="index.html" class="brand-link">
          <span class="brand-dot" aria-hidden="true"></span>
          <span class="brand-title">VLA Modeling</span>
        </a>
        <span class="brand-divider" aria-hidden="true">/</span>
        <span class="brand-subtitle">Sổ tay học tập</span>
      </div>
      <div class="header-actions">
        <button type="button" class="theme-toggle-btn" id="theme-toggle-btn" aria-label="Đổi giao diện sáng/tối">
          <span class="theme-icon-wrap" aria-hidden="true">
            <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
            <svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
          </span>
          <span class="theme-label">Tối</span>
        </button>
      </div>
    </header>

    <!-- HERO SECTION: 2 cột (Thông tin học tập + Robot Arm IK chuẩn xác) -->
    <section class="hero-section" aria-label="Tổng quan tiến trình học tập">
      <!-- Cột Trái: Trạng thái & Tiêu điểm -->
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-pulse-dot"></span>
          <span>Lộ trình Mentor giao · 6 Paper</span>
        </div>
        
        <h1 class="hero-headline">
          Kế hoạch nghiên cứu<br>
          <span class="gradient-text">Vision-Language-Action</span>
        </h1>

        <!-- Thẻ tiêu điểm Paper đang học -->
        <div class="hero-focus-card" id="hero-focus-card">
          <div class="focus-meta">
            <span class="focus-tag" id="hero-focus-tag">ĐANG HỌC</span>
            <span class="focus-group-label" id="hero-focus-group">Đọc rộng</span>
          </div>
          <div class="focus-paper-title" id="hero-focus-title">Đang tải...</div>
          <p class="focus-paper-desc" id="hero-focus-desc">Đang đồng bộ dữ liệu lộ trình...</p>
          
          <div class="focus-actions">
            <a href="#" id="hero-focus-cta" class="btn btn--primary hero-cta-btn">
              <span>Tiếp tục học</span>
              <svg viewBox="0 0 20 20" fill="currentColor" class="btn-arrow-icon" aria-hidden="true">
                <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </a>
          </div>
        </div>

        <!-- Vòng tròn tiến độ SVG -->
        <div class="hero-progress-row">
          <div class="progress-ring-box">
            <svg class="progress-ring-svg" width="64" height="64" viewBox="0 0 64 64">
              <circle class="progress-ring-bg" cx="32" cy="32" r="26" stroke-width="5.5" fill="transparent"></circle>
              <circle id="hero-progress-circle" class="progress-ring-bar" cx="32" cy="32" r="26" stroke-width="5.5" fill="transparent" stroke-dasharray="163.36" stroke-dashoffset="163.36"></circle>
            </svg>
            <div class="progress-ring-text">
              <span id="hero-progress-fraction" class="ring-fraction">0/6</span>
            </div>
          </div>
          <div class="progress-ring-details">
            <div class="progress-ring-title">Tiến độ nghiên cứu</div>
            <div class="progress-ring-sub" id="hero-progress-sub">Đã hoàn thành 0/6 paper</div>
          </div>
        </div>
      </div>

      <!-- Cột Phải: Cánh tay Robot 2 khớp tính bằng Động học nghịch (2-Link IK) -->
      <div class="hero-visual" aria-hidden="true">
        <div class="robot-stage">
          <div class="stage-tag">pick & place</div>
          
          <svg id="robot-ik-svg" class="robot-ik-svg" viewBox="0 0 440 260" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="arm-metal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00897B" />
                <stop offset="100%" stop-color="#004D40" />
              </linearGradient>
              <linearGradient id="forearm-metal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FB8C00" />
                <stop offset="100%" stop-color="#B8650F" />
              </linearGradient>
            </defs>

            <!-- Mặt bàn thao tác phẳng sạch -->
            <rect x="20" y="230" width="400" height="14" rx="4" class="ik-bench" />
            <line x1="20" y1="230" x2="420" y2="230" stroke="var(--teal-500)" stroke-width="2" opacity="0.7" />

            <!-- Vật thể đích: Đĩa bên phải (cx=360, cy=225) -->
            <g class="ik-target-plate" transform="translate(360, 226)">
              <ellipse cx="0" cy="0" rx="34" ry="7" class="ik-plate-outer" />
              <ellipse cx="0" cy="0" rx="22" ry="4" class="ik-plate-inner" />
            </g>

            <!-- Vật thể nguồn: Bát bên trái (cx=80, cy=225) -->
            <g class="ik-source-bowl" transform="translate(80, 225)">
              <ellipse cx="0" cy="0" rx="26" ry="6" class="ik-bowl-lip" />
              <path d="M -26 0 Q 0 24 26 0 Z" class="ik-bowl-body" />
            </g>

            <!-- Khối Payload (Cube gắp đặt) -->
            <g id="ik-cube-payload" class="ik-cube-payload" transform="translate(80, 218)">
              <rect x="-8" y="-8" width="16" height="16" rx="3" class="ik-cube-face-front" />
              <path d="M -8 -8 L 0 -13 L 8 -8 L 0 -3 Z" class="ik-cube-face-top" />
              <path d="M 0 -3 L 8 -8 L 8 8 L 0 13 Z" class="ik-cube-face-right" />
            </g>

            <!-- Đế Robot cố định (cx=220, cy=230) -->
            <g class="ik-robot-base" transform="translate(220, 230)">
              <path d="M -34 0 L -22 -20 L 22 -20 L 34 0 Z" class="ik-pedestal" />
              <circle cx="0" cy="-20" r="14" class="ik-joint-base" />
              <circle cx="0" cy="-20" r="5" class="ik-joint-dot" />
            </g>

            <!-- CÁC KHỚP VÀ CÁNH TAY SẼ ĐƯỢC 2-LINK IK ĐIỀU KHIỂN TỌA ĐỘ -->
            <g id="ik-robot-arm-group">
              <!-- Link 1 (Cánh tay trên: 95px) -->
              <line id="ik-link-1-line" x1="220" y1="210" x2="160" y2="135" class="ik-arm-bar-1" />
              
              <!-- Khớp Elbow (Khớp 2) -->
              <circle id="ik-joint-elbow" cx="160" cy="135" r="10" class="ik-joint-elbow" />
              <circle id="ik-joint-elbow-dot" cx="160" cy="135" r="4" class="ik-joint-dot" />

              <!-- Link 2 (Cánh tay trước: 85px) -->
              <line id="ik-link-2-line" x1="160" y1="135" x2="80" y2="200" class="ik-arm-bar-2" />

              <!-- Khớp Cổ tay (Wrist) -->
              <circle id="ik-joint-wrist" cx="80" cy="200" r="7" class="ik-joint-wrist" />

              <!-- Đầu Kẹp (Gripper) -->
              <g id="ik-gripper-group" transform="translate(80, 200)">
                <rect x="-12" y="-4" width="24" height="6" rx="2" class="ik-gripper-crossbar" />
                <path id="ik-finger-left" d="M -10 2 L -10 18 L -4 18" class="ik-finger" />
                <path id="ik-finger-right" d="M 10 2 L 10 18 L 4 18" class="ik-finger" />
                <circle cx="0" cy="2" r="2.5" fill="#FB8C00" />
              </g>
            </g>
          </svg>
        </div>
      </div>
    </section>

    <!-- 1. DẢI BẢN ĐỒ TÀU ĐIỆN (SUBWAY LINE MAP) (Cao ~140px) -->
    <section class="subway-section" aria-label="Bản đồ trạm nghiên cứu VLA">
      <div class="subway-card">
        <div class="subway-header">
          <div class="subway-title-group">
            <svg class="subway-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="4" y="3" width="16" height="16" rx="3"></rect>
              <circle cx="8.5" cy="14.5" r="1.5"></circle>
              <circle cx="15.5" cy="14.5" r="1.5"></circle>
              <line x1="9" y1="19" x2="7" y2="21"></line>
              <line x1="15" y1="19" x2="17" y2="21"></line>
              <line x1="4" y1="11" x2="20" y2="11"></line>
            </svg>
            <h2 class="subway-title">Lộ trình Metro VLA</h2>
          </div>
          <div class="subway-legend">
            <span class="legend-item"><span class="legend-line legend-line--teal"></span> Tuyến Đọc rộng (Ga 1–3)</span>
            <span class="legend-item"><span class="legend-line legend-line--indigo"></span> Tuyến Đọc sâu (Ga 4–6)</span>
          </div>
        </div>

        <!-- SVG Bản đồ 2 Tuyến Metro với Đoàn tàu di chuyển -->
        <div class="subway-map-viewport" id="subway-map-container">
          <!-- Rendered dynamically by app.js -->
        </div>
      </div>
    </section>

    <!-- 2. KỆ SÁCH (BOOKSHELF GRID) - 2 KỆ ĐỌC RỘNG & ĐỌC SÂU -->
    <section class="bookshelf-section" aria-label="Kệ sách nghiên cứu VLA">
      <main id="bookshelf-container" class="bookshelf-container">
        <!-- Rendered dynamically by app.js using Covers from covers.js -->
      </main>
    </section>

    <!-- FOOTER -->
    <footer class="site-footer">
      <div class="footer-left">
        <strong>VLA Modeling</strong> · Sổ tay học tập và tra cứu tài liệu
      </div>
      <div class="footer-right">
        <span>Tĩnh hoàn toàn · HTML5/CSS3/Vanilla JS · 2-Link IK</span>
      </div>
    </footer>
  </div>

  <!-- Nạp Bìa SVG trước, sau đó là Dữ liệu PAPERS và App logic -->
  <script src="assets/covers.js?v=30.0"></script>
  <script src="papers.js?v=30.0"></script>
  <script src="assets/app.js?v=30.0"></script>
</body>
</html>
"""

STYLE_CSS = """/* ==========================================================================
   VLA MODELING - SỔ TAY HỌC TẬP (CSS CHUẨN FRONTEND-DESIGN)
   Bao gồm: 2-Link IK Robot Arm, Subway Line Map, Bookshelf 3-Column Grid, 3D Tilt Card & 6 SVG Covers
   ========================================================================== */

/* --- 1. DESIGN TOKENS --- */
:root {
  /* Bảng màu sáng */
  --bg-page: #F8FAF9;
  --bg-card: #FFFFFF;
  --bg-card-hover: #FCFDFB;
  --bg-card-subtle: #F3F6F4;
  --bg-active-wash: rgba(184, 101, 15, 0.04);

  --border: #E1E8E3;
  --border-subtle: #EEF2EF;
  --border-strong: #C4D0C7;
  --border-active: #B8650F;

  --ink-primary: #141E24;
  --ink-secondary: #4A5B68;
  --ink-muted: #7E909E;

  /* Màu nhấn Tuyến 1: Teal */
  --teal-500: #00897B;
  --teal-600: #00796B;
  --teal-700: #004D40;
  --teal-50: #E0F2F1;
  --teal-border: #80CBC4;

  /* Màu nhấn Tuyến 2: Chàm / Indigo */
  --indigo-500: #5B5BD6;
  --indigo-600: #4B4BC7;
  --indigo-50: #EEF0FF;
  --indigo-border: #A5A6F6;

  /* Màu nhấn Đang học / Tiếp theo: Cam */
  --orange-500: #B8650F;
  --orange-600: #9E5309;
  --orange-400: #FB8C00;
  --orange-50: #FEF3C7;
  --orange-border: #FCD34D;

  /* Typography */
  --font-sans: "Be Vietnam Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  /* Bo góc & Bóng đổ */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  --shadow-sm: 0 1px 3px rgba(18, 30, 24, 0.04), 0 1px 2px rgba(18, 30, 24, 0.02);
  --shadow-md: 0 4px 14px rgba(18, 30, 24, 0.06), 0 1px 3px rgba(18, 30, 24, 0.03);
  --shadow-lg: 0 12px 28px rgba(18, 30, 24, 0.08), 0 4px 10px rgba(18, 30, 24, 0.04);
  --shadow-active: 0 6px 20px rgba(184, 101, 15, 0.14);

  --transition-fast: 0.15s ease;
  --transition-normal: 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* --- 2. DARK THEME TOKENS --- */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg-page: #0E1519;
    --bg-card: #151F26;
    --bg-card-hover: #1A262F;
    --bg-card-subtle: #1C2933;
    --bg-active-wash: rgba(245, 158, 11, 0.08);

    --border: #263540;
    --border-subtle: #1C2730;
    --border-strong: #3B4E5D;
    --border-active: #F59E0B;

    --ink-primary: #F0F5F8;
    --ink-secondary: #9EB0BF;
    --ink-muted: #6C8091;

    --teal-500: #26A69A;
    --teal-600: #4DB6AC;
    --teal-700: #80CBC4;
    --teal-50: rgba(38, 166, 154, 0.18);
    --teal-border: rgba(38, 166, 154, 0.42);

    --indigo-500: #7C7CF8;
    --indigo-600: #9393FA;
    --indigo-50: rgba(91, 91, 214, 0.2);
    --indigo-border: rgba(124, 124, 248, 0.45);

    --orange-500: #F59E0B;
    --orange-600: #FBBF24;
    --orange-400: #FCD34D;
    --orange-50: rgba(245, 158, 11, 0.18);
    --orange-border: rgba(245, 158, 11, 0.42);

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 12px 30px rgba(0, 0, 0, 0.5);
    --shadow-active: 0 6px 24px rgba(245, 158, 11, 0.2);
  }
}

:root[data-theme="dark"] {
  --bg-page: #0E1519;
  --bg-card: #151F26;
  --bg-card-hover: #1A262F;
  --bg-card-subtle: #1C2933;
  --bg-active-wash: rgba(245, 158, 11, 0.08);

  --border: #263540;
  --border-subtle: #1C2730;
  --border-strong: #3B4E5D;
  --border-active: #F59E0B;

  --ink-primary: #F0F5F8;
  --ink-secondary: #9EB0BF;
  --ink-muted: #6C8091;

  --teal-500: #26A69A;
  --teal-600: #4DB6AC;
  --teal-700: #80CBC4;
  --teal-50: rgba(38, 166, 154, 0.18);
  --teal-border: rgba(38, 166, 154, 0.42);

  --indigo-500: #7C7CF8;
  --indigo-600: #9393FA;
  --indigo-50: rgba(91, 91, 214, 0.2);
  --indigo-border: rgba(124, 124, 248, 0.45);

  --orange-500: #F59E0B;
  --orange-600: #FBBF24;
  --orange-400: #FCD34D;
  --orange-50: rgba(245, 158, 11, 0.18);
  --orange-border: rgba(245, 158, 11, 0.42);

  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 12px 30px rgba(0, 0, 0, 0.5);
  --shadow-active: 0 6px 24px rgba(245, 158, 11, 0.2);
}

/* --- 3. RESET & BASE --- */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 15px;
  scroll-behavior: smooth;
  color-scheme: light dark;
}

body {
  font-family: var(--font-sans);
  background-color: var(--bg-page);
  color: var(--ink-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  transition: background-color var(--transition-normal), color var(--transition-normal);
}

body.page-home {
  background-image: radial-gradient(var(--border) 1px, transparent 1px);
  background-size: 24px 24px;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  background: none;
}

a:focus-visible,
button:focus-visible {
  outline: 2px solid var(--teal-500);
  outline-offset: 2px;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 24px 80px;
  position: relative;
  z-index: 1;
}

/* --- 4. AMBIENT GLOW ORBS --- */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
  filter: blur(90px);
}

.ambient-glow--teal {
  top: -100px;
  left: -80px;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #00897B, transparent 70%);
  opacity: 0.10;
}

.ambient-glow--indigo {
  top: 700px;
  right: -100px;
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, #5B5BD6, transparent 70%);
  opacity: 0.08;
}

.ambient-glow--orange {
  top: 120px;
  right: -60px;
  width: 440px;
  height: 440px;
  background: radial-gradient(circle, #FB8C00, transparent 70%);
  opacity: 0.08;
}

/* --- 5. SITE HEADER --- */
.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 36px;
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: var(--teal-500);
  box-shadow: 0 0 10px var(--teal-500);
}

.brand-title {
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--ink-primary);
}

.brand-divider {
  color: var(--border-strong);
  font-weight: 300;
  user-select: none;
}

.brand-subtitle {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  font-weight: 400;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 14px;
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--ink-secondary);
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.theme-toggle-btn:hover {
  color: var(--ink-primary);
  border-color: var(--border-strong);
  background: var(--bg-card-hover);
}

.theme-icon-wrap {
  display: inline-flex;
  position: relative;
  width: 16px;
  height: 16px;
  transition: transform 0.3s ease;
}

.theme-toggle-btn:hover .theme-icon-wrap {
  transform: rotate(20deg);
}

.sun-icon, .moon-icon {
  width: 16px;
  height: 16px;
  position: absolute;
  top: 0;
  left: 0;
  transition: opacity 0.25s ease, transform 0.25s ease;
}

:root[data-theme="light"] .sun-icon { opacity: 1; transform: scale(1); }
:root[data-theme="light"] .moon-icon { opacity: 0; transform: scale(0.5); }
:root[data-theme="dark"] .sun-icon { opacity: 0; transform: scale(0.5); }
:root[data-theme="dark"] .moon-icon { opacity: 1; transform: scale(1); }

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]):not([data-theme="dark"]) .sun-icon { opacity: 0; transform: scale(0.5); }
  :root:not([data-theme="light"]):not([data-theme="dark"]) .moon-icon { opacity: 1; transform: scale(1); }
}

/* --- 6. HERO SECTION --- */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 36px;
  align-items: center;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 36px;
  box-shadow: var(--shadow-md);
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  background: var(--teal-50);
  color: var(--teal-500);
  border: 1px solid var(--teal-border);
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  width: fit-content;
}

.badge-pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--teal-500);
  animation: badgePulse 2s infinite ease-in-out;
}

@keyframes badgePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.75); }
}

.hero-headline {
  font-size: 1.85rem;
  font-weight: 700;
  line-height: 1.25;
  letter-spacing: -0.025em;
  color: var(--ink-primary);
}

.gradient-text {
  background: linear-gradient(135deg, var(--teal-500), #004D40);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

:root[data-theme="dark"] .gradient-text {
  background: linear-gradient(135deg, #4DB6AC, #80CBC4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-focus-card {
  background: var(--bg-active-wash);
  border: 1px solid var(--orange-border);
  border-left: 4px solid var(--orange-500);
  border-radius: var(--radius-md);
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: transform var(--transition-normal), box-shadow var(--transition-normal);
}

.hero-focus-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-active);
}

.focus-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.focus-tag {
  display: inline-flex;
  padding: 3px 8px;
  background: var(--orange-50);
  color: var(--orange-500);
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  border-radius: var(--radius-sm);
  border: 1px solid var(--orange-border);
}

.focus-group-label {
  font-size: 0.8rem;
  color: var(--ink-muted);
  font-weight: 500;
}

.focus-paper-title {
  font-size: 1.22rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.focus-paper-desc {
  font-size: 0.88rem;
  color: var(--ink-secondary);
  line-height: 1.45;
}

.focus-actions {
  margin-top: 4px;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.88rem;
  border-radius: var(--radius-sm);
  padding: 9px 18px;
  transition: all var(--transition-normal);
  cursor: pointer;
}

.btn--primary {
  background-color: var(--teal-500);
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 137, 123, 0.25);
}

.btn--primary:hover {
  background-color: var(--teal-600);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 137, 123, 0.35);
  color: #FFFFFF;
}

.btn-arrow-icon {
  width: 16px;
  height: 16px;
  transition: transform var(--transition-fast);
}

.btn--primary:hover .btn-arrow-icon {
  transform: translateX(3px);
}

.hero-progress-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.progress-ring-box {
  position: relative;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-ring-svg {
  transform: rotate(-90deg);
}

.progress-ring-bg {
  stroke: var(--border);
}

.progress-ring-bar {
  stroke: var(--teal-500);
  stroke-linecap: round;
  transition: stroke-dashoffset 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.progress-ring-text {
  position: absolute;
  text-align: center;
}

.ring-fraction {
  font-size: 1rem;
  font-weight: 700;
  font-family: var(--font-sans);
  color: var(--teal-500);
}

.progress-ring-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.progress-ring-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--ink-primary);
}

.progress-ring-sub {
  font-size: 0.8rem;
  color: var(--ink-secondary);
}

/* --- 7. HERO VISUAL: 2-LINK IK ROBOT ARM --- */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.robot-stage {
  width: 100%;
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 14px;
  position: relative;
}

.stage-tag {
  position: absolute;
  top: 12px;
  right: 14px;
  font-size: 0.72rem;
  font-weight: 600;
  font-family: var(--font-mono);
  color: var(--ink-muted);
  background: var(--bg-card);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border);
  letter-spacing: 0.04em;
  z-index: 2;
}

.robot-ik-svg {
  width: 100%;
  height: auto;
  max-height: 240px;
  display: block;
}

/* Nét vẽ Robot IK */
.ik-bench { fill: var(--border-strong); }
.ik-pedestal { fill: #455A64; }
.ik-joint-base { fill: var(--teal-500); stroke: #FFFFFF; stroke-width: 2; }
.ik-joint-elbow { fill: #FB8C00; stroke: #FFFFFF; stroke-width: 2; }
.ik-joint-wrist { fill: #37474F; stroke: #FFFFFF; stroke-width: 1.5; }
.ik-joint-dot { fill: #FFFFFF; }

.ik-arm-bar-1 {
  stroke: var(--teal-500);
  stroke-width: 14;
  stroke-linecap: round;
}

.ik-arm-bar-2 {
  stroke: #FB8C00;
  stroke-width: 10;
  stroke-linecap: round;
}

.ik-gripper-crossbar { fill: #37474F; }
.ik-finger { stroke: #37474F; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; fill: none; transition: transform 0.15s ease; }

.ik-bowl-body { fill: #E0F2F1; stroke: #00897B; stroke-width: 2; }
.ik-bowl-lip { fill: #B2DFDB; stroke: #00897B; stroke-width: 1.5; }
.ik-plate-outer { fill: #FFF3E0; stroke: #FB8C00; stroke-width: 2; }
.ik-plate-inner { fill: #FFE0B2; stroke: #FB8C00; stroke-width: 1; }

.ik-cube-face-front { fill: #B8650F; }
.ik-cube-face-top { fill: #FFA726; }
.ik-cube-face-right { fill: #E65100; }

/* --- 8. SUBWAY LINE MAP (DẢI BẢN ĐỒ TÀU ĐIỆN) --- */
.subway-section {
  margin-bottom: 40px;
}

.subway-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 18px 24px 22px;
  box-shadow: var(--shadow-sm);
}

.subway-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 12px;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 10px;
}

.subway-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.subway-icon {
  width: 18px;
  height: 18px;
  color: var(--teal-500);
}

.subway-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--ink-primary);
}

.subway-legend {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 0.8rem;
  color: var(--ink-secondary);
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.legend-line {
  display: inline-block;
  width: 14px;
  height: 4px;
  border-radius: 2px;
}

.legend-line--teal { background-color: var(--teal-500); }
.legend-line--indigo { background-color: var(--indigo-500); }

.subway-map-viewport {
  position: relative;
  width: 100%;
  overflow-x: auto;
  scrollbar-width: none;
}
.subway-map-viewport::-webkit-scrollbar { display: none; }

.subway-svg {
  width: 100%;
  min-width: 720px;
  height: 120px;
  display: block;
}

/* Đường ray Metro */
.subway-track-bg {
  stroke: var(--border);
  stroke-width: 5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.subway-track-teal {
  stroke: var(--teal-500);
  stroke-width: 5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

.subway-track-indigo {
  stroke: var(--indigo-500);
  stroke-width: 5;
  stroke-linecap: round;
  stroke-linejoin: round;
  fill: none;
}

/* Trạm dừng (Station Nodes) */
.subway-station {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.subway-station:hover {
  transform: translateY(-2px);
}

.subway-station-node {
  stroke-width: 2.5;
  transition: all 0.2s ease;
}

.station-node--done {
  fill: var(--teal-500);
  stroke: #FFFFFF;
}

.station-node--active {
  fill: var(--orange-500);
  stroke: #FFFFFF;
}

.station-node--pending {
  fill: var(--bg-card);
  stroke: var(--border-strong);
}

.station-pulse-ring {
  fill: none;
  stroke: var(--orange-500);
  stroke-width: 2;
  animation: stationPulseRing 2s infinite ease-out;
  transform-origin: center;
}

@keyframes stationPulseRing {
  0% { r: 10; opacity: 0.9; }
  100% { r: 20; opacity: 0; }
}

.subway-station-label {
  font-family: var(--font-sans);
  font-size: 12px;
  font-weight: 600;
  fill: var(--ink-primary);
  text-anchor: middle;
  pointer-events: none;
}

.subway-station-num {
  font-family: var(--font-mono);
  font-size: 10px;
  fill: var(--ink-muted);
  text-anchor: middle;
  pointer-events: none;
}

/* Đoàn tàu chạy trên ray (Train Indicator) */
.subway-train-dot {
  fill: var(--orange-500);
  stroke: #FFFFFF;
  stroke-width: 3;
  filter: drop-shadow(0 2px 5px rgba(184, 101, 15, 0.4));
  transition: cx 1.2s cubic-bezier(0.16, 1, 0.3, 1), cy 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Tooltip nổi cho Ga tàu điện */
.subway-tooltip {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%) translateY(10px);
  background: var(--ink-primary);
  color: #FFFFFF;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.76rem;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease, transform 0.2s ease;
  white-space: nowrap;
  z-index: 10;
  box-shadow: var(--shadow-md);
}

.subway-tooltip.is-visible {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* --- 9. KỆ SÁCH (BOOKSHELF GRID) --- */
.bookshelf-container {
  display: flex;
  flex-direction: column;
  gap: 48px;
}

.shelf-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.shelf-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid var(--border-subtle);
  padding-bottom: 12px;
}

.shelf-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.shelf-title {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--ink-primary);
}

.shelf-title--teal { color: var(--teal-500); }
.shelf-title--indigo { color: var(--indigo-500); }

.shelf-count-pill {
  font-size: 0.76rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: var(--radius-full);
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
}

.shelf-desc {
  font-size: 0.86rem;
  color: var(--ink-muted);
}

/* Lưới thẻ sách dựng đứng: 3 cột Desktop, 2 cột Mobile */
.shelf-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

/* Thẻ sách (Book Card) với hiệu ứng 3D Tilt */
.book-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease;
  position: relative;
  opacity: 0;
  transform: translateY(20px);
}

.book-card.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.book-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--border-strong);
}

/* Thẻ đang học / Tiếp theo */
.book-card--active {
  border: 2px solid var(--orange-500);
  background: var(--bg-active-wash);
  box-shadow: var(--shadow-active);
}

.book-card--active .book-cover-wrap {
  border-bottom: 2px solid var(--orange-border);
}

/* Thẻ được cuộn tới khi bấm vào trạm Metro */
.book-card.is-highlighted-target {
  animation: cardHighlightPulse 1.4s ease-out;
}

@keyframes cardHighlightPulse {
  0% { transform: scale(1.03); box-shadow: 0 0 0 6px var(--teal-500); }
  50% { transform: scale(1.02); box-shadow: 0 0 0 4px var(--teal-border); }
  100% { transform: scale(1); box-shadow: var(--shadow-md); }
}

/* Khung bìa SVG tỉ lệ 4:3 */
.book-cover-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: var(--bg-card-subtle);
  border-bottom: 1px solid var(--border-subtle);
}

.book-cover-inner {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 12px;
  transition: filter 0.3s ease;
}

/* Nền Bìa theo nhóm */
.cover-bg--teal {
  background: linear-gradient(135deg, #E0F2F1, #B2DFDB);
}
:root[data-theme="dark"] .cover-bg--teal {
  background: linear-gradient(135deg, #092622, #0E3B35);
}

.cover-bg--indigo {
  background: linear-gradient(135deg, #EEF0FF, #DCDFFF);
}
:root[data-theme="dark"] .cover-bg--indigo {
  background: linear-gradient(135deg, #131336, #1E1E4E);
}

/* Paper chưa học: Bìa giảm bão hoà màu, hover thì rõ lại */
.book-card--unstudied .book-cover-inner {
  filter: grayscale(85%) opacity(0.75);
}

.book-card--unstudied:hover .book-cover-inner {
  filter: grayscale(0%) opacity(1);
}

.book-cover-svg {
  width: 100%;
  height: 100%;
  display: block;
}

/* Nét vẽ SVG trong Bìa */
.cv-stroke {
  stroke-linecap: round;
  stroke-linejoin: round;
}

.cv-watermark-num {
  font-family: var(--font-mono);
  font-size: 38px;
  font-weight: 700;
  fill: var(--ink-primary);
  opacity: 0.12;
}

.cv-plate { fill: var(--bg-card); stroke: var(--teal-500); stroke-width: 1.5; }
.cv-box { fill: var(--teal-50); stroke: var(--teal-500); stroke-width: 1.5; }
.cv-pill { fill: var(--teal-50); stroke: var(--teal-border); stroke-width: 1; }
.cv-plate-outer { fill: #FFF3E0; stroke: #FB8C00; stroke-width: 1.5; }
.cv-plate-inner { fill: #FFE0B2; stroke: #FB8C00; stroke-width: 1; }
.cv-bowl-body { fill: #E0F2F1; stroke: #00897B; stroke-width: 2; }
.cv-cube-item { fill: #B8650F; }

.cv-tag-text { font-size: 10px; font-weight: 600; fill: var(--ink-secondary); text-anchor: middle; font-family: var(--font-sans); }
.cv-mini-text { font-size: 9px; font-weight: 600; fill: var(--teal-700); text-anchor: middle; font-family: var(--font-sans); }
.cv-mini-label { font-size: 9px; font-weight: 600; fill: var(--ink-muted); text-anchor: middle; font-family: var(--font-sans); }

.cv-block-system2 { fill: #E0F2F1; stroke: var(--teal-500); stroke-width: 2; }
.cv-block-system1 { fill: #FFF3E0; stroke: #FB8C00; stroke-width: 2; }
.cv-system-text { font-size: 11px; font-weight: 700; fill: var(--ink-primary); text-anchor: middle; font-family: var(--font-sans); }
.cv-accent-dot { fill: var(--teal-500); }
.cv-neural-line { stroke: var(--teal-500); stroke-width: 2; stroke-dasharray: 3 3; }
.cv-limb-line { stroke: var(--border-strong); stroke-width: 2.5; fill: none; }
.cv-hand-dot { fill: #FB8C00; stroke: #FFFFFF; stroke-width: 1.5; }

.cv-eye-outline { fill: var(--bg-card); stroke: var(--teal-500); stroke-width: 1.5; }
.cv-eye-pupil { fill: var(--teal-500); }
.cv-chat-bubble { fill: var(--bg-card); stroke: var(--teal-500); stroke-width: 1.5; }
.cv-core-block { fill: var(--bg-card); stroke: var(--teal-500); stroke-width: 2; }
.cv-core-title { font-size: 13px; font-weight: 700; fill: var(--teal-500); text-anchor: middle; font-family: var(--font-sans); }
.cv-core-sub { font-size: 10px; font-weight: 600; fill: var(--ink-secondary); text-anchor: middle; font-family: var(--font-sans); }
.cv-action-path { stroke: #FB8C00; stroke-width: 2; stroke-linecap: round; }
.cv-arrow-head { fill: #FB8C00; }
.cv-act-label { font-size: 10px; font-weight: 700; fill: #FB8C00; font-family: var(--font-mono); }

.cv-axis-line { stroke: var(--indigo-500); stroke-width: 1.5; }
.cv-axis-label { font-size: 9px; font-weight: 600; fill: var(--ink-muted); font-family: var(--font-sans); }
.cv-chunk-box { fill: var(--bg-card); stroke: var(--indigo-500); stroke-width: 1.5; }
.cv-chunk-active { fill: var(--indigo-50); stroke: var(--indigo-500); stroke-width: 2; }
.cv-chunk-text { font-size: 9.5px; font-weight: 600; fill: var(--indigo-600); text-anchor: middle; font-family: var(--font-sans); }
.cv-overlap-box { fill: rgba(91, 91, 214, 0.25); stroke: var(--indigo-border); stroke-width: 1; stroke-dasharray: 2 2; }
.cv-rtc-pill { font-size: 9px; font-weight: 700; fill: var(--indigo-500); text-anchor: middle; font-family: var(--font-sans); }

.cv-train-loop-bg { fill: none; stroke: var(--border); stroke-width: 2; }
.cv-train-loop { stroke: var(--indigo-500); stroke-width: 2.5; stroke-dasharray: 8 4; }
.cv-train-block { fill: var(--bg-card); stroke: var(--indigo-500); stroke-width: 2; }

.cv-router-box { fill: var(--indigo-50); stroke: var(--indigo-500); stroke-width: 2; }
.cv-expert-line { stroke: var(--indigo-500); stroke-width: 1.5; stroke-dasharray: 2 2; }
.cv-expert-box { fill: var(--bg-card); stroke: var(--indigo-500); stroke-width: 1.5; transition: fill 0.2s, stroke-width 0.2s; }
.cv-exp-led { fill: var(--border-strong); transition: fill 0.2s; }

/* 2-3 Từ khoá nhỏ góc dưới bìa */
.cv-keywords-row {
  position: absolute;
  bottom: 8px;
  left: 10px;
  right: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.cv-kw-tag {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.85);
  color: var(--ink-secondary);
  border: 1px solid rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(4px);
}

:root[data-theme="dark"] .cv-kw-tag {
  background: rgba(21, 31, 38, 0.85);
  color: var(--ink-secondary);
  border-color: rgba(255, 255, 255, 0.08);
}

/* HOẠT ẢNH KHI HOVER TRÊN TỪNG BÌA */
/* 1. Libero: Bát trượt sang Đĩa */
.book-card:hover .cv-anim-bowl-slide {
  transform: translate(200px, 115px);
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 2. Groot: Tín hiệu thần kinh chạy từ đầu xuống tay */
.cv-signal-pulse {
  fill: var(--orange-500);
  opacity: 0;
}

.book-card:hover .cv-signal-pulse {
  opacity: 1;
  animation: signalTravel 1.2s infinite ease-in-out;
}

@keyframes signalTravel {
  0% { transform: translateY(0); opacity: 0; }
  20% { opacity: 1; }
  80% { transform: translateY(60px); opacity: 1; }
  100% { transform: translateY(60px); opacity: 0; }
}

/* 3. Qwen: Các mũi tên hành động bắn ra */
.book-card:hover .cv-arrow-1 { animation: arrowShoot 0.8s infinite alternate ease-in-out; }
.book-card:hover .cv-arrow-2 { animation: arrowShoot 0.8s 0.15s infinite alternate ease-in-out; }
.book-card:hover .cv-arrow-3 { animation: arrowShoot 0.8s 0.3s infinite alternate ease-in-out; }

@keyframes arrowShoot {
  0% { transform: translate(178px, var(--y, 78px)) scaleX(0.9); }
  100% { transform: translate(186px, var(--y, 78px)) scaleX(1.15); }
}

/* 4. RTC-Infer: Action Chunks trượt khớp nối */
.book-card:hover .cv-chunk-1 { animation: chunkSlide 1s infinite alternate ease-in-out; }
.book-card:hover .cv-chunk-3 { animation: chunkSlide 1s 0.2s infinite alternate ease-in-out; }

@keyframes chunkSlide {
  0% { transform: translateX(0); }
  100% { transform: translateX(6px); }
}

/* 5. RTC-Train: Vòng xoay huấn luyện quay liên tục */
.book-card:hover .cv-loop-group {
  animation: loopRotate 3s infinite linear;
  transform-origin: 140px 92px;
}

@keyframes loopRotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 6. MoE: Từng Expert sáng lên lần lượt */
.book-card:hover .cv-exp-1 .cv-expert-box { fill: var(--indigo-50); stroke-width: 2.5; }
.book-card:hover .cv-exp-1 .cv-exp-led { fill: #10B981; }

.book-card:hover .cv-exp-2 { animation: expertLight 1.6s 0.2s infinite ease-in-out; }
.book-card:hover .cv-exp-3 { animation: expertLight 1.6s 0.4s infinite ease-in-out; }
.book-card:hover .cv-exp-4 { animation: expertLight 1.6s 0.6s infinite ease-in-out; }

@keyframes expertLight {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; filter: brightness(1.2); }
}

/* --- 10. THÔNG TIN THẺ SÁCH (BOOK INFO) --- */
.book-info {
  padding: 16px 18px 18px;
  display: flex;
  flex-direction: column;
  flex: 1;
  gap: 10px;
}

.book-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.book-idx {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--ink-muted);
}

.book-status-tag {
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.book-status-tag--done {
  background: var(--teal-50);
  color: var(--teal-500);
  border: 1px solid var(--teal-border);
}

.book-status-tag--active {
  background: var(--orange-50);
  color: var(--orange-500);
  border: 1px solid var(--orange-border);
}

.book-status-tag--pending {
  background: var(--bg-card-subtle);
  color: var(--ink-muted);
  border: 1px solid var(--border);
}

.book-title {
  font-size: 1.18rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: var(--ink-primary);
  line-height: 1.3;
}

.arxiv-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--teal-500);
  background: var(--teal-50);
  border: 1px solid var(--teal-border);
  padding: 2px 7px;
  border-radius: var(--radius-sm);
  width: fit-content;
  transition: all var(--transition-fast);
}

.arxiv-badge:hover {
  background: var(--teal-500);
  color: #FFFFFF;
}

.book-desc {
  font-size: 0.88rem;
  color: var(--ink-secondary);
  line-height: 1.45;
  flex: 1;
}

/* Hàng nút icon tài liệu kèm Tooltip */
.book-actions-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--border-subtle);
}

.action-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-sm);
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
  transition: all var(--transition-fast);
  position: relative;
}

.action-icon-btn:hover {
  background: var(--teal-50);
  border-color: var(--teal-border);
  color: var(--teal-500);
  transform: translateY(-2px);
}

.action-icon-btn svg {
  width: 16px;
  height: 16px;
}

.no-files-label {
  font-size: 0.78rem;
  font-style: italic;
  color: var(--ink-muted);
}

/* --- 11. FOOTER & VIEWER SHARED --- */
.site-footer {
  margin-top: 60px;
  padding-top: 24px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.82rem;
  color: var(--ink-muted);
}

/* --- 12. RESPONSIVE MEDIA QUERIES --- */
@media (max-width: 960px) {
  .hero-section {
    grid-template-columns: 1fr;
    padding: 28px;
    gap: 28px;
  }

  .shelf-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 680px) {
  .container {
    padding: 16px 16px 60px;
  }

  .shelf-grid {
    grid-template-columns: 1fr;
  }

  .subway-legend {
    display: none;
  }
}

/* Giảm chuyển động theo Accessibility */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
"""

APP_JS = """/**
 * app.js - Logic điều khiển giao diện VLA Modeling
 * Bao gồm:
 * 0. 2-Link Inverse Kinematics (IK) cho cánh tay Robot Hero (requestAnimationFrame)
 * 1. Subway Line Map (Bản đồ tàu điện với vẽ lộ trình động & cuộn mượt tới thẻ sách)
 * 2. Bookshelf 3D Mouse Tilt & Render thẻ sách từ PAPERS + Covers
 * 3. Theme switch, hash sync, paper viewer
 */

(function () {
  'use strict';

  // --- 1. THEME MANAGEMENT (SÁNG / TỐI) ---
  const THEME_KEY = 'vla_theme_pref';

  function getSavedTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {}
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeToggleUI(theme);
  }

  function updateThemeToggleUI(currentTheme) {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
      const isDark = currentTheme === 'dark';
      btn.setAttribute('aria-label', isDark ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối');
      const label = btn.querySelector('.theme-label');
      if (label) label.textContent = isDark ? 'Sáng' : 'Tối';
    });
  }

  function initTheme() {
    const saved = getSavedTheme();
    if (saved === 'dark' || saved === 'light') {
      applyTheme(saved);
    } else {
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      applyTheme(prefersDark ? 'dark' : 'light');
    }

    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.theme-toggle-btn');
      if (!btn) return;
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
      saveTheme(nextTheme);
    });

    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
        if (!getSavedTheme()) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }
  }

  // --- 2. 2-LINK INVERSE KINEMATICS (IK) CHO CÁNH TAY ROBOT HERO ---
  function initRobotArmIK() {
    const svg = document.getElementById('robot-ik-svg');
    if (!svg) return;

    const link1Line = document.getElementById('ik-link-1-line');
    const link2Line = document.getElementById('ik-link-2-line');
    const elbowJoint = document.getElementById('ik-joint-elbow');
    const elbowDot = document.getElementById('ik-joint-elbow-dot');
    const wristJoint = document.getElementById('ik-joint-wrist');
    const gripperGroup = document.getElementById('ik-gripper-group');
    const fingerLeft = document.getElementById('ik-finger-left');
    const fingerRight = document.getElementById('ik-finger-right');
    const payloadCube = document.getElementById('ik-cube-payload');

    if (!link1Line || !link2Line || !elbowJoint || !wristJoint || !gripperGroup) return;

    // Thông số hình học
    const baseOrigin = { x: 220, y: 210 };
    const L1 = 95;
    const L2 = 85;
    const gripperLength = 20;

    // Vị trí các điểm mốc
    const posHome = { x: 180, y: 110 };
    const posBowlApproach = { x: 80, y: 160 };
    const posBowlPick = { x: 80, y: 212 };
    const posApex = { x: 220, y: 75 };
    const posPlateApproach = { x: 360, y: 160 };
    const posPlatePlace = { x: 360, y: 218 };
    const posPlateLift = { x: 330, y: 120 };

    // Hàm nội suy Bezier mượt
    function lerp(a, b, t) {
      return a + (b - a) * t;
    }
    function easeInOutQuad(t) {
      return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }

    // Giải Động học nghịch 2 khâu (2-link Analytical Inverse Kinematics)
    function solveIK(targetX, targetY) {
      // Đầu kẹp nằm dưới cổ tay gripperLength
      const wristX = targetX;
      const wristY = targetY - gripperLength;

      const dx = wristX - baseOrigin.x;
      const dy = wristY - baseOrigin.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      // Giới hạn trong tầm với
      const clampedDist = Math.min(Math.max(dist, 10), L1 + L2 - 0.5);
      const scale = clampedDist / (dist || 1);
      const targetDx = dx * scale;
      const targetDy = dy * scale;

      // Law of Cosines
      const cosAngle2 = (clampedDist * clampedDist - L1 * L1 - L2 * L2) / (2 * L1 * L2);
      const safeCos2 = Math.min(Math.max(cosAngle2, -1), 1);
      const angle2 = Math.acos(safeCos2); // Góc khớp khuỷu

      const alpha = Math.atan2(targetDy, targetDx);
      const beta = Math.atan2(L2 * Math.sin(angle2), L1 + L2 * Math.cos(angle2));
      const angle1 = alpha - beta; // Góc khớp vai

      const joint1X = baseOrigin.x + L1 * Math.cos(angle1);
      const joint1Y = baseOrigin.y + L1 * Math.sin(angle1);

      const joint2X = joint1X + L2 * Math.cos(angle1 + angle2);
      const joint2Y = joint1Y + L2 * Math.sin(angle1 + angle2);

      return {
        elbow: { x: joint1X, y: joint1Y },
        wrist: { x: joint2X, y: joint2Y },
        gripperTip: { x: joint2X, y: joint2Y + gripperLength }
      };
    }

    let startTime = performance.now();
    const cycleDuration = 6000; // Chu trình 6 giây

    function animate(currentTime) {
      const elapsed = (currentTime - startTime) % cycleDuration;
      const progress = elapsed / cycleDuration;

      let target = { x: posHome.x, y: posHome.y };
      let gripState = 0; // 0 = mở, 1 = đóng
      let cubePos = { x: 80, y: 218 };

      // Lộ trình 6 giai đoạn
      if (progress < 0.15) {
        // Giai đoạn 1: Từ Home tới gần Bát (0 -> 0.15)
        const t = easeInOutQuad(progress / 0.15);
        target.x = lerp(posHome.x, posBowlApproach.x, t);
        target.y = lerp(posHome.y, posBowlApproach.y, t);
        gripState = 0;
        cubePos = { x: 80, y: 218 };
      } else if (progress < 0.25) {
        // Giai đoạn 2: Hạ xuống Bát kẹp vật (0.15 -> 0.25)
        const t = easeInOutQuad((progress - 0.15) / 0.10);
        target.x = lerp(posBowlApproach.x, posBowlPick.x, t);
        target.y = lerp(posBowlApproach.y, posBowlPick.y, t);
        gripState = t > 0.6 ? 1 : 0;
        cubePos = { x: 80, y: 218 };
      } else if (progress < 0.50) {
        // Giai đoạn 3: Nhấc vật bay qua Đỉnh sang Đĩa (0.25 -> 0.50)
        const t = easeInOutQuad((progress - 0.25) / 0.25);
        if (t < 0.5) {
          const subT = t * 2;
          target.x = lerp(posBowlPick.x, posApex.x, subT);
          target.y = lerp(posBowlPick.y, posApex.y, subT);
        } else {
          const subT = (t - 0.5) * 2;
          target.x = lerp(posApex.x, posPlatePlace.x, subT);
          target.y = lerp(posApex.y, posPlatePlace.y, subT);
        }
        gripState = 1;
        cubePos = { x: target.x, y: target.y + 4 };
      } else if (progress < 0.65) {
        // Giai đoạn 4: Đặt lên Đĩa và nhả kẹp (0.50 -> 0.65)
        const t = easeInOutQuad((progress - 0.50) / 0.15);
        target.x = posPlatePlace.x;
        target.y = posPlatePlace.y;
        gripState = t > 0.4 ? 0 : 1;
        cubePos = { x: 360, y: 222 };
      } else if (progress < 0.80) {
        // Giai đoạn 5: Nhấc tay lên từ Đĩa (0.65 -> 0.80)
        const t = easeInOutQuad((progress - 0.65) / 0.15);
        target.x = lerp(posPlatePlace.x, posPlateLift.x, t);
        target.y = lerp(posPlatePlace.y, posPlateLift.y, t);
        gripState = 0;
        cubePos = { x: 360, y: 222 };
      } else {
        // Giai đoạn 6: Quay về vị trí nghỉ Home (0.80 -> 1.0)
        const t = easeInOutQuad((progress - 0.80) / 0.20);
        target.x = lerp(posPlateLift.x, posHome.x, t);
        target.y = lerp(posPlateLift.y, posHome.y, t);
        gripState = 0;
        cubePos = { x: 360, y: 222 };
      }

      // Giải IK và cập nhật SVG elements
      const ikResult = solveIK(target.x, target.y);

      link1Line.setAttribute('x1', baseOrigin.x);
      link1Line.setAttribute('y1', baseOrigin.y);
      link1Line.setAttribute('x2', ikResult.elbow.x);
      link1Line.setAttribute('y2', ikResult.elbow.y);

      elbowJoint.setAttribute('cx', ikResult.elbow.x);
      elbowJoint.setAttribute('cy', ikResult.elbow.y);
      elbowDot.setAttribute('cx', ikResult.elbow.x);
      elbowDot.setAttribute('cy', ikResult.elbow.y);

      link2Line.setAttribute('x1', ikResult.elbow.x);
      link2Line.setAttribute('y1', ikResult.elbow.y);
      link2Line.setAttribute('x2', ikResult.wrist.x);
      link2Line.setAttribute('y2', ikResult.wrist.y);

      wristJoint.setAttribute('cx', ikResult.wrist.x);
      wristJoint.setAttribute('cy', ikResult.wrist.y);

      gripperGroup.setAttribute('transform', `translate(${ikResult.wrist.x}, ${ikResult.wrist.y})`);

      // Ngón kẹp mở/đóng
      if (gripState === 1) {
        fingerLeft.setAttribute('transform', 'rotate(10, -10, 2)');
        fingerRight.setAttribute('transform', 'rotate(-10, 10, 2)');
      } else {
        fingerLeft.setAttribute('transform', 'rotate(-12, -10, 2)');
        fingerRight.setAttribute('transform', 'rotate(12, 10, 2)');
      }

      // Cập nhật vị trí khối Cube
      if (payloadCube) {
        payloadCube.setAttribute('transform', `translate(${cubePos.x}, ${cubePos.y})`);
      }

      requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
  }

  // --- 3. SUBWAY LINE MAP (BẢN ĐỒ TÀU ĐIỆN) ---
  function initSubwayMap(papers, activePaper) {
    const container = document.getElementById('subway-map-container');
    if (!container) return;

    // Tọa độ 6 trạm trên bản đồ SVG
    const stationsConfig = [
      { id: 'libero', name: '1. LIBERO', x: 60, y: 45, line: 'teal' },
      { id: 'gr00t-n1', name: '2. GR00T N1', x: 190, y: 45, line: 'teal' },
      { id: 'qwen-vla', name: '3. Qwen-VLA', x: 320, y: 45, line: 'teal' },
      { id: 'rtc-inference', name: '4. RTC-Infer', x: 460, y: 85, line: 'indigo' },
      { id: 'rtc-training', name: '5. RTC-Train', x: 590, y: 85, line: 'indigo' },
      { id: 'lingbot-vla', name: '6. LingBot-VLA', x: 720, y: 85, line: 'indigo' }
    ];

    const activeIndex = papers.findIndex(p => p.id === activePaper.id);
    const activeStation = stationsConfig[activeIndex >= 0 ? activeIndex : 1];

    let stationsSvg = '';
    stationsConfig.forEach((st, i) => {
      const paperData = papers[i] || {};
      const isDone = paperData.trangThai === 'da-present';
      const isActive = paperData.id === activePaper.id;

      let nodeClass = 'station-node--pending';
      let checkmark = '';
      let pulseRing = '';

      if (isDone) {
        nodeClass = 'station-node--done';
        checkmark = `<polyline points="${st.x - 4} ${st.y} ${st.x - 1} ${st.y + 3} ${st.x + 4} ${st.y - 3}" stroke="#FFFFFF" stroke-width="2" fill="none" />`;
      } else if (isActive) {
        nodeClass = 'station-node--active';
        pulseRing = `<circle cx="${st.x}" cy="${st.y}" r="11" class="station-pulse-ring" />`;
      }

      stationsSvg += `
        <g class="subway-station" data-paper-id="${st.id}" data-desc="${paperData.moTa || ''}" data-name="${paperData.ten}">
          ${pulseRing}
          <circle cx="${st.x}" cy="${st.y}" r="10" class="subway-station-node ${nodeClass}" />
          ${checkmark}
          <text x="${st.x}" y="${st.y + 24}" class="subway-station-label">${st.name}</text>
        </g>
      `;
    });

    const svgMarkup = `
      <svg class="subway-svg" viewBox="0 0 780 120" xmlns="http://www.w3.org/2000/svg">
        <!-- Đường ray nền mờ -->
        <path d="M 60 45 L 320 45 Q 390 45 400 65 Q 410 85 460 85 L 720 85" class="subway-track-bg" />

        <!-- Tuyến Đọc rộng (Teal: 1-3) -->
        <path d="M 60 45 L 320 45" class="subway-track-teal" />

        <!-- Đoạn chuyển tuyến (Interchange: 3-4) -->
        <path d="M 320 45 Q 390 45 400 65 Q 410 85 460 85" class="subway-track-indigo" stroke-dasharray="4 4" />

        <!-- Tuyến Đọc sâu (Indigo: 4-6) -->
        <path d="M 460 85 L 720 85" class="subway-track-indigo" />

        <!-- Các trạm ga -->
        ${stationsSvg}

        <!-- Đoàn tàu di chuyển tới trạm hiện tại -->
        <circle id="subway-train-dot" cx="${activeStation.x}" cy="${activeStation.y}" r="6.5" class="subway-train-dot" />
      </svg>
      <div id="subway-tooltip" class="subway-tooltip"></div>
    `;

    container.innerHTML = svgMarkup;

    // Tooltip & Click to scroll mượt tới thẻ sách
    const tooltip = document.getElementById('subway-tooltip');
    const stations = container.querySelectorAll('.subway-station');

    stations.forEach(station => {
      station.addEventListener('mouseenter', function (e) {
        const name = this.getAttribute('data-name');
        const desc = this.getAttribute('data-desc');
        if (tooltip) {
          tooltip.textContent = `${name}: ${desc}`;
          tooltip.classList.add('is-visible');
        }
      });

      station.addEventListener('mouseleave', function () {
        if (tooltip) tooltip.classList.remove('is-visible');
      });

      station.addEventListener('click', function () {
        const paperId = this.getAttribute('data-paper-id');
        const targetCard = document.getElementById(`card-${paperId}`);
        if (targetCard) {
          targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
          targetCard.classList.remove('is-highlighted-target');
          void targetCard.offsetWidth; // Trigger reflow
          targetCard.classList.add('is-highlighted-target');
        }
      });
    });
  }

  // --- 4. BOOKSHELF GRID & 3D TILT EFFECT ---
  function initBookshelf(papers, activePaper) {
    const container = document.getElementById('bookshelf-container');
    if (!container) return;

    const groups = [
      { name: 'Đọc rộng', themeClass: 'shelf-title--teal', hint: 'Nắm bức tranh tổng quan và các benchmark chuẩn' },
      { name: 'Đọc sâu', themeClass: 'shelf-title--indigo', hint: 'Đi vào kiến trúc chi tiết, huấn luyện và MoE' }
    ];

    let overallIndex = 1;
    let html = '';

    groups.forEach(group => {
      const groupPapers = papers.filter(p => p.nhom === group.name);
      if (groupPapers.length === 0) return;

      html += `
        <div class="shelf-group">
          <div class="shelf-header">
            <div class="shelf-title-wrap">
              <h2 class="shelf-title ${group.themeClass}">${group.name}</h2>
              <span class="shelf-count-pill">${groupPapers.length} paper</span>
            </div>
            <span class="shelf-desc">${group.hint}</span>
          </div>
          <div class="shelf-grid">
      `;

      groupPapers.forEach(paper => {
        const isDone = paper.trangThai === 'da-present';
        const isActive = paper.id === activePaper.id;
        const isUnstudied = !isDone && !isActive;

        let cardClass = 'book-card';
        if (isActive) cardClass += ' book-card--active';
        if (isUnstudied) cardClass += ' book-card--unstudied';

        // Tag trạng thái
        let statusTagHtml = '';
        if (isDone) {
          statusTagHtml = '<span class="book-status-tag book-status-tag--done">Đã xong</span>';
        } else if (isActive) {
          statusTagHtml = '<span class="book-status-tag book-status-tag--active">Tiếp theo</span>';
        } else {
          statusTagHtml = '<span class="book-status-tag book-status-tag--pending">Sắp có</span>';
        }

        // Bìa SVG từ Covers
        const coverBia = paper.bia || paper.id;
        const coverSvgMarkup = (window.Covers && typeof window.Covers.render === 'function')
          ? window.Covers.render(coverBia, paper, overallIndex)
          : `<div style="padding: 40px; text-align: center;">${paper.ten}</div>`;

        // Các nút tài liệu dạng icon nhỏ kèm tooltip
        const files = paper.files || {};
        const buttons = [];

        if (files.docHieu) {
          buttons.push(`
            <a href="paper.html?id=${paper.id}#doc-hieu" class="action-icon-btn" title="Đọc hiểu: Bản phân tích chi tiết">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
            </a>
          `);
        }
        if (files.slide) {
          buttons.push(`
            <a href="paper.html?id=${paper.id}#slide" class="action-icon-btn" title="Slide: Trình chiếu báo cáo">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
            </a>
          `);
        }
        if (files.pdfGoc) {
          buttons.push(`
            <a href="paper.html?id=${paper.id}#pdf-goc" class="action-icon-btn" title="PDF gốc: Tiếng Anh">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
            </a>
          `);
        }
        if (files.pdfViet) {
          buttons.push(`
            <a href="paper.html?id=${paper.id}#ban-dich" class="action-icon-btn" title="Bản dịch: Tiếng Việt">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg>
            </a>
          `);
        }

        const actionsHtml = buttons.length > 0
          ? buttons.join('')
          : '<span class="no-files-label">Sắp có</span>';

        const idxPad = String(overallIndex).padStart(2, '0');

        html += `
          <article class="${cardClass}" id="card-${paper.id}" data-index="${overallIndex}">
            <!-- Khung Bìa SVG 4:3 -->
            <div class="book-cover-wrap">
              ${coverSvgMarkup}
            </div>

            <!-- Thông tin bên dưới -->
            <div class="book-info">
              <div class="book-header-row">
                <span class="book-idx">${idxPad}</span>
                ${statusTagHtml}
              </div>

              <h3 class="book-title">${paper.ten}</h3>
              
              <a href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Xem trên arXiv">
                <span>arXiv:${paper.arxiv}</span>
                <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>

              <p class="book-desc">${paper.moTa}</p>

              <div class="book-actions-row">
                ${actionsHtml}
              </div>
            </div>
          </article>
        `;

        overallIndex++;
      });

      html += `
          </div>
        </div>
      `;
    });

    container.innerHTML = html;

    // Kích hoạt hiệu ứng 3D Tilt khi di chuột
    initCard3DTilt();

    // Fade-up từng thẻ với IntersectionObserver
    initScrollAnimation();
  }

  // Hiệu ứng nghiêng 3D nhẹ (tối đa 4 độ) theo vị trí chuột
  function initCard3DTilt() {
    const cards = document.querySelectorAll('.book-card');
    cards.forEach(card => {
      card.addEventListener('mousemove', function (e) {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -4; // Max 4 deg
        const rotateY = ((x - centerX) / centerX) * 4;

        card.style.transform = `perspective(800px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateY(-4px)`;
      });

      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  function initScrollAnimation() {
    const items = document.querySelectorAll('.book-card');
    if (!items.length) return;

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = parseInt(entry.target.getAttribute('data-index') || '1', 10);
            setTimeout(() => {
              entry.target.classList.add('is-visible');
            }, (index % 3) * 80);
            obs.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -40px 0px', threshold: 0.1 });

      items.forEach(item => observer.observe(item));
    } else {
      items.forEach(item => item.classList.add('is-visible'));
    }
  }

  // --- 5. INITIALIZE HOME PAGE ---
  function initHomePage() {
    if (!window.PAPERS || !Array.isArray(window.PAPERS)) return;

    const papers = window.PAPERS;
    const totalCount = papers.length;
    const completedCount = papers.filter(p => p.trangThai === 'da-present').length;

    let activePaper = papers.find(p => p.trangThai === 'dang-doc');
    if (!activePaper) {
      activePaper = papers.find(p => p.trangThai === 'chua-doc') || papers[0];
    }

    // Cập nhật thẻ tiêu điểm Hero
    const heroTitle = document.getElementById('hero-focus-title');
    const heroDesc = document.getElementById('hero-focus-desc');
    const heroGroup = document.getElementById('hero-focus-group');
    const heroTag = document.getElementById('hero-focus-tag');
    const heroCta = document.getElementById('hero-focus-cta');

    if (activePaper && heroTitle) {
      heroTitle.textContent = activePaper.ten;
      if (heroDesc) heroDesc.textContent = activePaper.moTa;
      if (heroGroup) heroGroup.textContent = activePaper.nhom;
      if (heroTag) heroTag.textContent = activePaper.trangThai === 'dang-doc' ? 'ĐANG HỌC' : 'TIẾP THEO';
      if (heroCta) {
        heroCta.href = `paper.html?id=${activePaper.id}`;
      }
    }

    // Cập nhật vòng tròn tiến độ SVG và đếm số
    const progressCircle = document.getElementById('hero-progress-circle');
    const progressFraction = document.getElementById('hero-progress-fraction');
    const progressSub = document.getElementById('hero-progress-sub');

    if (progressCircle && progressFraction) {
      const circumference = 2 * Math.PI * 26; // r=26 -> 163.36
      const targetOffset = totalCount > 0 ? circumference * (1 - completedCount / totalCount) : circumference;

      setTimeout(() => {
        progressCircle.style.strokeDashoffset = targetOffset;
      }, 150);

      let currentNum = 0;
      const stepTime = Math.max(Math.floor(1000 / (completedCount || 1)), 50);
      const timer = setInterval(() => {
        if (currentNum < completedCount) {
          currentNum++;
          progressFraction.textContent = `${currentNum}/${totalCount}`;
        } else {
          progressFraction.textContent = `${completedCount}/${totalCount}`;
          clearInterval(timer);
        }
      }, stepTime);

      if (progressSub) {
        progressSub.textContent = `Đã hoàn thành ${completedCount}/${totalCount} paper`;
      }
    }

    // 0. Robot Arm 2-Link IK
    initRobotArmIK();

    // 1. Subway Line Map
    initSubwayMap(papers, activePaper);

    // 2. Bookshelf Grid
    initBookshelf(papers, activePaper);
  }

  // --- 6. PAPER VIEWER (paper.html) ---
  const TAB_KEYS = ['doc-hieu', 'slide', 'pdf-goc', 'ban-dich', 'song-song'];

  function initPaperViewer() {
    const viewerRoot = document.getElementById('paper-viewer-root');
    if (!viewerRoot) return;

    if (!window.PAPERS || !Array.isArray(window.PAPERS)) return;

    const urlParams = new URLSearchParams(window.location.search);
    const paperId = urlParams.get('id');
    if (!paperId) return;

    const papers = window.PAPERS;
    const currentIndex = papers.findIndex(p => p.id === paperId);
    if (currentIndex === -1) return;

    const currentPaper = papers[currentIndex];
    const prevPaper = currentIndex > 0 ? papers[currentIndex - 1] : null;
    const nextPaper = currentIndex < papers.length - 1 ? papers[currentIndex + 1] : null;

    document.title = `${currentPaper.ten} · VLA Modeling`;
    const titleEl = document.getElementById('viewer-paper-title');
    if (titleEl) titleEl.textContent = currentPaper.ten;

    const arxivEl = document.getElementById('viewer-arxiv-link');
    if (arxivEl) {
      arxivEl.href = `https://arxiv.org/abs/${currentPaper.arxiv}`;
      arxivEl.innerHTML = `<span>arXiv:${currentPaper.arxiv}</span><svg viewBox="0 0 24 24" class="external-icon" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`;
    }

    const prevBtn = document.getElementById('btn-prev-paper');
    const nextBtn = document.getElementById('btn-next-paper');
    if (prevBtn) {
      if (prevPaper) {
        prevBtn.href = `paper.html?id=${prevPaper.id}`;
        prevBtn.classList.remove('is-disabled');
      } else {
        prevBtn.removeAttribute('href');
        prevBtn.classList.add('is-disabled');
      }
    }
    if (nextBtn) {
      if (nextPaper) {
        nextBtn.href = `paper.html?id=${nextPaper.id}`;
        nextBtn.classList.remove('is-disabled');
      } else {
        nextBtn.removeAttribute('href');
        nextBtn.classList.add('is-disabled');
      }
    }

    const files = currentPaper.files || {};
    const availability = {
      'doc-hieu': !!files.docHieu,
      'slide': !!files.slide,
      'pdf-goc': !!files.pdfGoc,
      'ban-dich': !!files.pdfViet,
      'song-song': !!(files.pdfGoc && files.pdfViet)
    };

    TAB_KEYS.forEach(tabKey => {
      const tabBtn = document.querySelector(`.tab-btn[data-tab="${tabKey}"]`);
      if (tabBtn) {
        if (availability[tabKey]) {
          tabBtn.classList.remove('is-disabled');
          tabBtn.removeAttribute('aria-disabled');
          const badge = tabBtn.querySelector('.tab-badge-soon');
          if (badge) badge.remove();
        } else {
          tabBtn.classList.add('is-disabled');
          tabBtn.setAttribute('aria-disabled', 'true');
          if (!tabBtn.querySelector('.tab-badge-soon')) {
            const badge = document.createElement('span');
            badge.className = 'tab-badge-soon';
            badge.textContent = 'Sắp có';
            tabBtn.appendChild(badge);
          }
        }
      }
    });

    let defaultTab = null;
    for (const key of TAB_KEYS) {
      if (availability[key]) {
        defaultTab = key;
        break;
      }
    }

    if (!defaultTab) return;

    function getSelectedTabFromHash() {
      const hash = window.location.hash.replace('#', '').trim();
      if (hash && TAB_KEYS.includes(hash) && availability[hash]) {
        return hash;
      }
      return defaultTab;
    }

    function updateTabIndicator(activeBtn) {
      const indicator = document.getElementById('tab-indicator-bar');
      if (!indicator || !activeBtn) return;
      const rect = activeBtn.getBoundingClientRect();
      const parentRect = activeBtn.parentElement.getBoundingClientRect();
      const left = rect.left - parentRect.left;
      const width = rect.width;
      indicator.style.transform = `translateX(${left}px)`;
      indicator.style.width = `${width}px`;
    }

    function switchTab(targetTab) {
      if (!availability[targetTab]) return;

      if (window.location.hash.replace('#', '') !== targetTab) {
        window.location.hash = targetTab;
      }

      let activeBtn = null;
      document.querySelectorAll('.tab-btn').forEach(btn => {
        const isMatch = btn.getAttribute('data-tab') === targetTab;
        btn.classList.toggle('is-active', isMatch);
        btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
        if (isMatch) activeBtn = btn;
      });

      if (activeBtn) updateTabIndicator(activeBtn);

      const singlePane = document.getElementById('single-view-pane');
      const parallelPane = document.getElementById('parallel-view-pane');
      const singleIframe = document.getElementById('single-iframe');
      const singleSkeleton = document.getElementById('single-skeleton');
      const openExternalBtn = document.getElementById('btn-open-external');

      if (targetTab === 'song-song') {
        if (singlePane) singlePane.classList.remove('is-active');
        if (parallelPane) parallelPane.classList.add('is-active');
        if (openExternalBtn) openExternalBtn.style.display = 'none';

        const pdfGocIframe = document.getElementById('parallel-iframe-goc');
        const pdfVietIframe = document.getElementById('parallel-iframe-viet');
        const skeletonGoc = document.getElementById('parallel-skeleton-goc');
        const skeletonViet = document.getElementById('parallel-skeleton-viet');
        const linkGoc = document.getElementById('parallel-link-goc');
        const linkViet = document.getElementById('parallel-link-viet');

        const encodedGoc = encodeURI(files.pdfGoc || '');
        const encodedViet = encodeURI(files.pdfViet || '');

        if (pdfGocIframe && pdfGocIframe.getAttribute('src') !== encodedGoc) {
          if (skeletonGoc) skeletonGoc.classList.remove('is-hidden');
          pdfGocIframe.onload = () => { if (skeletonGoc) skeletonGoc.classList.add('is-hidden'); };
          pdfGocIframe.src = encodedGoc;
        }
        if (pdfVietIframe && pdfVietIframe.getAttribute('src') !== encodedViet) {
          if (skeletonViet) skeletonViet.classList.remove('is-hidden');
          pdfVietIframe.onload = () => { if (skeletonViet) skeletonViet.classList.add('is-hidden'); };
          pdfVietIframe.src = encodedViet;
        }

        if (linkGoc) linkGoc.href = encodedGoc;
        if (linkViet) linkViet.href = encodedViet;

      } else {
        if (parallelPane) parallelPane.classList.remove('is-active');
        if (singlePane) singlePane.classList.add('is-active');
        if (openExternalBtn) openExternalBtn.style.display = 'inline-flex';

        let targetFile = null;
        if (targetTab === 'doc-hieu') targetFile = files.docHieu;
        else if (targetTab === 'slide') targetFile = files.slide;
        else if (targetTab === 'pdf-goc') targetFile = files.pdfGoc;
        else if (targetTab === 'ban-dich') targetFile = files.pdfViet;

        const encodedFile = encodeURI(targetFile || '');

        if (singleIframe && singleIframe.getAttribute('src') !== encodedFile) {
          if (singleSkeleton) singleSkeleton.classList.remove('is-hidden');
          singleIframe.classList.remove('is-loaded');

          singleIframe.onload = () => {
            if (singleSkeleton) singleSkeleton.classList.add('is-hidden');
            singleIframe.classList.add('is-loaded');
          };
          singleIframe.src = encodedFile;
        }

        if (targetTab === 'slide') {
          singleIframe.setAttribute('allow', 'fullscreen');
          singleIframe.setAttribute('allowfullscreen', 'true');
        } else {
          singleIframe.removeAttribute('allow');
        }

        if (openExternalBtn) openExternalBtn.href = encodedFile;
      }
    }

    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const tab = this.getAttribute('data-tab');
        if (availability[tab]) switchTab(tab);
      });
    });

    window.addEventListener('hashchange', function () {
      switchTab(getSelectedTabFromHash());
    });

    switchTab(getSelectedTabFromHash());
  }

  // --- 7. TỰ ĐỘNG KHỞI CHẠY ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initHomePage();
    initPaperViewer();
  });

})();
"""

README_MD = """# VLA Modeling · Sổ tay học tập

Web học tập tĩnh (HTML/CSS/JS thuần, không framework, không build) phục vụ theo dõi lộ trình đọc 6 paper VLA (Vision-Language-Action) và mở nhanh 4 loại tài liệu: trang đọc hiểu, slide trình bày, PDF gốc và PDF bản dịch tiếng Việt.

---

## 1. Cách chạy với extension Live Server

1. Trong VS Code, mở thư mục dự án `d:\\VLA Modeling`.
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
"""

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(root, 'papers.js'), 'w', encoding='utf-8') as f:
        f.write(PAPERS_JS)
    print("Updated papers.js")

    with open(os.path.join(root, 'assets', 'covers.js'), 'w', encoding='utf-8') as f:
        f.write(COVERS_JS)
    print("Created assets/covers.js")

    with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    print("Updated index.html")

    with open(os.path.join(root, 'assets', 'style.css'), 'w', encoding='utf-8') as f:
        f.write(STYLE_CSS)
    print("Updated assets/style.css")

    with open(os.path.join(root, 'assets', 'app.js'), 'w', encoding='utf-8') as f:
        f.write(APP_JS)
    print("Updated assets/app.js")

    with open(os.path.join(root, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(README_MD)
    print("Updated README.md")

if __name__ == '__main__':
    main()
