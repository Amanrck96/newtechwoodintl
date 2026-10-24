/**
 * F7: Board Anatomy Hotspots
 * Real Photographic / 3D Render UltraShield 360 board with interactive benefit hotspots:
 * 1. 360° All-Round Protective Shield
 * 2. Advanced UV Protection
 * 3. Mold & Mildew Resistance
 * 4. 25-Year Warranty
 * 5. High Stain Resistance
 * 6. Natural Hardwood Surface
 * 7. Dense Recycled Composite Core (95% Reclaimed Content)
 */

(function () {
  'use strict';

  const HOTSPOTS = [
    {
      id: 'fully-capped',
      num: 1,
      x: 36,
      y: 74,
      title: '360° All-Round Protective Shield',
      tag: 'Patented Co-Extrusion',
      desc: 'Unlike conventional composites that leave bottoms and grooves exposed to moisture, UltraShield is 100% encapsulated on all four sides and inside the hidden clip channels, preventing swelling and delamination.'
    },
    {
      id: 'uv-protection',
      num: 2,
      x: 58,
      y: 20,
      title: 'Advanced UV Protection',
      tag: 'Sunlight Defense',
      desc: 'Formulated with high-grade UV inhibitors and light stabilizers that shield color pigments against severe tropical solar exposure, ensuring minimal color shift over decades.'
    },
    {
      id: 'mold-resistance',
      num: 3,
      x: 80,
      y: 26,
      title: 'Mold & Mildew Resistance',
      tag: 'Moisture Barrier',
      desc: 'The non-porous outer polymer capping exhibits virtually 0% water absorption. Algae and mold spores cannot penetrate or root into the material, even during torrential monsoons.'
    },
    {
      id: 'warranty',
      num: 4,
      x: 66,
      y: 44,
      title: '25-Year Warranty',
      tag: 'Long-Term Confidence',
      desc: 'Every UltraShield board is backed by an industry-leading 25-year limited residential warranty guaranteeing structural performance against rot, splitting, and decay.'
    },
    {
      id: 'stain-resistance',
      num: 5,
      x: 45,
      y: 32,
      title: 'High Stain Resistance',
      tag: 'Easy Cleaning',
      desc: 'Red wine, coffee, mustard, barbecue fats, and sunscreen cannot penetrate the outer shield. Spills remain on the surface and wash away easily with plain water and mild detergent.'
    },
    {
      id: 'natural-surface',
      num: 6,
      x: 72,
      y: 35,
      title: 'Natural Hardwood Surface',
      tag: 'Multi-Chromatic Aesthetics',
      desc: 'Deep multi-tonal wood grain patterns with varied color streaks provide the organic visual warmth and matte tactile feel of exotic timber without any artificial plastic shine.'
    },
    {
      id: 'eco-friendly',
      num: 7,
      x: 24,
      y: 52,
      title: 'Dense Recycled Composite Core',
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
              <div class="ntw-hotspots-image-container">
                <!-- Real Photorealistic 3D Render of UltraShield 360 Board Profile -->
                <img 
                  src="/wp-content/uploads/2026/04/UltraShield-360.png" 
                  alt="NewTechWood UltraShield 360 Co-extruded Composite Board Profile with dense recycled core" 
                  class="ntw-hotspots-board-real-img"
                  width="800"
                  height="523"
                />

                <!-- 1. Left Core Callout Badge -->
                <div class="ntw-callout-badge ntw-callout-core">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">DENSE RECYCLED COMPOSITE CORE</span>
                    <span class="ntw-callout-badge-sub">95% Reclaimed Hardwood Fiber &amp; Polyethylene</span>
                  </div>
                </div>

                <!-- 2. Right/Bottom Shield Callout Badge -->
                <div class="ntw-callout-badge ntw-callout-shield">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">360° ALL-ROUND PROTECTIVE SHIELD</span>
                    <span class="ntw-callout-badge-sub">100% Encapsulated Co-Extrusion Outer Capping</span>
                  </div>
                </div>

                <!-- Hotspot Pins Positioned Directly on the Real Board -->
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
