/**
 * F5: Project Filter
 * Tabs: All / International / National (India) with URL hash synchronization,
 * animated card transitions, counter updates, and empty-state fallback.
 */

(function () {
  'use strict';

  let currentRegion = 'all';
  let currentCategory = 'all';

  function initProjectFilter() {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;

    setupEmptyState(grid);
    setupHashListener();
    readInitialHash();
    bindTabEvents();
    applyFilterTransitions();
  }

  function setupEmptyState(grid) {
    if (grid.querySelector('.ntw-projects-empty-state')) return;

    const empty = document.createElement('div');
    empty.className = 'ntw-projects-empty-state';
    empty.innerHTML = `
      <div class="ntw-empty-icon">
        <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10H7v-2h10v2z"/></svg>
      </div>
      <h3 class="ntw-empty-title">No matching installations found</h3>
      <p class="ntw-empty-desc">We couldn't find any projects matching the selected combination. Reset your filters to browse our complete architectural portfolio.</p>
      <button type="button" class="ntw-empty-reset-btn" id="ntw-reset-filters-btn">Reset Filters</button>
    `;

    grid.appendChild(empty);

    const resetBtn = empty.querySelector('#ntw-reset-filters-btn');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        setRegion('all', true);
        setCategory('all');
      });
    }
  }

  function readInitialHash() {
    const hash = window.location.hash.toLowerCase().replace('#', '');
    if (hash === 'national' || hash === 'international' || hash === 'all') {
      currentRegion = hash;
    } else {
      currentRegion = 'all';
    }
    updateRegionButtonsUI();
  }

  function setupHashListener() {
    window.addEventListener('hashchange', () => {
      const hash = window.location.hash.toLowerCase().replace('#', '');
      const valid = ['all', 'national', 'international'];
      const target = valid.includes(hash) ? hash : 'all';
      if (target !== currentRegion) {
        currentRegion = target;
        updateRegionButtonsUI();
        applyFilterTransitions();
      }
    });
  }

  function updateRegionButtonsUI() {
    const regionBtns = document.querySelectorAll('#region-filter-group .filter-btn');
    regionBtns.forEach(btn => {
      const filter = (btn.getAttribute('data-filter') || '').toLowerCase();
      const isActive = (filter === currentRegion);
      btn.classList.toggle('active', isActive);
      btn.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });
  }

  function bindTabEvents() {
    const regionGroup = document.getElementById('region-filter-group');
    if (regionGroup) {
      const btns = regionGroup.querySelectorAll('.filter-btn');
      btns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const filter = btn.getAttribute('data-filter') || 'all';
          setRegion(filter, true);
        });
      });
    }

    const catGroup = document.getElementById('category-filter-group');
    if (catGroup) {
      const catBtns = catGroup.querySelectorAll('.filter-btn');
      catBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const cat = btn.getAttribute('data-cat') || 'all';
          setCategory(cat);
        });
      });
    }

    // Expose global bridge for backwards compatibility with any inline onclicks
    window.filterProjects = function (region, btn) {
      setRegion(region, true);
    };

    window.filterCategory = function (cat, btn) {
      setCategory(cat);
    };
  }

  function setRegion(region, syncHash) {
    currentRegion = region.toLowerCase();
    if (syncHash) {
      if (history.replaceState) {
        history.replaceState(null, '', currentRegion === 'all' ? window.location.pathname : '#' + currentRegion);
      } else {
        window.location.hash = currentRegion;
      }
    }
    updateRegionButtonsUI();
    applyFilterTransitions();
  }

  function setCategory(cat) {
    currentCategory = cat.toLowerCase();
    const catBtns = document.querySelectorAll('#category-filter-group .filter-btn');
    catBtns.forEach(btn => {
      const c = (btn.getAttribute('data-cat') || '').toLowerCase();
      btn.classList.toggle('active-gold', c === currentCategory);
    });
    applyFilterTransitions();
  }

  function applyFilterTransitions() {
    const grid = document.getElementById('projects-grid');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.project-card'));
    let visibleCount = 0;

    cards.forEach(card => {
      const cardRegion = (card.getAttribute('data-region') || '').toLowerCase();
      const cardCats = (card.getAttribute('data-cat') || '').toLowerCase();

      const matchRegion = (currentRegion === 'all' || cardRegion === currentRegion);
      const matchCat = (currentCategory === 'all' || cardCats.includes(currentCategory));

      if (matchRegion && matchCat) {
        visibleCount++;
        card.classList.remove('is-hidden');
        card.classList.add('is-entering');
        void card.offsetHeight; // Force reflow
        card.classList.remove('is-entering');
      } else {
        card.classList.add('is-hidden');
      }
    });

    // Update Counter
    const counter = document.getElementById('project-counter');
    if (counter) {
      counter.innerText = `Showing ${visibleCount} Showcase Project${visibleCount === 1 ? '' : 's'}`;
    }

    // Toggle Empty State
    const emptyState = grid.querySelector('.ntw-projects-empty-state');
    if (emptyState) {
      emptyState.classList.toggle('is-visible', visibleCount === 0);
    }
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
    document.addEventListener('DOMContentLoaded', initProjectFilter);
  } else {
    initProjectFilter();
  }
})();

