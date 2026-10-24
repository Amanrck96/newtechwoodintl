/**
 * F4: Experience Centre Filter
 * Provides interactive state filtering for NewTechWood Experience Centres
 * across India (Delhi, Karnataka, Rajasthan, Gujarat, Punjab + All).
 */

(function () {
  'use strict';

  function initExperienceCentreFilter() {
    const sections = document.querySelectorAll('.ll-experience-centre');
    if (!sections || sections.length === 0) return;

    sections.forEach((sec) => {
      setupSection(sec);
    });
  }

  function setupSection(section) {
    const grid = section.querySelector('.ll-ec-grid');
    if (!grid) return;

    // Check if filter bar already injected
    if (section.querySelector('.ntw-ec-filter-bar')) return;

    const cards = Array.from(grid.querySelectorAll('.ll-ec-card'));
    if (cards.length === 0) return;

    // Determine city keys for each card
    cards.forEach((card) => {
      const cityElem = card.querySelector('.ll-ec-card-city') || card.querySelector('.ll-ec-city-badge');
      const cityName = cityElem ? cityElem.textContent.trim().toLowerCase() : '';
      let cityKey = 'other';
      if (cityName.includes('delhi')) cityKey = 'delhi';
      else if (cityName.includes('karnataka') || cityName.includes('bengaluru') || cityName.includes('bangalore')) cityKey = 'karnataka';
      else if (cityName.includes('rajasthan') || cityName.includes('jaipur')) cityKey = 'rajasthan';
      else if (cityName.includes('gujarat') || cityName.includes('surat')) cityKey = 'gujarat';
      else if (cityName.includes('punjab')) cityKey = 'punjab';

      card.setAttribute('data-ntw-city', cityKey);
    });

    // Counts
    const counts = {
      all: cards.length,
      delhi: cards.filter(c => c.getAttribute('data-ntw-city') === 'delhi').length,
      karnataka: cards.filter(c => c.getAttribute('data-ntw-city') === 'karnataka').length,
      rajasthan: cards.filter(c => c.getAttribute('data-ntw-city') === 'rajasthan').length,
      gujarat: cards.filter(c => c.getAttribute('data-ntw-city') === 'gujarat').length,
      punjab: cards.filter(c => c.getAttribute('data-ntw-city') === 'punjab').length
    };

    // Filter Chips Config
    const filters = [
      { id: 'all', label: 'All Centres', count: counts.all },
      { id: 'delhi', label: 'Delhi', count: counts.delhi },
      { id: 'karnataka', label: 'Karnataka', count: counts.karnataka },
      { id: 'rajasthan', label: 'Rajasthan', count: counts.rajasthan },
      { id: 'gujarat', label: 'Gujarat', count: counts.gujarat },
      { id: 'punjab', label: 'Punjab', count: counts.punjab }
    ];

    // Build Filter Bar HTML
    const filterBar = document.createElement('div');
    filterBar.className = 'ntw-ec-filter-bar';
    filterBar.setAttribute('role', 'tablist');
    filterBar.setAttribute('aria-label', 'Filter experience centres by state');

    filters.forEach((f, idx) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = `ntw-ec-filter-chip${idx === 0 ? ' active' : ''}`;
      btn.setAttribute('role', 'tab');
      btn.setAttribute('aria-selected', idx === 0 ? 'true' : 'false');
      btn.setAttribute('data-filter', f.id);
      btn.id = `ntw-chip-${f.id}`;
      btn.innerHTML = `
        <span>${escapeHtml(f.label)}</span>
        <span class="chip-count">${f.count}</span>
      `;

      btn.addEventListener('click', () => {
        applyFilter(f.id, btn, filterBar, cards, grid);
      });

      filterBar.appendChild(btn);
    });

    // Keyboard navigation (Left / Right arrow)
    filterBar.addEventListener('keydown', (e) => {
      const chips = Array.from(filterBar.querySelectorAll('.ntw-ec-filter-chip'));
      const activeIndex = chips.indexOf(document.activeElement);
      if (activeIndex === -1) return;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        const next = (activeIndex + 1) % chips.length;
        chips[next].focus();
        chips[next].click();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        const prev = (activeIndex - 1 + chips.length) % chips.length;
        chips[prev].focus();
        chips[prev].click();
      }
    });

    // Insert Filter Bar right before the grid
    grid.parentNode.insertBefore(filterBar, grid);

    // Add Empty State Container to grid
    const emptyState = document.createElement('div');
    emptyState.className = 'ntw-ec-empty-state';
    emptyState.innerHTML = `<p>No experience centre currently active for the selected region. Explore our nearby centres or connect with our team on WhatsApp for architectural consultation.</p>`;
    grid.appendChild(emptyState);
  }

  function applyFilter(filterId, activeBtn, filterBar, cards, grid) {
    // Update button states
    const chips = filterBar.querySelectorAll('.ntw-ec-filter-chip');
    chips.forEach(c => {
      const isSelected = (c === activeBtn);
      c.classList.toggle('active', isSelected);
      c.setAttribute('aria-selected', isSelected ? 'true' : 'false');
    });

    let visibleCount = 0;

    cards.forEach(card => {
      const cityKey = card.getAttribute('data-ntw-city');
      const matches = (filterId === 'all' || cityKey === filterId);

      if (matches) {
        visibleCount++;
        card.classList.remove('ntw-filter-hidden');
        card.classList.add('ntw-filter-entering');
        // Force reflow
        void card.offsetHeight;
        card.classList.remove('ntw-filter-entering');
      } else {
        card.classList.add('ntw-filter-hidden');
      }
    });

    const emptyState = grid.querySelector('.ntw-ec-empty-state');
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
    document.addEventListener('DOMContentLoaded', initExperienceCentreFilter);
  } else {
    initExperienceCentreFilter();
  }
})();
