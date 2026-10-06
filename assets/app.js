/**
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
