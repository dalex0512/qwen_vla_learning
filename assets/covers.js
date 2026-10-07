/* Bìa minh hoạ cho từng paper.
   Dùng: window.VLA_COVERS[key]  -> chuỗi <svg>…</svg>
   key: libero | groot | qwen | rtc-infer | rtc-train | moe
   Màu lấy từ biến CSS trong covers.css (tự đổi theo sáng/tối).
   Hoạt ảnh chạy khi phần tử cha có class "cv-host" được hover, hoặc có class "is-active". */
(function () {
  const bg = (id, deep) => `
    <defs>
      <linearGradient id="${id}-g" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" style="stop-color:var(${deep ? '--cv-bgd1' : '--cv-bg1'})"/>
        <stop offset="1" style="stop-color:var(${deep ? '--cv-bgd2' : '--cv-bg2'})"/>
      </linearGradient>
    </defs>
    <rect width="400" height="300" fill="url(#${id}-g)"/>
    <circle cx="352" cy="38" r="90" class="cv-blob"/>
    <circle cx="40" cy="282" r="70" class="cv-blob"/>`;

  const svg = (key, body) =>
    `<svg class="cv cv-${key}" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true" focusable="false">${body}</svg>`;

  const COVERS = {
    /* 1. LIBERO — bàn bếp nhìn từ trên xuống: kẹp robot mang cái bát sang đĩa */
    libero: svg('libero', bg('libero', false) + `
      <rect x="62" y="78" width="280" height="168" rx="24" class="cv-shadow"/>
      <rect x="58" y="70" width="284" height="168" rx="24" class="cv-surface"/>
      <rect x="252" y="88" width="70" height="46" rx="10" class="cv-indigo-2"/>
      <rect x="276" y="106" width="22" height="5" rx="2.5" class="cv-indigo"/>
      <circle cx="272" cy="188" r="32" class="cv-surface cv-stroke"/>
      <circle cx="272" cy="188" r="21" class="cv-none cv-stroke-thin"/>
      <g class="cv-move-bowl">
        <circle cx="128" cy="174" r="25" class="cv-amber"/>
        <circle cx="128" cy="174" r="15" class="cv-amber-2"/>
        <rect x="110" y="134" width="36" height="14" rx="7" class="cv-teal"/>
        <rect x="108" y="140" width="8" height="24" rx="4" class="cv-teal"/>
        <rect x="140" y="140" width="8" height="24" rx="4" class="cv-teal"/>
        <rect x="122" y="102" width="12" height="36" rx="6" class="cv-teal"/>
      </g>
      <rect x="80" y="214" width="12" height="12" rx="3" class="cv-teal"/>
      <rect x="98" y="214" width="12" height="12" rx="3" class="cv-amber"/>
      <rect x="116" y="214" width="12" height="12" rx="3" class="cv-indigo"/>
      <rect x="134" y="214" width="12" height="12" rx="3" class="cv-ink-soft"/>`),

    /* 2. GR00T N1 — người máy: đầu (Hệ 2, suy nghĩ) phát tín hiệu xuống tay (Hệ 1, hành động) */
    groot: svg('groot', bg('groot', false) + `
      <circle cx="200" cy="84" r="44" class="cv-amber-2 cv-halo"/>
      <line x1="182" y1="214" x2="174" y2="268" class="cv-limb cv-limb-dark"/>
      <line x1="218" y1="214" x2="226" y2="268" class="cv-limb cv-limb-dark"/>
      <polyline points="166,140 128,186 136,230" class="cv-limb"/>
      <polyline points="234,140 276,176 300,146" class="cv-limb"/>
      <rect x="190" y="104" width="20" height="20" rx="6" class="cv-teal"/>
      <rect x="158" y="118" width="84" height="100" rx="26" class="cv-teal"/>
      <circle cx="200" cy="158" r="12" class="cv-surface cv-dim"/>
      <circle cx="200" cy="84" r="28" class="cv-amber"/>
      <rect x="186" y="78" width="28" height="9" rx="4.5" class="cv-surface"/>
      <circle cx="300" cy="146" r="11" class="cv-amber"/>
      <circle r="6" class="cv-signal cv-surface" style="offset-path: path('M200 92 L200 158 L234 140 L276 176 L300 146')"/>`),

    /* 3. Qwen-VLA — ảnh (mắt) + lệnh (bong bóng) vào bộ não VLM, ra quỹ đạo hành động */
    qwen: svg('qwen', bg('qwen', false) + `
      <path d="M128 108 C 160 108, 180 150, 200 150" class="cv-flow"/>
      <path d="M128 196 C 160 196, 180 150, 200 150" class="cv-flow"/>
      <path d="M46 108 Q 86 74 126 108 Q 86 142 46 108 Z" class="cv-surface cv-stroke"/>
      <circle cx="86" cy="108" r="13" class="cv-teal"/>
      <circle cx="91" cy="103" r="4" class="cv-surface"/>
      <path d="M50 176 h70 a12 12 0 0 1 12 12 v18 a12 12 0 0 1 -12 12 h-46 l-12 12 v-12 h-12 a12 12 0 0 1 -12 -12 v-18 a12 12 0 0 1 12 -12 Z" class="cv-surface cv-stroke"/>
      <rect x="54" y="189" width="54" height="6" rx="3" class="cv-ink-soft"/>
      <rect x="54" y="200" width="36" height="6" rx="3" class="cv-ink-soft"/>
      <rect x="164" y="114" width="72" height="72" rx="22" class="cv-teal"/>
      <rect x="180" y="130" width="17" height="17" rx="5" class="cv-teal-2"/>
      <rect x="203" y="130" width="17" height="17" rx="5" class="cv-surface cv-dim"/>
      <rect x="180" y="153" width="17" height="17" rx="5" class="cv-surface cv-dim"/>
      <rect x="203" y="153" width="17" height="17" rx="5" class="cv-teal-2"/>
      <path id="qwen-traj" d="M236 150 C 270 150, 280 92, 314 100 S 350 170, 362 132" class="cv-traj"/>
      <circle r="7" class="cv-amber cv-dot cv-dot1" style="offset-path: path('M236 150 C 270 150, 280 92, 314 100 S 350 170, 362 132')"/>
      <circle r="7" class="cv-amber cv-dot cv-dot2" style="offset-path: path('M236 150 C 270 150, 280 92, 314 100 S 350 170, 362 132')"/>
      <circle r="7" class="cv-amber cv-dot cv-dot3" style="offset-path: path('M236 150 C 270 150, 280 92, 314 100 S 350 170, 362 132')"/>`),

    /* 4. RTC inference — các action chunk nối tiếp trên trục thời gian, chỗ nối được làm mượt */
    'rtc-infer': svg('rtc-infer', bg('rtcI', true) + `
      <path d="M48 120 C 100 60, 140 170, 200 118 S 300 70, 352 112" class="cv-traj cv-traj-wide"/>
      <rect x="152" y="96" width="44" height="150" rx="10" class="cv-amber-2 cv-soft"/>
      <rect x="252" y="96" width="44" height="150" rx="10" class="cv-amber-2 cv-soft"/>
      <rect x="48" y="168" width="148" height="24" rx="12" class="cv-indigo cv-chunk cv-chunk1"/>
      <rect x="152" y="196" width="144" height="24" rx="12" class="cv-indigo-mid cv-chunk cv-chunk2"/>
      <rect x="252" y="224" width="100" height="24" rx="12" class="cv-indigo-2 cv-chunk cv-chunk3"/>
      <line x1="48" y1="266" x2="352" y2="266" class="cv-axis"/>
      <path d="M344 260 L354 266 L344 272" class="cv-axis cv-none"/>`),

    /* 5. RTC training — action chunk đặt trong vòng lặp huấn luyện */
    'rtc-train': svg('rtc-train', bg('rtcT', true) + `
      <circle cx="200" cy="150" r="96" class="cv-ring-track"/>
      <g class="cv-spin">
        <circle cx="200" cy="150" r="96" class="cv-ring"/>
        <path d="M290 112 L306 136 L278 136 Z" class="cv-indigo"/>
        <path d="M110 188 L94 164 L122 164 Z" class="cv-indigo"/>
      </g>
      <rect x="120" y="114" width="80" height="22" rx="11" class="cv-indigo"/>
      <rect x="160" y="141" width="80" height="22" rx="11" class="cv-indigo-mid"/>
      <rect x="200" y="168" width="80" height="22" rx="11" class="cv-indigo-2"/>
      <rect x="160" y="141" width="40" height="22" rx="11" class="cv-amber cv-overlap"/>
      <rect x="200" y="168" width="40" height="22" rx="11" class="cv-amber cv-overlap"/>`),

    /* 6. LingBot MoE — router chia token tới vài chuyên gia (chỉ vài chuyên gia sáng) */
    moe: svg('moe', bg('moe', true) + `
      <path d="M78 150 L132 150" class="cv-wire"/>
      <path d="M188 150 C 210 150, 210 70, 250 70" class="cv-wire cv-w1"/>
      <path d="M188 150 C 210 150, 210 123, 250 123" class="cv-wire cv-w2"/>
      <path d="M188 150 C 210 150, 210 177, 250 177" class="cv-wire cv-w3"/>
      <path d="M188 150 C 210 150, 210 230, 250 230" class="cv-wire cv-w4"/>
      <path d="M318 70 C 340 70, 336 150, 356 150 M318 123 C 340 123, 336 150, 356 150 M318 177 C 340 177, 336 150, 356 150 M318 230 C 340 230, 336 150, 356 150" class="cv-wire cv-wire-faint"/>
      <circle cx="70" cy="150" r="13" class="cv-ink-soft"/>
      <path d="M160 120 L190 150 L160 180 L130 150 Z" class="cv-indigo" stroke-linejoin="round"/>
      <rect x="250" y="54" width="68" height="32" rx="16" class="cv-expert cv-e1"/>
      <rect x="250" y="107" width="68" height="32" rx="16" class="cv-expert cv-e2"/>
      <rect x="250" y="161" width="68" height="32" rx="16" class="cv-expert cv-e3"/>
      <rect x="250" y="214" width="68" height="32" rx="16" class="cv-expert cv-e4"/>
      <circle cx="360" cy="150" r="11" class="cv-teal"/>`)
  };

  window.VLA_COVERS = COVERS;
  // Bìa cơ bản: nền phẳng theo nhóm, số thứ tự lớn và tên paper
  window.Covers = {
    render: function (key, paper) {
      if (!paper) return '';
      const list = window.PAPERS || [];
      const idx = String(list.findIndex(p => p.id === paper.id) + 1).padStart(2, '0');
      const deep = paper.nhom === 'Đọc sâu';
      return `<div class="cover-basic ${deep ? 'cover-basic--indigo' : 'cover-basic--teal'}">
        <span class="cover-basic-num">${idx}</span>
        <span class="cover-basic-group">${paper.nhom}</span>
        <span class="cover-basic-name">${paper.ten}</span>
      </div>`;
    }
  };
})();
