/**
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
