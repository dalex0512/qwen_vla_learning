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

        let cardClass = 'book-card cv-host';
        if (isActive) cardClass += ' book-card--active is-active';
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

        // Bìa SVG từ Covers / VLA_COVERS
        const coverBia = paper.bia || paper.id;
        let coverSvgMarkup = '';
        if (window.VLA_COVERS && window.VLA_COVERS[coverBia]) {
          coverSvgMarkup = window.VLA_COVERS[coverBia];
        } else if (window.Covers && typeof window.Covers.render === 'function') {
          coverSvgMarkup = window.Covers.render(coverBia, paper, overallIndex);
        } else {
          coverSvgMarkup = `<div style="padding: 40px; text-align: center;">${paper.ten}</div>`;
        }

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
