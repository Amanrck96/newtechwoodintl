/**
 * F2: Client-Side Live Search Overlay
 * Instant search over search-index.json grouped into:
 * - Products
 * - Projects
 * - Pages
 * - Articles
 * "No results" state with 3 fallback buttons:
 * - Products
 * - Colours
 * - Experience Centre
 * Focus trap, Esc to close, keyboard navigation (Up/Down/Enter), Ctrl+K & / triggers.
 */

(function () {
  'use strict';

  let searchIndex = [];
  let isIndexLoaded = false;
  let activeResults = [];
  let selectedIndex = -1;
  let previousActiveElement = null;

  const POPULAR_ITEMS = [
    { title: 'Decking Systems', url: '/product/decking/', category: 'Products' },
    { title: 'Wall Cladding & Siding', url: '/product/wall-cladding/', category: 'Products' },
    { title: 'Order Free Sample Kit', url: '/#ntw-sample-request', category: 'Pages' },
    { title: 'Experience Centres', url: '/#experience-centre', category: 'Pages' },
    { title: 'National Projects (India)', url: '/projects/#national', category: 'Projects' },
    { title: 'Color Swatch Explorer', url: '/#ntw-color-swatch-explorer', category: 'Products' }
  ];

  const CATEGORY_ORDER = ['Products', 'Projects', 'Pages', 'Articles'];
  const CATEGORY_ICONS = {
    Products: '🏷️',
    Projects: '🏢',
    Pages: '📄',
    Articles: '📰'
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSearchOverlay);
  } else {
    initSearchOverlay();
  }

  function initSearchOverlay() {
    loadSearchIndex();
    createOverlayMarkup();
    bindGlobalShortcuts();
    window.addEventListener('ntw:open-search', openSearch);
  }

  function loadSearchIndex() {
    fetch('/assets/ntw-v2/features/search-index.json')
      .then(res => res.json())
      .then(data => {
        searchIndex = data;
        isIndexLoaded = true;
      })
      .catch(err => {
        console.warn('NTW Search: search-index.json fallback', err);
        searchIndex = POPULAR_ITEMS.map(p => ({
          title: p.title,
          category: p.category,
          url: p.url,
          description: `Explore NewTechWood ${p.title} specifications and architectural solutions.`,
          keywords: [p.title.toLowerCase()]
        }));
        isIndexLoaded = true;
      });
  }

  function createOverlayMarkup() {
    if (document.getElementById('ntw-search-modal')) return;

    const overlay = document.createElement('div');
    overlay.className = 'ntw-search-backdrop';
    overlay.id = 'ntw-search-modal';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Search NewTechWood');
    overlay.setAttribute('aria-hidden', 'true');

    overlay.innerHTML = `
      <div class="ntw-search-dialog" id="ntw-search-dialog">
        
        <div class="ntw-search-input-wrap">
          <svg class="search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <input type="text" class="ntw-search-input" id="ntw-search-input" placeholder="Search products, projects, colours, articles..." autocomplete="off" spellcheck="false" />
          <button type="button" class="ntw-search-clear-btn" id="ntw-search-clear-btn" aria-label="Clear search input">&times;</button>
          <button type="button" class="ntw-search-close-key" id="ntw-search-close-btn" aria-label="Close search (Esc)">ESC</button>
        </div>

        <div class="ntw-search-body" id="ntw-search-body">
          <div class="ntw-popular-wrap" id="ntw-popular-wrap">
            <div class="ntw-search-section-title">Popular Quick Links</div>
            <div class="ntw-popular-links">
              ${POPULAR_ITEMS.map(item => `
                <a href="${item.url}" class="ntw-popular-chip">
                  <span>${escapeHtml(item.title)}</span>
                </a>
              `).join('')}
            </div>
          </div>

          <div class="ntw-search-results-wrap" id="ntw-search-results-wrap" style="display:none;"></div>

          <div class="ntw-search-no-results" id="ntw-search-no-results" style="display:none;">
            <svg class="ntw-search-empty-icon" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>
            <div class="ntw-search-empty-title" id="ntw-search-empty-msg">No matching solutions found.</div>
            <p class="ntw-search-empty-desc">Check spelling, try broader keywords, or jump directly to one of our core sections:</p>
            <div class="ntw-search-fallback-buttons">
              <a href="/product/decking/" class="ntw-search-fallback-btn primary" id="ntw-fallback-products">
                <svg viewBox="0 0 24 24"><path d="M4 6h16v2H4zm0 5h16v2H4zm0 5h16v2H4z"/></svg>
                <span>Products</span>
              </a>
              <a href="/#ntw-color-swatch-explorer" class="ntw-search-fallback-btn" id="ntw-fallback-colours">
                <svg viewBox="0 0 24 24"><path d="M12 3c-4.97 0-9 4.03-9 9 0 2.12.74 4.07 1.97 5.61L4.35 19.4c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0l1.9-1.9C9.22 19.59 10.56 20 12 20c4.97 0 9-4.03 9-9s-4.03-9-9-9zm0 15c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z"/></svg>
                <span>Colours</span>
              </a>
              <a href="/#experience-centre" class="ntw-search-fallback-btn" id="ntw-fallback-centres">
                <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <span>Experience Centre</span>
              </a>
            </div>
          </div>
        </div>

        <div class="ntw-search-footer">
          <div class="ntw-search-shortcuts">
            <span><strong>&uarr; &darr;</strong> Navigate</span>
            <span><strong>ENTER</strong> Open</span>
            <span><strong>ESC</strong> Close</span>
          </div>
          <div>Live Architecture Search &bull; NewTechWood</div>
        </div>

      </div>
    `;

    document.body.appendChild(overlay);
    bindOverlayEvents(overlay);
  }

  function bindOverlayEvents(overlay) {
    const input = document.getElementById('ntw-search-input');
    const clearBtn = document.getElementById('ntw-search-clear-btn');
    const closeBtn = document.getElementById('ntw-search-close-btn');

    if (closeBtn) closeBtn.addEventListener('click', closeSearch);

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        input.value = '';
        clearBtn.classList.remove('active');
        renderPopular();
        input.focus();
      });
    }

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeSearch();
    });

    if (input) {
      input.addEventListener('input', () => {
        const query = input.value.trim();
        clearBtn.classList.toggle('active', query.length > 0);
        if (query.length === 0) {
          renderPopular();
        } else {
          executeSearch(query);
        }
      });

      input.addEventListener('keydown', handleKeyNavigation);
    }

    // Bind Focus Trap inside dialog
    overlay.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        const focusable = overlay.querySelectorAll('button, [href], input, [tabindex="0"]');
        const focusableArr = Array.from(focusable).filter(el => el.offsetParent !== null);
        if (focusableArr.length === 0) return;

        const first = focusableArr[0];
        const last = focusableArr[focusableArr.length - 1];

        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      } else if (e.key === 'Escape') {
        closeSearch();
      }
    });

    // Fallback button events
    const fallbackColours = overlay.querySelector('#ntw-fallback-colours');
    if (fallbackColours) {
      fallbackColours.addEventListener('click', () => {
        closeSearch();
      });
    }
    const fallbackProducts = overlay.querySelector('#ntw-fallback-products');
    if (fallbackProducts) {
      fallbackProducts.addEventListener('click', () => {
        closeSearch();
      });
    }
    const fallbackCentres = overlay.querySelector('#ntw-fallback-centres');
    if (fallbackCentres) {
      fallbackCentres.addEventListener('click', () => {
        closeSearch();
      });
    }
  }

  function bindGlobalShortcuts() {
    document.addEventListener('keydown', (e) => {
      // Ctrl+K / Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        toggleSearch();
        return;
      }

      // Single forward slash '/' when not inside an input/textarea
      if (e.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
        e.preventDefault();
        openSearch();
      }
    });
  }

  function openSearch() {
    const overlay = document.getElementById('ntw-search-modal');
    const input = document.getElementById('ntw-search-input');
    if (!overlay || !input) return;

    previousActiveElement = document.activeElement;
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    setTimeout(() => {
      input.focus();
      if (input.value.trim().length > 0) {
        executeSearch(input.value.trim());
      } else {
        renderPopular();
      }
    }, 50);
  }

  function closeSearch() {
    const overlay = document.getElementById('ntw-search-modal');
    if (!overlay) return;

    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';

    if (previousActiveElement && typeof previousActiveElement.focus === 'function') {
      previousActiveElement.focus();
    }
  }

  function toggleSearch() {
    const overlay = document.getElementById('ntw-search-modal');
    if (overlay && overlay.classList.contains('is-open')) {
      closeSearch();
    } else {
      openSearch();
    }
  }

  function renderPopular() {
    const popularWrap = document.getElementById('ntw-popular-wrap');
    const resultsWrap = document.getElementById('ntw-search-results-wrap');
    const noResults = document.getElementById('ntw-search-no-results');

    if (popularWrap) popularWrap.style.display = 'block';
    if (resultsWrap) resultsWrap.style.display = 'none';
    if (noResults) noResults.style.display = 'none';

    activeResults = [];
    selectedIndex = -1;
  }

  function executeSearch(query) {
    const popularWrap = document.getElementById('ntw-popular-wrap');
    const resultsWrap = document.getElementById('ntw-search-results-wrap');
    const noResults = document.getElementById('ntw-search-no-results');
    const emptyMsg = document.getElementById('ntw-search-empty-msg');

    if (!popularWrap || !resultsWrap || !noResults) return;

    popularWrap.style.display = 'none';
    const qLower = query.toLowerCase();

    // Score and filter
    const scored = [];
    for (const item of searchIndex) {
      let score = 0;
      const titleLower = (item.title || '').toLowerCase();
      const descLower = (item.description || '').toLowerCase();
      const catLower = (item.category || '').toLowerCase();
      const keywords = (item.keywords || []).map(k => String(k).toLowerCase());

      if (titleLower.includes(qLower)) score += 10;
      if (titleLower.startsWith(qLower)) score += 15;
      if (keywords.some(k => k === qLower)) score += 20;
      if (keywords.some(k => k.includes(qLower))) score += 5;
      if (catLower.includes(qLower)) score += 8;
      if (descLower.includes(qLower)) score += 3;

      if (score > 0) {
        scored.push({ item, score });
      }
    }

    scored.sort((a, b) => b.score - a.score);
    const matches = scored.map(s => s.item);

    if (matches.length === 0) {
      resultsWrap.style.display = 'none';
      noResults.style.display = 'block';
      if (emptyMsg) {
        emptyMsg.textContent = `No matching solutions found for "${query}".`;
      }
      activeResults = [];
      selectedIndex = -1;
      return;
    }

    noResults.style.display = 'none';
    resultsWrap.style.display = 'block';

    // Group matches into Products, Projects, Pages, Articles
    const grouped = {
      Products: [],
      Projects: [],
      Pages: [],
      Articles: []
    };

    for (const match of matches) {
      const cat = match.category || 'Products';
      if (grouped[cat]) {
        grouped[cat].push(match);
      } else {
        grouped['Products'].push(match);
      }
    }

    // Build ordered list of active results for keyboard navigation
    activeResults = [];
    let html = '';

    CATEGORY_ORDER.forEach(groupName => {
      const groupItems = grouped[groupName];
      if (groupItems && groupItems.length > 0) {
        const icon = CATEGORY_ICONS[groupName] || '🔹';
        html += `
          <div class="ntw-search-group">
            <div class="ntw-search-group-header">
              <span>${icon} ${groupName}</span>
              <span class="ntw-search-group-count">${groupItems.length}</span>
            </div>
            <ul class="ntw-search-results-list" role="listbox">
              ${groupItems.map(item => {
                const currentIndex = activeResults.length;
                activeResults.push(item);
                const pillClass = `pill-${groupName.toLowerCase()}`;

                return `
                  <li>
                    <a href="${item.url}" class="ntw-search-result-item" data-index="${currentIndex}" role="option">
                      <div class="ntw-search-result-header">
                        <h4 class="ntw-search-result-title">${highlightMatch(escapeHtml(item.title), query)}</h4>
                        <span class="ntw-search-category-pill ${pillClass}">${escapeHtml(item.category)}</span>
                      </div>
                      <p class="ntw-search-result-desc">${highlightMatch(escapeHtml(item.description || ''), query)}</p>
                    </a>
                  </li>
                `;
              }).join('')}
            </ul>
          </div>
        `;
      }
    });

    resultsWrap.innerHTML = html;
    selectedIndex = -1;
  }

  function handleKeyNavigation(e) {
    if (activeResults.length === 0) return;

    const items = document.querySelectorAll('.ntw-search-result-item');
    if (items.length === 0) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = (selectedIndex + 1) % items.length;
      updateSelected(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = (selectedIndex - 1 + items.length) % items.length;
      updateSelected(items);
    } else if (e.key === 'Enter') {
      if (selectedIndex >= 0 && selectedIndex < items.length) {
        e.preventDefault();
        items[selectedIndex].click();
      }
    }
  }

  function updateSelected(items) {
    items.forEach((item, idx) => {
      const isSel = idx === selectedIndex;
      item.classList.toggle('is-selected', isSel);
      item.setAttribute('aria-selected', isSel ? 'true' : 'false');
      if (isSel) {
        item.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  function highlightMatch(text, query) {
    if (!query) return text;
    const escapedQ = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escapedQ})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
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
