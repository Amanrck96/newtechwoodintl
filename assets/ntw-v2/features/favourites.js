/**
 * F13: Favourites Drawer & Wishlist
 * Client-side wishlist with persistent LocalStorage, heart toggle injection,
 * and seamless transfer to the F9 sample modal.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'ntw_favourites_v2';
  let favourites = [];

  function loadFavourites() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      favourites = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(favourites)) favourites = [];
    } catch (e) {
      favourites = [];
    }
  }

  function saveFavourites() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(favourites));
    } catch (e) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFavourites);
  } else {
    initFavourites();
  }

  function initFavourites() {
    loadFavourites();
    renderDOM();
    bindEvents();
    updateUI();
    injectHeartButtons();
  }

  function renderDOM() {
    // 1. Floating Trigger Button
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.id = 'ntw-fav-trigger';
    trigger.className = 'ntw-fav-trigger-btn';
    trigger.setAttribute('aria-label', 'View saved favorite products');
    trigger.innerHTML = `
      <svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
      <span>Saved</span>
      <span class="ntw-fav-badge" id="ntw-fav-badge">0</span>
    `;
    document.body.appendChild(trigger);

    // 2. Slide-out Drawer
    const backdrop = document.createElement('div');
    backdrop.id = 'ntw-fav-backdrop';
    backdrop.className = 'ntw-fav-drawer-backdrop';
    backdrop.setAttribute('role', 'dialog');
    backdrop.setAttribute('aria-modal', 'true');
    backdrop.setAttribute('aria-hidden', 'true');
    backdrop.setAttribute('aria-label', 'Saved Finishes Drawer');

    backdrop.innerHTML = `
      <div class="ntw-fav-drawer">
        <div class="ntw-fav-header">
          <h3 class="ntw-fav-title">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="#dc2626"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            <span>Saved Finishes</span>
          </h3>
          <button type="button" class="ntw-fav-close-btn" id="ntw-fav-close" aria-label="Close saved finishes drawer">&times;</button>
        </div>

        <div class="ntw-fav-body" id="ntw-fav-body">
          <!-- Rendered dynamically -->
        </div>

        <div class="ntw-fav-footer">
          <button type="button" class="ntw-fav-sample-cta" id="ntw-fav-sample-cta">
            <span>Request Samples for Saved (0)</span>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(backdrop);
  }

  function bindEvents() {
    const trigger = document.getElementById('ntw-fav-trigger');
    const backdrop = document.getElementById('ntw-fav-backdrop');
    const closeBtn = document.getElementById('ntw-fav-close');
    const sampleCta = document.getElementById('ntw-fav-sample-cta');

    if (trigger) trigger.addEventListener('click', openDrawer);
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    if (backdrop) {
      backdrop.addEventListener('click', (e) => {
        if (e.target === backdrop) closeDrawer();
      });
    }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && backdrop && backdrop.classList.contains('active')) {
        closeDrawer();
      }
    });

    if (sampleCta) {
      sampleCta.addEventListener('click', () => {
        if (favourites.length === 0) return;
        closeDrawer();

        const itemNames = favourites.map(f => `${f.name} (${f.series || 'UltraShield'})`).join(', ');
        const notes = `Saved finishes from wishlist: ${itemNames}`;

        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal', {
          detail: {
            color: favourites[0].name,
            notes: notes
          }
        }));

        const notesField = document.getElementById('ntw-input-address');
        if (notesField && !notesField.value) {
          notesField.value = notes;
        }
      });
    }

    // Global listener for toggling favorites from other components
    window.addEventListener('ntw:toggle-favourite', (e) => {
      if (!e.detail || !e.detail.id) return;
      toggleItem(e.detail);
    });

    window.addEventListener('ntw:open-favourites', () => {
      openDrawer();
    });
  }

  function openDrawer() {
    const backdrop = document.getElementById('ntw-fav-backdrop');
    if (backdrop) {
      backdrop.classList.add('active');
      backdrop.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeDrawer() {
    const backdrop = document.getElementById('ntw-fav-backdrop');
    if (backdrop) {
      backdrop.classList.remove('active');
      backdrop.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  function toggleItem(item) {
    const existingIndex = favourites.findIndex(f => f.id === item.id);
    if (existingIndex >= 0) {
      favourites.splice(existingIndex, 1);
    } else {
      favourites.push({
        id: item.id,
        name: item.name || 'UltraShield Finish',
        series: item.series || 'UltraShield Naturale',
        image: item.image || '/product-images/deck.jpg'
      });
    }
    saveFavourites();
    updateUI();
    syncHeartButtons();
  }

  function removeItem(id) {
    favourites = favourites.filter(f => f.id !== id);
    saveFavourites();
    updateUI();
    syncHeartButtons();
  }

  function updateUI() {
    const badge = document.getElementById('ntw-fav-badge');
    const body = document.getElementById('ntw-fav-body');
    const sampleCta = document.getElementById('ntw-fav-sample-cta');

    if (badge) badge.textContent = favourites.length;

    if (sampleCta) {
      sampleCta.disabled = (favourites.length === 0);
      sampleCta.querySelector('span').textContent = `Request Samples for Saved (${favourites.length})`;
    }

    if (!body) return;

    if (favourites.length === 0) {
      body.innerHTML = `
        <div class="ntw-fav-empty">
          <svg class="ntw-fav-empty-icon" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
          <div class="ntw-fav-empty-title">Your saved finishes list is empty</div>
          <p class="ntw-fav-empty-text">Click the heart icon on any color swatch, category card, or product to save finishes for your project.</p>
        </div>
      `;
      return;
    }

    body.innerHTML = favourites.map(item => `
      <div class="ntw-fav-item" id="fav-item-${escapeHtml(item.id)}">
        <img src="${escapeHtml(item.image)}" alt="${escapeHtml(item.name)}" class="ntw-fav-item-thumb" />
        <div class="ntw-fav-item-info">
          <div class="ntw-fav-item-name">${escapeHtml(item.name)}</div>
          <div class="ntw-fav-item-series">${escapeHtml(item.series)}</div>
        </div>
        <button type="button" class="ntw-fav-item-remove" data-remove="${escapeHtml(item.id)}" title="Remove ${escapeHtml(item.name)}">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
        </button>
      </div>
    `).join('');

    body.querySelectorAll('.ntw-fav-item-remove').forEach(btn => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-remove');
        removeItem(id);
      });
    });
  }

  function injectHeartButtons() {
    // Inject heart toggle on the Color Swatch Explorer card
    const swatchContent = document.querySelector('.ntw-se-content');
    if (swatchContent && !swatchContent.querySelector('.ntw-heart-toggle-btn')) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'ntw-heart-toggle-btn';
      btn.setAttribute('aria-label', 'Save finish to favourites');
      btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`;
      btn.style.marginLeft = 'auto';

      btn.addEventListener('click', () => {
        const title = (document.querySelector('.ntw-se-title') || {}).textContent || 'Peruvian Teak';
        const series = (document.querySelector('.ntw-se-series') || {}).textContent || 'UltraShield Naturale';
        const img = (document.querySelector('.ntw-se-img') || {}).getAttribute('src') || '/product-images/deck.jpg';
        toggleItem({
          id: `swatch-${title.toLowerCase().replace(/\s+/g, '-')}`,
          name: title,
          series: series,
          image: img
        });
      });

      const metaRow = swatchContent.querySelector('.ntw-se-meta-row');
      if (metaRow) metaRow.appendChild(btn);
    }
  }

  function syncHeartButtons() {
    const swatchBtn = document.querySelector('.ntw-se-content .ntw-heart-toggle-btn');
    if (swatchBtn) {
      const title = (document.querySelector('.ntw-se-title') || {}).textContent || 'Peruvian Teak';
      const id = `swatch-${title.toLowerCase().replace(/\s+/g, '-')}`;
      const isFav = favourites.some(f => f.id === id);
      swatchBtn.classList.toggle('is-active', isFav);
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
})();
