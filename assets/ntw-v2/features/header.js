/**
 * NTW v2: Navigation & Header Enhancement Engine (N1 - N12)
 *
 * Implements:
 * - N1: Header Favourites count badges, bump animation, opens F13 finish drawer
 * - N2: Desktop prominent CTA button ("Order Free Samples") next to CONTACT US
 * - N3: "Material Calculator" quick link in utility bar and Resources menu
 * - N4: "Experience Centres" offset-compensated smooth scrolling
 * - N5: "Resources" Mega Menu linking built features
 * - N6: Dynamic Mega Menu side promo preview with 0.25s crossfade on sub-link hover
 * - N7: Debounced hover-intent timers (150ms open delay, 250ms close delay), click-outside dismiss, and Esc handler
 * - N8: Keyboard navigation (Arrow keys, Home, End, visible high-contrast focus ring)
 * - N9: High-visibility Skip Link focus support
 * - N10: Active page underline indicator and aria-current="page"
 * - N11: Mobile Drawer upgrades (Search field, Favourites row, touch swipe-left dismiss, focus trap)
 * - N12: Optional smart scroll direction & transparent hero header motion (configurable via flags)
 */

(function () {
  'use strict';

  // Configurable Flags for N12 Optional Header Motion
  const HEADER_CONFIG = {
    enableSmartScroll: true,      // Hide on scroll down, show on scroll up
    enableTransparentHero: true   // Transparent over hero video, turning solid after 80px
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAllHeaderFeatures);
  } else {
    initAllHeaderFeatures();
  }

  function initAllHeaderFeatures() {
    renderUtilityBar();
    initDesktopNavActions();
    initStickyHeaderMotion();
    initHoverIntentAndDismiss();
    initKeyboardNavigation();
    initActivePageHighlight();
    injectMegaMenuPromos();
    initMobileDrawer();
    initFavouritesSync();
    initSmoothScrollOffset();
  }

  /* --------------------------------------------------------------------------
     1. Top Utility Bar (N1, N3, N4)
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
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
            <span>+91 98241 44670</span>
          </a>
          <span class="ntw-utility-badge">Official India Partner: Lumber Life</span>
        </div>
        <div class="ntw-utility-right">
          <a href="/#experience-centre" class="ntw-utility-item" id="ntw-utility-centre-link">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
            <span>Experience Centres</span>
          </a>
          <button type="button" class="ntw-utility-item ntw-utility-fav-btn" id="ntw-utility-fav-btn" aria-label="View Saved Items">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            <span>Favourites</span>
            <span class="ntw-fav-count-badge" id="ntw-utility-fav-count">0</span>
          </button>
          <a href="/login/index.html" class="ntw-utility-item">
            <span>Architect &amp; Trade Portal</span>
          </a>
          <button type="button" class="ntw-utility-search-btn" id="ntw-utility-search-trigger" aria-label="Open Search (Ctrl+K)">
            <svg viewBox="0 0 24 24" style="width:13px;height:13px;fill:currentColor;" aria-hidden="true"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
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

    // Bind Utility Favourites Button
    const favBtn = bar.querySelector('#ntw-utility-fav-btn');
    if (favBtn) {
      favBtn.addEventListener('click', openFavouritesDrawer);
    }
  }

  /* --------------------------------------------------------------------------
     2. Desktop Navbar Actions (N1, N2)
     -------------------------------------------------------------------------- */
  function initDesktopNavActions() {
    const desktopFav = document.getElementById('ntw-header-fav-btn');
    if (desktopFav) {
      desktopFav.addEventListener('click', openFavouritesDrawer);
    }

    const sampleCta = document.getElementById('ntw-nav-sample-cta');
    if (sampleCta) {
      sampleCta.addEventListener('click', (e) => {
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
     3. Sticky Header Motion & Smart Scroll (N12)
     -------------------------------------------------------------------------- */
  function initStickyHeaderMotion() {
    const header = document.querySelector('.elementor-location-header');
    if (!header) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    // Check if on home page for transparent hero
    const isHomePage = window.location.pathname === '/' || window.location.pathname === '/index.html' || window.location.pathname.endsWith('/');

    function updateHeaderMotion() {
      const currentScrollY = window.scrollY;

      // 1. Sticky Shrink (Always active)
      if (currentScrollY > 60) {
        header.classList.add('ntw-header-shrunk');
      } else {
        header.classList.remove('ntw-header-shrunk');
      }

      // 2. Smart Scroll Hide/Show
      if (HEADER_CONFIG.enableSmartScroll) {
        if (currentScrollY > 140 && currentScrollY > lastScrollY && (currentScrollY - lastScrollY > 6)) {
          // Scrolling down -> hide header
          header.classList.add('ntw-header-hidden');
          header.classList.remove('ntw-header-visible');
        } else if (currentScrollY < lastScrollY && (lastScrollY - currentScrollY > 6)) {
          // Scrolling up -> show header
          header.classList.remove('ntw-header-hidden');
          header.classList.add('ntw-header-visible');
        }
      }

      // 3. Hero Video Transparency
      if (HEADER_CONFIG.enableTransparentHero && isHomePage) {
        if (currentScrollY < 80) {
          header.classList.add('ntw-header-transparent');
        } else {
          header.classList.remove('ntw-header-transparent');
        }
      }

      lastScrollY = currentScrollY;
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateHeaderMotion);
        ticking = true;
      }
    }, { passive: true });

    // Initial check
    updateHeaderMotion();
  }

  /* --------------------------------------------------------------------------
     4. Hover Intent & Dismiss Protocol (N7)
     -------------------------------------------------------------------------- */
  function initHoverIntentAndDismiss() {
    const menuItems = document.querySelectorAll('.e-n-menu-item');
    if (!menuItems.length) return;

    const OPEN_DELAY_MS = 150;
    const CLOSE_DELAY_MS = 250;

    menuItems.forEach((item) => {
      const dropdown = item.querySelector('.e-n-menu-content');
      const toggleBtn = item.querySelector('.e-n-menu-dropdown-icon');
      if (!dropdown || !toggleBtn) return;

      let openTimer = null;
      let closeTimer = null;

      function openMenu() {
        clearTimeout(closeTimer);
        // Exclusivity: close other open dropdowns immediately
        closeAllDropdowns(item);

        toggleBtn.setAttribute('aria-expanded', 'true');
        const con = dropdown.querySelector('.e-con');
        if (con) con.classList.add('e-active');
        item.classList.add('ntw-hover-open');
      }

      function closeMenu() {
        clearTimeout(openTimer);
        toggleBtn.setAttribute('aria-expanded', 'false');
        const con = dropdown.querySelector('.e-con');
        if (con) con.classList.remove('e-active');
        item.classList.remove('ntw-hover-open');
      }

      // Hover on desktop (> 991px)
      item.addEventListener('mouseenter', () => {
        if (window.innerWidth <= 991) return;
        clearTimeout(closeTimer);
        openTimer = setTimeout(openMenu, OPEN_DELAY_MS);
      });

      item.addEventListener('mouseleave', () => {
        if (window.innerWidth <= 991) return;
        clearTimeout(openTimer);
        closeTimer = setTimeout(closeMenu, CLOSE_DELAY_MS);
      });

      // Click on dropdown trigger button
      toggleBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const isOpen = toggleBtn.getAttribute('aria-expanded') === 'true';
        if (isOpen) {
          closeMenu();
        } else {
          openMenu();
        }
      });
    });

    // Dismiss on click outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.e-n-menu-wrapper')) {
        closeAllDropdowns();
      }
    });

    // Dismiss on Escape key & return focus to trigger
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const openItem = document.querySelector('.e-n-menu-item.ntw-hover-open');
        if (openItem) {
          const trigger = openItem.querySelector('.e-n-menu-dropdown-icon') || openItem.querySelector('a');
          closeAllDropdowns();
          if (trigger) trigger.focus();
        }
      }
    });

    function closeAllDropdowns(exceptItem) {
      menuItems.forEach((m) => {
        if (m === exceptItem) return;
        const btn = m.querySelector('.e-n-menu-dropdown-icon');
        const con = m.querySelector('.e-n-menu-content .e-con');
        if (btn) btn.setAttribute('aria-expanded', 'false');
        if (con) con.classList.remove('e-active');
        m.classList.remove('ntw-hover-open');
      });
    }
  }

  /* --------------------------------------------------------------------------
     5. Full Keyboard Navigation (N8)
     -------------------------------------------------------------------------- */
  function initKeyboardNavigation() {
    const topMenuItems = Array.from(document.querySelectorAll('.e-n-menu-heading > .e-n-menu-item'));
    if (!topMenuItems.length) return;

    topMenuItems.forEach((item, index) => {
      const trigger = item.querySelector('.e-n-menu-dropdown-icon') || item.querySelector('.e-n-menu-title-container a') || item.querySelector('.e-n-menu-title-text');
      const dropdown = item.querySelector('.e-n-menu-content');

      if (trigger) {
        trigger.setAttribute('tabindex', '0');
        trigger.addEventListener('keydown', (e) => {
          // Arrow Right -> Next top-level item
          if (e.key === 'ArrowRight') {
            e.preventDefault();
            const nextIdx = (index + 1) % topMenuItems.length;
            const nextTrigger = topMenuItems[nextIdx].querySelector('.e-n-menu-dropdown-icon') || topMenuItems[nextIdx].querySelector('a');
            if (nextTrigger) nextTrigger.focus();
          }

          // Arrow Left -> Previous top-level item
          if (e.key === 'ArrowLeft') {
            e.preventDefault();
            const prevIdx = (index - 1 + topMenuItems.length) % topMenuItems.length;
            const prevTrigger = topMenuItems[prevIdx].querySelector('.e-n-menu-dropdown-icon') || topMenuItems[prevIdx].querySelector('a');
            if (prevTrigger) prevTrigger.focus();
          }

          // Arrow Down -> Open dropdown & focus first link
          if (e.key === 'ArrowDown' && dropdown) {
            e.preventDefault();
            const toggleBtn = item.querySelector('.e-n-menu-dropdown-icon');
            if (toggleBtn) toggleBtn.setAttribute('aria-expanded', 'true');
            const con = dropdown.querySelector('.e-con');
            if (con) con.classList.add('e-active');
            item.classList.add('ntw-hover-open');

            const firstLink = dropdown.querySelector('a, button');
            if (firstLink) firstLink.focus();
          }
        });
      }

      // Sub-menu arrow navigation inside dropdown
      if (dropdown) {
        const subLinks = Array.from(dropdown.querySelectorAll('a, button'));
        subLinks.forEach((subLink, subIdx) => {
          subLink.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
              e.preventDefault();
              const nextSub = subLinks[(subIdx + 1) % subLinks.length];
              if (nextSub) nextSub.focus();
            } else if (e.key === 'ArrowUp') {
              e.preventDefault();
              if (subIdx === 0) {
                if (trigger) trigger.focus();
              } else {
                const prevSub = subLinks[subIdx - 1];
                if (prevSub) prevSub.focus();
              }
            } else if (e.key === 'Home') {
              e.preventDefault();
              subLinks[0].focus();
            } else if (e.key === 'End') {
              e.preventDefault();
              subLinks[subLinks.length - 1].focus();
            }
          });
        });
      }
    });
  }

  /* --------------------------------------------------------------------------
     6. Active Page Highlight (N10)
     -------------------------------------------------------------------------- */
  function initActivePageHighlight() {
    function applyActiveHighlight() {
      const currentPath = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
      const currentHash = window.location.hash;

      const navLinks = document.querySelectorAll('.e-n-menu a, .ntw-drawer-nav a');
      let matched = false;

      navLinks.forEach((link) => {
        link.classList.remove('ntw-nav-active');
        link.removeAttribute('aria-current');

        const href = link.getAttribute('href');
        if (!href) return;

        const normalizedHref = href.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';

        // Match hash or path
        if (currentHash && href.includes(currentHash)) {
          link.classList.add('ntw-nav-active');
          link.setAttribute('aria-current', 'page');
          const parentItem = link.closest('.e-n-menu-item');
          if (parentItem) parentItem.classList.add('ntw-nav-active');
          matched = true;
        } else if (!currentHash && normalizedHref !== '/' && currentPath === normalizedHref) {
          link.classList.add('ntw-nav-active');
          link.setAttribute('aria-current', 'page');
          const parentItem = link.closest('.e-n-menu-item');
          if (parentItem) parentItem.classList.add('ntw-nav-active');
          matched = true;
        }
      });

      if (!matched && (currentPath === '/' || window.location.pathname.includes('index.html'))) {
        const firstMenuItem = document.querySelector('.e-n-menu-item');
        if (firstMenuItem) {
          firstMenuItem.classList.add('ntw-nav-active');
          const titleText = firstMenuItem.querySelector('.e-n-menu-title-text');
          if (titleText) titleText.setAttribute('aria-current', 'page');
        }
      }
    }

    applyActiveHighlight();
    window.addEventListener('hashchange', applyActiveHighlight);
  }

  /* --------------------------------------------------------------------------
     7. Mega Menu Promo Panels with Dynamic Hover Preview (N6)
     -------------------------------------------------------------------------- */
  function injectMegaMenuPromos() {
    const productsMenu = document.querySelector('.ntw-products-grid-inner');
    if (!productsMenu) return;

    const MEGA_PREVIEWS = {
      'decking': {
        tag: 'UltraShield® Decking',
        img: '/product-images/deck.jpg',
        title: 'UltraShield® 360 Capping',
        desc: 'Zero staining, mold resistance, and 25-year structural warranty engineered for India\'s climate.'
      },
      'cladding': {
        tag: 'All-Weather Cladding',
        img: '/product-images/clads.jpg',
        title: 'Architectural Wall Cladding',
        desc: 'Castellation, Shadowline & Noir fluted profiles for contemporary exterior and interior facades.'
      },
      'beams': {
        tag: 'Screening & Louvers',
        img: '/product-images/twix.jpg',
        title: 'Architectural Louvers & Beams',
        desc: 'Lightweight composite battens and sun-shading pergolas for private villas and hospitality hubs.'
      },
      'deck-tiles': {
        tag: 'QuickDeck System',
        img: '/wp-content/uploads/2021/01/09-ultrashield-deck-tiles.png',
        title: 'Interlocking Deck Tiles',
        desc: 'Instant click-lock modular tiles for balconies, terraces, and garden patios without joist substructure.'
      },
      'fencing': {
        tag: 'UltraEasy Fencing',
        img: '/wp-content/uploads/2019/01/composite-deck-with-fence.jpg',
        title: 'Composite Privacy Fencing',
        desc: 'Tongue-and-groove composite panels with powder-coated aluminum posts for zero maintenance.'
      },
      'railing': {
        tag: 'Railing Systems',
        img: '/wp-content/uploads/2019/01/deck-and-railing.jpg',
        title: 'Composite & Aluminum Railing',
        desc: 'Engineered balustrades and handrails offering structural safety, elegance, and durability.'
      },
      'planter-box': {
        tag: 'Modular Planters',
        img: '/wp-content/uploads/2018/12/NewTechWood-Planter-Box-13.jpg',
        title: 'Modular Planter Boxes',
        desc: 'Weatherproof composite planters resistant to water rot and root expansion.'
      }
    };

    let promo = productsMenu.querySelector('.ntw-mega-promo');
    if (!promo) {
      promo = document.createElement('div');
      promo.className = 'ntw-mega-promo';
      promo.innerHTML = `
        <div>
          <span class="ntw-mega-promo-tag">${MEGA_PREVIEWS.decking.tag}</span>
          <div class="ntw-mega-promo-img-wrap">
            <img src="${MEGA_PREVIEWS.decking.img}" alt="NewTechWood Composite System" class="ntw-mega-promo-img" loading="lazy" />
          </div>
          <h4 class="ntw-mega-promo-title">${MEGA_PREVIEWS.decking.title}</h4>
          <p class="ntw-mega-promo-desc">${MEGA_PREVIEWS.decking.desc}</p>
        </div>
        <a href="/#ntw-sample-request" class="ntw-mega-promo-btn" id="ntw-mega-sample-btn">
          <span>Order Free Sample Kit</span>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
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

    // Dynamic Preview Crossfade on sub-category hover/focus
    const promoImg = promo.querySelector('.ntw-mega-promo-img');
    const promoTag = promo.querySelector('.ntw-mega-promo-tag');
    const promoTitle = promo.querySelector('.ntw-mega-promo-title');
    const promoDesc = promo.querySelector('.ntw-mega-promo-desc');

    function updatePreview(key) {
      const data = MEGA_PREVIEWS[key];
      if (!data) return;

      promo.classList.add('ntw-text-fading');
      if (promoImg) promoImg.classList.add('ntw-crossfading');

      setTimeout(() => {
        if (promoTag) promoTag.textContent = data.tag;
        if (promoTitle) promoTitle.textContent = data.title;
        if (promoDesc) promoDesc.textContent = data.desc;
        if (promoImg) {
          promoImg.src = data.img;
          promoImg.classList.remove('ntw-crossfading');
        }
        promo.classList.remove('ntw-text-fading');
      }, 140);
    }

    // Attach listener to each column's links
    const columns = productsMenu.querySelectorAll('.ntw-mega-col');
    columns.forEach((col) => {
      const heading = col.querySelector('.elementor-heading-title a') || col.querySelector('.elementor-heading-title');
      const headingText = heading ? heading.textContent.trim().toLowerCase() : '';
      let categoryKey = 'decking';

      if (headingText.includes('decking')) categoryKey = 'decking';
      else if (headingText.includes('cladding')) categoryKey = 'cladding';
      else if (headingText.includes('beam')) categoryKey = 'beams';
      else if (headingText.includes('tile')) categoryKey = 'deck-tiles';
      else if (headingText.includes('fenc')) categoryKey = 'fencing';
      else if (headingText.includes('rail')) categoryKey = 'railing';
      else if (headingText.includes('planter')) categoryKey = 'planter-box';

      const links = col.querySelectorAll('a');
      links.forEach((l) => {
        l.addEventListener('mouseenter', () => updatePreview(categoryKey));
        l.addEventListener('focus', () => updatePreview(categoryKey));
      });
    });

    // Reset to default on mouseleave
    productsMenu.addEventListener('mouseleave', () => {
      updatePreview('decking');
    });
  }

  /* --------------------------------------------------------------------------
     8. Accessible Mobile Drawer with Accordions & Swipe Dismiss (N11)
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
            <svg viewBox="0 0 24 24" style="width:20px;height:20px;fill:currentColor;" aria-hidden="true"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>

        <div class="ntw-drawer-search-wrap">
          <form class="ntw-drawer-search-form" id="ntw-drawer-search-form" action="/#search" onsubmit="return false;">
            <input type="search" class="ntw-drawer-search-input" id="ntw-drawer-search-input" placeholder="Search products, finishes, projects..." aria-label="Search site" />
            <button type="submit" class="ntw-drawer-search-submit" aria-label="Submit Search">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
            </button>
          </form>
        </div>

        <a href="#ntw-saved-finishes" class="ntw-drawer-fav-link" id="ntw-drawer-fav-link">
          <div class="ntw-drawer-fav-left">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            <span>Saved Finishes</span>
          </div>
          <span class="ntw-fav-count-badge" id="ntw-drawer-fav-count">0</span>
        </a>

        <nav class="ntw-drawer-nav" aria-label="Mobile Directory">
          
          <!-- Accordion 1: Why NewTechWood? -->
          <div class="ntw-accordion-item">
            <button type="button" class="ntw-accordion-trigger" aria-expanded="false" aria-controls="ntw-drawer-why-panel">
              <span>Why NewTechWood?</span>
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
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
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
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
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
            </button>
            <div class="ntw-accordion-panel" id="ntw-drawer-proj-panel">
              <a href="/projects/#national" class="ntw-drawer-sublink"><strong>National Projects (India)</strong></a>
              <a href="/projects/#international" class="ntw-drawer-sublink">International Landmarks</a>
              <a href="/projects/" class="ntw-drawer-sublink">All Architectural Case Studies</a>
            </div>
          </div>

          <!-- Accordion 4: Resources (N5) -->
          <div class="ntw-accordion-item">
            <button type="button" class="ntw-accordion-trigger" aria-expanded="false" aria-controls="ntw-drawer-res-panel">
              <span>Resources &amp; Tools</span>
              <svg class="ntw-accordion-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
            </button>
            <div class="ntw-accordion-panel" id="ntw-drawer-res-panel">
              <a href="/#ntw-color-swatch-explorer" class="ntw-drawer-sublink"><strong>Colour Swatch Explorer</strong></a>
              <a href="/#ntw-brochures-block" class="ntw-drawer-sublink">Architectural Catalogues &amp; Flipbook</a>
              <a href="/projects/" class="ntw-drawer-sublink">Project Portfolio &amp; Gallery</a>
            </div>
          </div>

          <!-- Direct Links -->
          <a href="/#experience-centre" class="ntw-drawer-direct-link">Experience Centres &amp; Studios</a>
          <a href="/contact/" class="ntw-drawer-direct-link">Contact Us</a>
          <a href="/login/index.html" class="ntw-drawer-direct-link">Architect &amp; Trade Portal</a>

        </nav>

        <div class="ntw-drawer-footer">
          <button type="button" class="ntw-drawer-cta-primary" id="ntw-drawer-sample-btn">
            <svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:currentColor;" aria-hidden="true"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm6 12H6v-1.4c0-2 4-3.1 6-3.1s6 1.1 6 3.1V18z"/></svg>
            <span>Request Free Sample Box</span>
          </button>
          <div class="ntw-drawer-contact-row">
            <a href="tel:+919824144670" class="ntw-drawer-contact-btn">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
              <span>Call Us</span>
            </a>
            <a href="https://wa.me/919824144670?text=Hello%20NewTechWood%20India%2C%20I%20would%20like%20to%20inquire%20about%20your%20products." target="_blank" rel="noopener noreferrer" class="ntw-drawer-contact-btn">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38c1.45.79 3.08 1.21 4.74 1.21 5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.816 9.816 0 0 0 12.04 2zm.01 1.67c2.2 0 4.26.86 5.82 2.42a8.225 8.225 0 0 1 2.41 5.83c0 4.54-3.7 8.24-8.24 8.24-1.42 0-2.82-.37-4.06-1.07l-.29-.17-3.12.82.83-3.04-.19-.3a8.21 8.21 0 0 1-1.26-4.48c0-4.54 3.7-8.24 8.24-8.24zm4.52 11.66c-.25-.13-1.47-.72-1.7-.81-.23-.08-.39-.13-.56.13-.17.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.13-1.05-.39-2-1.23-.74-.66-1.24-1.47-1.39-1.72-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.13-.14.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.56-1.35-.77-1.85-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.44.06-.67.31-.23.25-.88.86-.88 2.1 0 1.24.9 2.44 1.03 2.61.13.17 1.78 2.72 4.31 3.81.6.26 1.07.42 1.44.54.61.19 1.16.16 1.6.1.49-.07 1.47-.6 1.68-1.18.21-.59.21-1.09.15-1.18-.06-.09-.23-.15-.48-.28z"/></svg>
              <span>WhatsApp</span>
            </a>
          </div>
        </div>

      </div>
    `;

    document.body.appendChild(drawerRoot);

    // Accordions
    const accordionTriggers = drawerRoot.querySelectorAll('.ntw-accordion-trigger');
    accordionTriggers.forEach((trigger) => {
      trigger.addEventListener('click', () => {
        const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
        const panelId = trigger.getAttribute('aria-controls');
        const panel = document.getElementById(panelId);

        // Close other accordions
        accordionTriggers.forEach((t) => {
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
    document.querySelectorAll('#menu-toggle-185').forEach((toggle) => {
      toggle.addEventListener('click', (e) => {
        if (window.innerWidth <= 991) {
          e.preventDefault();
          e.stopPropagation();
          openDrawer();
        }
      });
    });

    // Drawer Search Form
    const searchForm = drawerRoot.querySelector('#ntw-drawer-search-form');
    const searchInput = drawerRoot.querySelector('#ntw-drawer-search-input');
    if (searchForm && searchInput) {
      searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const term = searchInput.value.trim();
        closeDrawer();
        window.dispatchEvent(new CustomEvent('ntw:open-search', { detail: { query: term } }));
      });
    }

    // Drawer Favourites Link
    const drawerFav = drawerRoot.querySelector('#ntw-drawer-fav-link');
    if (drawerFav) {
      drawerFav.addEventListener('click', (e) => {
        e.preventDefault();
        closeDrawer();
        openFavouritesDrawer();
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

    // Touch Swipe-Left to dismiss drawer
    let touchStartX = 0;
    let touchStartY = 0;
    drawerRoot.addEventListener('touchstart', (e) => {
      if (!e.changedTouches || !e.changedTouches.length) return;
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    drawerRoot.addEventListener('touchend', (e) => {
      if (!e.changedTouches || !e.changedTouches.length) return;
      const diffX = e.changedTouches[0].screenX - touchStartX;
      const diffY = e.changedTouches[0].screenY - touchStartY;
      // Swiped left by > 50px
      if (diffX < -50 && Math.abs(diffX) > Math.abs(diffY)) {
        closeDrawer();
      }
    }, { passive: true });

    // Focus Trap inside drawer when open
    drawerRoot.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab' || !drawerRoot.classList.contains('is-open')) return;
      const focusables = Array.from(drawerRoot.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'))
        .filter((el) => !el.hasAttribute('disabled') && el.offsetParent !== null);
      if (!focusables.length) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

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
      const toggleBtn = document.querySelector('#menu-toggle-185');
      if (toggleBtn) toggleBtn.focus();
    }
  }

  /* --------------------------------------------------------------------------
     9. Favourites Live Synchronization (N1)
     -------------------------------------------------------------------------- */
  function openFavouritesDrawer(e) {
    if (e && e.preventDefault) e.preventDefault();
    const favBackdrop = document.getElementById('ntw-fav-backdrop');
    if (favBackdrop) {
      favBackdrop.classList.add('active');
      favBackdrop.classList.add('is-open');
      favBackdrop.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      const closeBtn = document.getElementById('ntw-fav-close') || document.getElementById('ntw-fav-close-btn');
      if (closeBtn) closeBtn.focus();
    }
    window.dispatchEvent(new CustomEvent('ntw:open-favourites'));
  }

  function initFavouritesSync() {
    function updateFavouritesCount() {
      let count = 0;
      try {
        const saved = JSON.parse(localStorage.getItem('ntw_favourites_v2') || '[]');
        count = Array.isArray(saved) ? saved.length : 0;
      } catch (err) {
        count = 0;
      }

      const badges = document.querySelectorAll('.ntw-fav-count-badge');
      badges.forEach((b) => {
        b.textContent = count;
        b.classList.remove('ntw-fav-bump');
        void b.offsetWidth; // Force CSS repaint
        b.classList.add('ntw-fav-bump');
      });
    }

    // Initial count
    updateFavouritesCount();

    // Event listeners
    window.addEventListener('storage', updateFavouritesCount);
    window.addEventListener('ntw:favourites-updated', updateFavouritesCount);
  }

  /* --------------------------------------------------------------------------
     10. Smooth Scrolling with Sticky Offset (N3, N4)
     -------------------------------------------------------------------------- */
  function initSmoothScrollOffset() {
    const selector = 'a[href*="#experience-centre"], a[href*="#ntw-color-swatch-explorer"], a[href*="#ntw-brochures-block"]';
    document.querySelectorAll(selector).forEach((link) => {
      link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        if (!href || !href.includes('#')) return;

        const hash = href.split('#')[1];
        if (!hash) return;

        const target = document.getElementById(hash);
        if (target && (window.location.pathname === '/' || window.location.pathname === '/index.html' || window.location.pathname.endsWith('/'))) {
          e.preventDefault();
          const header = document.querySelector('.elementor-location-header');
          const offset = header ? header.offsetHeight + 10 : 80;
          const targetTop = target.getBoundingClientRect().top + window.pageYOffset - offset;

          window.scrollTo({
            top: targetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  }

})();
