/**
 * app.js - Logic điều khiển giao diện VLA Modeling
 * Hỗ trợ chế độ sáng/tối, điều hướng tab, song song hóa PDF, responsive và an toàn localStorage.
 */

(function () {
  'use strict';

  // --- 1. QUẢN LÝ GIAO DIỆN SÁNG / TỐI (THEME) ---
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
      const isDark = currentTheme === 'dark';
      btn.setAttribute('aria-label', isDark ? 'Chuyển sang giao diện sáng' : 'Chuyển sang giao diện tối');
      btn.innerHTML = isDark
        ? `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg> <span>Sáng</span>`
        : `<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg> <span>Tối</span>`;
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

  // --- 2. TIỆN ÍCH CHUNG ---
  function safeEncode(url) {
    if (!url) return '';
    return encodeURI(url);
  }

  function getStatusLabel(status) {
    switch (status) {
      case 'da-present':
        return { text: 'Đã present', className: 'da-present' };
      case 'dang-doc':
        return { text: 'Đang đọc', className: 'dang-doc' };
      case 'chua-doc':
      default:
        return { text: 'Chưa đọc', className: 'chua-doc' };
    }
  }

  // --- 3. XỬ LÝ TRANG CHỦ (index.html) ---
  function initHomePage() {
    const paperContainer = document.getElementById('paper-timeline');
    if (!paperContainer) return;

    if (!window.PAPERS || !Array.isArray(window.PAPERS)) {
      paperContainer.innerHTML = '<p class="error-msg">Không tìm thấy dữ liệu mảng PAPERS trong papers.js.</p>';
      return;
    }

    const papers = window.PAPERS;
    const totalCount = papers.length;
    const completedCount = papers.filter(p => p.trangThai === 'da-present').length;

    // Cập nhật thanh tiến độ
    const scoreEl = document.getElementById('progress-score-num');
    const fillEl = document.getElementById('progress-bar-fill');
    if (scoreEl) scoreEl.textContent = `${completedCount}/${totalCount}`;
    if (fillEl) {
      const pct = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;
      fillEl.style.width = `${pct}%`;
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
        <section class="timeline-section">
          <div class="section-label">
            <span class="section-pill">${group.name}</span>
            <span class="section-hint">${group.hint}</span>
          </div>
          <div class="paper-list">
      `;

      groupPapers.forEach(paper => {
        const statusMeta = getStatusLabel(paper.trangThai);
        const isReading = paper.trangThai === 'dang-doc';
        const isPresent = paper.trangThai === 'da-present';

        const hasDocHieu = !!(paper.files && paper.files.docHieu);
        const hasSlide = !!(paper.files && paper.files.slide);
        const hasPdfGoc = !!(paper.files && paper.files.pdfGoc);
        const hasPdfViet = !!(paper.files && paper.files.pdfViet);

        const itemClasses = ['paper-item'];
        if (isReading) itemClasses.push('is-reading');
        if (isPresent) itemClasses.push('is-present');

        html += `
          <article class="${itemClasses.join(' ')}" id="paper-${paper.id}">
            <div class="paper-index" aria-label="Số thứ tự ${overallIndex}">${overallIndex}</div>
            <div class="paper-card">
              <div class="card-header-row">
                <div class="card-title-group">
                  <h3 class="card-title">${paper.ten}</h3>
                  <a href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer" class="arxiv-link" title="Xem trên arXiv">
                    <span>arXiv:${paper.arxiv}</span>
                    <svg viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  </a>
                </div>
                <span class="status-badge ${statusMeta.className}">
                  ${statusMeta.text}
                </span>
              </div>
              <p class="card-desc">${paper.moTa}</p>
              
              <div class="card-actions-grid">
                ${renderDocButton('Đọc hiểu', hasDocHieu, `paper.html?id=${paper.id}#doc-hieu`, 'HTML')}
                ${renderDocButton('Slide', hasSlide, `paper.html?id=${paper.id}#slide`, 'Trình chiếu')}
                ${renderDocButton('PDF gốc', hasPdfGoc, `paper.html?id=${paper.id}#pdf-goc`, 'Bản gốc')}
                ${renderDocButton('Bản dịch', hasPdfViet, `paper.html?id=${paper.id}#ban-dich`, 'Tiếng Việt')}
              </div>
            </div>
          </article>
        `;
        overallIndex++;
      });

      html += `
          </div>
        </section>
      `;
    });

    paperContainer.innerHTML = html;
  }

  function renderDocButton(title, isAvailable, link, metaText) {
    if (isAvailable) {
      return `
        <a href="${link}" class="doc-btn" title="Mở ${title}">
          <span class="btn-label">${title}</span>
          <span class="btn-meta">${metaText}</span>
        </a>
      `;
    }
    return `
      <span class="doc-btn is-disabled" aria-disabled="true" title="Chưa có file">
        <span class="btn-label">${title}</span>
        <span class="btn-meta">Sắp có</span>
      </span>
    `;
  }

  // --- 4. XỬ LÝ TRANG XEM PAPER (paper.html) ---
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
      renderNotFound('Thiếu tham số ID paper trong đường dẫn.');
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
      arxivEl.textContent = `arXiv:${currentPaper.arxiv}`;
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

    // Nếu không có file nào sẵn sàng
    if (!defaultTab) {
      renderEmptyPaper(currentPaper);
      return;
    }

    // Xác định tab đang chọn từ URL hash
    function getSelectedTabFromHash() {
      const hash = window.location.hash.replace('#', '').trim();
      if (hash && TAB_KEYS.includes(hash) && availability[hash]) {
        return hash;
      }
      return defaultTab;
    }

    function switchTab(targetTab) {
      if (!availability[targetTab]) return;

      // Cập nhật hash không reload nếu khác
      if (window.location.hash.replace('#', '') !== targetTab) {
        window.location.hash = targetTab;
      }

      // Cập nhật active class cho tab button
      document.querySelectorAll('.tab-btn').forEach(btn => {
        const isMatch = btn.getAttribute('data-tab') === targetTab;
        btn.classList.toggle('is-active', isMatch);
        btn.setAttribute('aria-selected', isMatch ? 'true' : 'false');
      });

      // Ẩn/hiện container tương ứng
      const singlePane = document.getElementById('single-view-pane');
      const parallelPane = document.getElementById('parallel-view-pane');
      const singleIframe = document.getElementById('single-iframe');
      const openExternalBtn = document.getElementById('btn-open-external');

      if (targetTab === 'song-song') {
        if (singlePane) singlePane.classList.remove('is-active');
        if (parallelPane) parallelPane.classList.add('is-active');
        if (openExternalBtn) openExternalBtn.style.display = 'none';

        // Load 2 iframes song song
        const pdfGocIframe = document.getElementById('parallel-iframe-goc');
        const pdfVietIframe = document.getElementById('parallel-iframe-viet');
        const linkGoc = document.getElementById('parallel-link-goc');
        const linkViet = document.getElementById('parallel-link-viet');

        const encodedGoc = safeEncode(files.pdfGoc);
        const encodedViet = safeEncode(files.pdfViet);

        if (pdfGocIframe && pdfGocIframe.getAttribute('src') !== encodedGoc) {
          pdfGocIframe.src = encodedGoc;
        }
        if (pdfVietIframe && pdfVietIframe.getAttribute('src') !== encodedViet) {
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

        const encodedFile = safeEncode(targetFile);

        if (singleIframe && singleIframe.getAttribute('src') !== encodedFile) {
          singleIframe.src = encodedFile;
        }

        // Cho phép toàn màn hình nếu là slide
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

    // Lắng nghe sự kiện click tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const tab = this.getAttribute('data-tab');
        if (availability[tab]) {
          switchTab(tab);
        }
      });
    });

    // Lắng nghe thay đổi hash (Back / Forward trình duyệt)
    window.addEventListener('hashchange', function () {
      const tab = getSelectedTabFromHash();
      switchTab(tab);
    });

    // Kích hoạt tab ban đầu
    switchTab(getSelectedTabFromHash());

    // Xử lý bộ gạt song song trên màn hình nhỏ (< 900px)
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
        <h2>Không tìm thấy paper</h2>
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
        <h3 class="empty-title">Chưa có tài liệu</h3>
        <p class="empty-text">Paper "<strong>${paper.ten}</strong>" hiện chưa có file đọc hiểu, slide hay PDF nào sẵn sàng. Bạn có thể thêm file vào thư mục dự án và khai báo đường dẫn trong file <code>papers.js</code>.</p>
        <a href="index.html" class="back-home-btn">← Quay lại trang chủ</a>
      </div>
    `;
  }

  // --- 5. TỰ ĐỘNG KHỞI CHẠY ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initHomePage();
    initPaperViewer();
  });

})();
