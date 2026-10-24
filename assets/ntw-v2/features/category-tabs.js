/**
 * F4: Category Tabs
 * Interactive category switch: Decking, Cladding, Beams, Deck Tile, Fencing, Railing, Planter Box.
 * Crossfade scene images, display swatches, and trigger sample requests.
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
      img: '/wp-content/uploads/2025/09/NewTechWood-decking.jpg',
      alt: 'UltraShield composite decking outdoor terrace',
      colorsCount: 6,
      swatches: [
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Brazilian Ipe', hex: '#422e20' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Canadian Maple', hex: '#c9a374' },
        { name: 'Spanish Walnut', hex: '#34251a' },
        { name: 'Charcoal', hex: '#282a2b' }
      ]
    },
    {
      id: 'cladding',
      name: 'Cladding',
      tag: 'Architectural Wall Siding',
      title: 'All-Weather & Castellated Wall Cladding',
      desc: 'Transform plain brick and concrete exterior walls with contemporary fluted shadowlines and natural wood grain textures. Engineered with hidden clip expansion systems.',
      url: '/product/cladding/',
      img: '/wp-content/uploads/2025/09/NewTechWood-cladding.jpg',
      alt: 'NewTechWood castellated fluted wall cladding facade',
      colorsCount: 6,
      swatches: [
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Brazilian Ipe', hex: '#422e20' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Spanish Walnut', hex: '#34251a' },
        { name: 'Silver Grey', hex: '#9ca3af' },
        { name: 'Midnight Black', hex: '#111827' }
      ]
    },
    {
      id: 'beams',
      name: 'Beams & Louvers',
      tag: 'Exterior Screening & Louvers',
      title: 'Architectural Louvers & Sun Control Beams',
      desc: 'Continuous lightweight composite beams designed for outdoor pergolas, architectural fins, and decorative ceiling baffles that will never sag, split, or rot.',
      url: '/product/screening/',
      img: '/wp-content/uploads/2025/09/beams.jpg',
      alt: 'Architectural composite louvers and pergola sun shading',
      colorsCount: 4,
      swatches: [
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Brazilian Ipe', hex: '#422e20' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Spanish Walnut', hex: '#34251a' }
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
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Canadian Maple', hex: '#c9a374' },
        { name: 'Silver Grey', hex: '#9ca3af' }
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
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Brazilian Ipe', hex: '#422e20' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Charcoal', hex: '#282a2b' }
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
        { name: 'Matte Black', hex: '#18181b' },
        { name: 'Bronze', hex: '#451a03' },
        { name: 'Peruvian Teak', hex: '#b57644' }
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
        { name: 'Peruvian Teak', hex: '#b57644' },
        { name: 'Roman Antique', hex: '#7b7268' },
        { name: 'Spanish Walnut', hex: '#34251a' }
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
      // Insert right before color-swatch-explorer or after hero promo
      const anchor = document.getElementById('ntw-color-swatch-explorer') || document.querySelector('.ll-history-highlight');
      if (!anchor) return;
      mount = document.createElement('div');
      mount.id = 'ntw-category-tabs';
      anchor.parentNode.insertBefore(mount, anchor);
    }

    let activeCatIndex = 0;

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

              <div class="ntw-cat-swatches-box">
                <div class="ntw-cat-swatches-label">
                  <span>Signature Color Range</span>
                  <span id="ntw-cat-colors-count">${CATEGORIES[0].colorsCount} Standard Colors</span>
                </div>
                <div class="ntw-cat-swatches-row" id="ntw-cat-swatches-row">
                  ${CATEGORIES[0].swatches.map(sw => `
                    <span class="ntw-cat-swatch-thumb" style="background-color: ${sw.hex};" title="${escapeHtml(sw.name)}" aria-label="${escapeHtml(sw.name)}"></span>
                  `).join('')}
                </div>
              </div>

              <div class="ntw-cat-panel-actions">
                <a href="${CATEGORIES[0].url}" class="ntw-cat-panel-btn-primary" id="ntw-cat-explore-btn">
                  <span>Explore ${escapeHtml(CATEGORIES[0].name)}</span>
                  <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                </a>
                <button type="button" class="ntw-cat-panel-btn-sample" id="ntw-cat-sample-btn">
                  <span>Request Sample Box</span>
                </button>
              </div>
            </div>

            <div class="ntw-cat-panel-media">
              <img src="${CATEGORIES[0].img}" alt="${escapeHtml(CATEGORIES[0].alt)}" class="ntw-cat-panel-img" id="ntw-cat-img" />
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
    const exploreBtn = document.getElementById('ntw-cat-explore-btn');
    const sampleBtn = document.getElementById('ntw-cat-sample-btn');
    const imgEl = document.getElementById('ntw-cat-img');

    function switchCategory(idx) {
      if (idx === activeCatIndex) return;
      activeCatIndex = idx;
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

      // Update swatches
      swatchesRow.innerHTML = cat.swatches.map(sw => `
        <span class="ntw-cat-swatch-thumb" style="background-color: ${sw.hex};" title="${escapeHtml(sw.name)}" aria-label="${escapeHtml(sw.name)}"></span>
      `).join('');

      // Crossfade image
      imgEl.classList.add('crossfade-out');
      setTimeout(() => {
        imgEl.src = cat.img;
        imgEl.alt = cat.alt;
        imgEl.classList.remove('crossfade-out');
      }, 200);
    }

    tabBtns.forEach((btn, idx) => {
      btn.addEventListener('click', () => switchCategory(idx));

      // Arrow key navigation
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

    if (sampleBtn) {
      sampleBtn.addEventListener('click', () => {
        const currentCat = CATEGORIES[activeCatIndex];
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: { productCategory: currentCat.name }
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
