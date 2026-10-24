/**
 * F5: Color Swatch Explorer
 * Interactive architectural finish selector featuring the official NewTechWood
 * global color palette with real board finishes, specifications, and sample ordering.
 */

(function () {
  'use strict';

  // Comprehensive official NewTechWood global color range
  const PALETTE = [
    {
      name: 'Peruvian Teak',
      code: 'TK',
      series: 'UltraShield® Naturale™',
      color: '#b57644',
      image: '/wp-content/uploads/2025/12/decking-1.jpg',
      alt: 'NewTechWood UltraShield Peruvian Teak natural wood composite finish',
      description: 'Warm, classic golden-honey brown inspired by natural virgin teak timber. Features multi-chromatic streaking for authentic hardwood depth with superior UV fade resistance.',
      applications: 'Decking, Cladding, Screening, Deck Tiles',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Brazilian Ipe',
      code: 'IP',
      series: 'UltraShield® Naturale™',
      color: '#3f2a1d',
      image: '/wp-content/uploads/2025/12/decking-2.jpg',
      alt: 'Luxury poolside terrace featuring NewTechWood Brazilian Ipe composite',
      description: 'Rich, luxurious dark walnut-brown tones reflecting the dense elegance of South American Ipe hardwood. Engineered to resist heavy sun, red wine, and monsoon moisture.',
      applications: 'Decking, Cladding, Pergolas, Louvers',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Spanish Walnut',
      code: 'WN',
      series: 'UltraShield® Naturale™',
      color: '#34251a',
      image: '/wp-content/uploads/2025/12/decking-4.jpg',
      alt: 'Modern architectural exterior with Spanish Walnut composite finish',
      description: 'Deep espresso dark chocolate finish engineered for bold modern luxury facades and terrace living. 100% encapsulated against oils, barbecue grease, and stains.',
      applications: 'Decking, Castellated Cladding, Screening',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Roman Antique',
      code: 'AT',
      series: 'UltraShield® Naturale™',
      color: '#756c62',
      image: '/wp-content/uploads/2025/12/decking-3-1.jpg',
      alt: 'Architectural patio and fence installed with Roman Antique composite wood',
      description: 'Subtle weathered grey-brown blend designed to emulate mature European timber. Harmonizes effortlessly with natural stone, concrete, and minimalist glass architecture.',
      applications: 'Decking, Cladding, Fencing, Deck Tiles',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Silver Grey',
      code: 'SI',
      series: 'UltraShield® Naturale™',
      color: '#8d918d',
      image: '/product-images/clads.jpg',
      alt: 'Contemporary silver grey composite cladding finish',
      description: 'Refined contemporary silver patina offering clean architectural lines without the splintering, silvering, or rot associated with untreated exterior cedar.',
      applications: 'Wall Cladding, Decking, Deck Tiles',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Hawaiian Charcoal',
      code: 'CH',
      series: 'UltraShield® Naturale™',
      color: '#2b2d2f',
      image: '/wp-content/uploads/2025/12/pool-deck.jpg',
      alt: 'Commercial installation featuring Hawaiian Charcoal composite profiles',
      description: 'Dramatic volcanic graphite tone providing modern definition and high architectural contrast. Maintains deep saturation under high-intensity tropical UV rays.',
      applications: 'Decking, Cladding, Fencing, Railing',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Canadian Maple',
      code: 'MP',
      series: 'UltraShield® Naturale™',
      color: '#c49c66',
      image: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png',
      alt: 'Sunlit relaxation deck crafted in Natural Maple composite boards',
      description: 'Light, sunlit golden tone that creates an expansive, airy ambience for residential terraces, balconies, and boutique hotel pool decks.',
      applications: 'Decking, Deck Tiles, Interior/Exterior Accents',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Westminster Gray',
      code: 'WG',
      series: 'UltraShield® Naturale™',
      color: '#5c6065',
      image: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg',
      alt: 'Westminster Gray architectural composite installation',
      description: 'Mid-tone slate grey with cool urban undertones, engineered for contemporary commercial walkways, urban rooftops, and luxury pool surroundings.',
      applications: 'Decking, Commercial Louvers, Cladding',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    },
    {
      name: 'Indian Ebony',
      code: 'EB',
      series: 'UltraShield® Naturale™',
      color: '#18181b',
      image: '/wp-content/uploads/2025/09/NewTechWood-cladding.jpg',
      alt: 'Dramatic Indian Ebony deep black composite siding',
      description: 'Intense obsidian finish providing the ultimate dark architectural silhouette. 360-degree capping ensures zero color bleaching or surface chalking over time.',
      applications: 'Castellated Cladding, Beams, Louvers',
      specs: { capping: '360° All-Round Polymer Shield', warranty: '25 Years', slipRating: 'R11 / Class C' }
    }
  ];

  function initExplorer() {
    const mountPoint = document.getElementById('ntw-color-swatch-explorer');
    if (!mountPoint) return;

    let currentIndex = 0;

    mountPoint.innerHTML = `
      <section class="ntw-swatch-explorer" aria-label="Interactive Color Swatch Explorer">
        <div class="ntw-se-card">
          
          <!-- Visual Showcase -->
          <div class="ntw-se-visual" aria-live="polite">
            <span class="ntw-se-badge" id="ntw-se-badge">
              <span class="ntw-se-badge-dot" style="background-color: ${PALETTE[0].color};"></span>
              <span id="ntw-se-badge-text">${escapeHtml(PALETTE[0].name)}</span>
            </span>
            <img 
              id="ntw-se-main-img" 
              class="ntw-se-img" 
              src="${escapeHtml(PALETTE[0].image)}" 
              alt="${escapeHtml(PALETTE[0].alt)}"
              loading="eager"
            />
            <div class="ntw-se-img-overlay">
              <span class="ntw-se-img-app" id="ntw-se-img-app">${escapeHtml(PALETTE[0].applications)}</span>
            </div>
          </div>

          <!-- Color Details & Swatches -->
          <div class="ntw-se-content">
            <div class="ntw-se-eyebrow">Explore Finishes</div>
            <h3 class="ntw-se-title" id="ntw-se-title">${escapeHtml(PALETTE[0].name)}</h3>
            
            <div class="ntw-se-meta-row">
              <span class="ntw-se-code" id="ntw-se-code">CODE: ${escapeHtml(PALETTE[0].code)}</span>
              <span class="ntw-se-series" id="ntw-se-series">${escapeHtml(PALETTE[0].series)}</span>
            </div>

            <p class="ntw-se-desc" id="ntw-se-desc">${escapeHtml(PALETTE[0].description)}</p>

            <!-- Specifications Grid -->
            <div class="ntw-se-specs-row">
              <div class="ntw-se-spec-item">
                <span class="ntw-se-spec-label">Capping</span>
                <span class="ntw-se-spec-val" id="ntw-se-spec-capping">${escapeHtml(PALETTE[0].specs.capping)}</span>
              </div>
              <div class="ntw-se-spec-item">
                <span class="ntw-se-spec-label">Warranty</span>
                <span class="ntw-se-spec-val" id="ntw-se-spec-warranty">${escapeHtml(PALETTE[0].specs.warranty)}</span>
              </div>
              <div class="ntw-se-spec-item">
                <span class="ntw-se-spec-label">Slip Rating</span>
                <span class="ntw-se-spec-val" id="ntw-se-spec-slip">${escapeHtml(PALETTE[0].specs.slipRating)}</span>
              </div>
            </div>

            <div class="ntw-se-swatches-header">
              <span class="ntw-se-swatches-title">Select Color Swatch</span>
              <span class="ntw-se-swatches-sub">9 Standard Global Architectural Finishes</span>
            </div>

            <div class="ntw-se-swatches-row" role="radiogroup" aria-label="Available Color Swatches">
              ${PALETTE.map((p, idx) => `
                <button 
                  type="button" 
                  class="ntw-se-swatch ${idx === 0 ? 'active' : ''}" 
                  style="background-color: ${p.color};" 
                  data-index="${idx}"
                  role="radio"
                  aria-checked="${idx === 0 ? 'true' : 'false'}"
                  aria-label="${escapeHtml(p.name)} (${escapeHtml(p.code)})"
                  title="${escapeHtml(p.name)} (${escapeHtml(p.code)})"
                  tabindex="${idx === 0 ? '0' : '-1'}"
                >
                  <span class="ntw-se-swatch-ring"></span>
                </button>
              `).join('')}
            </div>

            <div class="ntw-se-actions">
              <button type="button" class="ntw-se-btn-order" id="ntw-se-btn-order">
                <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
                <span>Order Free Sample in <strong id="ntw-se-btn-color-name">${escapeHtml(PALETTE[0].name)}</strong></span>
              </button>
            </div>

          </div>

        </div>
      </section>
    `;

    const mainImg = document.getElementById('ntw-se-main-img');
    const titleEl = document.getElementById('ntw-se-title');
    const badgeText = document.getElementById('ntw-se-badge-text');
    const badgeDot = document.querySelector('.ntw-se-badge-dot');
    const codeEl = document.getElementById('ntw-se-code');
    const seriesEl = document.getElementById('ntw-se-series');
    const descEl = document.getElementById('ntw-se-desc');
    const appEl = document.getElementById('ntw-se-img-app');
    const specCapping = document.getElementById('ntw-se-spec-capping');
    const specWarranty = document.getElementById('ntw-se-spec-warranty');
    const specSlip = document.getElementById('ntw-se-spec-slip');
    const btnColorName = document.getElementById('ntw-se-btn-color-name');
    const orderBtn = document.getElementById('ntw-se-btn-order');
    const swatches = mountPoint.querySelectorAll('.ntw-se-swatch');

    function updateSelection(index, focus = false) {
      if (index === currentIndex) return;
      currentIndex = index;
      const item = PALETTE[index];
      if (!item) return;

      // Update Swatch Active State
      swatches.forEach((sw, idx) => {
        const isActive = idx === index;
        sw.classList.toggle('active', isActive);
        sw.setAttribute('aria-checked', isActive ? 'true' : 'false');
        sw.setAttribute('tabindex', isActive ? '0' : '-1');
        if (isActive && focus) {
          sw.focus();
        }
      });

      // Update Content Info
      titleEl.textContent = item.name;
      badgeText.textContent = item.name;
      if (badgeDot) badgeDot.style.backgroundColor = item.color;
      codeEl.textContent = `CODE: ${item.code}`;
      seriesEl.textContent = item.series;
      descEl.textContent = item.description;
      if (appEl) appEl.textContent = item.applications;
      if (btnColorName) btnColorName.textContent = item.name;

      if (specCapping) specCapping.textContent = item.specs.capping;
      if (specWarranty) specWarranty.textContent = item.specs.warranty;
      if (specSlip) specSlip.textContent = item.specs.slipRating;

      // Smooth Image Swap
      mainImg.classList.add('fade-out');
      setTimeout(() => {
        mainImg.src = item.image;
        mainImg.alt = item.alt;
        mainImg.classList.remove('fade-out');
      }, 150);
    }

    // Swatch Listeners
    swatches.forEach((sw, idx) => {
      sw.addEventListener('mouseenter', () => updateSelection(idx));
      sw.addEventListener('click', () => updateSelection(idx, true));

      sw.addEventListener('keydown', (e) => {
        let nextIdx = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          nextIdx = (currentIndex + 1) % PALETTE.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          nextIdx = (currentIndex - 1 + PALETTE.length) % PALETTE.length;
        } else if (e.key === 'Home') {
          e.preventDefault();
          nextIdx = 0;
        } else if (e.key === 'End') {
          e.preventDefault();
          nextIdx = PALETTE.length - 1;
        }

        if (nextIdx !== null) {
          updateSelection(nextIdx, true);
        }
      });
    });

    // Sample Modal Trigger
    if (orderBtn) {
      orderBtn.addEventListener('click', () => {
        const activeColor = PALETTE[currentIndex];
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: {
            color: activeColor.name,
            colorCode: activeColor.code,
            series: activeColor.series
          }
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

    // External listener for selecting a color from Category Tabs or Header
    window.addEventListener('ntw:select-color', (e) => {
      if (!e.detail) return;
      const { colorName, colorCode } = e.detail;
      const foundIdx = PALETTE.findIndex(p => 
        (colorCode && p.code.toLowerCase() === colorCode.toLowerCase()) ||
        (colorName && p.name.toLowerCase() === colorName.toLowerCase())
      );
      if (foundIdx >= 0) {
        updateSelection(foundIdx, false);
      }
    });
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initExplorer);
  } else {
    initExplorer();
  }
})();
