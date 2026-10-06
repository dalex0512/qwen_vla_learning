/**
 * app.js - Logic điều khiển giao diện VLA Modeling
 * Hỗ trợ chuyển theme, hoạt ảnh lộ trình, 3 kiểu thẻ paper, hero robot arm,
 * tab indicator trượt, iframe loader skeleton và chế độ đọc song song PDF.
 */

(function () {
  'use strict';

  // ==========================================
  // 1. QUẢN LÝ GIAO DIỆN SÁNG / TỐI (THEME)
  // ==========================================
  const THEME_KEY = 'vla_theme_pref';

  function getSavedTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      console.warn('Không thể truy cập localStorage:', e);
      return null;
    }
  }

  function saveTheme(theme) {
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {
      console.warn('Không thể lưu theme vào localStorage:', e);
    }
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeToggleUI(theme);
  }

  function updateThemeToggleUI(currentTheme) {
    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
      const label = btn.querySelector('.theme-label');
      const isDark = currentTheme === 'dark';
      btn.setAttribute('aria-label', isDark ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối');
      if (label) {
        label.textContent = isDark ? 'Sáng' : 'Tối';
      }
    });
  }

  function initTheme() {
    const saved = getSavedTheme();
    let currentTheme = 'light';
    if (saved === 'dark' || saved === 'light') {
      currentTheme = saved;
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      currentTheme = 'dark';
    }
    applyTheme(currentTheme);

    const toggleBtns = document.querySelectorAll('.theme-toggle-btn');
    toggleBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = activeTheme === 'dark' ? 'light' : 'dark';
        applyTheme(nextTheme);
        saveTheme(nextTheme);
      });
    });

    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!getSavedTheme()) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }
  }

  // ==========================================
  // 2. HELPER UTILITIES
  // ==========================================
  function safeEncode(uri) {
    if (!uri) return '';
    return encodeURI(uri);
  }

  function getActivePaper(papers) {
    // Ưu tiên paper đang đọc (dang-doc), nếu không có thì lấy paper chưa đọc đầu tiên
    const currentReading = papers.find(p => p.trangThai === 'dang-doc');
    if (currentReading) return { paper: currentReading, isStudying: true };
    const firstUnread = papers.find(p => p.trangThai === 'chua-doc');
    if (firstUnread) return { paper: firstUnread, isStudying: false };
    return { paper: papers[0], isStudying: false };
  }

  // ==========================================
  // 3. TRANG CHỦ (INDEX.HTML LOGIC)
  // ==========================================
  function initIndexPage() {
    const papers = window.PAPERS || [];
    const total = papers.length;
    const completedCount = papers.filter(p => p.trangThai === 'da-present').length;
    const { paper: activePaper, isStudying } = getActivePaper(papers);

    // 1. Cập nhật Hero Focus Card
    const focusTag = document.getElementById('hero-focus-tag');
    const focusGroup = document.getElementById('hero-focus-group');
    const focusTitle = document.getElementById('hero-focus-title');
    const focusDesc = document.getElementById('hero-focus-desc');
    const focusCta = document.getElementById('hero-focus-cta');

    if (activePaper && focusTitle) {
      if (focusTag) focusTag.textContent = isStudying ? 'ĐANG HỌC' : 'TIẾP THEO';
      if (focusGroup) focusGroup.textContent = activePaper.nhom || 'Lộ trình';
      focusTitle.textContent = activePaper.ten;
      if (focusDesc) focusDesc.textContent = activePaper.moTa || 'Tiếp tục theo dõi các tài liệu nghiên cứu.';
      if (focusCta) {
        focusCta.href = `paper.html?id=${activePaper.id}`;
      }
    }

    // 2. Cập nhật Vòng tròn Tiến độ Hero (SVG Ring)
    const ringCircle = document.getElementById('hero-progress-circle');
    const ringFraction = document.getElementById('hero-progress-fraction');
    const ringSub = document.getElementById('hero-progress-sub');

    if (ringCircle && ringFraction) {
      const radius = 28;
      const circumference = 2 * Math.PI * radius; // ~175.92
      const percent = total > 0 ? completedCount / total : 0;
      const offset = circumference - (percent * circumference);

      // Animation chạy vòng tròn sau 200ms
      setTimeout(() => {
        ringCircle.style.strokeDashoffset = offset;
      }, 200);

      // Đếm số tăng dần
      let currentDisplay = 0;
      const stepTime = 120;
      const counter = setInterval(() => {
        if (currentDisplay < completedCount) {
          currentDisplay++;
          ringFraction.textContent = `${currentDisplay}/${total}`;
        } else {
          ringFraction.textContent = `${completedCount}/${total}`;
          clearInterval(counter);
        }
      }, stepTime);

      if (ringSub) {
        ringSub.textContent = `Đã hoàn thành ${completedCount} trên ${total} bài báo`;
      }
    }

    // 3. Render Lộ trình Timeline & 3 Kiểu Thẻ Paper
    const timelineContainer = document.getElementById('paper-timeline');
    if (timelineContainer) {
      renderRoadmap(timelineContainer, papers, activePaper);
    }
  }

  function renderRoadmap(container, papers, activePaper) {
    // Gom nhóm theo trường 'nhom' ("Đọc rộng", "Đọc sâu")
    const groups = {};
    papers.forEach((p, idx) => {
      const gName = p.nhom || 'Khác';
      if (!groups[gName]) groups[gName] = [];
      groups[gName].push({ ...p, globalIndex: idx + 1 });
    });

    let html = '';

    for (const [groupName, groupPapers] of Object.entries(groups)) {
      const isDeep = groupName.toLowerCase().includes('sâu');
      const badgeClass = isDeep ? 'group-badge group-badge--deep' : 'group-badge';

      html += `
        <section class="timeline-group" aria-label="Nhóm ${groupName}">
          <div class="group-header">
            <h3 class="group-title">${groupName}</h3>
            <span class="${badgeClass}">${groupPapers.length} paper</span>
          </div>
          <div class="group-list">
      `;

      groupPapers.forEach(paper => {
        const isCompleted = paper.trangThai === 'da-present';
        const isActive = activePaper && paper.id === activePaper.id && !isCompleted;
        const isUpcoming = !isCompleted && !isActive;

        let itemModifier = 'timeline-item--upcoming';
        let nodeContent = `${paper.globalIndex}`;

        if (isCompleted) {
          itemModifier = 'timeline-item--completed';
          nodeContent = `
            <svg viewBox="0 0 20 20" fill="currentColor" class="timeline-node-icon" aria-hidden="true">
              <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          `;
        } else if (isActive) {
          itemModifier = 'timeline-item--active';
          nodeContent = `${paper.globalIndex}`;
        }

        html += `
          <div class="timeline-item ${itemModifier}" data-paper-id="${paper.id}">
            <div class="timeline-node" aria-hidden="true">${nodeContent}</div>
            ${renderPaperCard(paper, isCompleted, isActive, isUpcoming)}
          </div>
        `;
      });

      html += `
          </div>
        </section>
      `;
    }

    container.innerHTML = html;

    // Kích hoạt animation xuất hiện lần lượt (Staggered Reveal)
    setupStaggeredReveal(container);
  }

  function renderPaperCard(paper, isCompleted, isActive, isUpcoming) {
    const arxivUrl = `https://arxiv.org/abs/${paper.arxiv}`;
    const files = paper.files || {};
    
    // --- KIỂU 1: ĐÃ XONG (da-present) ---
    if (isCompleted) {
      return `
        <article class="paper-card paper-card--completed">
          <div class="paper-card-header">
            <div class="paper-heading-wrap">
              <h4 class="paper-title">${paper.ten}</h4>
              <a href="${arxivUrl}" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Mở bài báo trên arXiv">
                arXiv:${paper.arxiv} ↗
              </a>
            </div>
            <span class="status-pill status-pill--completed">Đã present</span>
          </div>
          
          <p class="paper-desc">${paper.moTa}</p>
          
          <div class="paper-actions-grid">
            <a href="paper.html?id=${paper.id}#doc-hieu" class="action-btn" title="Mở trang Đọc hiểu">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>
              <span>Đọc hiểu</span>
            </a>
            <a href="paper.html?id=${paper.id}#slide" class="action-btn" title="Mở Slide trình bày">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
              <span>Slide</span>
            </a>
            <a href="paper.html?id=${paper.id}#pdf-goc" class="action-btn" title="Mở PDF gốc">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
              <span>PDF gốc</span>
            </a>
            <a href="paper.html?id=${paper.id}#ban-dich" class="action-btn" title="Mở Bản dịch tiếng Việt">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg>
              <span>Bản dịch</span>
            </a>
          </div>
        </article>
      `;
    }

    // --- KIỂU 2: ĐANG HỌC / TIẾP THEO (dang-doc hoặc active) ---
    if (isActive) {
      const missingList = [];
      if (!files.docHieu) missingList.push('Đọc hiểu');
      if (!files.slide) missingList.push('Slide');
      if (!files.pdfGoc) missingList.push('PDF gốc');
      if (!files.pdfViet) missingList.push('Bản dịch');

      const hasAnyFile = files.docHieu || files.slide || files.pdfGoc || files.pdfViet;

      return `
        <article class="paper-card paper-card--active">
          <div class="paper-card-header">
            <div class="paper-heading-wrap">
              <h4 class="paper-title">${paper.ten}</h4>
              <a href="${arxivUrl}" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Mở bài báo trên arXiv">
                arXiv:${paper.arxiv} ↗
              </a>
            </div>
            <span class="status-pill status-pill--active">Tiếp theo</span>
          </div>

          <p class="paper-desc">${paper.moTa}</p>

          ${hasAnyFile ? `
            <div class="paper-actions-grid">
              ${files.docHieu ? `<a href="paper.html?id=${paper.id}#doc-hieu" class="action-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg><span>Đọc hiểu</span></a>` : ''}
              ${files.slide ? `<a href="paper.html?id=${paper.id}#slide" class="action-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg><span>Slide</span></a>` : ''}
              ${files.pdfGoc ? `<a href="paper.html?id=${paper.id}#pdf-goc" class="action-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg><span>PDF gốc</span></a>` : ''}
              ${files.pdfViet ? `<a href="paper.html?id=${paper.id}#ban-dich" class="action-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 8l6 6"></path><path d="M4 14l6-6 2-3"></path><path d="M2 5h12"></path><path d="M7 2h1"></path><path d="M22 22l-5-10-5 10"></path><path d="M14 18h6"></path></svg><span>Bản dịch</span></a>` : ''}
            </div>
          ` : ''}

          ${missingList.length > 0 ? `
            <div class="missing-files-note">
              <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" /></svg>
              <span>Còn thiếu: ${missingList.join(', ')}</span>
            </div>
          ` : ''}
        </article>
      `;
    }

    // --- KIỂU 3: CHƯA TỚI / THU GỌN 1 DÒNG (Upcoming) ---
    // Nếu có file (như Qwen-VLA có 2 PDF), hiện mini buttons
    const miniButtons = [];
    if (files.docHieu) miniButtons.push(`<a href="paper.html?id=${paper.id}#doc-hieu" class="mini-btn">Đọc hiểu</a>`);
    if (files.slide) miniButtons.push(`<a href="paper.html?id=${paper.id}#slide" class="mini-btn">Slide</a>`);
    if (files.pdfGoc) miniButtons.push(`<a href="paper.html?id=${paper.id}#pdf-goc" class="mini-btn">PDF</a>`);
    if (files.pdfViet) miniButtons.push(`<a href="paper.html?id=${paper.id}#ban-dich" class="mini-btn">Bản dịch</a>`);

    return `
      <article class="paper-card paper-card--compact">
        <div class="compact-left">
          <h4 class="compact-title">${paper.ten}</h4>
          <a href="${arxivUrl}" target="_blank" rel="noopener noreferrer" class="arxiv-badge" title="Mở arXiv">
            arXiv:${paper.arxiv} ↗
          </a>
          <span class="compact-desc" title="${paper.moTa}">${paper.moTa}</span>
        </div>

        <div class="compact-right">
          ${miniButtons.length > 0 ? miniButtons.join('') : ''}
          <span class="status-pill status-pill--upcoming">Sắp có</span>
        </div>
      </article>
    `;
  }

  function setupStaggeredReveal(container) {
    const items = container.querySelectorAll('.timeline-item');
    if (!('IntersectionObserver' in window)) {
      items.forEach(el => el.classList.add('is-revealed'));
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    items.forEach((item, index) => {
      // Delay so le nhẹ nhàng khi cuộn tới
      setTimeout(() => {
        observer.observe(item);
      }, index * 60);
    });
  }

  // ==========================================
  // 4. TRANG CHI TIẾT (PAPER.HTML LOGIC)
  // ==========================================
  function initPaperPage() {
    const papers = window.PAPERS || [];
    const urlParams = new URLSearchParams(window.location.search);
    const paperId = urlParams.get('id');

    if (!paperId) return;

    const currentIndex = papers.findIndex(p => p.id === paperId);
    const currentPaper = papers[currentIndex];

    // Xử lý lỗi không tìm thấy ID
    if (!currentPaper) {
      showPaperNotFound();
      return;
    }

    // 1. Cập nhật Tiêu đề và arXiv
    const titleEl = document.getElementById('viewer-paper-title');
    const arxivLink = document.getElementById('viewer-arxiv-link');
    const arxivIdSpan = document.getElementById('viewer-arxiv-id');
    
    if (titleEl) titleEl.textContent = currentPaper.ten;
    if (arxivLink && arxivIdSpan) {
      arxivLink.href = `https://arxiv.org/abs/${currentPaper.arxiv}`;
      arxivIdSpan.textContent = currentPaper.arxiv;
    }
    document.title = `${currentPaper.ten} · VLA Modeling`;

    // 2. Cài đặt nút Paper Trước / Sau
    setupPrevNextNav(papers, currentIndex);

    // 3. Cài đặt các Tab tài liệu
    setupPaperTabs(currentPaper);
  }

  function showPaperNotFound() {
    const stage = document.getElementById('viewer-stage');
    const emptyPanel = document.getElementById('panel-empty');
    if (stage && emptyPanel) {
      document.querySelectorAll('.tab-panel').forEach(p => p.style.display = 'none');
      emptyPanel.style.display = 'flex';
      emptyPanel.classList.add('is-active');
    }
  }

  function setupPrevNextNav(papers, currentIndex) {
    const prevBtn = document.getElementById('viewer-prev-btn');
    const nextBtn = document.getElementById('viewer-next-btn');

    if (prevBtn) {
      if (currentIndex > 0) {
        prevBtn.href = `paper.html?id=${papers[currentIndex - 1].id}`;
        prevBtn.classList.remove('is-disabled');
      } else {
        prevBtn.classList.add('is-disabled');
        prevBtn.removeAttribute('href');
      }
    }

    if (nextBtn) {
      if (currentIndex < papers.length - 1) {
        nextBtn.href = `paper.html?id=${papers[currentIndex + 1].id}`;
        nextBtn.classList.remove('is-disabled');
      } else {
        nextBtn.classList.add('is-disabled');
        nextBtn.removeAttribute('href');
      }
    }
  }

  function setupPaperTabs(paper) {
    const files = paper.files || {};
    const tabConfig = {
      'doc-hieu': { file: files.docHieu, btnId: 'tab-btn-doc-hieu' },
      'slide': { file: files.slide, btnId: 'tab-btn-slide' },
      'pdf-goc': { file: files.pdfGoc, btnId: 'tab-btn-pdf-goc' },
      'ban-dich': { file: files.pdfViet, btnId: 'tab-btn-ban-dich' },
      'song-song': { file: (files.pdfGoc && files.pdfViet) ? 'dual' : null, btnId: 'tab-btn-song-song' }
    };

    const availableTabs = [];

    // Vô hiệu hóa tab thiếu file
    for (const [key, cfg] of Object.entries(tabConfig)) {
      const btn = document.getElementById(cfg.btnId);
      if (!btn) continue;

      if (!cfg.file) {
        btn.classList.add('is-disabled');
        btn.setAttribute('aria-disabled', 'true');
      } else {
        btn.classList.remove('is-disabled');
        btn.removeAttribute('aria-disabled');
        availableTabs.push(key);
      }
    }

    // Xác định tab ban đầu: Ưu tiên hash trên URL, nếu không hợp lệ thì lấy tab đầu tiên có file
    let targetTab = window.location.hash.replace('#', '');
    if (!availableTabs.includes(targetTab)) {
      targetTab = availableTabs[0] || 'doc-hieu';
    }

    // Chuyển tới tab mục tiêu
    switchTab(targetTab, tabConfig, paper);

    // Bắt sự kiện bấm tab
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.classList.contains('is-disabled')) return;
        const tabKey = btn.getAttribute('data-tab');
        if (tabKey) {
          window.location.hash = tabKey;
          switchTab(tabKey, tabConfig, paper);
        }
      });
    });

    // Theo dõi đổi hash khi người dùng ấn nút Back/Forward của trình duyệt
    window.addEventListener('hashchange', () => {
      const hashTab = window.location.hash.replace('#', '');
      if (availableTabs.includes(hashTab)) {
        switchTab(hashTab, tabConfig, paper);
      }
    });

    // Setup tính năng cho chế độ Song song (Dual view)
    setupCompareView(files);
  }

  function switchTab(tabKey, tabConfig, paper) {
    const cfg = tabConfig[tabKey];
    if (!cfg || !cfg.file) return;

    // 1. Cập nhật trạng thái active trên các nút tab
    const allBtns = document.querySelectorAll('.tab-btn');
    let activeBtn = null;
    allBtns.forEach(btn => {
      if (btn.getAttribute('data-tab') === tabKey) {
        btn.classList.add('is-active');
        btn.setAttribute('aria-selected', 'true');
        activeBtn = btn;
      } else {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-selected', 'false');
      }
    });

    // 2. Di chuyển thanh gạch chân trượt (Sliding Indicator)
    updateIndicator(activeBtn);

    // 3. Chuyển đổi panels
    const singlePanel = document.getElementById('panel-single');
    const comparePanel = document.getElementById('panel-compare');
    const singleFrame = document.getElementById('single-frame');
    const skeleton = document.getElementById('viewer-skeleton');
    const externalLink = document.getElementById('viewer-external-link');

    if (tabKey === 'song-song') {
      if (singlePanel) singlePanel.classList.remove('is-active');
      if (comparePanel) comparePanel.classList.add('is-active');
      if (externalLink) externalLink.style.display = 'none';
      if (skeleton) skeleton.classList.remove('is-loading');
    } else {
      if (comparePanel) comparePanel.classList.remove('is-active');
      if (singlePanel) singlePanel.classList.add('is-active');
      if (externalLink) {
        externalLink.style.display = 'inline-flex';
        externalLink.href = safeEncode(cfg.file);
      }

      // Nạp iframe với Skeleton loader
      if (singleFrame && cfg.file) {
        const targetSrc = safeEncode(cfg.file);
        if (singleFrame.getAttribute('src') !== targetSrc) {
          if (skeleton) skeleton.classList.add('is-loading');
          singleFrame.onload = () => {
            if (skeleton) skeleton.classList.remove('is-loading');
          };
          singleFrame.src = targetSrc;
        }
      }
    }
  }

  function updateIndicator(activeBtn) {
    const indicator = document.getElementById('tab-indicator-line');
    if (!indicator || !activeBtn) return;

    const btnRect = activeBtn.getBoundingClientRect();
    const parentRect = activeBtn.parentElement.getBoundingClientRect();
    
    const leftOffset = btnRect.left - parentRect.left;
    const width = btnRect.width;

    indicator.style.transform = `translateX(${leftOffset}px)`;
    indicator.style.width = `${width}px`;
  }

  function setupCompareView(files) {
    const leftFrame = document.getElementById('compare-frame-left');
    const rightFrame = document.getElementById('compare-frame-right');
    const gocLink = document.getElementById('col-goc-link');
    const vietLink = document.getElementById('col-viet-link');

    if (files.pdfGoc && leftFrame) {
      const srcGoc = safeEncode(files.pdfGoc);
      leftFrame.src = srcGoc;
      if (gocLink) gocLink.href = srcGoc;
    }

    if (files.pdfViet && rightFrame) {
      const srcViet = safeEncode(files.pdfViet);
      rightFrame.src = srcViet;
      if (vietLink) vietLink.href = srcViet;
    }

    // Mobile switcher (<900px)
    const segLeft = document.getElementById('seg-btn-left');
    const segRight = document.getElementById('seg-btn-right');
    const colLeft = document.getElementById('col-pdf-goc');
    const colRight = document.getElementById('col-pdf-viet');

    if (colLeft) colLeft.classList.add('is-mobile-active');

    if (segLeft && segRight) {
      segLeft.addEventListener('click', () => {
        segLeft.classList.add('is-active');
        segRight.classList.remove('is-active');
        if (colLeft) colLeft.classList.add('is-mobile-active');
        if (colRight) colRight.classList.remove('is-mobile-active');
      });

      segRight.addEventListener('click', () => {
        segRight.classList.add('is-active');
        segLeft.classList.remove('is-active');
        if (colRight) colRight.classList.add('is-mobile-active');
        if (colLeft) colLeft.classList.remove('is-mobile-active');
      });
    }
  }

  // ==========================================
  // 5. KHỞI TẠO TOÀN TRANG KHI SẴN SÀNG
  // ==========================================
  document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initIndexPage();
    initPaperPage();

    // Cập nhật lại vị trí sliding indicator khi resize cửa sổ
    window.addEventListener('resize', () => {
      const activeBtn = document.querySelector('.tab-btn.is-active');
      if (activeBtn) updateIndicator(activeBtn);
    });
  });

})();
