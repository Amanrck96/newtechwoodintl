/**
 * F7: Board Anatomy Hotspots & 360° Technology Inspection
 * Real Photorealistic 3D Render UltraShield 360 board with interactive benefit hotspots:
 * 1. 360° All-Round Protective Shield (Interactive 360 Capping Inspection)
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
      tag: 'Patented 4-Side Co-Extrusion',
      desc: 'Unlike conventional composites that leave bottoms and hidden clip grooves exposed to moisture, UltraShield is 100% encapsulated on all four sides and inside the hidden clip channels, preventing swelling, delamination, and rotting.',
      is360: true,
      comparison: {
        cappedTitle: 'UltraShield® 360° Complete Polymer Shield',
        cappedPoints: [
          '100% 4-sided polymer envelope including inside fastener grooves',
          '0.0% moisture penetration — prevents swelling, rotting, and fungal decay',
          'High-temperature co-extrusion fusing shield directly to core (zero glues)'
        ],
        uncappedTitle: 'Conventional / Uncapped Composite',
        uncappedPoints: [
          'Exposed bottom and grooves absorb rainwater and morning condensation',
          'Susceptible to internal mold growth, warping, and surface cracking',
          'Requires harsh chemical treatments and ongoing maintenance'
        ]
      }
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
    let comparisonMode = 'capped'; // 'capped' or 'uncapped'

    mount.innerHTML = `
      <section class="ntw-hotspots-section" id="ntw-hotspots-section" aria-label="UltraShield Board Anatomy and Technology">
        <div class="ntw-hotspots-container">
          
          <div class="ntw-hotspots-header">
            <span class="ntw-hotspots-eyebrow">Anatomy of Innovation</span>
            <h2 class="ntw-hotspots-title">What Makes UltraShield® Different?</h2>
            <p class="ntw-hotspots-subtitle">Click on any hotspot or feature badge below to explore the advanced co-extrusion technology engineered into every NewTechWood profile.</p>
          </div>

          <div class="ntw-hotspots-stage">
            
            <div class="ntw-hotspots-diagram-wrap">
              <div class="ntw-hotspots-image-container">
                
                <!-- 360 Shield Aura Highlight -->
                <div class="ntw-360-aura-wrapper active" id="ntw-360-aura" aria-hidden="true">
                  <div class="ntw-360-aura-ring"></div>
                  <div class="ntw-360-tag-pill">
                    <span class="ntw-360-pill-icon">360°</span>
                    <span>FULL 4-SIDED ENCAPSULATION</span>
                  </div>
                </div>

                <!-- Real Photorealistic 3D Render of UltraShield 360 Board Profile -->
                <img 
                  src="/wp-content/uploads/2026/04/UltraShield-360.png" 
                  alt="NewTechWood UltraShield 360 Co-extruded Composite Board Profile with dense recycled core" 
                  class="ntw-hotspots-board-real-img"
                  width="800"
                  height="523"
                />

                <!-- 1. Left Core Callout Badge (Interactive Button) -->
                <button type="button" class="ntw-callout-badge ntw-callout-core" id="ntw-btn-badge-core" aria-label="Explore Dense Recycled Composite Core">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">DENSE RECYCLED COMPOSITE CORE</span>
                    <span class="ntw-callout-badge-sub">95% Reclaimed Hardwood Fiber &amp; Polyethylene</span>
                  </div>
                </button>

                <!-- 2. Right/Bottom Shield Callout Badge (Interactive Button) -->
                <button type="button" class="ntw-callout-badge ntw-callout-shield active" id="ntw-btn-badge-shield" aria-label="Explore 360° All-Round Protective Shield">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">360° ALL-ROUND PROTECTIVE SHIELD</span>
                    <span class="ntw-callout-badge-sub">100% Encapsulated Co-Extrusion Outer Capping &bull; Click to Inspect</span>
                  </div>
                </button>

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
              <div class="ntw-hp-top-row">
                <span class="ntw-hotspot-badge" id="ntw-hp-tag">${escapeHtml(HOTSPOTS[0].tag)}</span>
                <span class="ntw-hp-active-num" id="ntw-hp-active-num">Benefit #1 of 7</span>
              </div>

              <h3 class="ntw-hotspot-title" id="ntw-hp-title">${escapeHtml(HOTSPOTS[0].title)}</h3>
              <p class="ntw-hotspot-desc" id="ntw-hp-desc">${escapeHtml(HOTSPOTS[0].desc)}</p>

              <!-- Interactive 360 Technology Comparison Box -->
              <div class="ntw-360-comparison-box" id="ntw-360-comparison-box">
                <div class="ntw-360-tabs-row" role="tablist" aria-label="360 Technology Comparison">
                  <button type="button" class="ntw-360-tab-btn active" id="ntw-tab-360-capped" role="tab" aria-selected="true">
                    <span>✓ UltraShield 360°</span>
                  </button>
                  <button type="button" class="ntw-360-tab-btn" id="ntw-tab-360-uncapped" role="tab" aria-selected="false">
                    <span>✗ Uncapped Ordinary</span>
                  </button>
                </div>

                <div class="ntw-360-tab-content" id="ntw-360-tab-content">
                  <div class="ntw-360-points-list" id="ntw-360-points-list">
                    <div class="ntw-360-point-item">
                      <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                      <span>100% 4-sided polymer envelope wraps all four sides and clip grooves.</span>
                    </div>
                    <div class="ntw-360-point-item">
                      <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                      <span>0.0% moisture absorption prevents swelling, rotting, and mold decay.</span>
                    </div>
                    <div class="ntw-360-point-item">
                      <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                      <span>Simultaneous high-temp co-extrusion creates permanent impermeable bond.</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Hotspots List Navigation -->
              <div class="ntw-hotspot-list-header">
                <span>All 7 Engineering Benefits</span>
              </div>
              <div class="ntw-hotspot-list" role="tablist" aria-label="Board Benefits">
                ${HOTSPOTS.map((h, idx) => `
                  <button type="button" class="ntw-hotspot-item-btn ${idx === 0 ? 'active' : ''}" data-hotspot-idx="${idx}" role="tab" aria-selected="${idx === 0 ? 'true' : 'false'}">
                    <span class="ntw-hotspot-item-num">${h.num}</span>
                    <span>${escapeHtml(h.title)}</span>
                  </button>
                `).join('')}
              </div>

              <!-- Action Bar -->
              <div class="ntw-hp-actions">
                <button type="button" class="ntw-hp-btn-sample" id="ntw-hp-btn-sample">
                  <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
                  <span>Request 360° Sample Kit</span>
                </button>
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
    const activeNumEl = document.getElementById('ntw-hp-active-num');
    const auraEl = document.getElementById('ntw-360-aura');
    const comparisonBox = document.getElementById('ntw-360-comparison-box');
    const tabCapped = document.getElementById('ntw-tab-360-capped');
    const tabUncapped = document.getElementById('ntw-tab-360-uncapped');
    const pointsList = document.getElementById('ntw-360-points-list');
    const sampleBtn = document.getElementById('ntw-hp-btn-sample');

    const badgeShield = document.getElementById('ntw-btn-badge-shield');
    const badgeCore = document.getElementById('ntw-btn-badge-core');

    function updateComparison(mode) {
      comparisonMode = mode;
      const isCapped = mode === 'capped';

      if (tabCapped) {
        tabCapped.classList.toggle('active', isCapped);
        tabCapped.setAttribute('aria-selected', isCapped ? 'true' : 'false');
      }
      if (tabUncapped) {
        tabUncapped.classList.toggle('active', !isCapped);
        tabUncapped.setAttribute('aria-selected', !isCapped ? 'true' : 'false');
      }

      if (isCapped) {
        pointsList.innerHTML = `
          <div class="ntw-360-point-item">
            <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            <span><strong>100% 4-Sided Envelope:</strong> Wraps all four sides and fastener grooves with zero exposed core.</span>
          </div>
          <div class="ntw-360-point-item">
            <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            <span><strong>0.0% Moisture Absorption:</strong> Eliminates swelling, cupping, warping, and mold decay.</span>
          </div>
          <div class="ntw-360-point-item">
            <svg viewBox="0 0 24 24" class="ntw-check-icon"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            <span><strong>High-Temp Co-Extrusion:</strong> Fuses polymer shield to dense core without chemical adhesives.</span>
          </div>
        `;
      } else {
        pointsList.innerHTML = `
          <div class="ntw-360-point-item ntw-warn-point">
            <svg viewBox="0 0 24 24" class="ntw-cross-icon"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
            <span><strong>Exposed Grooves &amp; Bottom:</strong> Rainwater enters untreated wood fibers beneath the board.</span>
          </div>
          <div class="ntw-360-point-item ntw-warn-point">
            <svg viewBox="0 0 24 24" class="ntw-cross-icon"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
            <span><strong>Water Absorption Risk:</strong> Internal dampness promotes mold infestation, rotting, and swelling.</span>
          </div>
          <div class="ntw-360-point-item ntw-warn-point">
            <svg viewBox="0 0 24 24" class="ntw-cross-icon"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
            <span><strong>Ongoing Maintenance Required:</strong> Vulnerable to staining, surface delamination, and bleaching.</span>
          </div>
        `;
      }
    }

    if (tabCapped) tabCapped.addEventListener('click', () => updateComparison('capped'));
    if (tabUncapped) tabUncapped.addEventListener('click', () => updateComparison('uncapped'));

    function selectHotspot(idx) {
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

      // Update badges
      if (badgeShield) badgeShield.classList.toggle('active', idx === 0);
      if (badgeCore) badgeCore.classList.toggle('active', idx === 6);

      // 360 Aura highlight
      if (auraEl) {
        auraEl.classList.toggle('active', idx === 0);
      }

      // Comparison box visibility
      if (comparisonBox) {
        comparisonBox.style.display = idx === 0 ? 'block' : 'none';
      }

      // Update text
      tagEl.textContent = h.tag;
      titleEl.textContent = h.title;
      descEl.textContent = h.desc;
      activeNumEl.textContent = `Benefit #${h.num} of 7`;
    }

    // Pin click listeners
    pins.forEach((p, idx) => {
      p.addEventListener('click', () => selectHotspot(idx));
    });

    // List item click listeners
    listBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => selectHotspot(idx));
    });

    // Callout badges interactive triggers
    if (badgeShield) {
      badgeShield.addEventListener('click', () => {
        selectHotspot(0);
        updateComparison('capped');
      });
    }

    if (badgeCore) {
      badgeCore.addEventListener('click', () => {
        selectHotspot(6);
      });
    }

    // Sample button click listener
    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: { notes: 'Requested sample kit highlighting UltraShield 360-degree protective shield.' }
        }));
        const modal = document.getElementById('ntw-sample-modal');
        if (modal) {
          modal.classList.add('is-open');
          modal.setAttribute('aria-hidden', 'false');
          document.body.style.overflow = 'hidden';
        } else {
          window.location.href = '/#ntw-sample-request';
        }
      });
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/&lt;/g, '&lt;')
      .replace(/&gt;/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

})();
