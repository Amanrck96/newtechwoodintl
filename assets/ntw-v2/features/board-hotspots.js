/**
 * F7: Board Anatomy Hotspots
 * Interactive SVG UltraShield board diagram with clickable benefit hotspots:
 * 1. Fully capped
 * 2. UV protection
 * 3. Mold/mildew resistance
 * 4. 25-year warranty
 * 5. Stain resistance
 * 6. Natural surface
 * 7. Environmentally friendly
 */

(function () {
  'use strict';

  const HOTSPOTS = [
    {
      id: 'fully-capped',
      num: 1,
      x: 18,
      y: 28,
      title: 'Fully Capped 360° Shield',
      tag: 'Patented Co-Extrusion',
      desc: 'Unlike conventional composites that leave bottoms and grooves exposed to moisture, UltraShield is 100% encapsulated on all four sides and inside the hidden clip channels, preventing swelling and delamination.'
    },
    {
      id: 'uv-protection',
      num: 2,
      x: 36,
      y: 16,
      title: 'Advanced UV Protection',
      tag: 'Sunlight Defense',
      desc: 'Formulated with high-grade UV inhibitors and light stabilizers that shield color pigments against severe tropical solar exposure, ensuring minimal color shift over decades.'
    },
    {
      id: 'mold-resistance',
      num: 3,
      x: 84,
      y: 35,
      title: 'Mold & Mildew Resistance',
      tag: 'Moisture Barrier',
      desc: 'The non-porous outer polymer capping exhibits virtually 0% water absorption. Algae and mold spores cannot penetrate or root into the material, even during torrential monsoons.'
    },
    {
      id: 'warranty',
      num: 4,
      x: 50,
      y: 52,
      title: '25-Year Warranty',
      tag: 'Long-Term Confidence',
      desc: 'Every UltraShield board is backed by an industry-leading 25-year limited residential warranty guaranteeing structural performance against rot, splitting, and decay.'
    },
    {
      id: 'stain-resistance',
      num: 5,
      x: 64,
      y: 20,
      title: 'High Stain Resistance',
      tag: 'Easy Cleaning',
      desc: 'Red wine, coffee, mustard, barbecue fats, and sunscreen cannot penetrate the outer shield. Spills remain on the surface and wash away easily with plain water and mild detergent.'
    },
    {
      id: 'natural-surface',
      num: 6,
      x: 78,
      y: 20,
      title: 'Natural Hardwood Surface',
      tag: 'Multi-Chromatic Aesthetics',
      desc: 'Deep multi-tonal wood grain patterns with varied color streaks provide the organic visual warmth and matte tactile feel of exotic timber without any artificial plastic shine.'
    },
    {
      id: 'eco-friendly',
      num: 7,
      x: 34,
      y: 72,
      title: 'Environmentally Friendly',
      tag: '95% Recycled Content',
      desc: 'Manufactured from 95% recycled materials, combining dense reclaimed hardwood sawdust fibers with recycled high-density plastics, keeping thousands of tons of waste out of landfills.'
    }
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBoardHotspots);
  } else {
    initBoardHotspots();
  }

  function initBoardHotspots() {
    let mount = document.getElementById('ntw-board-hotspots');

    if (!mount) {
      const anchor = document.getElementById('ntw-color-swatch-explorer') || document.getElementById('ntw-sample-request');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-board-hotspots';
      anchor.parentNode.insertBefore(mount, anchor.nextSibling);
    }

    let activeIndex = 0;

    mount.innerHTML = `
      <section class="ntw-hotspots-section" aria-label="UltraShield Board Anatomy and Technology">
        <div class="ntw-hotspots-container">
          
          <div class="ntw-hotspots-header">
            <span class="ntw-hotspots-eyebrow">Anatomy of Innovation</span>
            <h2 class="ntw-hotspots-title">What Makes UltraShield® Different?</h2>
            <p class="ntw-hotspots-subtitle">Click on any hotspot below to explore the advanced co-extrusion technology engineered into every NewTechWood profile.</p>
          </div>

          <div class="ntw-hotspots-stage">
            
            <div class="ntw-hotspots-diagram-wrap">
              <!-- SVG Cross-Section of UltraShield Decking Board -->
              <svg class="ntw-hotspots-svg" viewBox="0 0 800 480" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="UltraShield board cross-section diagram">
                <defs>
                  <!-- Outer Shield Gradient -->
                  <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#b57644" />
                    <stop offset="50%" stop-color="#8a5327" />
                    <stop offset="100%" stop-color="#5a3416" />
                  </linearGradient>
                  <!-- Core Matrix Gradient -->
                  <linearGradient id="coreGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#2d2218" />
                    <stop offset="100%" stop-color="#1e1610" />
                  </linearGradient>
                  <pattern id="coreTexture" width="20" height="20" patternUnits="userSpaceOnUse">
                    <circle cx="5" cy="5" r="1.5" fill="rgba(255,255,255,0.06)" />
                    <circle cx="15" cy="15" r="1.2" fill="rgba(255,255,255,0.04)" />
                  </pattern>
                </defs>

                <!-- Board Shadow -->
                <ellipse cx="400" cy="420" rx="360" ry="24" fill="rgba(0,0,0,0.12)" />

                <!-- 1. Outer 360 Capping Layer -->
                <path d="M 80,120 Q 400,95 720,120 C 740,122 750,135 750,155 L 750,280 C 750,300 735,315 715,315 L 685,315 L 675,260 L 635,260 L 635,315 L 165,315 L 165,260 L 125,260 L 115,315 L 85,315 C 65,315 50,300 50,280 L 50,155 C 50,135 60,122 80,120 Z" fill="url(#shieldGrad)" stroke="#42240c" stroke-width="6" />

                <!-- 2. Wood Grain Accent Waves on Outer Shield -->
                <path d="M 100,128 Q 280,116 460,126 T 700,128" stroke="rgba(255,255,255,0.22)" stroke-width="2.5" fill="none" />
                <path d="M 120,140 Q 320,128 520,138 T 680,140" stroke="rgba(0,0,0,0.2)" stroke-width="2" fill="none" />

                <!-- 3. Inner Dense Core Layer -->
                <path d="M 94,142 Q 400,122 706,142 C 720,144 728,154 728,168 L 728,265 C 728,280 716,290 700,290 L 672,290 L 660,245 L 648,245 L 648,290 L 152,290 L 152,245 L 140,245 L 128,290 L 100,290 C 84,290 72,280 72,265 L 72,168 C 72,154 80,144 94,142 Z" fill="url(#coreGrad)" stroke="#2b1a0d" stroke-width="4" />
                <path d="M 94,142 Q 400,122 706,142 C 720,144 728,154 728,168 L 728,265 C 728,280 716,290 700,290 L 672,290 L 660,245 L 648,245 L 648,290 L 152,290 L 152,245 L 140,245 L 128,290 L 100,290 C 84,290 72,280 72,265 L 72,168 C 72,154 80,144 94,142 Z" fill="url(#coreTexture)" />

                <!-- Text Annotations inside diagram -->
                <text x="400" y="215" fill="#e5e7eb" font-family="'Inter', sans-serif" font-size="18" font-weight="700" text-anchor="middle" letter-spacing="1">DENSE RECYCLED COMPOSITE CORE</text>
                <text x="400" y="240" fill="#9ca3af" font-family="'Inter', sans-serif" font-size="13" text-anchor="middle">95% Reclaimed Hardwood Fiber &amp; Polyethylene</text>
                
                <!-- Side Shield Callout -->
                <text x="400" y="80" fill="#b57644" font-family="'Inter', sans-serif" font-size="14" font-weight="700" text-anchor="middle">360° ALL-ROUND PROTECTIVE SHIELD</text>
                <path d="M 400,90 L 400,115" stroke="#b57644" stroke-width="2" stroke-dasharray="3,3" />
              </svg>

              <!-- Hotspot Pins Positioned Relative to Diagram -->
              ${HOTSPOTS.map((h, idx) => `
                <button type="button" 
                  class="ntw-hotspot-pin ${idx === 0 ? 'active' : ''}" 
                  style="left: ${h.x}%; top: ${h.y}%;" 
                  data-hotspot-idx="${idx}" 
                  id="ntw-hotspot-pin-${h.id}"
                  aria-label="${escapeHtml(h.title)}"
                  aria-expanded="${idx === 0 ? 'true' : 'false'}"
                  aria-controls="ntw-hotspot-panel"
                >${h.num}</button>
              `).join('')}
            </div>

            <div class="ntw-hotspot-panel" id="ntw-hotspot-panel">
              <span class="ntw-hotspot-badge" id="ntw-hp-tag">${escapeHtml(HOTSPOTS[0].tag)}</span>
              <h3 class="ntw-hotspot-title" id="ntw-hp-title">${escapeHtml(HOTSPOTS[0].title)}</h3>
              <p class="ntw-hotspot-desc" id="ntw-hp-desc">${escapeHtml(HOTSPOTS[0].desc)}</p>

              <div class="ntw-hotspot-list" role="tablist" aria-label="Board Benefits">
                ${HOTSPOTS.map((h, idx) => `
                  <button type="button" class="ntw-hotspot-item-btn ${idx === 0 ? 'active' : ''}" data-hotspot-idx="${idx}" role="tab" aria-selected="${idx === 0 ? 'true' : 'false'}">
                    <span class="ntw-hotspot-item-num">${h.num}</span>
                    <span>${escapeHtml(h.title)}</span>
                  </button>
                `).join('')}
              </div>
            </div>

          </div>

        </div>
      </section>
    `;

    const pins = mount.querySelectorAll('.ntw-hotspot-pin');
    const listBtns = mount.querySelectorAll('.ntw-hotspot-item-btn');
    const tagEl = document.getElementById('ntw-hp-tag');
    const titleEl = document.getElementById('ntw-hp-title');
    const descEl = document.getElementById('ntw-hp-desc');

    function selectHotspot(idx) {
      if (idx === activeIndex) return;
      activeIndex = idx;
      const h = HOTSPOTS[idx];

      // Update pins
      pins.forEach((p, pIdx) => {
        const isActive = pIdx === idx;
        p.classList.toggle('active', isActive);
        p.setAttribute('aria-expanded', isActive ? 'true' : 'false');
      });

      // Update list items
      listBtns.forEach((btn, bIdx) => {
        const isActive = bIdx === idx;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      // Update text
      tagEl.textContent = h.tag;
      titleEl.textContent = h.title;
      descEl.textContent = h.desc;
    }

    pins.forEach((p, idx) => {
      p.addEventListener('click', () => selectHotspot(idx));
    });

    listBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => selectHotspot(idx));
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

})();
