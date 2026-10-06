import os

INDEX_HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>VLA Modeling · Sổ tay học tập</title>
  <meta name="description" content="Sổ tay học tập và theo dõi lộ trình đọc paper VLA (Vision-Language-Action) modeling.">
  
  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/style.css?v=10.0">
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
  <!-- Mảng màu mờ trang trí nền (Ambient Glow Orbs) -->
  <div class="ambient-glow ambient-glow--teal" aria-hidden="true"></div>
  <div class="ambient-glow ambient-glow--orange" aria-hidden="true"></div>
  <div class="ambient-glow ambient-glow--bottom" aria-hidden="true"></div>

  <div class="container main-layout">
    <!-- Header thương hiệu & Đổi giao diện -->
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

    <!-- HERO SECTION: 2 cột (Thông tin học tập + Robot Arm SVG) -->
    <section class="hero-section" aria-label="Tổng quan học tập">
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

        <!-- Bộ đo tiến độ vòng tròn (Circular Progress Ring) -->
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
            <div class="progress-ring-title">Tiến độ trình bày</div>
            <div class="progress-ring-sub" id="hero-progress-sub">Đã hoàn thành 0 trên 6 bài báo</div>
          </div>
        </div>
      </div>

      <!-- Cánh tay robot 2 khớp mô phỏng tác vụ gắp đặt (Manipulation Task) -->
      <div class="hero-visual" aria-hidden="true">
        <div class="robot-stage">
          <div class="stage-tag">VLA Manipulation Task · Pick & Place</div>
          
          <svg class="robot-arm-svg" viewBox="0 0 420 300" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid-pattern" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" stroke-width="0.5" class="svg-grid-line" />
              </pattern>
              <linearGradient id="arm-grad-teal" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#00897B" />
                <stop offset="100%" stop-color="#004D40" />
              </linearGradient>
              <linearGradient id="arm-grad-orange" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FB8C00" />
                <stop offset="100%" stop-color="#B8650F" />
              </linearGradient>
            </defs>
            <rect x="10" y="10" width="400" height="250" fill="url(#grid-pattern)" opacity="0.4" rx="12" />

            <!-- Bàn thao tác -->
            <rect x="20" y="250" width="380" height="12" rx="4" class="svg-bench" />
            <line x1="20" y1="250" x2="400" y2="250" stroke="#00897B" stroke-width="2" opacity="0.6" />

            <!-- Vật thể nguồn: Bát bên trái -->
            <g class="svg-source-bowl">
              <ellipse cx="90" cy="246" rx="26" ry="6" class="svg-bowl-lip" />
              <path d="M 64 246 Q 90 270 116 246 Z" class="svg-bowl-body" />
              <text x="90" y="280" text-anchor="middle" class="svg-label-text">Bát vật thể</text>
            </g>

            <!-- Vật thể đích: Đĩa bên phải -->
            <g class="svg-target-plate">
              <ellipse cx="320" cy="248" rx="34" ry="7" class="svg-plate-outer" />
              <ellipse cx="320" cy="248" rx="22" ry="4.5" class="svg-plate-inner" />
              <text x="320" y="280" text-anchor="middle" class="svg-label-text">Đĩa đích</text>
            </g>

            <!-- Khối lập phương thao tác -->
            <g class="robot-cube-payload">
              <rect x="-10" y="-10" width="20" height="20" rx="3" class="svg-cube-body" />
              <path d="M -10 -10 L 0 -16 L 10 -10 L 0 -4 Z" class="svg-cube-top" />
              <path d="M 0 -4 L 10 -10 L 10 10 L 0 16 Z" class="svg-cube-right" />
            </g>

            <!-- Đế Robot -->
            <g class="robot-base-group" transform="translate(200, 250)">
              <path d="M -36 0 L -24 -24 L 24 -24 L 36 0 Z" class="svg-base-pedestal" />
              <circle cx="0" cy="-24" r="14" class="svg-joint-outer" />
              <circle cx="0" cy="-24" r="6" class="svg-joint-inner" />
            </g>

            <!-- Khớp 1 & Cánh tay trên -->
            <g class="robot-link-1" transform="translate(200, 226)">
              <rect x="-8" y="-95" width="16" height="95" rx="8" class="svg-arm-segment-1" />
              <line x1="0" y1="-8" x2="0" y2="-87" stroke="#80CBC4" stroke-width="2" stroke-linecap="round" opacity="0.8" />
              
              <!-- Khớp 2 -->
              <g class="robot-link-2" transform="translate(0, -95)">
                <circle cx="0" cy="0" r="11" class="svg-joint-outer" />
                <circle cx="0" cy="0" r="4.5" class="svg-joint-inner" />
                
                <!-- Cánh tay trước -->
                <rect x="-6" y="-80" width="12" height="80" rx="6" class="svg-arm-segment-2" />
                <line x1="0" y1="-6" x2="0" y2="-74" stroke="#FFE082" stroke-width="2" stroke-linecap="round" opacity="0.8" />
                
                <!-- Tay kẹp -->
                <g class="robot-gripper" transform="translate(0, -80)">
                  <circle cx="0" cy="0" r="7" class="svg-joint-small" />
                  <rect x="-14" y="-6" width="28" height="6" rx="2" class="svg-gripper-crossbar" />
                  
                  <path d="M -12 -6 L -12 -22 L -6 -22" class="svg-finger-left" />
                  <path d="M 12 -6 L 12 -22 L 6 -22" class="svg-finger-right" />
                  
                  <polygon points="0,-4 -18,-42 18,-42" class="svg-sensor-cone" opacity="0.15" />
                  <circle cx="0" cy="-3" r="2" fill="#FB8C00" />
                </g>
              </g>
            </g>
          </svg>
          <div class="stage-footer">
            <span class="stage-status-dot"></span>
            <span>Chế độ mô phỏng trực quan liên tục</span>
          </div>
        </div>
      </div>
    </section>

    <!-- KHU VỰC LỘ TRÌNH CHÍNH (Roadmap Timeline) -->
    <section class="roadmap-section" aria-label="Lộ trình chi tiết 6 paper">
      <div class="roadmap-header-bar">
        <h2 class="roadmap-heading">Lộ trình nghiên cứu</h2>
        <span class="roadmap-sub">Theo dõi từ nền tảng benchmark đến các cấu trúc chuyên sâu</span>
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

  <script src="papers.js?v=10.0"></script>
  <script src="assets/app.js?v=10.0"></script>
</body>
</html>
'''

PAPER_HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>Đọc paper · VLA Modeling</title>
  
  <!-- Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="assets/style.css?v=10.0">
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
<body class="page-paper">
  <div class="viewer-shell">
    <!-- THANH ĐIỀU HƯỚNG TRÊN CÙNG -->
    <header class="viewer-header">
      <div class="viewer-nav-left">
        <a href="index.html" class="viewer-back-btn" title="Quay lại danh sách tổng quan">
          <svg viewBox="0 0 20 20" fill="currentColor" class="nav-icon" aria-hidden="true">
            <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
          </svg>
          <span>Trang chủ</span>
        </a>

        <div class="viewer-title-group">
          <h1 id="viewer-paper-title" class="viewer-paper-title">Đang tải...</h1>
          <a id="viewer-arxiv-link" href="#" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Mở trang bài báo trên arXiv">
            arXiv: <span id="viewer-arxiv-id">------</span> ↗
          </a>
        </div>
      </div>

      <div class="viewer-nav-right">
        <nav class="paper-prev-next-group" aria-label="Chuyển bài báo">
          <a href="#" id="viewer-prev-btn" class="nav-pager-btn" title="Paper trước đó">
            <svg viewBox="0 0 20 20" fill="currentColor" class="nav-icon" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
            <span>Paper trước</span>
          </a>
          <a href="#" id="viewer-next-btn" class="nav-pager-btn" title="Paper tiếp theo">
            <span>Paper sau</span>
            <svg viewBox="0 0 20 20" fill="currentColor" class="nav-icon" aria-hidden="true">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </a>
        </nav>

        <button type="button" class="theme-toggle-btn viewer-theme-btn" id="theme-toggle-btn" aria-label="Đổi giao diện sáng/tối">
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

    <!-- THANH TAB TÀI LIỆU -->
    <nav class="viewer-tabs-bar" aria-label="Tài liệu của bài báo">
      <div class="tabs-list-wrapper">
        <div class="tabs-list" role="tablist" id="viewer-tab-list">
          <button type="button" role="tab" class="tab-btn" id="tab-btn-doc-hieu" data-tab="doc-hieu" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
            <span>Đọc hiểu</span>
          </button>
          <button type="button" role="tab" class="tab-btn" id="tab-btn-slide" data-tab="slide" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
            <span>Slide</span>
          </button>
          <button type="button" role="tab" class="tab-btn" id="tab-btn-pdf-goc" data-tab="pdf-goc" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            <span>PDF gốc</span>
          </button>
          <button type="button" role="tab" class="tab-btn" id="tab-btn-ban-dich" data-tab="ban-dich" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg>
            <span>Bản dịch (Vi)</span>
          </button>
          <button type="button" role="tab" class="tab-btn tab-btn--compare" id="tab-btn-song-song" data-tab="song-song" aria-selected="false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="12" y1="3" x2="12" y2="21"></line></svg>
            <span>Song song</span>
          </button>
          
          <div class="tab-indicator-line" id="tab-indicator-line" aria-hidden="true"></div>
        </div>
      </div>

      <div class="tab-actions-right">
        <a href="#" id="viewer-external-link" target="_blank" rel="noopener noreferrer" class="open-external-btn" title="Mở file này trong một tab trình duyệt mới">
          <span>Mở tab mới</span>
          <svg viewBox="0 0 20 20" fill="currentColor" class="btn-icon-xs" aria-hidden="true">
            <path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" />
            <path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" />
          </svg>
        </a>
      </div>
    </nav>

    <!-- KHU VỰC HIỂN THỊ NỘI DUNG CHÍNH -->
    <main class="viewer-stage" id="viewer-stage">
      <!-- SKELETON SHIMMER -->
      <div class="viewer-skeleton" id="viewer-skeleton" aria-hidden="true">
        <div class="skeleton-shimmer"></div>
        <div class="skeleton-content">
          <div class="skeleton-icon-pulse">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
            </svg>
          </div>
          <div class="skeleton-text">Đang tải tài liệu...</div>
        </div>
      </div>

      <!-- Tab Đơn -->
      <div class="tab-panel tab-panel--single" id="panel-single">
        <iframe id="single-frame" class="viewer-frame" title="Nội dung tài liệu" allow="fullscreen; allow-scripts; allow-same-origin"></iframe>
      </div>

      <!-- Tab Song song -->
      <div class="tab-panel tab-panel--compare" id="panel-compare">
        <div class="compare-mobile-nav">
          <button type="button" class="compare-seg-btn is-active" id="seg-btn-left" data-target="left">PDF Gốc</button>
          <button type="button" class="compare-seg-btn" id="seg-btn-right" data-target="right">Bản dịch (Vi)</button>
        </div>

        <div class="compare-grid">
          <div class="compare-column compare-column--left is-visible" id="col-pdf-goc">
            <div class="column-header">
              <span class="column-badge badge--teal">PDF GỐC</span>
              <a href="#" id="col-goc-link" target="_blank" rel="noopener noreferrer" class="column-action-btn" title="Mở PDF gốc trong tab mới">
                <span>Tab mới</span>
                <svg viewBox="0 0 20 20" fill="currentColor" class="btn-icon-xs"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" /><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" /></svg>
              </a>
            </div>
            <div class="column-body">
              <iframe id="compare-frame-left" class="viewer-frame" title="PDF gốc"></iframe>
            </div>
          </div>

          <div class="compare-column compare-column--right is-visible" id="col-pdf-viet">
            <div class="column-header">
              <span class="column-badge badge--orange">BẢN DỊCH TIẾNG VIỆT</span>
              <a href="#" id="col-viet-link" target="_blank" rel="noopener noreferrer" class="column-action-btn" title="Mở bản dịch trong tab mới">
                <span>Tab mới</span>
                <svg viewBox="0 0 20 20" fill="currentColor" class="btn-icon-xs"><path d="M11 3a1 1 0 100 2h2.586l-6.293 6.293a1 1 0 101.414 1.414L15 6.414V9a1 1 0 102 0V4a1 1 0 00-1-1h-5z" /><path d="M5 5a2 2 0 00-2 2v8a2 2 0 002 2h8a2 2 0 002-2v-3a1 1 0 10-2 0v3H5V7h3a1 1 0 000-2H5z" /></svg>
              </a>
            </div>
            <div class="column-body">
              <iframe id="compare-frame-right" class="viewer-frame" title="Bản dịch tiếng Việt"></iframe>
            </div>
          </div>
        </div>
      </div>

      <!-- Trạng thái trống hoặc lỗi ID -->
      <div class="tab-panel tab-panel--empty" id="panel-empty" style="display: none;">
        <div class="empty-state-box">
          <div class="empty-icon-bubble">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
          </div>
          <h2 id="empty-state-title" class="empty-title">Không tìm thấy bài báo</h2>
          <p id="empty-state-desc" class="empty-desc">Bài báo bạn đang tìm không tồn tại hoặc tài liệu này chưa sẵn sàng.</p>
          <a href="index.html" class="btn btn--primary">
            <span>← Quay về danh sách Paper</span>
          </a>
        </div>
      </div>
    </main>
  </div>

  <script src="papers.js?v=10.0"></script>
  <script src="assets/app.js?v=10.0"></script>
</body>
</html>
'''

with open('d:/VLA Modeling/index.html', 'w', encoding='utf-8') as f:
    f.write(INDEX_HTML)

with open('d:/VLA Modeling/paper.html', 'w', encoding='utf-8') as f:
    f.write(PAPER_HTML)

print("Applied index.html and paper.html")
