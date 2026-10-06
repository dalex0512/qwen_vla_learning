# -*- coding: utf-8 -*-
import os

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
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/style.css?v=20.0">
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
  <div class="ambient-glow ambient-glow--orange" aria-hidden="true"></div>
  <div class="ambient-glow ambient-glow--bottom" aria-hidden="true"></div>

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

    <!-- HERO SECTION: 2 cột -->
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
            <svg class="progress-ring-svg" width="68" height="68" viewBox="0 0 68 68">
              <circle class="progress-ring-bg" cx="34" cy="34" r="28" stroke-width="6" fill="transparent"></circle>
              <circle id="hero-progress-circle" class="progress-ring-bar" cx="34" cy="34" r="28" stroke-width="6" fill="transparent" stroke-dasharray="175.92" stroke-dashoffset="175.92"></circle>
            </svg>
            <div class="progress-ring-text">
              <span id="hero-progress-fraction" class="ring-fraction">0/6</span>
            </div>
          </div>
          <div class="progress-ring-details">
            <div class="progress-ring-title">Tiến độ bài học</div>
            <div class="progress-ring-sub" id="hero-progress-sub">Đã xong 0/6 paper</div>
          </div>
        </div>
      </div>

      <!-- Cột Phải: SVG Robot Arm 2 khớp chạy pick & place -->
      <div class="hero-visual" aria-hidden="true">
        <div class="robot-stage">
          <div class="stage-tag">VLA Manipulation Task · Pick & Place</div>
          
          <svg class="robot-arm-svg" viewBox="0 0 420 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid-pattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" stroke-width="0.5" class="svg-grid-line" />
              </pattern>
              <linearGradient id="arm-teal-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00897B" />
                <stop offset="100%" stop-color="#004D40" />
              </linearGradient>
              <linearGradient id="arm-orange-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FB8C00" />
                <stop offset="100%" stop-color="#B8650F" />
              </linearGradient>
            </defs>

            <!-- Lưới tọa độ bàn làm việc -->
            <rect x="10" y="10" width="400" height="250" fill="url(#grid-pattern)" opacity="0.4" rx="12" />

            <!-- Mặt bàn thao tác -->
            <rect x="20" y="250" width="380" height="12" rx="4" class="svg-bench" />
            <line x1="20" y1="250" x2="400" y2="250" stroke="#00897B" stroke-width="2" opacity="0.6" />

            <!-- Vật thể nguồn: Bát bên trái (cx=90) -->
            <g class="svg-source-bowl">
              <ellipse cx="90" cy="246" rx="28" ry="7" class="svg-bowl-lip" />
              <path d="M 62 246 Q 90 272 118 246 Z" class="svg-bowl-body" />
              <text x="90" y="282" text-anchor="middle" class="svg-label-text">Bát vật thể</text>
            </g>

            <!-- Vật thể đích: Đĩa bên phải (cx=320) -->
            <g class="svg-target-plate">
              <ellipse cx="320" cy="248" rx="36" ry="8" class="svg-plate-outer" />
              <ellipse cx="320" cy="248" rx="24" ry="5" class="svg-plate-inner" />
              <text x="320" y="282" text-anchor="middle" class="svg-label-text">Đĩa đích</text>
            </g>

            <!-- Khối lập phương thao tác (Cube payload) -->
            <g class="robot-cube-payload">
              <rect x="-10" y="-10" width="20" height="20" rx="3" class="svg-cube-body" />
              <path d="M -10 -10 L 0 -16 L 10 -10 L 0 -4 Z" class="svg-cube-top" />
              <path d="M 0 -4 L 10 -10 L 10 10 L 0 16 Z" class="svg-cube-right" />
            </g>

            <!-- Đế cố định của Robot (cx=200, cy=250) -->
            <g class="robot-base-group" transform="translate(200, 250)">
              <path d="M -36 0 L -24 -24 L 24 -24 L 36 0 Z" class="svg-base-pedestal" />
              <circle cx="0" cy="-24" r="14" class="svg-joint-outer" />
              <circle cx="0" cy="-24" r="6" class="svg-joint-inner" />
            </g>

            <!-- Khớp 1 & Cánh tay trên (Link 1) -->
            <g class="robot-link-1" transform="translate(200, 226)">
              <rect x="-8" y="-95" width="16" height="95" rx="8" class="svg-arm-segment-1" />
              <line x1="0" y1="-8" x2="0" y2="-87" stroke="#80CBC4" stroke-width="2" stroke-linecap="round" opacity="0.8" />
              
              <!-- Khớp 2 & Cánh tay trước (Link 2) -->
              <g class="robot-link-2" transform="translate(0, -95)">
                <circle cx="0" cy="0" r="11" class="svg-joint-outer" />
                <circle cx="0" cy="0" r="4.5" class="svg-joint-inner" />
                
                <rect x="-6" y="-80" width="12" height="80" rx="6" class="svg-arm-segment-2" />
                <line x1="0" y1="-6" x2="0" y2="-74" stroke="#FFE082" stroke-width="2" stroke-linecap="round" opacity="0.8" />
                
                <!-- Khớp quay cổ tay & Tay kẹp (Gripper) -->
                <g class="robot-gripper" transform="translate(0, -80)">
                  <circle cx="0" cy="0" r="7" class="svg-joint-small" />
                  <rect x="-14" y="-6" width="28" height="6" rx="2" class="svg-gripper-crossbar" />
                  
                  <path d="M -12 -6 L -12 -22 L -6 -22" class="svg-finger-left" />
                  <path d="M 12 -6 L 12 -22 L 6 -22" class="svg-finger-right" />
                  
                  <!-- Vùng quét camera / cảm biến VLA -->
                  <polygon points="0,-4 -18,-42 18,-42" class="svg-sensor-cone" opacity="0.15" />
                  <circle cx="0" cy="-3" r="2" fill="#FB8C00" />
                </g>
              </g>
            </g>
          </svg>
          <div class="stage-footer">
            <span class="stage-status-dot"></span>
            <span>Mô phỏng chu trình gắp đặt VLA (6.5s)</span>
          </div>
        </div>
      </div>
    </section>

    <!-- KHU VỰC LỘ TRÌNH CHÍNH (Roadmap Timeline) -->
    <section class="roadmap-section" aria-label="Lộ trình chi tiết 6 paper">
      <div class="roadmap-header-bar">
        <h2 class="roadmap-heading">Lộ trình nghiên cứu</h2>
        <span class="roadmap-sub">Theo dõi từ nền tảng benchmark đến các kiến trúc chuyên sâu</span>
      </div>

      <!-- Main Timeline Container -->
      <main id="paper-timeline" class="timeline-container"></main>
    </section>

    <!-- FOOTER -->
    <footer class="site-footer">
      <div class="footer-left">
        <strong>VLA Modeling</strong> · Sổ tay học tập và tra cứu tài liệu
      </div>
      <div class="footer-right">
        <span>Tĩnh hoàn toàn · HTML5/CSS3/Vanilla JS</span>
      </div>
    </footer>
  </div>

  <script src="papers.js?v=20.0"></script>
  <script src="assets/app.js?v=20.0"></script>
</body>
</html>
"""

PAPER_HTML = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Đang tải paper... · VLA Modeling</title>
  <meta name="description" content="Trình đọc tài liệu nghiên cứu VLA Modeling với hỗ trợ đọc hiểu HTML, slide và đối chiếu bản dịch song song.">
  
  <!-- Typography Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/style.css?v=20.0">
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
<body class="page-viewer">
  <div id="paper-viewer-root" class="viewer-layout">
    <!-- Top Navigation Bar -->
    <header class="viewer-topbar">
      <div class="viewer-topbar-left">
        <a href="index.html" class="nav-back-link" title="Quay lại danh sách lộ trình">
          <svg viewBox="0 0 24 24" class="nav-back-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span>Lộ trình</span>
        </a>

        <span class="nav-sep" aria-hidden="true">/</span>

        <div class="viewer-paper-info">
          <h1 id="viewer-paper-title" class="viewer-paper-title">Đang tải...</h1>
          <a id="viewer-arxiv-link" href="#" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Mở trang bài báo trên arXiv">
            <span>arXiv</span>
            <svg viewBox="0 0 24 24" class="external-icon" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
              <polyline points="15 3 21 3 21 9"></polyline>
              <line x1="10" y1="14" x2="21" y2="3"></line>
            </svg>
          </a>
        </div>
      </div>

      <div class="viewer-topbar-right">
        <!-- Nút chuyển trước / sau -->
        <div class="paper-nav-pager">
          <a href="#" id="btn-prev-paper" class="pager-btn" aria-label="Paper trước">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
            <span class="pager-text">Trước</span>
          </a>
          <a href="#" id="btn-next-paper" class="pager-btn" aria-label="Paper sau">
            <span class="pager-text">Sau</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </a>
        </div>

        <span class="nav-sep" aria-hidden="true">|</span>

        <!-- Nút mở tab mới -->
        <a href="#" id="btn-open-external" target="_blank" rel="noopener noreferrer" class="tool-btn" title="Mở file hiện tại trong tab mới">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
          <span class="tool-text">Tab mới</span>
        </a>

        <!-- Nút đổi theme -->
        <button type="button" class="theme-toggle-btn" id="theme-toggle-btn" aria-label="Đổi giao diện sáng/tối">
          <span class="theme-icon-wrap" aria-hidden="true">
            <svg class="sun-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
            <svg class="moon-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
          </span>
        </button>
      </div>
    </header>

    <!-- Tab Strip Bar với Gạch chân trượt linh hoạt -->
    <nav class="viewer-tabs-bar" aria-label="Các chế độ xem tài liệu">
      <div class="tabs-list-wrapper">
        <div class="tabs-list" role="tablist">
          <button type="button" class="tab-btn is-active" data-tab="doc-hieu" role="tab" aria-selected="true">
            <svg viewBox="0 0 24 24" class="tab-icon" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
            <span>Đọc hiểu</span>
          </button>
          <button type="button" class="tab-btn" data-tab="slide" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" class="tab-icon" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
            <span>Slide</span>
          </button>
          <button type="button" class="tab-btn" data-tab="pdf-goc" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" class="tab-icon" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <span>PDF gốc</span>
          </button>
          <button type="button" class="tab-btn" data-tab="ban-dich" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" class="tab-icon" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg>
            <span>Bản dịch Tiếng Việt</span>
          </button>
          <button type="button" class="tab-btn" data-tab="song-song" role="tab" aria-selected="false">
            <svg viewBox="0 0 24 24" class="tab-icon" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="3" x2="12" y2="21"></line></svg>
            <span>Song song (Gốc & Dịch)</span>
          </button>
          <!-- Gạch chân trượt (Sliding Indicator) -->
          <div class="tab-indicator-bar" id="tab-indicator-bar" aria-hidden="true"></div>
        </div>
      </div>
    </nav>

    <!-- Main Viewport Workspace -->
    <div id="viewer-workspace" class="viewer-workspace">
      <!-- 1. Single Viewport Pane (Đọc hiểu / Slide / PDF Gốc / Bản dịch) -->
      <section id="single-view-pane" class="viewer-iframe-pane is-active">
        <div class="iframe-skeleton-loader" id="single-skeleton" aria-hidden="true">
          <div class="skeleton-shimmer"></div>
          <div class="skeleton-content">
            <div class="skeleton-title"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line" style="width: 80%;"></div>
            <div class="skeleton-line" style="width: 65%;"></div>
          </div>
        </div>
        <iframe id="single-iframe" class="viewer-iframe" title="Khung hiển thị tài liệu"></iframe>
      </section>

      <!-- 2. Parallel Dual Viewport Pane (Song song Gốc & Dịch) -->
      <section id="parallel-view-pane" class="viewer-iframe-pane">
        <!-- Switcher thanh gạt trên thiết bị di động (< 900px) -->
        <div class="parallel-toggle-bar">
          <button type="button" class="parallel-segment-btn is-active" id="seg-btn-goc">PDF Gốc (Tiếng Anh)</button>
          <button type="button" class="parallel-segment-btn" id="seg-btn-viet">Bản dịch (Tiếng Việt)</button>
        </div>

        <div class="parallel-container">
          <!-- Cột Trái: PDF Gốc -->
          <div class="parallel-pane parallel-pane--left is-selected-mobile" id="pane-goc">
            <div class="parallel-header">
              <span class="parallel-tag"><span class="dot"></span> PDF GỐC (ENGLISH)</span>
              <a href="#" id="parallel-link-goc" target="_blank" rel="noopener noreferrer" class="parallel-popout" title="Mở toàn màn hình">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
            <div class="parallel-frame-wrap">
              <div class="iframe-skeleton-loader" id="parallel-skeleton-goc">
                <div class="skeleton-shimmer"></div>
              </div>
              <iframe id="parallel-iframe-goc" class="parallel-iframe" title="Khung PDF Gốc"></iframe>
            </div>
          </div>

          <!-- Cột Phải: Bản dịch Tiếng Việt -->
          <div class="parallel-pane parallel-pane--right" id="pane-viet">
            <div class="parallel-header">
              <span class="parallel-tag"><span class="dot dot--orange"></span> BẢN DỊCH (TIẾNG VIỆT)</span>
              <a href="#" id="parallel-link-viet" target="_blank" rel="noopener noreferrer" class="parallel-popout" title="Mở toàn màn hình">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              </a>
            </div>
            <div class="parallel-frame-wrap">
              <div class="iframe-skeleton-loader" id="parallel-skeleton-viet">
                <div class="skeleton-shimmer"></div>
              </div>
              <iframe id="parallel-iframe-viet" class="parallel-iframe" title="Khung PDF Bản dịch"></iframe>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>

  <script src="papers.js?v=20.0"></script>
  <script src="assets/app.js?v=20.0"></script>
</body>
</html>
"""

STYLE_CSS = """/* ==========================================================================
   VLA MODELING - SỔ TAY HỌC TẬP (CSS THUẦN CHUẨN CAO CẤP)
   Hỗ trợ: Responsive, Chế độ sáng/tối, Keyframes hoạt ảnh robot arm, Lộ trình, 3 Kiểu Card
   ========================================================================== */

/* --- 1. DESIGN SYSTEM TOKENS --- */
:root {
  /* Bảng màu sáng ấm áp, chuẩn Web Interface Guidelines */
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

  /* Màu nhấn Teal chính */
  --teal-500: #00897B;
  --teal-600: #00796B;
  --teal-700: #004D40;
  --teal-50: #E0F2F1;
  --teal-border: #80CBC4;

  /* Màu nhấn Cam (Đang học / Tiêu điểm) */
  --orange-500: #B8650F;
  --orange-600: #9E5309;
  --orange-400: #FB8C00;
  --orange-50: #FEF3C7;
  --orange-border: #FCD34D;

  /* Họa tiết & Lộ trình */
  --dot-grid-color: #D3DFD7;
  --timeline-track: #DFE7E1;
  --timeline-line-done: #00897B;

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
  --shadow-active: 0 6px 20px rgba(184, 101, 15, 0.12);

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

    --orange-500: #F59E0B;
    --orange-600: #FBBF24;
    --orange-400: #FCD34D;
    --orange-50: rgba(245, 158, 11, 0.18);
    --orange-border: rgba(245, 158, 11, 0.42);

    --dot-grid-color: #212F3B;
    --timeline-track: #263642;
    --timeline-line-done: #26A69A;

    --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 12px 30px rgba(0, 0, 0, 0.5);
    --shadow-active: 0 6px 24px rgba(245, 158, 11, 0.18);
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

  --orange-500: #F59E0B;
  --orange-600: #FBBF24;
  --orange-400: #FCD34D;
  --orange-50: rgba(245, 158, 11, 0.18);
  --orange-border: rgba(245, 158, 11, 0.42);

  --dot-grid-color: #212F3B;
  --timeline-track: #263642;
  --timeline-line-done: #26A69A;

  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 12px 30px rgba(0, 0, 0, 0.5);
  --shadow-active: 0 6px 24px rgba(245, 158, 11, 0.18);
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

/* Lưới chấm rất nhạt trên nền */
body.page-home {
  background-image: radial-gradient(var(--dot-grid-color) 1px, transparent 1px);
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

/* Focus outline rõ ràng */
a:focus-visible,
button:focus-visible {
  outline: 2px solid var(--teal-500);
  outline-offset: 2px;
}

/* Container chuẩn 1100px trên màn hình lớn */
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 28px 24px 80px;
  position: relative;
  z-index: 1;
}

/* --- 4. MẢNG MÀU TRÒN MỜ TRANG TRÍ (AMBIENT GLOW ORBS) --- */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
  opacity: 0.12;
  filter: blur(80px);
}

.ambient-glow--teal {
  top: -100px;
  left: -100px;
  width: 520px;
  height: 520px;
  background: radial-gradient(circle, #00897B, transparent 70%);
}

.ambient-glow--orange {
  top: 80px;
  right: -80px;
  width: 480px;
  height: 480px;
  background: radial-gradient(circle, #FB8C00, transparent 70%);
  opacity: 0.09;
}

.ambient-glow--bottom {
  top: 600px;
  left: 20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, #00897B, transparent 70%);
  opacity: 0.06;
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

/* Nút đổi theme với icon xoay 300ms */
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

/* --- 6. HERO SECTION (2 CỘT) --- */
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
  margin-bottom: 48px;
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

/* Thẻ tiêu điểm Paper đang học trong Hero */
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
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.focus-paper-desc {
  font-size: 0.88rem;
  color: var(--ink-secondary);
  line-height: 1.45;
}

.focus-actions {
  margin-top: 6px;
}

/* Nút CTA Tiếp tục học */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 600;
  font-size: 0.9rem;
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

/* Vòng tròn tiến độ SVG */
.hero-progress-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 6px;
}

.progress-ring-box {
  position: relative;
  width: 68px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-ring-svg {
  transform: rotate(-90deg);
}

.progress-ring-bg {
  stroke: var(--timeline-track);
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
  font-size: 1.05rem;
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

/* --- 7. CỘT PHẢI: HOẠT ẢNH ROBOT ARM 2 KHỚP SVG (CSS KEYFRAMES 6.5s) --- */
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
  padding: 16px;
  position: relative;
}

.stage-tag {
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--ink-muted);
  margin-bottom: 8px;
}

.robot-arm-svg {
  width: 100%;
  height: auto;
  max-height: 250px;
  display: block;
}

/* Nét vẽ phẳng SVG */
.svg-grid-line { stroke: var(--border-strong); }
.svg-bench { fill: var(--border-strong); }
.svg-bowl-body { fill: #E0F2F1; stroke: #00897B; stroke-width: 2; }
.svg-bowl-lip { fill: #B2DFDB; stroke: #00897B; stroke-width: 1.5; }
.svg-plate-outer { fill: #FFF3E0; stroke: #FB8C00; stroke-width: 2; }
.svg-plate-inner { fill: #FFE0B2; stroke: #FB8C00; stroke-width: 1; }
.svg-label-text { font-size: 11px; fill: var(--ink-muted); font-family: var(--font-sans); font-weight: 500; }

.svg-base-pedestal { fill: #455A64; }
.svg-joint-outer { fill: #00897B; stroke: #FFFFFF; stroke-width: 2; }
.svg-joint-inner { fill: #FFFFFF; }
.svg-joint-small { fill: #FB8C00; stroke: #FFFFFF; stroke-width: 1.5; }
.svg-arm-segment-1 { fill: #00897B; }
.svg-arm-segment-2 { fill: #FB8C00; }
.svg-gripper-crossbar { fill: #37474F; }
.svg-finger-left, .svg-finger-right { stroke: #37474F; stroke-width: 3.5; stroke-linecap: round; stroke-linejoin: round; fill: none; }
.svg-sensor-cone { fill: #FB8C00; }

.svg-cube-body { fill: #B8650F; }
.svg-cube-top { fill: #FFA726; }
.svg-cube-right { fill: #E65100; }

.stage-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 0.75rem;
  color: var(--ink-muted);
}

.stage-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--teal-500);
}

/* ROBOT ARM KEYFRAME ANIMATIONS (6.5s Cycle) */
/* Khớp 1: Quay quanh gốc (200, 226) */
.robot-link-1 {
  animation: armLink1Cycle 6.5s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
  transform-origin: 0 0;
}

@keyframes armLink1Cycle {
  0%   { transform: rotate(-15deg); }
  12%  { transform: rotate(-48deg); } /* Xuống bát gắp */
  22%  { transform: rotate(-48deg); } /* Kẹp vật */
  38%  { transform: rotate(0deg); }   /* Nhấc lên đỉnh */
  54%  { transform: rotate(44deg); }  /* Hạ xuống đĩa */
  64%  { transform: rotate(44deg); }  /* Nhả vật */
  78%  { transform: rotate(10deg); }  /* Nhấc lên */
  90%  { transform: rotate(-15deg); } /* Về vị trí nghỉ */
  100% { transform: rotate(-15deg); }
}

/* Khớp 2: Quay quanh đầu cánh tay 1 */
.robot-link-2 {
  animation: armLink2Cycle 6.5s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
  transform-origin: 0 0;
}

@keyframes armLink2Cycle {
  0%   { transform: rotate(30deg); }
  12%  { transform: rotate(72deg); }  /* Cong xuống bát */
  22%  { transform: rotate(72deg); }
  38%  { transform: rotate(15deg); }  /* Duỗi nhẹ khi qua đỉnh */
  54%  { transform: rotate(-68deg); } /* Cong xuống đĩa */
  64%  { transform: rotate(-68deg); }
  78%  { transform: rotate(15deg); }
  90%  { transform: rotate(30deg); }
  100% { transform: rotate(30deg); }
}

/* Cổ tay / Tay kẹp Gripper */
.robot-gripper {
  animation: gripperAngleCycle 6.5s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
  transform-origin: 0 0;
}

@keyframes gripperAngleCycle {
  0%   { transform: rotate(-15deg); }
  12%  { transform: rotate(-24deg); } /* Giữ thẳng vuông góc bề mặt */
  22%  { transform: rotate(-24deg); }
  38%  { transform: rotate(-15deg); }
  54%  { transform: rotate(24deg); }
  64%  { transform: rotate(24deg); }
  78%  { transform: rotate(-5deg); }
  90%  { transform: rotate(-15deg); }
  100% { transform: rotate(-15deg); }
}

/* Ngón tay kẹp (Fingers) mở & đóng */
.svg-finger-left {
  animation: fingerLeftGrip 6.5s infinite ease-in-out;
  transform-origin: -12px -6px;
}
.svg-finger-right {
  animation: fingerRightGrip 6.5s infinite ease-in-out;
  transform-origin: 12px -6px;
}

@keyframes fingerLeftGrip {
  0%, 10% { transform: rotate(-12deg); }
  16%, 60% { transform: rotate(0deg); } /* Đóng kẹp chặt khối cube */
  64%, 100% { transform: rotate(-12deg); } /* Mở ngón */
}

@keyframes fingerRightGrip {
  0%, 10% { transform: rotate(12deg); }
  16%, 60% { transform: rotate(0deg); }
  64%, 100% { transform: rotate(12deg); }
}

/* Khối cube di chuyển theo chu trình */
.robot-cube-payload {
  animation: cubePayloadMotion 6.5s infinite cubic-bezier(0.45, 0.05, 0.55, 0.95);
}

@keyframes cubePayloadMotion {
  0%, 15% { transform: translate(90px, 240px) scale(0.9); } /* Nằm trong bát */
  22%     { transform: translate(90px, 238px) scale(1); }   /* Được gắp */
  38%     { transform: translate(200px, 120px) scale(1); }  /* Bay qua giữa */
  54%, 64% { transform: translate(320px, 240px) scale(1); } /* Đặt lên đĩa */
  76%, 100% { transform: translate(320px, 240px) scale(0.9); } /* Nằm trên đĩa */
}

/* --- 8. ROADMAP SECTION & TIMELINE --- */
.roadmap-section {
  margin-top: 10px;
}

.roadmap-header-bar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 32px;
  border-bottom: 2px solid var(--border-subtle);
  padding-bottom: 14px;
}

.roadmap-heading {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--ink-primary);
}

.roadmap-sub {
  font-size: 0.88rem;
  color: var(--ink-secondary);
}

.timeline-container {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

/* Nhóm Lộ trình: Đọc rộng / Đọc sâu */
.timeline-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 8px 0;
}

.group-title-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.group-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.group-count-pill {
  display: inline-flex;
  padding: 3px 10px;
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ink-secondary);
}

.group-desc {
  font-size: 0.85rem;
  color: var(--ink-muted);
}

/* Danh sách Node nối nhau bằng đường kẻ dọc */
.paper-list {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-left: 54px;
}

/* Đường dọc nối các paper */
.paper-list::before {
  content: "";
  position: absolute;
  top: 24px;
  bottom: 24px;
  left: 20px;
  width: 2px;
  background: var(--timeline-track);
  border-left: 2px dashed var(--border-strong);
  z-index: 0;
}

/* Node trên lộ trình */
.paper-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.paper-item.is-visible {
  opacity: 1;
  transform: translateY(0);
}

/* Biểu tượng nút tròn Timeline */
.timeline-node {
  position: absolute;
  left: -54px;
  top: 16px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.95rem;
  z-index: 2;
  transition: all var(--transition-normal);
  background: var(--bg-card);
}

/* 1. Trạng thái ĐÃ XONG (da-present) */
.timeline-node--done {
  background: var(--teal-500);
  color: #FFFFFF;
  box-shadow: 0 0 0 4px var(--teal-50);
}

.timeline-node--done svg {
  width: 18px;
  height: 18px;
  stroke: #FFFFFF;
  stroke-width: 3;
}

/* 2. Trạng thái ĐANG HỌC (is-active / is-reading) */
.timeline-node--active {
  background: var(--bg-card);
  border: 3px solid var(--orange-500);
  color: var(--orange-500);
  box-shadow: 0 0 0 4px var(--orange-50);
  animation: activeNodePulse 2s infinite ease-in-out;
}

@keyframes activeNodePulse {
  0%, 100% { box-shadow: 0 0 0 4px var(--orange-50), 0 0 12px rgba(184, 101, 15, 0.2); }
  50% { box-shadow: 0 0 0 8px rgba(184, 101, 15, 0.1), 0 0 18px rgba(184, 101, 15, 0.35); }
}

/* 3. Trạng thái CHƯA TỚI (chua-doc) */
.timeline-node--pending {
  background: var(--bg-card);
  border: 2px solid var(--border-strong);
  color: var(--ink-muted);
}

/* --- 9. THẺ PAPER: 3 KIỂU CARD --- */
.paper-card {
  flex: 1;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal), border-color var(--transition-normal);
}

.paper-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--border-strong);
}

/* KIỂU 1: ĐÃ XONG (da-present) - Thẻ đầy đủ, 4 nút SVG */
.paper-card--completed {
  padding: 20px 24px;
}

.card-top-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 8px;
}

.card-title-group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.card-title {
  font-size: 1.18rem;
  font-weight: 700;
  color: var(--ink-primary);
}

.arxiv-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--teal-500);
  background: var(--teal-50);
  border: 1px solid var(--teal-border);
  padding: 2px 7px;
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.arxiv-link:hover {
  background: var(--teal-500);
  color: #FFFFFF;
}

.arxiv-link svg {
  width: 12px;
  height: 12px;
}

.card-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 600;
}

.card-badge--completed {
  background: var(--teal-50);
  color: var(--teal-500);
  border: 1px solid var(--teal-border);
}

.card-badge--active {
  background: var(--orange-50);
  color: var(--orange-500);
  border: 1px solid var(--orange-border);
}

.card-badge--pending {
  background: var(--bg-card-subtle);
  color: var(--ink-muted);
  border: 1px solid var(--border);
}

.card-desc {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 18px;
}

/* Lưới 4 nút hành động SVG */
.card-actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.doc-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px 14px;
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: all var(--transition-normal);
  color: var(--ink-primary);
  text-decoration: none;
  cursor: pointer;
}

.doc-btn:hover {
  background: var(--teal-50);
  border-color: var(--teal-border);
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 137, 123, 0.12);
}

.doc-btn-header {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.84rem;
  font-weight: 600;
  margin-bottom: 2px;
}

.doc-btn-icon {
  width: 15px;
  height: 15px;
  stroke: var(--teal-500);
  transition: transform var(--transition-fast);
}

.doc-btn:hover .doc-btn-icon {
  transform: translateY(-1px) scale(1.08);
}

.doc-btn-sub {
  font-size: 0.72rem;
  color: var(--ink-muted);
}

/* KIỂU 2: ĐANG HỌC / TIẾP THEO (is-active / dang-doc) */
.paper-card--active {
  padding: 24px;
  border-left: 4px solid var(--orange-500);
  background: var(--bg-active-wash);
  box-shadow: var(--shadow-active);
}

.missing-docs-note {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: var(--bg-card);
  border: 1px dashed var(--orange-border);
  border-radius: var(--radius-sm);
  font-size: 0.8rem;
  color: var(--orange-500);
  margin-top: 10px;
}

.missing-docs-note svg {
  width: 14px;
  height: 14px;
}

/* KIỂU 3: CHƯA TỚI (chua-doc) - Thu gọn 1 dòng (Compact single row) */
.paper-card--compact {
  padding: 14px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.compact-info-col {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.compact-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--ink-primary);
  white-space: nowrap;
}

.compact-desc {
  font-size: 0.85rem;
  color: var(--ink-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.compact-actions-col {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.mini-action-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  font-size: 0.75rem;
  font-weight: 500;
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  color: var(--ink-secondary);
  transition: all var(--transition-fast);
}

.mini-action-pill:hover {
  background: var(--teal-50);
  border-color: var(--teal-border);
  color: var(--teal-500);
}

.mini-action-pill svg {
  width: 12px;
  height: 12px;
}

/* --- 10. SITE FOOTER --- */
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

/* --- 11. PAPER VIEWER STYLES (paper.html) --- */
.page-viewer {
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.viewer-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
}

.viewer-topbar {
  flex-shrink: 0;
  height: 54px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  gap: 16px;
}

.viewer-topbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.nav-back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--ink-secondary);
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.nav-back-link:hover {
  color: var(--ink-primary);
  border-color: var(--border-strong);
}

.nav-back-icon {
  width: 15px;
  height: 15px;
}

.nav-sep {
  color: var(--border-strong);
  user-select: none;
}

.viewer-paper-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.viewer-paper-title {
  font-size: 1.05rem;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--ink-primary);
}

.arxiv-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: var(--font-mono);
  font-size: 0.74rem;
  color: var(--teal-500);
  background: var(--teal-50);
  border: 1px solid var(--teal-border);
  padding: 2px 6px;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.external-icon {
  width: 11px;
  height: 11px;
}

.viewer-topbar-right {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.paper-nav-pager {
  display: inline-flex;
  align-items: center;
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.pager-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 9px;
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--ink-secondary);
  transition: all var(--transition-fast);
}

.pager-btn:hover:not(.is-disabled) {
  background: var(--bg-card);
  color: var(--ink-primary);
}

.pager-btn.is-disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}

.pager-btn svg {
  width: 14px;
  height: 14px;
}

.tool-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--ink-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  transition: all var(--transition-fast);
}

.tool-btn:hover {
  color: var(--ink-primary);
  border-color: var(--border-strong);
}

.tool-btn svg {
  width: 14px;
  height: 14px;
}

/* Tab Strip Bar với Gạch chân trượt */
.viewer-tabs-bar {
  flex-shrink: 0;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  padding: 0 16px;
}

.tabs-list-wrapper {
  overflow-x: auto;
  scrollbar-width: none;
}
.tabs-list-wrapper::-webkit-scrollbar { display: none; }

.tabs-list {
  display: inline-flex;
  align-items: center;
  position: relative;
  gap: 4px;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  font-size: 0.86rem;
  font-weight: 500;
  color: var(--ink-secondary);
  position: relative;
  z-index: 1;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  transition: color var(--transition-fast);
}

.tab-btn:hover:not(.is-disabled) {
  color: var(--ink-primary);
}

.tab-btn.is-active {
  color: var(--teal-500);
  font-weight: 600;
}

.tab-btn.is-disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.tab-icon {
  width: 15px;
  height: 15px;
}

.tab-badge-soon {
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: var(--radius-full);
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  color: var(--ink-muted);
}

/* Thanh gạch chân trượt (Sliding Indicator) */
.tab-indicator-bar {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: var(--teal-500);
  border-radius: 3px 3px 0 0;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), width 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  pointer-events: none;
  z-index: 2;
}

/* Workspace & Iframe Skeleton */
.viewer-workspace {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #1E293B;
}

.viewer-iframe-pane {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: none;
}

.viewer-iframe-pane.is-active {
  display: flex;
}

.viewer-iframe {
  flex: 1;
  width: 100%;
  height: 100%;
  border: none;
  background: #FFFFFF;
  opacity: 0;
  transition: opacity 0.35s ease;
}

.viewer-iframe.is-loaded {
  opacity: 1;
}

/* Khung xương tải trang (Skeleton Shimmer) */
.iframe-skeleton-loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--bg-page);
  display: flex;
  flex-direction: column;
  padding: 40px;
  gap: 20px;
  z-index: 1;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.iframe-skeleton-loader.is-hidden {
  opacity: 0;
}

.skeleton-shimmer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
  animation: shimmerMove 1.5s infinite;
}

@keyframes shimmerMove {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.skeleton-content {
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-title {
  height: 28px;
  width: 50%;
  background: var(--border-strong);
  border-radius: var(--radius-sm);
  opacity: 0.5;
}

.skeleton-line {
  height: 14px;
  width: 100%;
  background: var(--border);
  border-radius: var(--radius-sm);
  opacity: 0.5;
}

/* Parallel View Container (Song song Gốc & Dịch) */
.parallel-container {
  flex: 1;
  display: flex;
  width: 100%;
  height: 100%;
  gap: 2px;
  background: var(--border);
}

.parallel-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-card);
  height: 100%;
  min-width: 0;
  transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.parallel-pane--left {
  animation: slideInLeft 0.35s ease forwards;
}

.parallel-pane--right {
  animation: slideInRight 0.35s ease forwards;
}

@keyframes slideInLeft {
  from { transform: translateX(-24px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInRight {
  from { transform: translateX(24px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.parallel-header {
  height: 38px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 14px;
  background: var(--bg-card-subtle);
  border-bottom: 1px solid var(--border);
  font-size: 0.78rem;
  font-weight: 600;
}

.parallel-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--ink-secondary);
}

.parallel-tag .dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--teal-500);
}

.parallel-tag .dot--orange {
  background: var(--orange-500);
}

.parallel-frame-wrap {
  flex: 1;
  position: relative;
  height: calc(100% - 38px);
}

.parallel-iframe {
  width: 100%;
  height: 100%;
  border: none;
  background: #FFFFFF;
}

/* Switcher gạt trên mobile (< 900px) */
.parallel-toggle-bar {
  display: none;
  padding: 8px 12px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
  gap: 8px;
}

.parallel-segment-btn {
  flex: 1;
  padding: 7px;
  font-size: 0.8rem;
  font-weight: 600;
  border-radius: var(--radius-sm);
  background: var(--bg-card-subtle);
  border: 1px solid var(--border);
  color: var(--ink-secondary);
}

.parallel-segment-btn.is-active {
  background: var(--teal-500);
  border-color: var(--teal-500);
  color: #FFFFFF;
}

/* Empty & 404 */
.viewer-empty-state, .not-found-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  max-width: 480px;
  margin: 0 auto;
}

.empty-icon {
  width: 48px;
  height: 48px;
  stroke: var(--ink-muted);
  stroke-width: 1.5;
  fill: none;
  margin-bottom: 16px;
}

.back-home-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  border-radius: var(--radius-sm);
  background: var(--teal-500);
  color: #FFFFFF;
  font-weight: 600;
  margin-top: 20px;
}

/* --- 12. RESPONSIVE MEDIA QUERIES --- */
@media (max-width: 900px) {
  .hero-section {
    grid-template-columns: 1fr;
    padding: 24px;
    gap: 24px;
  }

  .card-actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .parallel-container {
    flex-direction: column;
  }

  .parallel-toggle-bar {
    display: flex;
  }

  .parallel-pane {
    display: none;
  }

  .parallel-pane.is-selected-mobile {
    display: flex;
  }
}

@media (max-width: 640px) {
  .container {
    padding: 16px 16px 60px;
  }

  .paper-list {
    padding-left: 44px;
  }

  .paper-list::before {
    left: 16px;
  }

  .timeline-node {
    left: -44px;
    width: 34px;
    height: 34px;
    font-size: 0.85rem;
  }

  .card-actions-grid {
    grid-template-columns: 1fr;
  }

  .paper-card--compact {
    flex-direction: column;
    align-items: flex-start;
  }

  .viewer-paper-title {
    max-width: 160px;
  }
}

/* Giảm chuyển động theo cài đặt hệ thống (Accessibility) */
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
 * Hỗ trợ 3 kiểu thẻ paper, lộ trình SVG, đếm tiến độ vòng tròn, tab indicator và song song hóa PDF.
 */

(function () {
  'use strict';

  // --- 1. QUẢN LÝ GIAO DIỆN SÁNG / TỐI (THEME) ---
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

  // --- 2. XỬ LÝ TRANG CHỦ (index.html) ---
  function initHomePage() {
    const paperContainer = document.getElementById('paper-timeline');
    if (!paperContainer) return;

    if (!window.PAPERS || !Array.isArray(window.PAPERS)) {
      paperContainer.innerHTML = '<p style="padding: 20px; color: red;">Không tìm thấy danh sách PAPERS trong papers.js.</p>';
      return;
    }

    const papers = window.PAPERS;
    const totalCount = papers.length;
    const completedCount = papers.filter(p => p.trangThai === 'da-present').length;

    // Tìm paper "đang học": paper đầu tiên có trangThai === 'dang-doc', nếu không có thì lấy paper 'chua-doc' đầu tiên
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

    // Cập nhật vòng tròn tiến độ SVG và chạy đếm số từ 0 -> completedCount
    const progressCircle = document.getElementById('hero-progress-circle');
    const progressFraction = document.getElementById('hero-progress-fraction');
    const progressSub = document.getElementById('hero-progress-sub');

    if (progressCircle && progressFraction) {
      const circumference = 2 * Math.PI * 28; // r=28 -> ~175.92
      const targetOffset = totalCount > 0 ? circumference * (1 - completedCount / totalCount) : circumference;
      
      // Kích hoạt hoạt ảnh vòng tròn
      setTimeout(() => {
        progressCircle.style.strokeDashoffset = targetOffset;
      }, 150);

      // Đếm số tăng dần
      let currentNum = 0;
      const duration = 1000;
      const stepTime = Math.max(Math.floor(duration / (completedCount || 1)), 50);
      
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
        progressSub.textContent = `Đã hoàn thành ${completedCount} trên ${totalCount} paper`;
      }
    }

    // Nhóm papers theo nhom ("Đọc rộng" và "Đọc sâu")
    const groups = [
      { name: 'Đọc rộng', hint: 'Nắm bức tranh tổng quan và các benchmark chuẩn' },
      { name: 'Đọc sâu', hint: 'Đi vào kiến trúc chi tiết, huấn luyện và MoE' }
    ];

    let overallIndex = 1;
    let html = '';

    groups.forEach(group => {
      const groupPapers = papers.filter(p => p.nhom === group.name);
      if (groupPapers.length === 0) return;

      html += `
        <div class="timeline-group">
          <div class="group-header">
            <div class="group-title-wrap">
              <h3 class="group-title">${group.name}</h3>
              <span class="group-count-pill">${groupPapers.length} paper</span>
            </div>
            <span class="group-desc">${group.hint}</span>
          </div>
          <div class="paper-list">
      `;

      groupPapers.forEach(paper => {
        const isDone = paper.trangThai === 'da-present';
        const isActive = paper.id === activePaper.id;
        const isPending = !isDone && !isActive;

        // Xác định class cho timeline node
        let nodeClass = 'timeline-node--pending';
        let nodeContent = overallIndex;

        if (isDone) {
          nodeClass = 'timeline-node--done';
          nodeContent = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        } else if (isActive) {
          nodeClass = 'timeline-node--active';
          nodeContent = overallIndex;
        }

        const files = paper.files || {};
        const hasDocHieu = !!files.docHieu;
        const hasSlide = !!files.slide;
        const hasPdfGoc = !!files.pdfGoc;
        const hasPdfViet = !!files.pdfViet;

        html += `<article class="paper-item" data-index="${overallIndex}">`;
        html += `<div class="timeline-node ${nodeClass}">${nodeContent}</div>`;

        // 3 KIỂU THẺ:
        if (isDone) {
          // KIỂU 1: ĐÃ XONG (da-present) - Đầy đủ 4 nút SVG
          html += `
            <div class="paper-card paper-card--completed">
              <div class="card-top-row">
                <div class="card-title-group">
                  <h4 class="card-title">${paper.ten}</h4>
                  <a href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer" class="arxiv-link" title="Xem trên arXiv">
                    <span>arXiv:${paper.arxiv}</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  </a>
                </div>
                <span class="card-badge card-badge--completed">Đã xong</span>
              </div>
              <p class="card-desc">${paper.moTa}</p>
              <div class="card-actions-grid">
                <a href="paper.html?id=${paper.id}#doc-hieu" class="doc-btn">
                  <div class="doc-btn-header">
                    <svg class="doc-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                    <span>Đọc hiểu</span>
                  </div>
                  <span class="doc-btn-sub">Bản phân tích</span>
                </a>
                <a href="paper.html?id=${paper.id}#slide" class="doc-btn">
                  <div class="doc-btn-header">
                    <svg class="doc-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
                    <span>Slide</span>
                  </div>
                  <span class="doc-btn-sub">Trình chiếu</span>
                </a>
                <a href="paper.html?id=${paper.id}#pdf-goc" class="doc-btn">
                  <div class="doc-btn-header">
                    <svg class="doc-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                    <span>PDF gốc</span>
                  </div>
                  <span class="doc-btn-sub">Bản tiếng Anh</span>
                </a>
                <a href="paper.html?id=${paper.id}#ban-dich" class="doc-btn">
                  <div class="doc-btn-header">
                    <svg class="doc-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg>
                    <span>Bản dịch</span>
                  </div>
                  <span class="doc-btn-sub">Tiếng Việt</span>
                </a>
              </div>
            </div>
          `;
        } else if (isActive) {
          // KIỂU 2: ĐANG HỌC / TIẾP THEO - Nổi bật viền cam 4px, gộp các file còn thiếu
          const missingFiles = [];
          if (!hasDocHieu) missingFiles.push('Đọc hiểu');
          if (!hasSlide) missingFiles.push('Slide');
          if (!hasPdfGoc) missingFiles.push('PDF gốc');
          if (!hasPdfViet) missingFiles.push('Bản dịch');

          let actionButtonsHtml = '';
          if (hasDocHieu) actionButtonsHtml += `<a href="paper.html?id=${paper.id}#doc-hieu" class="doc-btn"><div class="doc-btn-header"><span>Đọc hiểu</span></div><span class="doc-btn-sub">HTML</span></a>`;
          if (hasSlide) actionButtonsHtml += `<a href="paper.html?id=${paper.id}#slide" class="doc-btn"><div class="doc-btn-header"><span>Slide</span></div><span class="doc-btn-sub">Trình chiếu</span></a>`;
          if (hasPdfGoc) actionButtonsHtml += `<a href="paper.html?id=${paper.id}#pdf-goc" class="doc-btn"><div class="doc-btn-header"><span>PDF gốc</span></div><span class="doc-btn-sub">Tiếng Anh</span></a>`;
          if (hasPdfViet) actionButtonsHtml += `<a href="paper.html?id=${paper.id}#ban-dich" class="doc-btn"><div class="doc-btn-header"><span>Bản dịch</span></div><span class="doc-btn-sub">Tiếng Việt</span></a>`;

          html += `
            <div class="paper-card paper-card--active">
              <div class="card-top-row">
                <div class="card-title-group">
                  <h4 class="card-title">${paper.ten}</h4>
                  <a href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer" class="arxiv-link" title="Xem trên arXiv">
                    <span>arXiv:${paper.arxiv}</span>
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  </a>
                </div>
                <span class="card-badge card-badge--active">Tiếp theo</span>
              </div>
              <p class="card-desc">${paper.moTa}</p>
              ${actionButtonsHtml ? `<div class="card-actions-grid" style="margin-bottom: 12px;">${actionButtonsHtml}</div>` : ''}
              ${missingFiles.length > 0 ? `
                <div class="missing-docs-note">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  <span>Còn thiếu: ${missingFiles.join(', ')}</span>
                </div>
              ` : ''}
            </div>
          `;
        } else {
          // KIỂU 3: CHƯA TỚI - Thẻ thu gọn 1 dòng (Compact)
          let miniActionsHtml = '';
          if (hasPdfGoc) miniActionsHtml += `<a href="paper.html?id=${paper.id}#pdf-goc" class="mini-action-pill" title="Mở PDF gốc">PDF gốc</a>`;
          if (hasPdfViet) miniActionsHtml += `<a href="paper.html?id=${paper.id}#ban-dich" class="mini-action-pill" title="Mở Bản dịch">Bản dịch</a>`;

          html += `
            <div class="paper-card paper-card--compact">
              <div class="compact-info-col">
                <span class="compact-title">${paper.ten}</span>
                <a href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer" class="arxiv-link">
                  <span>arXiv:${paper.arxiv}</span>
                </a>
                <span class="compact-desc">${paper.moTa}</span>
              </div>
              <div class="compact-actions-col">
                ${miniActionsHtml}
                <span class="card-badge card-badge--pending">Sắp có</span>
              </div>
            </div>
          `;
        }

        html += `</article>`;
        overallIndex++;
      });

      html += `
          </div>
        </div>
      `;
    });

    paperContainer.innerHTML = html;

    // Hiệu ứng Fade-up từng thẻ cách nhau 60ms với IntersectionObserver
    initScrollAnimation();
  }

  function initScrollAnimation() {
    const items = document.querySelectorAll('.paper-item');
    if (!items.length) return;

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const index = parseInt(entry.target.getAttribute('data-index') || '1', 10);
            setTimeout(() => {
              entry.target.classList.add('is-visible');
            }, (index % 6) * 60);
            obs.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -40px 0px', threshold: 0.1 });

      items.forEach(item => observer.observe(item));
    } else {
      items.forEach(item => item.classList.add('is-visible'));
    }
  }

  // --- 3. XỬ LÝ TRANG XEM PAPER (paper.html) ---
  const TAB_KEYS = ['doc-hieu', 'slide', 'pdf-goc', 'ban-dich', 'song-song'];

  function initPaperViewer() {
    const viewerRoot = document.getElementById('paper-viewer-root');
    if (!viewerRoot) return;

    if (!window.PAPERS || !Array.isArray(window.PAPERS)) {
      renderNotFound('Không tải được danh sách PAPERS từ papers.js.');
      return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const paperId = urlParams.get('id');

    if (!paperId) {
      renderNotFound('Thiếu tham số ID paper trong đường dẫn (?id=...).');
      return;
    }

    const papers = window.PAPERS;
    const currentIndex = papers.findIndex(p => p.id === paperId);

    if (currentIndex === -1) {
      renderNotFound(`Không tìm thấy paper với mã định danh "${paperId}".`);
      return;
    }

    const currentPaper = papers[currentIndex];
    const prevPaper = currentIndex > 0 ? papers[currentIndex - 1] : null;
    const nextPaper = currentIndex < papers.length - 1 ? papers[currentIndex + 1] : null;

    // Render thông tin header
    document.title = `${currentPaper.ten} · VLA Modeling`;
    const titleEl = document.getElementById('viewer-paper-title');
    if (titleEl) titleEl.textContent = currentPaper.ten;

    const arxivEl = document.getElementById('viewer-arxiv-link');
    if (arxivEl) {
      arxivEl.href = `https://arxiv.org/abs/${currentPaper.arxiv}`;
      arxivEl.innerHTML = `<span>arXiv:${currentPaper.arxiv}</span><svg viewBox="0 0 24 24" class="external-icon" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`;
    }

    // Nút điều hướng trước / sau
    const prevBtn = document.getElementById('btn-prev-paper');
    const nextBtn = document.getElementById('btn-next-paper');
    if (prevBtn) {
      if (prevPaper) {
        prevBtn.href = `paper.html?id=${prevPaper.id}`;
        prevBtn.classList.remove('is-disabled');
        prevBtn.setAttribute('title', `Paper trước: ${prevPaper.ten}`);
      } else {
        prevBtn.removeAttribute('href');
        prevBtn.classList.add('is-disabled');
      }
    }
    if (nextBtn) {
      if (nextPaper) {
        nextBtn.href = `paper.html?id=${nextPaper.id}`;
        nextBtn.classList.remove('is-disabled');
        nextBtn.setAttribute('title', `Paper sau: ${nextPaper.ten}`);
      } else {
        nextBtn.removeAttribute('href');
        nextBtn.classList.add('is-disabled');
      }
    }

    // Kiểm tra tính khả dụng của các tab
    const files = currentPaper.files || {};
    const availability = {
      'doc-hieu': !!files.docHieu,
      'slide': !!files.slide,
      'pdf-goc': !!files.pdfGoc,
      'ban-dich': !!files.pdfViet,
      'song-song': !!(files.pdfGoc && files.pdfViet)
    };

    // Cập nhật trạng thái các nút tab
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

    // Tìm tab mặc định đầu tiên có file
    let defaultTab = null;
    for (const key of TAB_KEYS) {
      if (availability[key]) {
        defaultTab = key;
        break;
      }
    }

    if (!defaultTab) {
      renderEmptyPaper(currentPaper);
      return;
    }

    function getSelectedTabFromHash() {
      const hash = window.location.hash.replace('#', '').trim();
      if (hash && TAB_KEYS.includes(hash) && availability[hash]) {
        return hash;
      }
      return defaultTab;
    }

    // Cập nhật vị trí gạch chân trượt theo tab đang chọn
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

      if (activeBtn) {
        updateTabIndicator(activeBtn);
      }

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

        if (openExternalBtn) {
          openExternalBtn.href = encodedFile;
        }
      }
    }

    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const tab = this.getAttribute('data-tab');
        if (availability[tab]) {
          switchTab(tab);
        }
      });
    });

    window.addEventListener('hashchange', function () {
      const tab = getSelectedTabFromHash();
      switchTab(tab);
    });

    window.addEventListener('resize', function () {
      const currentTab = getSelectedTabFromHash();
      const activeBtn = document.querySelector(`.tab-btn[data-tab="${currentTab}"]`);
      if (activeBtn) updateTabIndicator(activeBtn);
    });

    switchTab(getSelectedTabFromHash());
    initMobileParallelToggle();
  }

  function initMobileParallelToggle() {
    const btnGoc = document.getElementById('seg-btn-goc');
    const btnViet = document.getElementById('seg-btn-viet');
    const paneGoc = document.getElementById('pane-goc');
    const paneViet = document.getElementById('pane-viet');

    if (!btnGoc || !btnViet || !paneGoc || !paneViet) return;

    btnGoc.addEventListener('click', function () {
      btnGoc.classList.add('is-active');
      btnViet.classList.remove('is-active');
      paneGoc.classList.add('is-selected-mobile');
      paneViet.classList.remove('is-selected-mobile');
    });

    btnViet.addEventListener('click', function () {
      btnViet.classList.add('is-active');
      btnGoc.classList.remove('is-active');
      paneViet.classList.add('is-selected-mobile');
      paneGoc.classList.remove('is-selected-mobile');
    });
  }

  function renderNotFound(message) {
    const root = document.getElementById('paper-viewer-root');
    if (!root) return;
    root.innerHTML = `
      <div class="not-found-wrap">
        <h2>Không tìm thấy tài liệu</h2>
        <p>${message}</p>
        <a href="index.html" class="back-home-btn">← Quay lại trang chủ</a>
      </div>
    `;
  }

  function renderEmptyPaper(paper) {
    const workspace = document.getElementById('viewer-workspace');
    if (!workspace) return;
    workspace.innerHTML = `
      <div class="viewer-empty-state">
        <svg class="empty-icon" viewBox="0 0 24 24">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
          <polyline points="14 2 14 8 20 8"></polyline>
          <line x1="12" y1="18" x2="12" y2="12"></line>
          <line x1="9" y1="15" x2="15" y2="15"></line>
        </svg>
        <h3 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 8px;">Chưa có tài liệu</h3>
        <p style="font-size: 0.9rem; color: var(--ink-secondary); line-height: 1.5;">Paper "<strong>${paper.ten}</strong>" hiện chưa có file phân tích hoặc PDF nào sẵn sàng.</p>
        <a href="index.html" class="back-home-btn">← Quay lại danh sách</a>
      </div>
    `;
  }

  // --- 4. TỰ ĐỘNG KHỞI CHẠY ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initHomePage();
    initPaperViewer();
  });

})();
"""

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    
    with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(INDEX_HTML)
    print("Successfully written index.html")
    
    with open(os.path.join(root, 'paper.html'), 'w', encoding='utf-8') as f:
        f.write(PAPER_HTML)
    print("Successfully written paper.html")
    
    with open(os.path.join(root, 'assets', 'style.css'), 'w', encoding='utf-8') as f:
        f.write(STYLE_CSS)
    print("Successfully written assets/style.css")
    
    with open(os.path.join(root, 'assets', 'app.js'), 'w', encoding='utf-8') as f:
        f.write(APP_JS)
    print("Successfully written assets/app.js")

if __name__ == '__main__':
    main()
