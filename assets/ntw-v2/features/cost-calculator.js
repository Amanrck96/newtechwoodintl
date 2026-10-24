/**
 * F2: Wood vs Composite Cost Calculator
 * Interactive client-side comparison with Indian currency formatting.
 */

/* ==========================================================================
   CONFIG OBJECT (PRESETS) — TODO-VERIFY: Real values to be verified by user
   ========================================================================== */
const NTW_CALCULATOR_CONFIG = { // TODO-VERIFY
  presets: [
    { id: 'compact', label: 'Balcony / Compact Deck', yearlyCost: 15000 }, // TODO-VERIFY: ₹15,000/yr
    { id: 'standard', label: 'Standard Villa Terrace', yearlyCost: 35000 }, // TODO-VERIFY: ₹35,000/yr
    { id: 'luxury', label: 'Resort / Large Pool Deck', yearlyCost: 85000 }  // TODO-VERIFY: ₹85,000/yr
  ],
  defaultYears: 10,
  minYears: 1,
  maxYears: 25,
  defaultPresetIndex: 1,
  woodChores: [
    'Annual sanding & surface prep',
    'Chemical power washing & mold removal',
    'Seasonal sealing, staining & recoating',
    'Splinter, termite & rot board replacement'
  ],
  compositeBenefits: [
    'Zero sanding, painting, or oil staining',
    'Shielded all 4 sides against moisture & termites',
    'Simple routine wash with water and mild soap',
    'Backed by a 25-Year Limited Residential Warranty'
  ]
};

(function () {
  'use strict';

  // Indian currency formatting helper: e.g., 6750 -> "6,750", 125000 -> "1,25,000"
  function formatINR(amount) {
    if (isNaN(amount) || amount === null) return '₹0';
    const num = Math.round(Number(amount));
    return '₹' + num.toLocaleString('en-IN');
  }

  function initCalculator() {
    const mount = document.getElementById('ntw-cost-calculator');
    if (!mount) return;

    let selectedYearlyCost = NTW_CALCULATOR_CONFIG.presets[NTW_CALCULATOR_CONFIG.defaultPresetIndex].yearlyCost;
    let selectedYears = NTW_CALCULATOR_CONFIG.defaultYears;
    let isCustom = false;

    // Render Markup
    mount.innerHTML = `
      <section class="ntw-calculator-section" aria-label="Deck Cost Calculator">
        <div class="ntw-calc-container">
          
          <div class="ntw-calc-header">
            <div class="ntw-calc-eyebrow">Cost & Maintenance Comparison</div>
            <h2 class="ntw-calc-title">Real Wood vs NewTechWood UltraShield</h2>
            <p class="ntw-calc-subtitle">See how ongoing maintenance, staining, and repair costs accumulate over time.</p>
          </div>

          <!-- Question Box -->
          <div class="ntw-calc-question-box">
            <div class="ntw-calc-question" id="ntw-calc-q-label">What does keeping a wood deck up cost you each year?</div>
            
            <div class="ntw-calc-presets" role="radiogroup" aria-labelledby="ntw-calc-q-label">
              ${NTW_CALCULATOR_CONFIG.presets.map((p, idx) => `
                <button 
                  type="button" 
                  class="ntw-calc-preset-btn ${idx === NTW_CALCULATOR_CONFIG.defaultPresetIndex ? 'active' : ''}" 
                  data-cost="${p.yearlyCost}"
                  role="radio"
                  aria-checked="${idx === NTW_CALCULATOR_CONFIG.defaultPresetIndex ? 'true' : 'false'}"
                >
                  <span class="ntw-calc-preset-label">${escapeHtml(p.label)}</span>
                  <span class="ntw-calc-preset-val">${formatINR(p.yearlyCost)} <small style="font-size:12px;font-weight:400;color:#6b7280;">/yr</small></span>
                </button>
              `).join('')}

              <button 
                type="button" 
                class="ntw-calc-preset-btn" 
                id="ntw-calc-custom-toggle"
                role="radio"
                aria-checked="false"
              >
                <span class="ntw-calc-preset-label">Custom Estimate</span>
                <span class="ntw-calc-preset-val">Use my own number &rarr;</span>
              </button>
            </div>

            <!-- Custom Input Row -->
            <div class="ntw-calc-custom-wrap" id="ntw-calc-custom-wrap">
              <label for="ntw-calc-custom-val" class="ntw-calc-custom-label">Enter your estimated yearly upkeep in INR:</label>
              <div class="ntw-calc-custom-input-box">
                <span class="ntw-calc-custom-prefix">₹</span>
                <input 
                  type="number" 
                  id="ntw-calc-custom-val" 
                  class="ntw-calc-custom-input" 
                  placeholder="e.g. 45000" 
                  min="100" 
                  max="10000000" 
                  step="500" 
                />
              </div>
            </div>
          </div>

          <!-- Slider Section -->
          <div class="ntw-calc-slider-box">
            <div class="ntw-calc-slider-header">
              <span class="ntw-calc-slider-label">Duration of Ownership:</span>
              <span class="ntw-calc-slider-current" id="ntw-calc-years-display">${selectedYears} Years</span>
            </div>

            <input 
              type="range" 
              id="ntw-calc-years-slider" 
              class="ntw-calc-range" 
              min="${NTW_CALCULATOR_CONFIG.minYears}" 
              max="${NTW_CALCULATOR_CONFIG.maxYears}" 
              value="${selectedYears}" 
              aria-label="Years of deck ownership"
            />

            <div class="ntw-calc-ticks">
              <span class="ntw-calc-tick">1 Year</span>
              <span class="ntw-calc-tick">5 Years</span>
              <span class="ntw-calc-tick">10 Years</span>
              <span class="ntw-calc-tick">15 Years</span>
              <span class="ntw-calc-tick">20 Years</span>
              <span class="ntw-calc-tick">25 Years</span>
            </div>
          </div>

          <!-- Two Result Columns -->
          <div class="ntw-calc-results" aria-live="polite">
            
            <!-- Real Wood Column -->
            <div class="ntw-calc-card ntw-calc-card-wood">
              <div class="ntw-calc-card-header">
                <div class="ntw-calc-card-title">Traditional Wood</div>
                <span class="ntw-calc-tag-wood">High Maintenance</span>
              </div>
              
              <div class="ntw-calc-stat-block">
                <div class="ntw-calc-stat-label">Estimated Total Maintenance Spend:</div>
                <div class="ntw-calc-stat-number ntw-calc-stat-number-wood" id="ntw-wood-total-cost">₹0</div>
              </div>

              <div class="ntw-calc-weekends" id="ntw-wood-weekends">⏳ Upkeep Time Lost: ~${selectedYears} weekends</div>

              <ul class="ntw-calc-chore-list">
                ${NTW_CALCULATOR_CONFIG.woodChores.map(c => `
                  <li class="ntw-calc-chore-item">
                    <svg class="ntw-calc-chore-icon" fill="#b91c1c" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                    <span>${escapeHtml(c)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

            <!-- UltraShield Column -->
            <div class="ntw-calc-card ntw-calc-card-composite">
              <div class="ntw-calc-card-header">
                <div class="ntw-calc-card-title">NewTechWood UltraShield</div>
                <span class="ntw-calc-tag-composite">Zero Upkeep</span>
              </div>

              <div class="ntw-calc-stat-block">
                <div class="ntw-calc-stat-label">Routine Maintenance Cost:</div>
                <div class="ntw-calc-stat-number ntw-calc-stat-number-composite">₹0</div>
              </div>

              <div class="ntw-calc-weekends">✨ Upkeep Time: 0 weekends ("rinse with soap &amp; water")</div>

              <ul class="ntw-calc-chore-list">
                ${NTW_CALCULATOR_CONFIG.compositeBenefits.map(b => `
                  <li class="ntw-calc-chore-item">
                    <svg class="ntw-calc-chore-icon" fill="#c9a84c" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
                    <span>${escapeHtml(b)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>

          </div>

          <p class="ntw-calc-disclaimer">
            * Disclaimer: This is your own estimate, not a quote or a NewTechWood figure. Actual costs vary based on deck dimensions, environment, and regional labor rates.
          </p>

        </div>
      </section>
    `;

    // Elements
    const presetButtons = mount.querySelectorAll('.ntw-calc-preset-btn[data-cost]');
    const customToggleBtn = document.getElementById('ntw-calc-custom-toggle');
    const customWrap = document.getElementById('ntw-calc-custom-wrap');
    const customInput = document.getElementById('ntw-calc-custom-val');
    const slider = document.getElementById('ntw-calc-years-slider');
    const yearsDisplay = document.getElementById('ntw-calc-years-display');
    const woodTotalCostEl = document.getElementById('ntw-wood-total-cost');
    const woodWeekendsEl = document.getElementById('ntw-wood-weekends');

    function calculate() {
      const total = selectedYearlyCost * selectedYears;
      woodTotalCostEl.textContent = formatINR(total);
      woodWeekendsEl.textContent = `⏳ Upkeep Time Lost: ~${selectedYears} ${selectedYears === 1 ? 'weekend' : 'weekends'}`;
      yearsDisplay.textContent = `${selectedYears} ${selectedYears === 1 ? 'Year' : 'Years'}`;
    }

    // Preset Clicks
    presetButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        presetButtons.forEach(b => {
          b.classList.remove('active');
          b.setAttribute('aria-checked', 'false');
        });
        customToggleBtn.classList.remove('active');
        customToggleBtn.setAttribute('aria-checked', 'false');
        customWrap.classList.remove('active');

        btn.classList.add('active');
        btn.setAttribute('aria-checked', 'true');
        selectedYearlyCost = Number(btn.getAttribute('data-cost'));
        isCustom = false;
        calculate();
      });
    });

    // Custom Input Toggle
    customToggleBtn.addEventListener('click', () => {
      presetButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-checked', 'false');
      });
      customToggleBtn.classList.add('active');
      customToggleBtn.setAttribute('aria-checked', 'true');
      customWrap.classList.add('active');
      isCustom = true;
      if (customInput.value && Number(customInput.value) > 0) {
        selectedYearlyCost = Number(customInput.value);
      } else {
        selectedYearlyCost = 35000;
        customInput.value = '35000';
      }
      customInput.focus();
      calculate();
    });

    // Custom Input Change
    customInput.addEventListener('input', () => {
      const val = Number(customInput.value);
      if (!isNaN(val) && val >= 0) {
        selectedYearlyCost = Math.min(val, 10000000);
        calculate();
      }
    });

    // Slider Change
    slider.addEventListener('input', () => {
      selectedYears = Number(slider.value);
      calculate();
    });

    calculate();
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCalculator);
  } else {
    initCalculator();
  }
})();
