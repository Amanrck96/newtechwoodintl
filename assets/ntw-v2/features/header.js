/**
 * F1: Header Enhancements
 * - Top Utility Bar with phone, sample kit CTA, experience centres, trade login & search trigger
 * - Sticky Header shrink on scroll
 * - Mega Menu Promo Panel (rich featured imagery + CTA)
 * - Accessible Mobile Drawer with collapsible accordions
 */

(function () {
  'use strict';

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeaderEnhancements);
  } else {
    initHeaderEnhancements();
  }

  function initHeaderEnhancements() {
    renderUtilityBar();
    initStickyHeaderShrink();
    injectMegaMenuPromos();
    initMobileDrawer();
  }

  /* --------------------------------------------------------------------------
     1. Utility Top Bar
     -------------------------------------------------------------------------- */
  function renderUtilityBar() {
    if (document.getElementById('ntw-utility-bar')) return;

    const header = document.querySelector('.elementor-location-header') || document.querySelector('header');
    if (!header) return;

    const bar = document.createElement('div');
    bar.id = 'ntw-utility-bar';
    bar.className = 'ntw-utility-bar';
    bar.innerHTML = `
      <div class="ntw-utility-inner">
        <div class="ntw-utility-left">
          <a href="tel:+919824144670" class="ntw-utility-item" aria-label="Call NewTechWood India Support">
            <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
            <span>+91 98241 44670</span>
          </a>
          <span class="ntw-utility-badge">Official India Partner: Lumber Life</span>
        </div>
        <div class="ntw-utility-right">
          <a href="/#experience-centre" class="ntw-utility-item">
            <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
            <span>Experience Centres</span>
          </a>
          <a href="/#ntw-sample-request" class="ntw-utility-item" id="ntw-utility-sample-link">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V18z"/></svg>
            <span>Order Samples</span>
          </a>
          <a href="/login/index.html" class="ntw-utility-item">
            <span>Architect &amp; Trade Portal</span>
          </a>
          <button type="button" class="ntw-utility-search-btn" id="ntw-utility-search-trigger" aria-label="Open Search (Ctrl+K)">
            <svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:currentColor;"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            <span>Search</span>
            <kbd class="ntw-utility-kbd">Ctrl K</kbd>
          </button>
        </div>
      </div>
    `;

    header.parentNode.insertBefore(bar, header);

    // Bind Search Trigger
    const searchTrigger = bar.querySelector('#ntw-utility-search-trigger');
    if (searchTrigger) {
      searchTrigger.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('ntw:open-search'));
      });
    }

    // Bind Sample Link
    const sampleLink = bar.querySelector('#ntw-utility-sample-link');
    if (sampleLink) {
      sampleLink.addEventListener('click', (e) => {
        e.preventDefault();
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal'));
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

  /* --------------------------------------------------------------------------
     2. Sticky Header Shrink on Scroll
     -------------------------------------------------------------------------- */
  function initStickyHeaderShrink() {
    const header = document.querySelector('.elementor-location-header');
    if (!header) return;

    let ticking = false;

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > 60) {
            header.classList.add('ntw-header-shrunk');
          } else {
            header.classList.remove('ntw-header-shrunk');
          }
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  /* --------------------------------------------------------------------------
     3. Mega Menu Promo Panels (Desktop)
     -------------------------------------------------------------------------- */
  function injectMegaMenuPromos() {
    // Products dropdown
    const productsMenu = document.querySelector('.ntw-products-grid-inner');
    if (productsMenu && !productsMenu.querySelector('.ntw-mega-promo')) {
      const promo = document.createElement('div');
      promo.className = 'ntw-mega-promo';
      promo.innerHTML = `
        <div>
          <span class="ntw-mega-promo-tag">Featured System</span>
          <div class="ntw-mega-promo-img-wrap">
            <img src="/product-images/deck.jpg" alt="NewTechWood UltraShield Decking" class="ntw-mega-promo-img" loading="lazy" />
          </div>
          <h4 class="ntw-mega-promo-title">UltraShield® 360 Capping</h4>
          <p class="ntw-mega-promo-desc">Zero staining, mold resistance, and 25-year structural warranty engineered for India's weather.</p>
        </div>
        <a href="/#ntw-sample-request" class="ntw-mega-promo-btn" id="ntw-mega-sample-btn">
          <span>Order Free Sample Kit</span>
          <svg viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </a>
      `;
      productsMenu.appendChild(promo);

      const btn = promo.querySelector('#ntw-mega-sample-btn');
      if (btn) {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          window.dispatchEvent(new CustomEvent('ntw:open-sample-modal'));
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
  }

  /* --------------------------------------------------------------------------
     4. Accessible Mobile Drawer & Accordions
     -------------------------------------------------------------------------- */
  function initMobileDrawer() {
    if (document.getElementById('ntw-mobile-drawer-root')) return;

    const drawerRoot = document.createElement('div');
    drawerRoot.id = 'ntw-mobile-drawer-root';
    drawerRoot.className = 'ntw-drawer-backdrop';
    drawerRoot.setAttribute('aria-hidden', 'true');

    drawerRoot.innerHTML = `
      <div class="ntw-mobile-drawer" role="dialog" aria-modal="true" aria-label="Mobile Navigation Menu">
        
        <div class="ntw-drawer-header">
          <img src="/wp-content/uploads/2025/07/newtechwood-site-logo.svg" alt="NewTechWood" class="ntw-drawer-logo" />
          <button type="button" class="ntw-drawer-close" id="ntw-drawer-close-btn" aria-label="Close navigation menu">
            <svg viewBox="0 0 24 24" style="width:20px;height:20px;fill:currentColor;"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>

        <div class="ntw-drawer-search-wrap">
          <button type="button" class="ntw-drawer-search-btn" id="ntw-drawer-search-trigger">
            <svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            <span>Search products, projects, articles...</span>
          </button>
        </div>

        <nav class="ntw-drawer-nav" aria-label="Mobile Directory">
          
          <!-- Accordion 1: Why NewTechWood? -->
          <div class="ntw-accordion-item">
            <button type="button" class="ntw-accordion-trigger" aria-expanded="false" aria-controls="ntw-drawer-why-panel">
              <span>Why NewTechWood?</span>
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
            </button>
            <div class="ntw-accordion-panel" id="ntw-drawer-why-panel">
              <a href="/history/" class="ntw-drawer-sublink">Brand History</a>
              <a href="/ultrashield-technology/" class="ntw-drawer-sublink">UltraShield Technology</a>
              <a href="/sustainability/" class="ntw-drawer-sublink">Sustainability &amp; Eco Commitment</a>
              <a href="/laboratory/" class="ntw-drawer-sublink">Engineering Laboratory</a>
            </div>
          </div>

          <!-- Accordion 2: Products -->
          <div class="ntw-accordion-item">
            <button type="button" class="ntw-accordion-trigger" aria-expanded="false" aria-controls="ntw-drawer-prod-panel">
              <span>Products</span>
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
            </button>
            <div class="ntw-accordion-panel" id="ntw-drawer-prod-panel">
              <a href="/product/decking/" class="ntw-drawer-sublink"><strong>Decking Systems</strong> (Naturale, Marina, Old World)</a>
              <a href="/product/cladding/" class="ntw-drawer-sublink"><strong>Wall Cladding</strong> (All-Weather, Castellation, Noir)</a>
              <a href="/product/beams/" class="ntw-drawer-sublink"><strong>Architectural Louvers &amp; Beams</strong></a>
              <a href="/product/deck-tiles/" class="ntw-drawer-sublink"><strong>QuickDeck Deck Tiles</strong></a>
              <a href="/product/fencing/" class="ntw-drawer-sublink"><strong>UltraEasy Fencing</strong></a>
              <a href="/product/railing/" class="ntw-drawer-sublink"><strong>Composite &amp; Aluminum Railing</strong></a>
              <a href="/product/planter-box/" class="ntw-drawer-sublink"><strong>Modular Planter Boxes</strong></a>
            </div>
          </div>

          <!-- Accordion 3: Projects -->
          <div class="ntw-accordion-item">
            <button type="button" class="ntw-accordion-trigger" aria-expanded="false" aria-controls="ntw-drawer-proj-panel">
              <span>Projects</span>
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
            </button>
            <div class="ntw-accordion-panel" id="ntw-drawer-proj-panel">
              <a href="/projects/#national" class="ntw-drawer-sublink"><strong>National Projects (India)</strong></a>
              <a href="/projects/#international" class="ntw-drawer-sublink">International Landmarks</a>
              <a href="/projects/" class="ntw-drawer-sublink">All Architectural Case Studies</a>
            </div>
          </div>

          <!-- Direct Links -->
          <a href="/#experience-centre" class="ntw-drawer-direct-link">Experience Centres &amp; Studios</a>
          <a href="/contact/" class="ntw-drawer-direct-link">Contact Us</a>
          <a href="/login/index.html" class="ntw-drawer-direct-link">Architect &amp; Trade Portal</a>

        </nav>

        <div class="ntw-drawer-footer">
          <button type="button" class="ntw-drawer-cta-primary" id="ntw-drawer-sample-btn">
            <svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:currentColor;"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V18z"/></svg>
            <span>Request Free Sample Box</span>
          </button>
          <div class="ntw-drawer-contact-row">
            <a href="tel:+919824144670" class="ntw-drawer-contact-btn">
              <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
              <span>Call Us</span>
            </a>
            <a href="https://wa.me/919824144670?text=Hello%20NewTechWood%20India%2C%20I%20would%20like%20to%20inquire%20about%20your%20products." target="_blank" rel="noopener noreferrer" class="ntw-drawer-contact-btn">
              <svg viewBox="0 0 24 24"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.12.82.83-3.04-.19-.3a8.21 8.21 0 0 1-1.26-4.48c0-4.54 3.7-8.24 8.24-8.24zm4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.54.61.19 1.16.16 1.6.1.49-.07 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.18-.06-.09-.23-.15-.48-.28z"/></svg>
              <span>WhatsApp</span>
            </a>
          </div>
        </div>

      </div>
    `;

    document.body.appendChild(drawerRoot);

    // Accordions
    const accordionTriggers = drawerRoot.querySelectorAll('.ntw-accordion-trigger');
    accordionTriggers.forEach(trigger => {
      trigger.addEventListener('click', () => {
        const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
        const panelId = trigger.getAttribute('aria-controls');
        const panel = document.getElementById(panelId);

        // Close other accordions for clean accordion feel
        accordionTriggers.forEach(t => {
          if (t !== trigger) {
            t.setAttribute('aria-expanded', 'false');
            const otherPanel = document.getElementById(t.getAttribute('aria-controls'));
            if (otherPanel) otherPanel.classList.remove('is-expanded');
          }
        });

        trigger.setAttribute('aria-expanded', !isExpanded);
        if (panel) {
          panel.classList.toggle('is-expanded', !isExpanded);
        }
      });
    });

    // Close Button & Backdrop Click
    const closeBtn = drawerRoot.querySelector('#ntw-drawer-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
    drawerRoot.addEventListener('click', (e) => {
      if (e.target === drawerRoot) closeDrawer();
    });

    // Escape Key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && drawerRoot.classList.contains('is-open')) {
        closeDrawer();
      }
    });

    // Bind Mobile Toggle Button in existing header
    const existingToggle = document.getElementById('menu-toggle-185');
    if (existingToggle) {
      existingToggle.addEventListener('click', (e) => {
        // On mobile/tablet, open our enhanced drawer instead of the standard elementor dropdown
        if (window.innerWidth <= 991) {
          e.preventDefault();
          e.stopPropagation();
          openDrawer();
        }
      });
    }

    // Drawer Search Trigger
    const drawerSearch = drawerRoot.querySelector('#ntw-drawer-search-trigger');
    if (drawerSearch) {
      drawerSearch.addEventListener('click', () => {
        closeDrawer();
        window.dispatchEvent(new CustomEvent('ntw:open-search'));
      });
    }

    // Drawer Sample Button
    const drawerSample = drawerRoot.querySelector('#ntw-drawer-sample-btn');
    if (drawerSample) {
      drawerSample.addEventListener('click', () => {
        closeDrawer();
        window.dispatchEvent(new CustomEvent('ntw:open-sample-modal'));
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

    function openDrawer() {
      drawerRoot.classList.add('is-open');
      drawerRoot.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      if (closeBtn) closeBtn.focus();
    }

    function closeDrawer() {
      drawerRoot.classList.remove('is-open');
      drawerRoot.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
      if (existingToggle) existingToggle.focus();
    }
  }

})();
