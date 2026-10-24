/**
 * F11: Material BOQ & Quantity Estimator
 * Technical estimator for board/plank counts, clips, and wastage.
 * Strictly architectural material take-off. Zero pricing or cost figures.
 */

(function () {
  'use strict';

  const PROFILES = {
    'decking-138': {
      name: 'UltraShield Decking (138 × 23 × 2900 mm)',
      type: 'decking',
      widthMm: 138,
      lengthMm: 2900,
      areaSqM: 0.4002, // 0.138 * 2.9
      clipsPerSqM: 22,
      joistSpacing: '350mm to 400mm c/c'
    },
    'decking-140': {
      name: 'UltraShield Commercial Decking (140 × 25 × 2900 mm)',
      type: 'decking',
      widthMm: 140,
      lengthMm: 2900,
      areaSqM: 0.406, // 0.140 * 2.9
      clipsPerSqM: 20,
      joistSpacing: '300mm to 350mm c/c'
    },
    'cladding-castellated': {
      name: 'UltraShield Castellated Cladding (142 × 13 × 2900 mm)',
      type: 'cladding',
      widthMm: 142,
      lengthMm: 2900,
      areaSqM: 0.4118, // 0.142 * 2.9
      clipsPerSqM: 16,
      joistSpacing: '400mm to 500mm batten spacing'
    },
    'cladding-shiplap': {
      name: 'UltraShield Shiplap Cladding (142 × 13 × 2900 mm)',
      type: 'cladding',
      widthMm: 142,
      lengthMm: 2900,
      areaSqM: 0.4118,
      clipsPerSqM: 16,
      joistSpacing: '400mm to 500mm batten spacing'
    },
    'tiles-300': {
      name: 'QuickDeck DIY Deck Tiles (300 × 300 mm)',
      type: 'tiles',
      widthMm: 300,
      lengthMm: 300,
      areaSqM: 0.09,
      clipsPerSqM: 0,
      joistSpacing: 'Self-supporting interlocking base (no joists needed)'
    }
  };

  const SQM_TO_SQFT = 10.7639;

  let currentUnit = 'sqft'; // 'sqft' | 'sqm'
  let currentWastage = 0.10; // 10% default

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCalculator);
  } else {
    initCalculator();
  }

  function initCalculator() {
    let mount = document.getElementById('ntw-material-calculator');
    if (!mount) {
      const anchor = document.getElementById('ntw-board-hotspots') || document.getElementById('ntw-sample-request');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-material-calculator';
      anchor.parentNode.insertBefore(mount, anchor.nextSibling);
    }

    mount.innerHTML = `
      <section class="ntw-boq-section" aria-label="Material BOQ Estimator">
        <div class="ntw-boq-container">
          
          <div class="ntw-boq-header">
            <span class="ntw-boq-eyebrow">Architectural Planning Tool</span>
            <h2 class="ntw-boq-title">Material BOQ &amp; Quantity Estimator</h2>
            <p class="ntw-boq-subtitle">
              Calculate the exact number of UltraShield planks, fasteners, and substructure requirements based on your project dimensions.
            </p>
          </div>

          <div class="ntw-boq-grid">
            
            <!-- Controls Form -->
            <div class="ntw-boq-form">
              
              <div class="ntw-boq-group">
                <label class="ntw-boq-label" for="ntw-boq-profile">Select Product Profile</label>
                <select id="ntw-boq-profile" class="ntw-boq-select">
                  <option value="decking-138">UltraShield Decking (138 × 23 × 2900 mm)</option>
                  <option value="decking-140">UltraShield Commercial Decking (140 × 25 × 2900 mm)</option>
                  <option value="cladding-castellated">UltraShield Castellated Cladding (142 × 13 × 2900 mm)</option>
                  <option value="cladding-shiplap">UltraShield Shiplap Cladding (142 × 13 × 2900 mm)</option>
                  <option value="tiles-300">QuickDeck DIY Deck Tiles (300 × 300 mm)</option>
                </select>
              </div>

              <div class="ntw-boq-group">
                <div class="ntw-boq-label">
                  <span id="ntw-area-label-text">Total Area (sq ft)</span>
                  <div class="ntw-unit-toggle">
                    <button type="button" class="ntw-unit-btn active" data-unit="sqft" id="ntw-unit-sqft">Sq Ft</button>
                    <button type="button" class="ntw-unit-btn" data-unit="sqm" id="ntw-unit-sqm">Sq M</button>
                  </div>
                </div>
                <input type="number" id="ntw-boq-area-input" class="ntw-boq-input" value="350" min="10" max="50000" step="5" />
              </div>

              <div class="ntw-boq-group">
                <label class="ntw-boq-label">Installation Wastage Allowance</label>
                <div class="ntw-wastage-chips">
                  <button type="button" class="ntw-wastage-btn" data-wastage="0.05">
                    <span class="ntw-wastage-pct">5%</span>
                    <span class="ntw-wastage-note">Straight run</span>
                  </button>
                  <button type="button" class="ntw-wastage-btn active" data-wastage="0.10">
                    <span class="ntw-wastage-pct">10%</span>
                    <span class="ntw-wastage-note">Standard (Rec.)</span>
                  </button>
                  <button type="button" class="ntw-wastage-btn" data-wastage="0.15">
                    <span class="ntw-wastage-pct">15%</span>
                    <span class="ntw-wastage-note">Diagonal / Steps</span>
                  </button>
                </div>
              </div>

            </div>

            <!-- Results Output -->
            <div class="ntw-boq-results">
              <div>
                <div class="ntw-boq-results-title">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>
                  <span>Estimated Bill of Quantities (BOQ)</span>
                </div>

                <div class="ntw-boq-metrics">
                  <div class="ntw-boq-metric-card">
                    <div class="ntw-boq-metric-label">Estimated Planks</div>
                    <div class="ntw-boq-metric-val" id="ntw-metric-planks">89 <span class="ntw-boq-metric-unit">pcs</span></div>
                  </div>
                  <div class="ntw-boq-metric-card">
                    <div class="ntw-boq-metric-label">Hidden Clips / Fasteners</div>
                    <div class="ntw-boq-metric-val" id="ntw-metric-clips">720 <span class="ntw-boq-metric-unit">clips</span></div>
                  </div>
                  <div class="ntw-boq-metric-card">
                    <div class="ntw-boq-metric-label">Gross Coverage Area</div>
                    <div class="ntw-boq-metric-val" id="ntw-metric-gross">385 <span class="ntw-boq-metric-unit">sq ft</span></div>
                  </div>
                  <div class="ntw-boq-metric-card">
                    <div class="ntw-boq-metric-label">Substructure Joist Spacing</div>
                    <div class="ntw-boq-metric-val" id="ntw-metric-joists" style="font-size: 15px; font-weight: 700; padding-top: 6px;">400mm c/c</div>
                  </div>
                </div>

                <div class="ntw-boq-specs" id="ntw-boq-specs-note">
                  UltraShield boards feature 360° polymer capping. Substructure recommendation: Aluminium or composite joists at <strong>350–400 mm</strong> centre-to-centre spacing with starter clips at perimeter.
                </div>
              </div>

              <button type="button" class="ntw-boq-transfer-btn" id="ntw-boq-transfer-btn">
                <span>Transfer BOQ to Sample / Quote Request</span>
                <svg viewBox="0 0 24 24"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
              </button>

            </div>

          </div>

        </div>
      </section>
    `;

    bindEvents();
    recalculate();
  }

  function bindEvents() {
    const profileSelect = document.getElementById('ntw-boq-profile');
    const areaInput = document.getElementById('ntw-boq-area-input');
    const sqftBtn = document.getElementById('ntw-unit-sqft');
    const sqmBtn = document.getElementById('ntw-unit-sqm');
    const wastageBtns = document.querySelectorAll('.ntw-wastage-btn');
    const transferBtn = document.getElementById('ntw-boq-transfer-btn');

    if (profileSelect) profileSelect.addEventListener('change', recalculate);
    if (areaInput) {
      areaInput.addEventListener('input', recalculate);
      areaInput.addEventListener('change', recalculate);
    }

    if (sqftBtn && sqmBtn) {
      sqftBtn.addEventListener('click', () => {
        if (currentUnit === 'sqft') return;
        currentUnit = 'sqft';
        sqftBtn.classList.add('active');
        sqmBtn.classList.remove('active');
        document.getElementById('ntw-area-label-text').textContent = 'Total Area (sq ft)';
        // Convert current sqm value to sqft
        const currentVal = parseFloat(areaInput.value) || 0;
        areaInput.value = Math.round(currentVal * SQM_TO_SQFT);
        recalculate();
      });

      sqmBtn.addEventListener('click', () => {
        if (currentUnit === 'sqm') return;
        currentUnit = 'sqm';
        sqmBtn.classList.add('active');
        sqftBtn.classList.remove('active');
        document.getElementById('ntw-area-label-text').textContent = 'Total Area (sq m)';
        // Convert current sqft value to sqm
        const currentVal = parseFloat(areaInput.value) || 0;
        areaInput.value = Math.round(currentVal / SQM_TO_SQFT);
        recalculate();
      });
    }

    wastageBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        wastageBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentWastage = parseFloat(btn.getAttribute('data-wastage')) || 0.10;
        recalculate();
      });
    });

    if (transferBtn) {
      transferBtn.addEventListener('click', () => {
        const profileKey = (profileSelect || {}).value || 'decking-138';
        const profile = PROFILES[profileKey];
        const area = (areaInput || {}).value || '350';
        const planks = (document.getElementById('ntw-metric-planks') || {}).textContent || '';
        const clips = (document.getElementById('ntw-metric-clips') || {}).textContent || '';

        const boqNotes = `Calculated BOQ: ${area} ${currentUnit} of ${profile.name}. Quantity: ${planks}, Fasteners: ${clips}.`;

        // Map to sample product series
        let series = 'UltraShield Decking';
        if (profile.type === 'cladding') series = 'UltraShield Wall Cladding';
        else if (profile.type === 'tiles') series = 'DIY Deck Tiles';

        // Dispatch open sample modal
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: {
            product: series,
            notes: boqNotes
          }
        }));

        // Scroll to modal / open
        const modal = document.getElementById('ntw-sample-modal');
        if (modal) {
          const notesField = document.getElementById('ntw-input-address');
          if (notesField && !notesField.value) {
            notesField.value = boqNotes;
          }
          const productSelect = document.getElementById('ntw-select-product');
          if (productSelect) {
            for (let i = 0; i < productSelect.options.length; i++) {
              if (productSelect.options[i].value.includes(series)) {
                productSelect.selectedIndex = i;
                break;
              }
            }
          }
        }
      });
    }
  }

  function recalculate() {
    const profileSelect = document.getElementById('ntw-boq-profile');
    const areaInput = document.getElementById('ntw-boq-area-input');
    if (!profileSelect || !areaInput) return;

    const profileKey = profileSelect.value;
    const profile = PROFILES[profileKey] || PROFILES['decking-138'];

    const rawArea = Math.max(1, parseFloat(areaInput.value) || 0);

    // Normalize area to sq metres for calculation
    const areaSqM = (currentUnit === 'sqm') ? rawArea : (rawArea / SQM_TO_SQFT);
    const grossAreaSqM = areaSqM * (1 + currentWastage);
    const grossAreaDisplay = (currentUnit === 'sqm') ? Math.round(grossAreaSqM) : Math.round(grossAreaSqM * SQM_TO_SQFT);

    // Number of planks = ceil(grossAreaSqM / profile.areaSqM)
    const planks = Math.ceil(grossAreaSqM / profile.areaSqM);

    // Fastener clips = round(areaSqM * profile.clipsPerSqM)
    const clips = (profile.clipsPerSqM > 0) ? Math.round(grossAreaSqM * profile.clipsPerSqM) : 0;

    // Update DOM
    const metricPlanks = document.getElementById('ntw-metric-planks');
    const metricClips = document.getElementById('ntw-metric-clips');
    const metricGross = document.getElementById('ntw-metric-gross');
    const metricJoists = document.getElementById('ntw-metric-joists');
    const specsNote = document.getElementById('ntw-boq-specs-note');

    if (metricPlanks) {
      metricPlanks.innerHTML = `${planks} <span class="ntw-boq-metric-unit">${profile.type === 'tiles' ? 'tiles' : 'boards'}</span>`;
    }
    if (metricClips) {
      metricClips.innerHTML = (clips > 0)
        ? `${clips} <span class="ntw-boq-metric-unit">clips</span>`
        : `None <span class="ntw-boq-metric-unit">interlocking</span>`;
    }
    if (metricGross) {
      metricGross.innerHTML = `${grossAreaDisplay} <span class="ntw-boq-metric-unit">${currentUnit === 'sqm' ? 'sq m' : 'sq ft'}</span>`;
    }
    if (metricJoists) {
      metricJoists.textContent = profile.joistSpacing;
    }
    if (specsNote) {
      specsNote.innerHTML = `Board Dimensions: <strong>${profile.widthMm}mm × 2900mm</strong>. Substructure: <strong>${profile.joistSpacing}</strong>. Includes ${(currentWastage * 100).toFixed(0)}% allowance for end trimming and cutoffs.`;
    }
  }
})();
