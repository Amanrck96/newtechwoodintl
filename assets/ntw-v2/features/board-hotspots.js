/**
 * F7: Board Anatomy Hotspots & Real-Time 3D 360° Technology Model
 * Full WebGL 3D 360-degree interactive UltraShield composite board experience:
 * - Real-time 360° turntable & free orbit inspection (drag to rotate in all directions)
 * - 360° All-Round Protective Shield (co-extruded 4-sided impermeable polymer capping)
 * - Dense Recycled Composite Core (Benefit #7 - 95% Reclaimed Hardwood Sawdust & Polyethylene)
 * - 360° Exploded / Cross-Section View: pulls the outer shield away from the dense core in 3D
 * - Color Customizer in 3D: Teak, Ipe, Walnut, Silver Grey, Charcoal
 * - Preset 3D camera angles: Isometric, Core Cross-Section, Top Grain, Side Grooves
 * - Full interactive fallback to 2D photorealistic diagram with 7 engineering hotspots
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

  const COLOR_PALETTE = {
    tk: { name: 'Peruvian Teak (TK)', hex: '#8c542e', dark: '#522f18', light: '#b06f41' },
    ip: { name: 'Brazilian Ipe (IP)', hex: '#543d2b', dark: '#312217', light: '#73543b' },
    wn: { name: 'Spanish Walnut (WN)', hex: '#423229', dark: '#241a15', light: '#5e483b' },
    si: { name: 'Silver Grey (SI)', hex: '#828385', dark: '#525355', light: '#a6a7a9' },
    ch: { name: 'Hawaiian Charcoal (CH)', hex: '#2f3237', dark: '#181a1d', light: '#464a52' }
  };

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
    let currentViewMode = '3d';    // '3d' or 'diagram'

    mount.innerHTML = `
      <section class="ntw-hotspots-section" id="ntw-hotspots-section" aria-label="UltraShield Board Anatomy and Technology">
        <div class="ntw-hotspots-container">
          
          <div class="ntw-hotspots-header">
            <span class="ntw-hotspots-eyebrow">Anatomy of Innovation</span>
            <h2 class="ntw-hotspots-title">What Makes UltraShield® Different?</h2>
            <p class="ntw-hotspots-subtitle">Experience our interactive 3D 360° co-extruded board model. Inspect the 4-sided polymer capping and dense recycled core from any angle.</p>
          </div>

          <div class="ntw-hotspots-stage">
            
            <div class="ntw-hotspots-diagram-wrap">
              
              <!-- Mode Switcher Tabs -->
              <div class="ntw-stage-mode-switcher" role="tablist" aria-label="Anatomy View Mode">
                <button type="button" class="ntw-stage-mode-btn active" id="ntw-btn-mode-3d" role="tab" aria-selected="true">
                  <svg viewBox="0 0 24 24" class="ntw-btn-icon"><path d="M12 2l9 4.9v10.2L12 22l-9-4.9V6.9L12 2zm0 2.2L5.2 7.9 12 11.6l6.8-3.7L12 4.2zM4.5 9.1v7.6l6.5 3.5v-7.6L4.5 9.1zm15 0l-6.5 3.5v7.6l6.5-3.5V9.1z"/></svg>
                  <span>Interactive 3D 360° Model</span>
                </button>
                <button type="button" class="ntw-stage-mode-btn" id="ntw-btn-mode-diagram" role="tab" aria-selected="false">
                  <svg viewBox="0 0 24 24" class="ntw-btn-icon"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-8 14H7v-2h4v2zm6-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
                  <span>Hotspot Diagram</span>
                </button>
              </div>

              <!-- VIEW 1: Interactive 3D 360 WebGL Model -->
              <div class="ntw-3d-model-stage active" id="ntw-3d-stage">
                
                <div class="ntw-3d-canvas-wrap">
                  <canvas id="ntw-3d-board-canvas" class="ntw-3d-board-canvas" aria-label="Interactive 3D 360 model of UltraShield board"></canvas>
                  <div class="ntw-3d-loader" id="ntw-3d-loader">
                    <div class="ntw-3d-spinner"></div>
                    <span>Initializing 3D 360° Model...</span>
                  </div>
                </div>

                <!-- Top 3D Control Bar -->
                <div class="ntw-3d-top-bar">
                  <div class="ntw-3d-badge-pill">
                    <span class="ntw-360-live-dot"></span>
                    <span>360° REAL 3D MODEL</span>
                  </div>
                  <div class="ntw-3d-action-group">
                    <button type="button" class="ntw-3d-tool-btn" id="ntw-3d-btn-explode" title="Toggle 360° Exploded Cross-Section View">
                      <svg viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>
                      <span id="ntw-3d-explode-text">Explode / Cross-Section</span>
                    </button>
                    <button type="button" class="ntw-3d-tool-btn active" id="ntw-3d-btn-autorotate" title="Toggle 360° Auto-Rotation">
                      <svg viewBox="0 0 24 24"><path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/></svg>
                      <span>Auto-Rotate</span>
                    </button>
                    <button type="button" class="ntw-3d-tool-btn" id="ntw-3d-btn-reset" title="Reset 3D Perspective">
                      <svg viewBox="0 0 24 24"><path d="M17.65 6.35A7.958 7.958 0 0 0 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08A5.99 5.99 0 0 1 12 18c-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg>
                      <span>Reset</span>
                    </button>
                  </div>
                </div>

                <!-- Floating Exploded Annotations (Triggered in exploded mode) -->
                <div class="ntw-3d-callout-overlay" id="ntw-3d-callout-overlay">
                  <div class="ntw-3d-callout-item callout-shield-top">
                    <span class="ntw-callout-tag">OUTER SHIELD</span>
                    <strong>360° Polymer Capping</strong>
                    <small>100% 4-sided impermeable Surlyn barrier</small>
                  </div>
                  <div class="ntw-3d-callout-item callout-core-center">
                    <span class="ntw-callout-tag">95% RECYCLED</span>
                    <strong>Dense Recycled Composite Core</strong>
                    <small>Reclaimed Hardwood Sawdust &amp; Recycled HDPE</small>
                  </div>
                </div>

                <!-- Bottom 3D Angle & Color Controls -->
                <div class="ntw-3d-bottom-bar">
                  <div class="ntw-3d-presets-row">
                    <span class="ntw-3d-bar-label">Views:</span>
                    <button type="button" class="ntw-3d-preset-btn active" data-angle="iso">3D Isometric</button>
                    <button type="button" class="ntw-3d-preset-btn" data-angle="core">Core Cross-Section</button>
                    <button type="button" class="ntw-3d-preset-btn" data-angle="top">Top Grain</button>
                    <button type="button" class="ntw-3d-preset-btn" data-angle="groove">Side Groove</button>
                  </div>

                  <div class="ntw-3d-colors-row">
                    <span class="ntw-3d-bar-label">Color:</span>
                    <div class="ntw-3d-swatches">
                      <button type="button" class="ntw-3d-swatch-chip active" data-color="tk" style="background:#8c542e;" title="Peruvian Teak"></button>
                      <button type="button" class="ntw-3d-swatch-chip" data-color="ip" style="background:#543d2b;" title="Brazilian Ipe"></button>
                      <button type="button" class="ntw-3d-swatch-chip" data-color="wn" style="background:#423229;" title="Spanish Walnut"></button>
                      <button type="button" class="ntw-3d-swatch-chip" data-color="si" style="background:#828385;" title="Silver Grey"></button>
                      <button type="button" class="ntw-3d-swatch-chip" data-color="ch" style="background:#2f3237;" title="Hawaiian Charcoal"></button>
                    </div>
                    <span class="ntw-3d-active-color-name" id="ntw-3d-color-name">Peruvian Teak (TK)</span>
                  </div>
                </div>

                <!-- Drag interaction hint -->
                <div class="ntw-3d-hint">
                  <span>👆 Click and drag 360° to rotate in 3D &bull; Scroll to zoom</span>
                </div>

              </div>

              <!-- VIEW 2: 2D Hotspots Diagram (Fallback & Detailed Hotspot Pins) -->
              <div class="ntw-hotspots-image-container" id="ntw-diagram-stage">
                
                <!-- 360 Shield Aura Highlight -->
                <div class="ntw-360-aura-wrapper active" id="ntw-360-aura" aria-hidden="true">
                  <div class="ntw-360-aura-ring"></div>
                  <div class="ntw-360-tag-pill">
                    <span class="ntw-360-pill-icon">360°</span>
                    <span>FULL 4-SIDED ENCAPSULATION</span>
                  </div>
                </div>

                <!-- Photorealistic 3D Render of UltraShield 360 Board Profile -->
                <img 
                  src="/wp-content/uploads/2026/04/UltraShield-360.png" 
                  alt="NewTechWood UltraShield 360 Co-extruded Composite Board Profile with dense recycled core" 
                  class="ntw-hotspots-board-real-img"
                  width="800"
                  height="523"
                />

                <!-- Left Core Callout Badge (Interactive Button) -->
                <button type="button" class="ntw-callout-badge ntw-callout-core" id="ntw-btn-badge-core" aria-label="Explore Dense Recycled Composite Core">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">DENSE RECYCLED COMPOSITE CORE</span>
                    <span class="ntw-callout-badge-sub">95% Reclaimed Hardwood Fiber &amp; Polyethylene</span>
                  </div>
                </button>

                <!-- Right/Bottom Shield Callout Badge (Interactive Button) -->
                <button type="button" class="ntw-callout-badge ntw-callout-shield active" id="ntw-btn-badge-shield" aria-label="Explore 360° All-Round Protective Shield">
                  <div class="ntw-callout-badge-line"></div>
                  <div class="ntw-callout-badge-content">
                    <span class="ntw-callout-badge-title">360° ALL-ROUND PROTECTIVE SHIELD</span>
                    <span class="ntw-callout-badge-sub">100% Encapsulated Co-Extrusion Outer Capping &bull; Click to Inspect</span>
                  </div>
                </button>

                <!-- Hotspot Pins Positioned Directly on the Board -->
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

            <!-- Right Column: Technical Details & Comparison Tool -->
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

    // Elements
    const btnMode3d = mount.querySelector('#ntw-btn-mode-3d');
    const btnModeDiagram = mount.querySelector('#ntw-btn-mode-diagram');
    const stage3d = mount.querySelector('#ntw-3d-stage');
    const stageDiagram = mount.querySelector('#ntw-diagram-stage');

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

    // View Mode Switching
    function switchViewMode(mode) {
      currentViewMode = mode;
      const is3d = mode === '3d';

      if (btnMode3d) {
        btnMode3d.classList.toggle('active', is3d);
        btnMode3d.setAttribute('aria-selected', is3d ? 'true' : 'false');
      }
      if (btnModeDiagram) {
        btnModeDiagram.classList.toggle('active', !is3d);
        btnModeDiagram.setAttribute('aria-selected', !is3d ? 'true' : 'false');
      }

      if (stage3d) stage3d.classList.toggle('active', is3d);
      if (stageDiagram) stageDiagram.classList.toggle('active', !is3d);

      if (is3d && window.__ntw3DViewer) {
        window.__ntw3DViewer.resize();
      }
    }

    if (btnMode3d) btnMode3d.addEventListener('click', () => switchViewMode('3d'));
    if (btnModeDiagram) btnModeDiagram.addEventListener('click', () => switchViewMode('diagram'));

    // Comparison Mode
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

      // Sync with 3D viewer if active
      if (window.__ntw3DViewer) {
        if (idx === 6) {
          // Benefit #7: Dense Recycled Composite Core (95% Recycled)
          window.__ntw3DViewer.focusCore();
        } else if (idx === 0) {
          // Benefit #1: 360 Shield
          window.__ntw3DViewer.focusShield();
        } else if (idx === 5) {
          // Benefit #6: Wood grain
          window.__ntw3DViewer.setAngle('top');
        }
      }
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
        if (currentViewMode !== 'diagram') switchViewMode('diagram');
      });
    }

    if (badgeCore) {
      badgeCore.addEventListener('click', () => {
        selectHotspot(6);
        if (currentViewMode !== 'diagram') switchViewMode('diagram');
      });
    }

    // Sample button click listener
    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: { notes: 'Requested sample kit highlighting UltraShield 360-degree protective shield & dense recycled core.' }
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

    // Initialize the Three.js 3D WebGL Viewer
    init3DViewer(mount);
  }

  /* --------------------------------------------------------------------------
     Three.js Real-Time 3D 360° Composite Board Engine
     -------------------------------------------------------------------------- */
  function init3DViewer(mount) {
    const canvas = mount.querySelector('#ntw-3d-board-canvas');
    const loader = mount.querySelector('#ntw-3d-loader');
    if (!canvas) return;

    // Load Three.js library dynamically if not present
    loadThreeJs(() => {
      if (!window.THREE) {
        if (loader) loader.innerHTML = '<span>3D View not supported on this browser</span>';
        return;
      }
      buildScene();
    });

    function loadThreeJs(callback) {
      if (window.THREE) {
        callback();
        return;
      }
      const script = document.createElement('script');
      script.src = '/assets/ntw-v2/vendor/three.min.js';
      script.onload = () => callback();
      script.onerror = () => {
        // Fallback to CDN
        const cdnScript = document.createElement('script');
        cdnScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
        cdnScript.onload = () => callback();
        cdnScript.onerror = () => {
          if (loader) loader.innerHTML = '<span>Unable to load 3D engine</span>';
        };
        document.head.appendChild(cdnScript);
      };
      document.head.appendChild(script);
    }

    function buildScene() {
      const THREE = window.THREE;
      if (!THREE) return;

      const wrap = canvas.parentElement;
      const width = wrap.clientWidth || 680;
      const height = wrap.clientHeight || 450;

      // 1. Scene & Camera
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);
      camera.position.set(3.4, 2.2, 4.2);

      // 2. Renderer
      let renderer;
      try {
        renderer = new THREE.WebGLRenderer({
          canvas: canvas,
          antialias: true,
          alpha: true,
          powerPreference: 'high-performance'
        });
      } catch (err) {
        if (loader) loader.innerHTML = '<span>WebGL not supported</span>';
        return;
      }

      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      // Hide loader
      if (loader) loader.style.display = 'none';

      // 3. Lighting
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
      scene.add(ambientLight);

      const sunLight = new THREE.DirectionalLight(0xfff6ea, 0.95);
      sunLight.position.set(5, 8, 5);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 1024;
      sunLight.shadow.mapSize.height = 1024;
      scene.add(sunLight);

      const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.45);
      fillLight.position.set(-5, 4, -4);
      scene.add(fillLight);

      const bottomRimLight = new THREE.DirectionalLight(0xfff5dd, 0.3);
      bottomRimLight.position.set(0, -6, 2);
      scene.add(bottomRimLight);

      // Soft shadow plane
      const shadowPlaneGeo = new THREE.PlaneGeometry(8, 8);
      const shadowPlaneMat = new THREE.ShadowMaterial({ opacity: 0.15 });
      const shadowPlane = new THREE.Mesh(shadowPlaneGeo, shadowPlaneMat);
      shadowPlane.rotation.x = -Math.PI / 2;
      shadowPlane.position.y = -1.1;
      shadowPlane.receiveShadow = true;
      scene.add(shadowPlane);

      // 4. Procedural Textures
      function createWoodGrainCanvas(baseHex, darkHex, lightHex) {
        const c = document.createElement('canvas');
        c.width = 512;
        c.height = 512;
        const ctx = c.getContext('2d');

        // Base gradient
        const bgGrad = ctx.createLinearGradient(0, 0, 512, 0);
        bgGrad.addColorStop(0, darkHex);
        bgGrad.addColorStop(0.5, baseHex);
        bgGrad.addColorStop(1, lightHex);
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, 512, 512);

        // Long woodgrain streaks
        for (let i = 0; i < 48; i++) {
          const y = Math.random() * 512;
          const h = 2 + Math.random() * 8;
          ctx.fillStyle = Math.random() > 0.5 ? darkHex : lightHex;
          ctx.globalAlpha = 0.08 + Math.random() * 0.12;
          ctx.fillRect(0, y, 512, h);
        }

        // Fine grain lines
        for (let i = 0; i < 180; i++) {
          const y = Math.random() * 512;
          ctx.fillStyle = Math.random() > 0.5 ? '#111' : '#fff';
          ctx.globalAlpha = 0.03 + Math.random() * 0.05;
          ctx.fillRect(0, y, 512, 1);
        }

        ctx.globalAlpha = 1.0;
        return c;
      }

      function createCompositeCoreCanvas() {
        const c = document.createElement('canvas');
        c.width = 512;
        c.height = 512;
        const ctx = c.getContext('2d');

        // Dark composite base
        ctx.fillStyle = '#261e18';
        ctx.fillRect(0, 0, 512, 512);

        // 95% Reclaimed hardwood sawdust flecks & polymer granules
        for (let i = 0; i < 2400; i++) {
          const x = Math.random() * 512;
          const y = Math.random() * 512;
          const r = 0.8 + Math.random() * 2.2;
          const tone = Math.random();
          if (tone < 0.45) {
            ctx.fillStyle = '#8a6548'; // Reclaimed hardwood fiber
          } else if (tone < 0.8) {
            ctx.fillStyle = '#bfa588'; // Light sawdust granule
          } else {
            ctx.fillStyle = '#14110f'; // Dense recycled polyethylene
          }
          ctx.beginPath();
          ctx.arc(x, y, r, 0, Math.PI * 2);
          ctx.fill();
        }

        return c;
      }

      // Materials
      let currentKey = 'tk';
      let activeColor = COLOR_PALETTE[currentKey];

      const coreCanvas = createCompositeCoreCanvas();
      const coreTexture = new THREE.CanvasTexture(coreCanvas);
      coreTexture.wrapS = THREE.RepeatWrapping;
      coreTexture.wrapT = THREE.RepeatWrapping;

      const coreMaterial = new THREE.MeshStandardMaterial({
        map: coreTexture,
        roughness: 0.92,
        metalness: 0.05,
        color: 0xffffff
      });

      let woodTexture = new THREE.CanvasTexture(createWoodGrainCanvas(activeColor.hex, activeColor.dark, activeColor.light));
      woodTexture.wrapS = THREE.RepeatWrapping;
      woodTexture.wrapT = THREE.RepeatWrapping;
      woodTexture.repeat.set(1.5, 4);

      const shieldMaterial = new THREE.MeshStandardMaterial({
        map: woodTexture,
        roughness: 0.38,
        metalness: 0.08,
        color: 0xffffff
      });

      // 5. 3D Model Geometry (UltraShield Decking Profile)
      const boardGroup = new THREE.Group();
      scene.add(boardGroup);

      const boardLen = 4.8;
      const boardWidth = 1.48;
      const boardThick = 0.24;

      // Inner Dense Recycled Composite Core
      const coreGeo = new THREE.BoxGeometry(boardWidth - 0.07, boardThick - 0.06, boardLen - 0.02);
      const coreMesh = new THREE.Mesh(coreGeo, coreMaterial);
      coreMesh.castShadow = true;
      coreMesh.receiveShadow = true;
      boardGroup.add(coreMesh);

      // Outer 360 Protective Shield Shells (Top, Bottom, Left Groove, Right Groove)
      const shieldGroup = new THREE.Group();
      boardGroup.add(shieldGroup);

      // Top Shield (Wood grain finished)
      const topShieldGeo = new THREE.BoxGeometry(boardWidth, 0.03, boardLen);
      const topShieldMesh = new THREE.Mesh(topShieldGeo, shieldMaterial);
      topShieldMesh.position.y = (boardThick / 2) - 0.015;
      topShieldMesh.castShadow = true;
      shieldGroup.add(topShieldMesh);

      // Bottom Shield (360 Capping encapsulation)
      const botShieldGeo = new THREE.BoxGeometry(boardWidth, 0.03, boardLen);
      const botShieldMesh = new THREE.Mesh(botShieldGeo, shieldMaterial);
      botShieldMesh.position.y = -((boardThick / 2) - 0.015);
      botShieldMesh.castShadow = true;
      shieldGroup.add(botShieldMesh);

      // Left Side Cap with hidden fastener groove channel
      const leftShieldGeo = new THREE.BoxGeometry(0.04, boardThick, boardLen);
      const leftShieldMesh = new THREE.Mesh(leftShieldGeo, shieldMaterial);
      leftShieldMesh.position.x = -((boardWidth / 2) - 0.02);
      leftShieldMesh.castShadow = true;
      shieldGroup.add(leftShieldMesh);

      // Right Side Cap with hidden fastener groove channel
      const rightShieldGeo = new THREE.BoxGeometry(0.04, boardThick, boardLen);
      const rightShieldMesh = new THREE.Mesh(rightShieldGeo, shieldMaterial);
      rightShieldMesh.position.x = ((boardWidth / 2) - 0.02);
      rightShieldMesh.castShadow = true;
      shieldGroup.add(rightShieldMesh);

      // 6. Interactive States & Controls
      let isExploded = false;
      let explodeFactor = 0; // 0 = assembled, 1 = exploded
      let isAutoRotating = true;
      let isDragging = false;
      let prevMousePos = { x: 0, y: 0 };
      let rotationVelocity = { x: 0, y: 0.005 };

      // Target camera for smooth interpolation
      let targetCamPos = camera.position.clone();
      let targetBoardRot = boardGroup.rotation.clone();

      // Explode Button
      const explodeBtn = mount.querySelector('#ntw-3d-btn-explode');
      const explodeText = mount.querySelector('#ntw-3d-explode-text');
      const calloutOverlay = mount.querySelector('#ntw-3d-callout-overlay');

      function toggleExplode() {
        isExploded = !isExploded;
        if (explodeBtn) explodeBtn.classList.toggle('active', isExploded);
        if (explodeText) explodeText.textContent = isExploded ? 'Re-Assemble Board' : 'Explode / Cross-Section';
        if (calloutOverlay) calloutOverlay.classList.toggle('visible', isExploded);

        // Highlight core when exploded
        if (isExploded) {
          selectHotspot(6); // Benefit #7: Dense Recycled Composite Core
        }
      }

      if (explodeBtn) explodeBtn.addEventListener('click', toggleExplode);

      // Auto-Rotate Toggle
      const autoRotateBtn = mount.querySelector('#ntw-3d-btn-autorotate');
      if (autoRotateBtn) {
        autoRotateBtn.addEventListener('click', () => {
          isAutoRotating = !isAutoRotating;
          autoRotateBtn.classList.toggle('active', isAutoRotating);
        });
      }

      // Reset Button
      const resetBtn = mount.querySelector('#ntw-3d-btn-reset');
      if (resetBtn) {
        resetBtn.addEventListener('click', () => {
          isExploded = false;
          if (explodeBtn) explodeBtn.classList.remove('active');
          if (explodeText) explodeText.textContent = 'Explode / Cross-Section';
          if (calloutOverlay) calloutOverlay.classList.remove('visible');
          targetCamPos.set(3.4, 2.2, 4.2);
          targetBoardRot.set(0, 0.4, 0);
          isAutoRotating = true;
          if (autoRotateBtn) autoRotateBtn.classList.add('active');
        });
      }

      // Preset Angles
      const presetBtns = mount.querySelectorAll('.ntw-3d-preset-btn');
      presetBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          presetBtns.forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          const angle = btn.getAttribute('data-angle');
          setAngle(angle);
        });
      });

      function setAngle(angle) {
        isAutoRotating = false;
        if (autoRotateBtn) autoRotateBtn.classList.remove('active');

        if (angle === 'iso') {
          targetCamPos.set(3.4, 2.2, 4.2);
          targetBoardRot.set(0, 0.45, 0);
        } else if (angle === 'core') {
          // Focus directly on the 95% recycled core cross-section at the end of the board
          targetCamPos.set(0.2, 0.4, 4.4);
          targetBoardRot.set(0.05, 0.05, 0);
        } else if (angle === 'top') {
          // Focus top-down on natural hardwood grain
          targetCamPos.set(0, 4.5, 0.2);
          targetBoardRot.set(0, 0, 0);
        } else if (angle === 'groove') {
          // Focus directly on the hidden clip side groove
          targetCamPos.set(3.8, 0.2, 0.2);
          targetBoardRot.set(0, Math.PI / 2, 0);
        }
      }

      // Color Swatches
      const swatchBtns = mount.querySelectorAll('.ntw-3d-swatch-chip');
      const colorNameEl = mount.querySelector('#ntw-3d-color-name');

      swatchBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
          swatchBtns.forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          const colorKey = btn.getAttribute('data-color');
          setColor(colorKey);
        });
      });

      function setColor(key) {
        const pal = COLOR_PALETTE[key];
        if (!pal) return;
        currentKey = key;
        activeColor = pal;

        if (colorNameEl) colorNameEl.textContent = pal.name;

        // Generate updated woodgrain texture
        const updatedCanvas = createWoodGrainCanvas(pal.hex, pal.dark, pal.light);
        if (shieldMaterial.map) shieldMaterial.map.dispose();
        const newTex = new THREE.CanvasTexture(updatedCanvas);
        newTex.wrapS = THREE.RepeatWrapping;
        newTex.wrapT = THREE.RepeatWrapping;
        newTex.repeat.set(1.5, 4);
        shieldMaterial.map = newTex;
        shieldMaterial.needsUpdate = true;
      }

      // 7. Mouse & Touch Drag Interaction
      canvas.addEventListener('pointerdown', (e) => {
        isDragging = true;
        prevMousePos = { x: e.clientX, y: e.clientY };
        canvas.setPointerCapture(e.pointerId);
      });

      window.addEventListener('pointermove', (e) => {
        if (!isDragging) return;
        const deltaX = e.clientX - prevMousePos.x;
        const deltaY = e.clientY - prevMousePos.y;

        boardGroup.rotation.y += deltaX * 0.01;
        boardGroup.rotation.x += deltaY * 0.008;

        // Clamp vertical tilt
        boardGroup.rotation.x = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, boardGroup.rotation.x));

        targetBoardRot.copy(boardGroup.rotation);
        rotationVelocity = { x: deltaY * 0.002, y: deltaX * 0.003 };
        prevMousePos = { x: e.clientX, y: e.clientY };
      });

      window.addEventListener('pointerup', (e) => {
        isDragging = false;
        try {
          if (canvas.hasPointerCapture(e.pointerId)) {
            canvas.releasePointerCapture(e.pointerId);
          }
        } catch (_) {}
      });

      // Mouse Wheel Zoom
      canvas.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomDelta = e.deltaY * 0.003;
        targetCamPos.z = Math.max(2.2, Math.min(6.5, targetCamPos.z + zoomDelta));
        targetCamPos.y = Math.max(1.0, Math.min(4.5, targetCamPos.y + (zoomDelta * 0.4)));
      }, { passive: false });

      // Window Resize Handler
      function handleResize() {
        const newWidth = wrap.clientWidth || 680;
        const newHeight = wrap.clientHeight || 450;
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(newWidth, newHeight);
      }

      window.addEventListener('resize', handleResize);

      // 8. 60FPS Render & Animation Loop
      let animId;
      function animate() {
        animId = requestAnimationFrame(animate);

        // Smooth camera lerp
        camera.position.lerp(targetCamPos, 0.08);
        camera.lookAt(0, 0, 0);

        // Explode animation lerp
        const targetExplode = isExploded ? 1 : 0;
        explodeFactor += (targetExplode - explodeFactor) * 0.09;

        // Apply exploded displacement
        topShieldMesh.position.y = ((boardThick / 2) - 0.015) + (explodeFactor * 0.38);
        botShieldMesh.position.y = -((boardThick / 2) - 0.015) - (explodeFactor * 0.38);
        leftShieldMesh.position.x = -((boardWidth / 2) - 0.02) - (explodeFactor * 0.45);
        rightShieldMesh.position.x = ((boardWidth / 2) - 0.02) + (explodeFactor * 0.45);

        // Auto-rotation when idle
        if (isAutoRotating && !isDragging) {
          boardGroup.rotation.y += 0.0045;
          targetBoardRot.y = boardGroup.rotation.y;
        }

        renderer.render(scene, camera);
      }

      animate();

      // Expose public API for external triggers (like Benefit cards)
      window.__ntw3DViewer = {
        resize: handleResize,
        setAngle: setAngle,
        setColor: setColor,
        toggleExplode: toggleExplode,
        focusCore: function () {
          setAngle('core');
          if (!isExploded) toggleExplode();
        },
        focusShield: function () {
          setAngle('iso');
          if (isExploded) toggleExplode();
        }
      };
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
