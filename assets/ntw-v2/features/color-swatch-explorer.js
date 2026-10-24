/**
 * F1: Color Swatch Explorer
 * Vanilla JavaScript module, keyboard accessible, zero layout shift.
 */
(function () {
  'use strict';

  // Core palette dynamically mapped from products.json and UltraShield catalogue
  const PALETTE = [
    {
      name: 'Peruvian Teak',
      code: 'TK',
      series: 'UltraShield Naturale',
      color: '#b57644',
      image: '/product-images/deck.jpg',
      alt: 'NewTechWood UltraShield Decking in Peruvian Teak finish',
      description: 'Warm, classic medium brown inspired by natural teak hardwood with authentic grain texture and superior UV resistance.'
    },
    {
      name: 'Brazilian Ipe',
      code: 'IP',
      series: 'UltraShield Naturale',
      color: '#422e20',
      image: '/wp-content/uploads/2018/12/NewTechWood_UltraShield_Decking_359.jpg',
      alt: 'Luxury poolside terrace featuring NewTechWood Brazilian Ipe decking',
      description: 'Rich, luxurious dark brown tones reflecting the legendary strength and dense tropical elegance of South American Ipe.'
    },
    {
      name: 'Roman Antique',
      code: 'AT',
      series: 'UltraShield Naturale',
      color: '#7b7268',
      image: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg',
      alt: 'Architectural patio and fence installed with Roman Antique composite wood',
      description: 'Subtle gray-brown blend designed to emulate weathered European hardwood with timeless, contemporary aesthetics.'
    },
    {
      name: 'Natural Maple',
      code: 'MP',
      series: 'UltraShield Naturale',
      color: '#c9a374',
      image: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png',
      alt: 'Sunlit relaxation deck crafted in Natural Maple composite boards',
      description: 'Light, golden honey hues that brighten outdoor living areas, creating an airy Scandinavian outdoor ambience.'
    },
    {
      name: 'Spanish Walnut',
      code: 'WN',
      series: 'UltraShield Naturale',
      color: '#34251a',
      image: '/product-images/clads.jpg',
      alt: 'Modern architectural exterior with Spanish Walnut composite cladding',
      description: 'Deep espresso tones with rich chocolate nuances for bold, contrasting modern luxury facades and decks.'
    },
    {
      name: 'Hawaiian Charcoal',
      code: 'CH',
      series: 'UltraShield Naturale',
      color: '#282a2b',
      image: '/product-images/twix.jpg',
      alt: 'Commercial installation featuring Hawaiian Charcoal composite profiles',
      description: 'Modern volcanic graphite shade providing dramatic architectural definition and contemporary minimalist styling.'
    }
  ];

  // Preload images into memory
  function preloadImages() {
    PALETTE.forEach(item => {
      const img = new Image();
      img.src = item.image;
    });
  }

  function initExplorer() {
    const mountPoint = document.getElementById('ntw-color-swatch-explorer');
    if (!mountPoint) return;

    let currentIndex = 0;

    // Render Markup
    mountPoint.innerHTML = `
      <section class="ntw-swatch-explorer" aria-label="Interactive Color Swatch Explorer">
        <div class="ntw-se-card">
          <!-- Visual Showcase -->
          <div class="ntw-se-visual" aria-live="polite">
            <span class="ntw-se-badge" id="ntw-se-badge">
              <span class="ntw-se-badge-dot"></span>
              <span id="ntw-se-badge-text">${escapeHtml(PALETTE[0].name)}</span>
            </span>
            <img 
              id="ntw-se-main-img" 
              class="ntw-se-img" 
              src="${escapeHtml(PALETTE[0].image)}" 
              alt="${escapeHtml(PALETTE[0].alt)}"
              loading="eager"
            />
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

            <div class="ntw-se-swatches-title">Select Color Swatch</div>
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
                  tabindex="${idx === 0 ? '0' : '-1'}"
                ></button>
              `).join('')}
            </div>

            <button type="button" class="ntw-se-btn-order" id="ntw-se-btn-order">
              <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>
              <span>Order Free Sample in this Color</span>
            </button>
          </div>
        </div>
      </section>
    `;

    const mainImg = document.getElementById('ntw-se-main-img');
    const titleEl = document.getElementById('ntw-se-title');
    const badgeText = document.getElementById('ntw-se-badge-text');
    const codeEl = document.getElementById('ntw-se-code');
    const seriesEl = document.getElementById('ntw-se-series');
    const descEl = document.getElementById('ntw-se-desc');
    const orderBtn = document.getElementById('ntw-se-btn-order');
    const swatches = mountPoint.querySelectorAll('.ntw-se-swatch');

    function updateSelection(index, focus = false) {
      if (index === currentIndex) return;
      currentIndex = index;
      const item = PALETTE[index];

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
      codeEl.textContent = `CODE: ${item.code}`;
      seriesEl.textContent = item.series;
      descEl.textContent = item.description;

      // Smooth Image Swap (no layout shift)
      mainImg.classList.add('fade-out');
      setTimeout(() => {
        mainImg.src = item.image;
        mainImg.alt = item.alt;
        mainImg.classList.remove('fade-out');
      }, 150);
    }

    // Swatch Hover & Click Listeners
    swatches.forEach((sw, idx) => {
      // Desktop hover
      sw.addEventListener('mouseenter', () => updateSelection(idx));
      // Mobile tap / keyboard click
      sw.addEventListener('click', () => updateSelection(idx, true));

      // Keyboard arrow navigation
      sw.addEventListener('keydown', (e) => {
        let nextIdx = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          nextIdx = (currentIndex + 1) % PALETTE.length;
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          nextIdx = (currentIndex - 1 + PALETTE.length) % PALETTE.length;
        } else if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          updateSelection(idx, true);
        }

        if (nextIdx !== null) {
          updateSelection(nextIdx, true);
        }
      });
    });

    // "Order this color" button integration with F3 Sample Modal
    orderBtn.addEventListener('click', () => {
      const activeColor = PALETTE[currentIndex];
      // Dispatch custom event for F3 hook
      window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
        detail: {
          colorName: activeColor.name,
          colorCode: activeColor.code,
          series: activeColor.series
        }
      }));

      // If F3 modal function is directly accessible
      if (typeof window.openNewTechWoodSampleModal === 'function') {
        window.openNewTechWoodSampleModal({
          colorName: activeColor.name,
          colorCode: activeColor.code,
          series: activeColor.series
        });
      }
    });

    preloadImages();
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

  // Auto-initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initExplorer);
  } else {
    initExplorer();
  }
})();
