# HEADER & NAVIGATION AUDIT (NAV_AUDIT.md)

**Target Branch**: `features-v2`  
**Scope**: Header / Navigation System only (`/assets/ntw-v2/features/header.css`, `header.js`, and header markup in `index.html`)  
**Strict Policy**: CONTENT FREEZE in full effect. Zero existing text/menus rewritten or removed.  
**Role**: Researcher / Auditor  

---

## 1. What Exists in the Header Today

An initial baseline implementation of the header features was introduced in earlier stages:

1. **Top Utility Bar (`#ntw-utility-bar`)**:
   - Phone support link (`tel:+919824144670` - official Lumber Life support line).
   - "Official India Partner: Lumber Life" badge.
   - "Experience Centres" quick link (`/#experience-centre`).
   - "Order Samples" modal trigger (`#ntw-utility-sample-link` -> opens F9 modal).
   - "Architect & Trade Portal" link (`/login/index.html`).
   - Search trigger button (`#ntw-utility-search-trigger`) with `Ctrl K` shortcut indicator.
2. **Sticky Header Shrink on Scroll (`initStickyHeaderShrink`)**:
   - Detects `window.scrollY > 60` and toggles `.ntw-header-shrunk`.
   - Padding shrinks from 18px to 10px; logo scales smoothly.
3. **Products Mega-Menu Promo Panel (`injectMegaMenuPromos`)**:
   - Injected into desktop Products dropdown (`.ntw-products-grid-inner`).
   - Displays static featured card with `/product-images/deck.jpg`, title, description, and "Order Free Sample Kit" button.
4. **Mobile Drawer with Accordions (`initMobileDrawer`)**:
   - Injected backdrop and drawer container (`#ntw-mobile-drawer-root`).
   - Triggered by `#menu-toggle-185` on screen widths $\le$ 991px.
   - Accordions with `aria-expanded` and `aria-controls` for "Why NewTechWood?", "Products", and "Projects".
   - Direct quick links for Experience Centres, Contact Us, and Trade Portal.
   - Footer actions for "Request Free Sample Box", "Call Us", and WhatsApp.
5. **Skip to Content Link**:
   - `<a class="skip-link screen-reader-text" href="#content">Skip to content</a>` exists in markup at top of `<body>`.

---

## 2. Nav Features Audit Matrix (N1 – N12)

| Feature ID | Feature Description | Status | Current Reality vs Requirement Gap |
|---|---|---|---|
| **N1** | **Favourites in Header** | **MISSING** | F13 exists as a floating widget on bottom-left, but the header utility bar, desktop navbar, and mobile drawer have NO heart icon, live count badge, or bump animation connected to `localStorage['ntw_favourites_v2']`. |
| **N2** | **Quote / Sample CTA Button** | **PARTIAL** | "Order Samples" is present as a secondary text link in the utility top bar and inside the mobile drawer footer, but there is NO prominent, highlighted CTA button in the main desktop navbar next to the primary navigation items. |
| **N3** | **Calculator Link** | **MISSING** | Feature F11 (Material BOQ Estimator) exists on the page (`#ntw-material-calculator`), but there is NO link to it in either the utility bar or the navigation menus. |
| **N4** | **Find Centre Button** | **EXISTS** | Present in utility bar (`/#experience-centre`), mobile drawer, and main menu (`EXPERIENCE CENTRE`). Needs smooth-scroll enhancement to ensure anchor jumping seamlessly accounts for sticky header offset. |
| **N5** | **Resources Mega Menu** | **MISSING** | Dropdowns exist for "Why NewTechWood?", "Products", and "Projects". There is NO dedicated "Resources" or "Tools" dropdown linking the built features (Colour Explorer F5, Calculator F11, Brochures F12, Project Filter F15, Pro Resources F16). |
| **N6** | **Mega Menu Dynamic Preview** | **PARTIAL** | A static promo card exists in the Products menu, but hovering/focusing different product items (Decking, Cladding, Beams, Tiles, Railing) does NOT dynamically update the preview image with smooth crossfade. |
| **N7** | **Hover Intent & Dismiss** | **PARTIAL** | Currently relies on standard CSS `:hover` / click without debounced hover-intent timers (150ms open delay / 250ms close delay). Click-outside exists only on mobile; desktop Esc does not dismiss dropdowns and return focus to trigger. |
| **N8** | **Keyboard Navigation** | **PARTIAL** | Basic `Tab` traversal exists, but arrow keys (`ArrowDown`, `ArrowUp`, `ArrowRight`, `ArrowLeft`), `Home`, `End`, and focus-trapping inside open mega-menu panels are incomplete. Visible high-contrast focus rings are needed. |
| **N9** | **Skip Link** | **PARTIAL** | The anchor `<a class="skip-link" href="#content">` exists in HTML, but lacks high-visibility styling on `:focus` in `header.css`, and the main page container lacks `id="content"`. |
| **N10** | **Active Page Highlight** | **MISSING** | No dynamic evaluation of current URL/hash to set `aria-current="page"` and active underline indicator on current menu item and its parent. |
| **N11** | **Mobile Drawer Upgrade** | **PARTIAL** | Close button, search trigger, and accordions exist. Missing: sub-level Back button (hierarchical drill-down), Favourites entry with badge, touch swipe-left gesture to dismiss, and strict dialog focus trap. |
| **N12** | **Optional Header Motion** | **PARTIAL** | Sticky shrink (`.ntw-header-shrunk`) at `scrollY > 60` exists. Missing: configurable hide-on-scroll-down / show-on-scroll-up and transparent-to-solid hero transition (controlled by single JS config flag `ENABLE_SMART_SCROLL_HEADER = false`). |

---

## 3. Detailed Gap Analysis & Proposed Architectural Solutions

### N1: Favourites in Header (Missing $\rightarrow$ Build)
- **Gap**: Users cannot see their saved items count without scrolling to the floating button.
- **Solution**:
  - Add heart icon button with live badge `#ntw-header-fav-btn` in utility bar and desktop navbar.
  - Add Favourites entry in mobile drawer with live count `#ntw-drawer-fav-count`.
  - Listen for `'storage'` and custom `'ntw:favourites-updated'` events to bump animation (`transform: scale(1.3)`) and update count instantly.
  - Click opens the F13 saved finishes drawer.

### N2: Quote / Sample CTA Button (Partial $\rightarrow$ Upgrade)
- **Gap**: Primary conversion CTA is missing from the main desktop navigation bar.
- **Solution**:
  - Add high-contrast gold/green CTA button (`.ntw-nav-cta-btn`: "Order Free Samples") in the main navbar next to "CONTACT US".
  - Visible on desktop/laptop ($\ge 992px$); hidden on mobile/tablet where the mobile drawer footer button takes over.
  - Clicks trigger `ntw:open-sample-modal`.

### N3: Calculator Link (Missing $\rightarrow$ Build)
- **Gap**: Architects and homeowners have no quick way to navigate to the Material BOQ Estimator (F11).
- **Solution**:
  - Add "Material Calculator" link in the utility bar and under the Resources dropdown.
  - Smoothly scrolls to `#ntw-material-calculator` with sticky header offset.

### N4: Find Centre Button (Exists $\rightarrow$ Polish)
- **Gap**: Anchors jump abruptly without offset compensation.
- **Solution**:
  - Integrate with smooth scrolling handler to scroll cleanly to `#experience-centre` with 80px offset.

### N5: Resources Mega Menu (Missing $\rightarrow$ Build)
- **Gap**: Features F5, F11, F12, F15, F16 are built but not consolidated into navigation.
- **Solution**:
  - Add "RESOURCES" menu item to the main navigation (desktop + mobile drawer).
  - Sub-items link existing tools:
    - *Colour Swatch Explorer* (`/#ntw-color-swatch-explorer`)
    - *Material BOQ Calculator* (`/#ntw-material-calculator`)
    - *Architectural Catalogues & Flipbook* (`/#ntw-brochures-block`)
    - *Technical Specs & Certifications* (`/#ntw-pro-resources`)
    - *Project Portfolio & Gallery* (`/projects/`)
  - All labels use existing section titles.

### N6: Mega Menu Dynamic Preview (Partial $\rightarrow$ Upgrade)
- **Gap**: Mega menu side panel is static and does not respond to sub-category hover.
- **Solution**:
  - Hovering/focusing Decking, Cladding, Beams, Deck Tiles, Fencing, or Railing updates the preview image, title, and description in `.ntw-mega-promo` using existing repo images (`deck.jpg`, `clads.jpg`, `twix.jpg`, etc.) with 0.25s crossfade.
  - Mouse leaving resets to default featured showcase.

### N7: Hover Intent & Dismiss (Partial $\rightarrow$ Upgrade)
- **Gap**: Accidental mouse crossings trigger instant open/flicker; Esc key does not close open desktop menus.
- **Solution**:
  - Add 150ms open delay timer and 250ms close debounce timer in `header.js`.
  - Closing any open dropdown on click-outside or `Escape`.
  - Pressing `Escape` returns focus to the parent menu button.
  - Strict exclusivity: only one mega-menu or dropdown open at a time.

### N8: Keyboard Navigation (Partial $\rightarrow$ Upgrade)
- **Gap**: Users cannot navigate menu items with arrow keys; focus indicators are standard browser defaults.
- **Solution**:
  - `ArrowRight` / `ArrowLeft`: Move between top-level menu headings.
  - `ArrowDown` / `ArrowUp`: Open dropdown and navigate between sub-items.
  - `Home` / `End`: Jump to first / last item in active menu.
  - Visible `outline: 2px solid #c9a84c; outline-offset: 2px;` on all interactive links/buttons.
  - Correct `aria-expanded="true/false"`, `aria-haspopup="true"`, and `aria-controls`.

### N9: Skip Link (Partial $\rightarrow$ Upgrade)
- **Gap**: Skip link is present in DOM but lacks high-visibility styling on `:focus`.
- **Solution**:
  - Add `.skip-link:focus` in `header.css`: fixed at top-center, z-index 100000, gold background, bold text, high padding.
  - Ensure target `<main id="content">` or `<div id="content">` exists right after header.

### N10: Active Page Highlight (Missing $\rightarrow$ Build)
- **Gap**: Current page lacks visual indication in navigation.
- **Solution**:
  - Read `window.location.pathname` and `window.location.hash`.
  - Add `aria-current="page"` and `.ntw-nav-active` underline class on matching link and parent category.

### N11: Mobile Drawer Upgrade (Partial $\rightarrow$ Upgrade)
- **Gap**: Missing drill-down back navigation, dedicated favorites row, touch swipe gesture, and focus trap.
- **Solution**:
  - Add Favourites entry with badge counter at top of drawer navigation.
  - Add touch swipe-left handler (`touchstart` + `touchend` deltaX > 50px) to smoothly dismiss drawer.
  - Implement full keyboard focus trap inside `#ntw-mobile-drawer-root` while open.

### N12: Optional Header Motion (Partial $\rightarrow$ Build Last with Config Flag)
- **Gap**: Smart scroll direction and hero transparency not configurable.
- **Solution**:
  - Implement configurable module:
    ```javascript
    const HEADER_CONFIG = {
      enableSmartScroll: true,       // Hide on scroll down, show on scroll up
      enableTransparentHero: true    // Transparent over hero video, solid after 80px
    };
    ```
  - Easily toggleable via single boolean flags.

---

## 4. Proposed New Labels for NEW_LABELS.md (Under Content Freeze)

Only functional UI labels required for the new navigation features:
1. `Favourites` / `Saved ({count})` (Header badge & drawer entry)
2. `Order Free Samples` (Desktop navbar CTA button)
3. `Material Calculator` (Utility & menu link to F11)
4. `Resources` (Menu heading for tools & specs)
5. `Skip to content` (Accessibility skip link)
6. `Back` (Mobile sub-navigation back button)
7. `Close` (Drawer and modal close button aria-label)

---

## 5. Next Steps Pending Human Approval

1. **Awaiting approval** on `NAV_AUDIT.md` and the proposed labels.
2. Upon approval, begin execution in **ACT MODE** in strict TASKS order:
   - Foundation: N7 (Hover Intent), N8 (Keyboard Nav), N9 (Skip Link), N10 (Active Highlight).
   - Core Header Actions: N1 (Favourites in Header), N2 (Sample/Quote CTA), N3 (Calculator Link), N4 (Find Centre Polish).
   - Menus & Previews: N5 (Resources Mega Menu), N6 (Mega Menu Dynamic Preview).
   - Mobile & Motion: N11 (Mobile Drawer Upgrade), N12 (Optional Smart Motion).
   - Verification: Playwright automated suite across desktop, tablet, and mobile with zero console errors.
