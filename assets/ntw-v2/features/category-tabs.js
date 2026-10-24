/**
 * F4: Category Tabs
 * Interactive category switch: Decking, Cladding, Beams, Deck Tile, Fencing, Railing, Planter Box.
 * Features:
 * - Interactive Signature Color Range with live active states and color labels
 * - Instant finish preview switching
 * - "Explore Finishes" action linking directly to Color Swatch Explorer
 * - Request Sample Box integration
 */

(function () {
  'use strict';

  const CATEGORIES = [
    {
      id: 'decking',
      name: 'Decking',
      tag: 'Capped Composite Decking',
      title: 'UltraShield® Naturale Decking Systems',
      desc: 'Engineered with 360-degree capping for total resistance against wine, oil, UV fading, and heavy monsoon humidity. Available in Naturale, Marina, and Old World textures.',
      url: '/product/decking/',
      img: '/wp-content/uploads/2025/12/decking-1.jpg',
      alt: 'UltraShield composite decking outdoor terrace',
      colorsCount: 6,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2025/12/decking-1.jpg', desc: 'Warm natural honey teak with realistic grain variegation' },
        { name: 'Brazilian Ipe', code: 'IP', hex: '#3f2a1d', img: '/wp-content/uploads/2025/12/decking-2.jpg', desc: 'Rich, luxurious dark walnut-brown tones' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2025/12/decking-3-1.jpg', desc: 'Timeless weathered grey-brown European timber finish' },
        { name: 'Canadian Maple', code: 'MP', hex: '#c9a374', img: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png', desc: 'Light Scandinavian honey tones for bright spaces' },
        { name: 'Spanish Walnut', code: 'WN', hex: '#34251a', img: '/wp-content/uploads/2025/12/decking-4.jpg', desc: 'Deep espresso dark chocolate luxury finish' },
        { name: 'Charcoal', code: 'CH', hex: '#282a2b', img: '/wp-content/uploads/2025/12/pool-deck.jpg', desc: 'Contemporary minimalist volcanic graphite' }
      ]
    },
    {
      id: 'cladding',
      name: 'Cladding',
      tag: 'Architectural Wall Siding',
      title: 'All-Weather & Castellated Wall Cladding',
      desc: 'Transform plain brick and concrete exterior walls with contemporary fluted shadowlines and natural wood grain textures. Engineered with hidden clip expansion systems.',
      url: '/product/cladding/',
      img: '/wp-content/uploads/2025/12/Cladding-1.jpg',
      alt: 'NewTechWood castellated fluted wall cladding facade',
      colorsCount: 6,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2025/12/Cladding-1.jpg', desc: 'Golden teak facade planks with authentic wood grain' },
        { name: 'Brazilian Ipe', code: 'IP', hex: '#3f2a1d', img: '/wp-content/uploads/2025/12/Cladding-2.jpg', desc: 'Deep tropical hardwood tone for bold exterior accents' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2025/12/Cladding-3.jpg', desc: 'Weathered architectural patina blending with stone & glass' },
        { name: 'Spanish Walnut', code: 'WN', hex: '#34251a', img: '/wp-content/uploads/2025/12/Cladding-4.jpg', desc: 'Dark espresso luxury cladding for modern residential villas' },
        { name: 'Silver Grey', code: 'SI', hex: '#9ca3af', img: '/product-images/clads.jpg', desc: 'Clean silver-grey contemporary minimalist aesthetic' },
        { name: 'Midnight Black', code: 'EB', hex: '#111827', img: '/wp-content/uploads/2025/09/NewTechWood-cladding.jpg', desc: 'Dramatic matte obsidian for high-contrast architectural accents' }
      ]
    },
    {
      id: 'beams',
      name: 'Beams & Louvers',
      tag: 'Exterior Screening & Louvers',
      title: 'Architectural Louvers & Sun Control Beams',
      desc: 'Continuous lightweight composite beams designed for outdoor pergolas, architectural fins, and decorative ceiling baffles that will never sag, split, or rot.',
      url: '/product/screening/',
      img: '/wp-content/uploads/2025/12/Beams-1.jpg',
      alt: 'Architectural composite louvers and pergola sun shading',
      colorsCount: 4,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2025/12/Beams-1.jpg', desc: 'Louver profile in radiant natural teak' },
        { name: 'Brazilian Ipe', code: 'IP', hex: '#3f2a1d', img: '/wp-content/uploads/2025/12/Beams-2.jpg', desc: 'Heavy dark wood tone for pergolas and screening fins' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2025/12/Beams-3.jpg', desc: 'Contemporary weathered grey finish for exterior baffles' },
        { name: 'Spanish Walnut', code: 'WN', hex: '#34251a', img: '/wp-content/uploads/2025/12/Beams-4.jpg', desc: 'Sophisticated deep walnut for premium exterior accents' }
      ]
    },
    {
      id: 'deck-tile',
      name: 'Deck Tile',
      tag: 'DIY Interlocking Flooring',
      title: 'QuickDeck Interlocking Composite Tiles',
      desc: 'Instant click-together balcony and terrace flooring. Features snap-fit grid bases that allow water drainage and rapid DIY installation without framing.',
      url: '/product/deck-tiles/',
      img: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png',
      alt: 'QuickDeck composite tiles installed on luxury residential balcony',
      colorsCount: 4,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png', desc: 'Warm natural teak 4-slat interlocking tile' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg', desc: 'Weathered grey balcony tile with drainage base' },
        { name: 'Canadian Maple', code: 'MP', hex: '#c9a374', img: '/wp-content/uploads/2019/01/comfort-and-relaxation-deck.png', desc: 'Light honey tone for bright terrace flooring' },
        { name: 'Silver Grey', code: 'SI', hex: '#9ca3af', img: '/product-images/deck.jpg', desc: 'Modern silver tone for rooftop gardens & balconies' }
      ]
    },
    {
      id: 'fencing',
      name: 'Fencing',
      tag: 'Privacy Screens & Gates',
      title: 'UltraEasy Full Privacy Composite Fencing',
      desc: 'Tongue-and-groove composite fence boards fitting aluminum posts for private, storm-resistant boundary lines that never require staining or waterproofing.',
      url: '/product/fencing/',
      img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg',
      alt: 'UltraEasy composite privacy fence with integrated gate',
      colorsCount: 4,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg', desc: 'Warm timber boundary slats' },
        { name: 'Brazilian Ipe', code: 'IP', hex: '#3f2a1d', img: '/wp-content/uploads/2018/12/NewTechWood_UltraShield_Decking_359.jpg', desc: 'Dense dark wood privacy fence' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg', desc: 'Weathered fence boards for rustic elegance' },
        { name: 'Charcoal', code: 'CH', hex: '#282a2b', img: '/wp-content/uploads/2025/12/pool-deck.jpg', desc: 'Dark graphite boundary panels' }
      ]
    },
    {
      id: 'railing',
      name: 'Railing',
      tag: 'Balustrades & Safety Handrails',
      title: 'Composite & Minimalist Aluminum Railing',
      desc: 'Robust perimeter railing systems pairing smooth UltraShield composite top rails with powder-coated aluminum balusters for unobtrusive garden and terrace views.',
      url: '/product/railing/',
      img: '/wp-content/uploads/2018/12/NewTechWood_UltraShield_Decking_359.jpg',
      alt: 'Architectural railing installed on elevated composite deck',
      colorsCount: 3,
      swatches: [
        { name: 'Matte Black', code: 'BK', hex: '#18181b', img: '/wp-content/uploads/2018/12/NewTechWood_UltraShield_Decking_359.jpg', desc: 'Powder-coated architectural black balusters' },
        { name: 'Bronze', code: 'BZ', hex: '#451a03', img: '/wp-content/uploads/2025/12/decking-2.jpg', desc: 'Warm metallic architectural bronze frame' },
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2025/12/decking-1.jpg', desc: 'UltraShield capped top rail in Peruvian Teak' }
      ]
    },
    {
      id: 'planter-box',
      name: 'Planter Box',
      tag: 'Modular Planters & Accents',
      title: 'Modular Composite Garden Planters',
      desc: 'Weatherproof modular planters constructed from heavy-duty composite planks. Perfectly matched to your decking and cladding for cohesive landscape design.',
      url: '/product/planter-box/',
      img: '/wp-content/uploads/2025/08/NewTechWood-History.jpg',
      alt: 'Architectural modular composite planter boxes for urban terraces',
      colorsCount: 3,
      swatches: [
        { name: 'Peruvian Teak', code: 'TK', hex: '#b57644', img: '/wp-content/uploads/2025/08/NewTechWood-History.jpg', desc: 'Warm teak planter box accents' },
        { name: 'Roman Antique', code: 'AT', hex: '#7b7268', img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg', desc: 'Weathered stone-grey planters' },
        { name: 'Spanish Walnut', code: 'WN', hex: '#34251a', img: '/wp-content/uploads/2025/12/decking-4.jpg', desc: 'Dark espresso terrace planter box' }
      ]
    }
  ];

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCategoryTabs);
  } else {
    initCategoryTabs();
  }

  function initCategoryTabs() {
    let mount = document.getElementById('ntw-category-tabs');

    if (!mount) {
      const anchor = document.getElementById('ntw-color-swatch-explorer') || document.querySelector('.ll-history-highlight');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-category-tabs';
      anchor.parentNode.insertBefore(mount, anchor);
    }

    let activeCatIndex = 0;
    let activeSwatchIndex = 0;

    mount.innerHTML = `
      <section class="ntw-cat-tabs-section" aria-label="Product Categories Directory">
        <div class="ntw-cat-tabs-container">
          
          <div class="ntw-cat-tabs-header">
            <span class="ntw-cat-tabs-eyebrow">Complete Architectural Systems</span>
            <h2 class="ntw-cat-tabs-title">Engineered Composite Solutions</h2>
            <p class="ntw-cat-tabs-subtitle">Explore our complete range of UltraShield capped wood composite systems designed for long-lasting outdoor living.</p>
          </div>

          <div class="ntw-cat-tabs-nav" role="tablist" aria-label="Product Category Tabs">
            ${CATEGORIES.map((cat, idx) => `
              <button type="button" class="ntw-cat-tab-btn ${idx === 0 ? 'active' : ''}" role="tab" id="ntw-cat-tab-${cat.id}" aria-selected="${idx === 0 ? 'true' : 'false'}" aria-controls="ntw-cat-panel-content" data-cat-idx="${idx}">
                <span>${escapeHtml(cat.name)}</span>
                <span class="ntw-cat-tab-count">${cat.colorsCount} Colors</span>
              </button>
            `).join('')}
          </div>

          <div class="ntw-cat-panel" id="ntw-cat-panel-content" role="tabpanel" aria-labelledby="ntw-cat-tab-decking">
            
            <div class="ntw-cat-panel-left">
              <span class="ntw-cat-panel-tag" id="ntw-cat-tag">${escapeHtml(CATEGORIES[0].tag)}</span>
              <h3 class="ntw-cat-panel-h3" id="ntw-cat-title">${escapeHtml(CATEGORIES[0].title)}</h3>
              <p class="ntw-cat-panel-desc" id="ntw-cat-desc">${escapeHtml(CATEGORIES[0].desc)}</p>

              <!-- Interactive Signature Color Range -->
              <div class="ntw-cat-swatches-box">
                <div class="ntw-cat-swatches-label">
                  <span>Signature Color Range</span>
                  <span id="ntw-cat-colors-count">${CATEGORIES[0].colorsCount} Standard Colors</span>
                </div>
                
                <div class="ntw-cat-swatches-row" id="ntw-cat-swatches-row" role="radiogroup" aria-label="Signature Colors">
                  <!-- Rendered dynamically -->
                </div>

                <div class="ntw-cat-selected-info" id="ntw-cat-selected-info">
                  <div class="ntw-cat-selected-row">
                    <span class="ntw-cat-color-dot" id="ntw-cat-color-dot" style="background-color: ${CATEGORIES[0].swatches[0].hex};"></span>
                    <span class="ntw-cat-selected-name" id="ntw-cat-selected-name">${escapeHtml(CATEGORIES[0].swatches[0].name)} (${CATEGORIES[0].swatches[0].code})</span>
                  </div>
                  <span class="ntw-cat-selected-desc" id="ntw-cat-selected-desc">${escapeHtml(CATEGORIES[0].swatches[0].desc)}</span>
                </div>
              </div>

              <div class="ntw-cat-panel-actions">
                <a href="${CATEGORIES[0].url}" class="ntw-cat-panel-btn-primary" id="ntw-cat-explore-btn">
                  <span>Explore ${escapeHtml(CATEGORIES[0].name)}</span>
                  <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
                
                <a href="#ntw-color-swatch-explorer" class="ntw-cat-panel-btn-finishes" id="ntw-cat-finishes-btn">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.28 19.64 10.59 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
                  <span>Explore Finishes</span>
                </a>

                <button type="button" class="ntw-cat-panel-btn-sample" id="ntw-cat-sample-btn">
                  <span>Request Sample Box</span>
                </button>
              </div>
            </div>

            <div class="ntw-cat-panel-media">
              <div class="ntw-cat-media-badge" id="ntw-cat-media-badge">
                <span class="ntw-cat-badge-dot" id="ntw-cat-badge-dot" style="background-color: ${CATEGORIES[0].swatches[0].hex};"></span>
                <span id="ntw-cat-badge-text">${escapeHtml(CATEGORIES[0].swatches[0].name)} (${CATEGORIES[0].swatches[0].code})</span>
              </div>
              <img src="${CATEGORIES[0].swatches[0].img || CATEGORIES[0].img}" alt="${escapeHtml(CATEGORIES[0].alt)}" class="ntw-cat-panel-img" id="ntw-cat-img" />
            </div>

          </div>

        </div>
      </section>
    `;

    const tabBtns = mount.querySelectorAll('.ntw-cat-tab-btn');
    const tagEl = document.getElementById('ntw-cat-tag');
    const titleEl = document.getElementById('ntw-cat-title');
    const descEl = document.getElementById('ntw-cat-desc');
    const colorsCountEl = document.getElementById('ntw-cat-colors-count');
    const swatchesRow = document.getElementById('ntw-cat-swatches-row');
    const selectedNameEl = document.getElementById('ntw-cat-selected-name');
    const selectedDescEl = document.getElementById('ntw-cat-selected-desc');
    const colorDotEl = document.getElementById('ntw-cat-color-dot');
    const mediaBadgeText = document.getElementById('ntw-cat-badge-text');
    const mediaBadgeDot = document.getElementById('ntw-cat-badge-dot');
    const exploreBtn = document.getElementById('ntw-cat-explore-btn');
    const finishesBtn = document.getElementById('ntw-cat-finishes-btn');
    const sampleBtn = document.getElementById('ntw-cat-sample-btn');
    const imgEl = document.getElementById('ntw-cat-img');

    function renderSwatches(cat) {
      swatchesRow.innerHTML = cat.swatches.map((sw, sIdx) => `
        <button type="button" 
          class="ntw-cat-swatch-thumb ${sIdx === activeSwatchIndex ? 'active' : ''}" 
          style="background-color: ${sw.hex};" 
          data-swatch-idx="${sIdx}" 
          role="radio" 
          aria-checked="${sIdx === activeSwatchIndex ? 'true' : 'false'}"
          aria-label="${escapeHtml(sw.name)} (${sw.code})"
          title="${escapeHtml(sw.name)} (${sw.code})">
          <span class="ntw-cat-swatch-check"></span>
        </button>
      `).join('');

      // Swatch click & hover listeners
      swatchesRow.querySelectorAll('.ntw-cat-swatch-thumb').forEach((btn, sIdx) => {
        btn.addEventListener('click', () => selectSwatch(sIdx));
        btn.addEventListener('mouseenter', () => selectSwatch(sIdx, false));
      });
    }

    function selectSwatch(sIdx, permanent = true) {
      activeSwatchIndex = sIdx;
      const cat = CATEGORIES[activeCatIndex];
      const sw = cat.swatches[sIdx];
      if (!sw) return;

      // Update swatch active classes
      swatchesRow.querySelectorAll('.ntw-cat-swatch-thumb').forEach((btn, idx) => {
        const isActive = idx === sIdx;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-checked', isActive ? 'true' : 'false');
      });

      // Update text info
      selectedNameEl.innerHTML = `${escapeHtml(sw.name)} <strong>(${escapeHtml(sw.code)})</strong>`;
      selectedDescEl.textContent = sw.desc || `${sw.name} finish in UltraShield 360 co-extruded capping.`;
      colorDotEl.style.backgroundColor = sw.hex;

      // Update media badge
      if (mediaBadgeText) mediaBadgeText.textContent = `${sw.name} (${sw.code})`;
      if (mediaBadgeDot) mediaBadgeDot.style.backgroundColor = sw.hex;

      // Crossfade image if swatch has dedicated image
      const targetImg = sw.img || cat.img;
      if (imgEl && imgEl.src !== targetImg && permanent) {
        imgEl.classList.add('crossfade-out');
        setTimeout(() => {
          imgEl.src = targetImg;
          imgEl.alt = `${cat.name} in ${sw.name} finish`;
          imgEl.classList.remove('crossfade-out');
        }, 150);
      }
    }

    function switchCategory(idx) {
      if (idx === activeCatIndex) return;
      activeCatIndex = idx;
      activeSwatchIndex = 0;
      const cat = CATEGORIES[idx];

      // Update tabs
      tabBtns.forEach((btn, bIdx) => {
        const isActive = bIdx === idx;
        btn.classList.toggle('active', isActive);
        btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });

      // Update text
      tagEl.textContent = cat.tag;
      titleEl.textContent = cat.title;
      descEl.textContent = cat.desc;
      colorsCountEl.textContent = `${cat.colorsCount} Standard Colors`;

      exploreBtn.href = cat.url;
      exploreBtn.querySelector('span').textContent = `Explore ${cat.name}`;

      // Re-render swatches and select first
      renderSwatches(cat);
      selectSwatch(0, true);
    }

    // Initialize swatches for first category
    renderSwatches(CATEGORIES[0]);

    tabBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => switchCategory(idx));

      btn.addEventListener('keydown', (e) => {
        let targetIdx = null;
        if (e.key === 'ArrowRight') {
          e.preventDefault();
          targetIdx = (idx + 1) % CATEGORIES.length;
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          targetIdx = (idx - 1 + CATEGORIES.length) % CATEGORIES.length;
        } else if (e.key === 'Home') {
          e.preventDefault();
          targetIdx = 0;
        } else if (e.key === 'End') {
          e.preventDefault();
          targetIdx = CATEGORIES.length - 1;
        }

        if (targetIdx !== null) {
          tabBtns[targetIdx].focus();
          switchCategory(targetIdx);
        }
      });
    });

    // "Explore Finishes" button handler
    if (finishesBtn) {
      finishesBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const cat = CATEGORIES[activeCatIndex];
        const sw = cat.swatches[activeSwatchIndex];
        
        // Dispatch select-color event to Color Swatch Explorer
        if (sw) {
          window.dispatchEvent(new CustomEvent('ntw:select-color', {
            detail: { colorName: sw.name, colorCode: sw.code }
          }));
        }

        const target = document.getElementById('ntw-color-swatch-explorer');
        if (target) {
          const navOffset = 90;
          const elementPosition = target.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - navOffset;
          window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
        }
      });
    }

    // Sample request button
    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        const currentCat = CATEGORIES[activeCatIndex];
        const currentSw = currentCat.swatches[activeSwatchIndex];
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: { 
            productCategory: currentCat.name,
            color: currentSw ? currentSw.name : ''
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
