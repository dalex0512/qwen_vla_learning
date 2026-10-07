/**
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

  // --- 3. TRANG CHỦ: tuyến metro liền mạch, mỗi paper là một ga ---
  const DOC_LINKS = [
    { key: 'docHieu', tab: 'doc-hieu', label: 'Đọc hiểu', icon: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>' },
    { key: 'slide', tab: 'slide', label: 'Slide', icon: '<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/>' },
    { key: 'pdfGoc', tab: 'pdf-goc', label: 'PDF gốc', icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>' },
    { key: 'pdfViet', tab: 'ban-dich', label: 'Bản dịch', icon: '<path d="M5 8l6 6"/><path d="M4 14l6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="M22 22l-5-10-5 10"/><path d="M14 18h6"/>' }
  ];

  // Cấu hình hiển thị theo giá trị "nhom" trong papers.js. Nhóm lạ (vd. "Liên quan") dùng kiểu l3.
  const GROUPS = {
    'Đọc rộng': { title: 'Đọc nền', cls: 'l1', hint: 'Nắm bức tranh tổng quan và các benchmark chuẩn' },
    'Đọc sâu': { title: 'Đọc chuyên sâu', cls: 'l2', hint: 'Phương pháp chính: nối chunk thời gian thực (RTC) và MoE trong action expert.' },
    'Liên quan': { title: 'Paper liên quan', cls: 'l3', hint: 'Tài liệu mở rộng, đọc thêm khi cần' }
  };
  function groupInfo(name) {
    return GROUPS[name] || { title: name, cls: 'l3', hint: '' };
  }

  function stopHtml(paper, no, state) {
    const files = paper.files || {};
    // File dùng chung cho nhiều paper (vd. slide của cặp RTC) hiện nhãn "chung"
    const sharedCount = f => (window.PAPERS || []).filter(q => q.files && q.files.slide === f).length;
    const chips = DOC_LINKS.filter(d => files[d.key]).map(d => {
      const shared = d.key === 'slide' && sharedCount(files.slide) > 1;
      const label = shared ? 'Slide chung' : d.label;
      const hint = shared ? ' title="Một bộ slide cho cả cặp paper"' : '';
      return `<a class="chip${shared ? ' chip--shared' : ''}"${hint} href="paper.html?id=${paper.id}#${d.tab}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${d.icon}</svg>${label}</a>`;
    }).join('');
    const stateLabel = state === 'done' ? 'Đã xong' : (state === 'active' ? 'Đọc tiếp' : 'Sắp tới');
    const check = state === 'done'
      ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 12.5 10 17.5 19 7.5"/></svg>'
      : '';
    const capBadge = (paper.cap && paper.thuTuCap)
      ? `<span class="badge-cap">Cặp ${paper.cap} · ${paper.thuTuCap}/2</span>`
      : '';

    return `
      <li class="stop is-${state}" id="card-${paper.id}" style="--i:${no - 1}">
        <span class="node" aria-hidden="true">${check}</span>
        <article class="card" data-no="${String(no).padStart(2, '0')}">
          <div class="sign"><small>PAPER</small><b>${String(no).padStart(2, '0')}</b></div>
          <div class="card-body">
            <div class="card-head">
              <span class="state state--${state}">${stateLabel}</span>
              ${capBadge}
              <button type="button" class="tick" data-toggle="${paper.id}" aria-pressed="${state === 'done'}" title="Tự đánh dấu paper này đã xong hoặc chưa">
                <span class="tick-box"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 12.5 10 17.5 19 7.5"/></svg></span>
                <span class="tick-text">${state === 'done' ? 'Đã xong' : 'Đánh dấu xong'}</span>
              </button>
              <a class="arxiv" href="https://arxiv.org/abs/${paper.arxiv}" target="_blank" rel="noopener noreferrer">arXiv:${paper.arxiv}</a>
            </div>
            <h3 class="card-title"><a href="paper.html?id=${paper.id}">${paper.ten}</a></h3>
            <p class="card-desc">${paper.moTa}</p>
            <div class="chips">${chips || '<span class="soon">Sắp có</span>'}</div>
          </div>
        </article>
      </li>`;
  }

  function renderRoute(papers, activePaper) {
    const root = document.getElementById('route');
    if (!root) return;
    const order = [];
    papers.forEach(p => { if (!order.includes(p.nhom)) order.push(p.nhom); });
    let no = 0;
    let html = '';
    order.forEach(name => {
      const info = groupInfo(name);
      const list = papers.filter(p => p.nhom === name);
      
      let stopsHtml = '';
      let rtcGroupBuffer = [];

      list.forEach(p => {
        no++;
        const state = p.trangThai === 'da-present' ? 'done' : (p.id === activePaper.id ? 'active' : 'todo');
        const sHtml = stopHtml(p, no, state);

        if (p.cap === 'RTC') {
          rtcGroupBuffer.push(sHtml);
          if (p.thuTuCap === 2 || rtcGroupBuffer.length === 2) {
            stopsHtml += `
              <li class="pair-rtc-group"><ol class="pair-list">
                ${rtcGroupBuffer.join('')}</ol>
                <div class="pair-rtc-bracket" aria-hidden="true" title="Cặp bài RTC">
                  <svg class="pair-rtc-bracket-svg" viewBox="0 0 20 100" preserveAspectRatio="none">
                    <path d="M 2 2 C 14 2, 14 44, 18 50 C 14 56, 14 98, 2 98" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  </svg>
                </div>
              </li>`;
            rtcGroupBuffer = [];
          }
        } else {
          if (rtcGroupBuffer.length > 0) {
            stopsHtml += rtcGroupBuffer.join('');
            rtcGroupBuffer = [];
          }
          stopsHtml += sHtml;
        }
      });
      if (rtcGroupBuffer.length > 0) {
        stopsHtml += rtcGroupBuffer.join('');
      }

      html += `
        <section class="line ${info.cls}" aria-label="${info.title}">
          <header class="line-head">
            <span class="line-badge">${order.indexOf(name) + 1}</span>
            <div><h2>${info.title}</h2><p>${list.length} paper${info.hint ? ' · ' + info.hint : ''}</p></div>
          </header>
          <div class="track" aria-hidden="true"><i class="track-fill"></i></div>
          <ol class="stops">${stopsHtml}</ol>
        </section>`;
    });
    root.innerHTML = html;

    // Đường ray tô màu tới ga cuối cùng đã xong hoặc đang học
    function layoutTracks() {
      root.querySelectorAll('.line').forEach(sec => {
        const track = sec.querySelector('.track');
        const fill = track.querySelector('.track-fill');
        const reached = sec.querySelectorAll('.stop.is-done, .stop.is-active');
        if (!reached.length) { fill.style.setProperty('--fill', '0px'); return; }
        const node = reached[reached.length - 1].querySelector('.node');
        const y = node.getBoundingClientRect().top + node.offsetHeight / 2 - track.getBoundingClientRect().top;
        fill.style.setProperty('--fill', Math.max(0, y) + 'px');
      });
    }
    layoutTracks();
    if (!renderRoute.bound) {
      renderRoute.bound = true;
      renderRoute.layout = layoutTracks;
      window.addEventListener('resize', () => renderRoute.layout());
      window.addEventListener('load', () => renderRoute.layout());
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => renderRoute.layout());
    } else {
      renderRoute.layout = layoutTracks;
    }

    // Hiện dần khi cuộn tới
    const targets = root.querySelectorAll('.line, .stop');
    if (renderRoute.rendered) {
      targets.forEach(el => el.classList.add('is-in'));
      return;
    }
    renderRoute.rendered = true;
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries, obs) => {
        entries.forEach(e => {
          if (!e.isIntersecting) return;
          e.target.classList.add('is-in');
          obs.unobserve(e.target);
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });
      targets.forEach(el => io.observe(el));
    } else {
      targets.forEach(el => el.classList.add('is-in'));
    }
  }

  // Tiến độ do người dùng tự tích, lưu trong trình duyệt. papers.js chỉ là giá trị mặc định.
  const PROGRESS_KEY = 'vla_progress_v1';
  function loadOverrides() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {}; } catch (e) { return {}; }
  }
  function saveOverrides(o) {
    try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(o)); } catch (e) {}
  }
  function effectivePapers(overrides) {
    return window.PAPERS.map(p => {
      const ov = overrides[p.id];
      let st = p.trangThai;
      if (ov === 'done') st = 'da-present';
      else if (ov === 'todo' && st === 'da-present') st = 'chua-doc';
      return Object.assign({}, p, { trangThai: st });
    });
  }

  function initHomePage() {
    if (!window.PAPERS || !Array.isArray(window.PAPERS) || !document.getElementById('route')) return;

    let overrides = loadOverrides();

    function toggle(id) {
      const base = window.PAPERS.find(p => p.id === id);
      if (!base) return;
      const isDone = effectivePapers(overrides).find(p => p.id === id).trangThai === 'da-present';
      const wantDone = !isDone;
      if (wantDone === (base.trangThai === 'da-present')) delete overrides[id];
      else overrides[id] = wantDone ? 'done' : 'todo';
      saveOverrides(overrides);
      refresh();
    }

    function refresh() {
      const papers = effectivePapers(overrides);
      const total = papers.length;
      const done = papers.filter(p => p.trangThai === 'da-present').length;
      const activePaper = papers.find(p => p.trangThai === 'dang-doc')
        || papers.find(p => p.trangThai !== 'da-present')
        || papers[papers.length - 1];
      const activeNo = papers.indexOf(activePaper) + 1;

      const set = (id, text) => { const el = document.getElementById(id); if (el) el.textContent = text; };
      set('hero-focus-title', activePaper.ten);
      set('hero-focus-desc', activePaper.moTa);
      set('hero-focus-group', `${groupInfo(activePaper.nhom).title} · Paper ${activeNo}/${total}`);
      set('hero-eyebrow', `Sổ tay VLA · ${total} paper`);
      set('hero-progress-sub', done >= total ? `Đã đọc hết ${total} paper` : `${done}/${total} paper đã xong`);
      const cta = document.getElementById('hero-focus-cta');
      if (cta) cta.href = `paper.html?id=${activePaper.id}`;

      const pips = document.getElementById('hero-pips');
      if (pips) {
        pips.innerHTML = papers.map((p, i) => {
          const cls = p.trangThai === 'da-present' ? 'is-done' : (p.id === activePaper.id ? 'is-active' : '');
          return `<i class="${cls}" style="--i:${i}"></i>`;
        }).join('');
      }

      const resetBtn = document.getElementById('reset-progress');
      if (resetBtn) resetBtn.hidden = Object.keys(overrides).length === 0;

      renderRoute(papers, activePaper);
      initHomeExtras(papers, activePaper);
    }

    document.getElementById('route').addEventListener('click', function (e) {
      const btn = e.target.closest('[data-toggle]');
      if (btn) toggle(btn.getAttribute('data-toggle'));
    });
    const resetBtn = document.getElementById('reset-progress');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        overrides = {};
        saveOverrides(overrides);
        refresh();
      });
    }

    refresh();
  }

  // Thanh "Đọc tiếp" nổi + ánh sáng đi theo chuột trên thẻ
  function initHomeExtras(papers, activePaper) {
    const dock = document.getElementById('dock');
    if (dock) {
      dock.href = `paper.html?id=${activePaper.id}`;
      const t = document.getElementById('dock-title');
      if (t) t.textContent = activePaper.ten;
      const dp = document.getElementById('dock-pips');
      if (dp) {
        dp.innerHTML = papers.map(p =>
          `<i class="${p.trangThai === 'da-present' ? 'is-done' : (p.id === activePaper.id ? 'is-active' : '')}"></i>`
        ).join('');
      }
    }

    // Dải tên paper chạy ngang (tự lấy từ papers.js)
    const ticker = document.getElementById('ticker');
    if (ticker) {
      const item = p => {
        const st = p.trangThai === 'da-present' ? 'is-done' : (p.id === activePaper.id ? 'is-active' : '');
        return `<span class="tk ${st}"><i></i>${p.ten}<em>${p.arxiv}</em></span>`;
      };
      const once = papers.map(item).join('');
      ticker.innerHTML = once + once + once + once;
    }

    if (initHomeExtras.bound) return;
    initHomeExtras.bound = true;

    const heroEl = document.querySelector('.hero');
    if (dock && heroEl && 'IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        dock.classList.toggle('is-shown', !e.isIntersecting);
      }, { threshold: 0 }).observe(heroEl);
    }

    // Thanh tiến độ cuộn trang
    const bar = document.getElementById('scrollbar');
    if (bar) {
      let queued = false;
      const update = () => {
        queued = false;
        const max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.transform = `scaleX(${max > 0 ? Math.min(1, window.scrollY / max) : 0})`;
      };
      window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
      update();
    }

    // Vé nghiêng nhẹ theo chuột
    const ticket = document.querySelector('.ticket');
    const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (ticket && !reduce && window.matchMedia('(hover: hover)').matches) {
      const hero = document.querySelector('.hero');
      hero.addEventListener('pointermove', e => {
        const r = ticket.getBoundingClientRect();
        const x = (e.clientX - (r.left + r.width / 2)) / window.innerWidth;
        const y = (e.clientY - (r.top + r.height / 2)) / window.innerHeight;
        ticket.style.setProperty('--ry', (x * 14).toFixed(2) + 'deg');
        ticket.style.setProperty('--rx', (-y * 14).toFixed(2) + 'deg');
      });
      hero.addEventListener('pointerleave', () => {
        ticket.style.setProperty('--ry', '0deg');
        ticket.style.setProperty('--rx', '0deg');
      });
    }

    const route = document.getElementById('route');
    if (route) {
      route.addEventListener('pointermove', function (e) {
        const card = e.target.closest('.card');
        if (!card) return;
        const r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    }
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
