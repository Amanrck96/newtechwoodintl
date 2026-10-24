/**
 * F6: Client-Side Search Overlay
 * Instant search over search-index.json, Ctrl+K / '/' shortcut, Esc close,
 * popular links, and keyboard navigation.
 */

(function () {
  'use strict';

  let searchIndex = [];
  let isIndexLoaded = false;
  let selectedIndex = -1;

  const POPULAR_ITEMS = [
    { title: 'Decking Systems', url: '/product/decking/', category: 'Product' },
    { title: 'Wall Cladding & Siding', url: '/product/wall-cladding/', category: 'Product' },
    { title: 'Cost Calculator', url: '/#ntw-cost-calculator', category: 'Tool' },
    { title: 'Order Free Sample Kit', url: '/#ntw-sample-request', category: 'Service' },
    { title: 'Experience Centres', url: '/#experience-centre', category: 'Showrooms' },
    { title: 'National Projects (India)', url: '/projects/#national', category: 'Gallery' },
    { title: 'Color Swatch Explorer', url: '/#ntw-color-swatch-explorer', category: 'Finishes' }
  ];

  function initSearchOverlay() {
    loadSearchIndex();
    createOverlayMarkup();
    injectHeaderTrigger();
    bindGlobalShortcuts();
  }

  function loadSearchIndex() {
    fetch('/assets/ntw-v2/features/search-index.json')
      .then(res => res.json())
      .then(data => {
        searchIndex = data;
        isIndexLoaded = true;
      })
      .catch(err => {
        console.warn('NTW Search: search-index.json fetch fallback', err);
        // Fallback default index
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
      <div class="ntw-search-dialog">
        
        <div class="ntw-search-input-wrap">
          <svg class="search-icon" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          <input type="text" class="ntw-search-input" id="ntw-search-input" placeholder="Search products, colors, projects, or experience centres..." autocomplete="off" spellcheck="false" />
          <button type="button" class="ntw-search-clear-btn" id="ntw-search-clear-btn" aria-label="Clear search input">&times;</button>
          <button type="button" class="ntw-search-close-key" id="ntw-search-close-btn" aria-label="Close search">ESC</button>
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

          <div class="ntw-search-results-wrap" id="ntw-search-results-wrap" style="display:none;">
            <div class="ntw-search-section-title" id="ntw-results-count-title">Results</div>
            <ul class="ntw-search-results-list" id="ntw-results-list" role="listbox"></ul>
          </div>

          <div class="ntw-search-no-results" id="ntw-search-no-results" style="display:none;">
            No matching solutions found. Try searching for "Decking", "Teak", "Cladding", or "Delhi".
          </div>
        </div>

        <div class="ntw-search-footer">
          <div class="ntw-search-shortcuts">
            <span><strong>&uarr; &darr;</strong> to navigate</span>
            <span><strong>ENTER</strong> to open</span>
            <span><strong>ESC</strong> to dismiss</span>
          </div>
          <div>NewTechWood Architecture Search</div>
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

    if (closeBtn) {
      closeBtn.addEventListener('click', closeSearch);
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        input.value = '';
        clearBtn.classList.remove('active');
        renderPopular();
        input.focus();
      });
    }

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        closeSearch();
      }
    });

    if (input) {
      input.addEventListener('input', () => {
        const query = input.value.trim();
        clearBtn.classList.toggle('active', query.length > 0);
        if (query.length === 0) {
          renderPopular();
        } else {
          performSearch(query);
        }
      });

      input.addEventListener('keydown', (e) => {
        const results = document.querySelectorAll('.ntw-search-result-item');
        if (results.length === 0) return;

        if (e.key === 'ArrowDown') {
          e.preventDefault();
          selectedIndex = (selectedIndex + 1) % results.length;
          updateSelectedResult(results);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          selectedIndex = (selectedIndex - 1 + results.length) % results.length;
          updateSelectedResult(results);
        } else if (e.key === 'Enter') {
          if (selectedIndex >= 0 && selectedIndex < results.length) {
            e.preventDefault();
            const link = results[selectedIndex].querySelector('a');
            if (link) {
              closeSearch();
              window.location.href = link.href;
            }
          }
        }
      });
    }
  }

  function updateSelectedResult(results) {
    results.forEach((item, idx) => {
      item.classList.toggle('is-selected', idx === selectedIndex);
      if (idx === selectedIndex) {
        item.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  function performSearch(query) {
    const popularWrap = document.getElementById('ntw-popular-wrap');
    const resultsWrap = document.getElementById('ntw-search-results-wrap');
    const resultsList = document.getElementById('ntw-results-list');
    const noResults = document.getElementById('ntw-search-no-results');
    const countTitle = document.getElementById('ntw-results-count-title');

    if (popularWrap) popularWrap.style.display = 'none';

    selectedIndex = -1;
    const q = query.toLowerCase();

    // Fuzzy matching score
    const matches = searchIndex.filter(item => {
      const inTitle = item.title.toLowerCase().includes(q);
      const inDesc = (item.description || '').toLowerCase().includes(q);
      const inCat = (item.category || '').toLowerCase().includes(q);
      const inKeys = (item.keywords || []).some(k => k.toLowerCase().includes(q));
      return inTitle || inDesc || inCat || inKeys;
    }).slice(0, 8);

    if (matches.length === 0) {
      if (resultsWrap) resultsWrap.style.display = 'none';
      if (noResults) noResults.style.display = 'block';
    } else {
      if (noResults) noResults.style.display = 'none';
      if (resultsWrap) resultsWrap.style.display = 'block';
      if (countTitle) countTitle.innerText = `${matches.length} matching result${matches.length === 1 ? '' : 's'}`;

      resultsList.innerHTML = matches.map((item, idx) => `
        <li class="ntw-search-result-item" role="option">
          <a href="${item.url}" onclick="document.getElementById('ntw-search-modal').classList.remove('is-open');document.body.style.overflow='';">
            <div class="ntw-search-result-header">
              <h4 class="ntw-search-result-title">${highlightMatch(item.title, query)}</h4>
              <span class="ntw-search-category-pill">${escapeHtml(item.category)}</span>
            </div>
            <p class="ntw-search-result-desc">${highlightMatch(item.description, query)}</p>
          </a>
        </li>
      `).join('');
    }
  }

  function renderPopular() {
    const popularWrap = document.getElementById('ntw-popular-wrap');
    const resultsWrap = document.getElementById('ntw-search-results-wrap');
    const noResults = document.getElementById('ntw-search-no-results');

    if (popularWrap) popularWrap.style.display = 'block';
    if (resultsWrap) resultsWrap.style.display = 'none';
    if (noResults) noResults.style.display = 'none';
  }

  function highlightMatch(text, query) {
    if (!text || !query) return escapeHtml(text || '');
    const escapedText = escapeHtml(text);
    const escapedQuery = escapeHtml(query);
    const regex = new RegExp(`(${escapedQuery})`, 'gi');
    return escapedText.replace(regex, '<mark>$1</mark>');
  }

  function injectHeaderTrigger() {
    // Look for header navigation container
    const nav = document.querySelector('.elementor-widget-theme-site-logo') || document.querySelector('.e-n-menu');
    if (!nav) return;

    if (document.getElementById('ntw-header-search-btn')) return;

    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ntw-header-search-btn';
    btn.id = 'ntw-header-search-btn';
    btn.setAttribute('aria-label', 'Open search overlay');
    btn.innerHTML = `
      <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
      <span>Search</span>
      <span class="ntw-search-key-badge">&#x2318;K</span>
    `;

    btn.addEventListener('click', openSearch);

    // Place adjacent to nav
    if (nav.parentNode) {
      nav.parentNode.appendChild(btn);
    }
  }

  function openSearch() {
    const modal = document.getElementById('ntw-search-modal');
    if (!modal) return;

    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';

    const input = document.getElementById('ntw-search-input');
    if (input) {
      input.value = '';
      renderPopular();
      setTimeout(() => input.focus(), 80);
    }
  }

  function closeSearch() {
    const modal = document.getElementById('ntw-search-modal');
    if (!modal) return;

    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function bindGlobalShortcuts() {
    window.addEventListener('keydown', (e) => {
      const modal = document.getElementById('ntw-search-modal');
      const isOpen = modal && modal.classList.contains('is-open');

      if (e.key === 'Escape' && isOpen) {
        e.preventDefault();
        closeSearch();
        return;
      }

      // Ctrl+K or Cmd+K
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (isOpen) {
          closeSearch();
        } else {
          openSearch();
        }
        return;
      }

      // '/' trigger when not in an input
      if (e.key === '/' && !isOpen) {
        const tag = (document.activeElement.tagName || '').toLowerCase();
        if (tag !== 'input' && tag !== 'textarea' && !document.activeElement.isContentEditable) {
          e.preventDefault();
          openSearch();
        }
      }
    });

    // Expose global open helper
    window.ntwOpenSearch = openSearch;
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
    document.addEventListener('DOMContentLoaded', initSearchOverlay);
  } else {
    initSearchOverlay();
  }
})();
