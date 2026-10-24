# AUTONOMOUS EXECUTION MASTER WORKFLOW (TASKS.md)

**Branch**: `features-v2` (Dedicated clean feature branch)  
**Status**: COMPLETE ✅ (All features R0, F1–F18 verified with Playwright end-to-end suite)  

---

## Stage 0: Audit, Reconnaissance & Task R0 Preparation [DONE]
- [x] Create and checkout branch `features-v2`
- [x] Live Reconnaissance of reference sites (`FEATURE_RECON.md`)
- [x] Register new UI labels (`NEW_LABELS.md`)
- [x] Exhaustive scan for Cost/Maintenance Comparison strings (`scratch/audit_r0_removal.py` -> `REMOVAL_REPORT.md`)
- [x] Human approval received to proceed with implementation

---

## Stage 1: Task R0 Execution (Removal of Cost & Maintenance Comparison) [DONE]
- [x] Remove `#ntw-cost-calculator` HTML block from `index.html` (lines 1282-1288)
- [x] Remove `cost-calculator.css` link from `index.html` (line 279)
- [x] Remove `cost-calculator.js` script tag from `index.html` (line 1719)
- [x] Delete dead assets: `/assets/ntw-v2/features/cost-calculator.css` & `.js`
- [x] Remove cost calculator references from `search-index.json`, `search-overlay.js`, and `whatsapp-floating.js`
- [x] Update Action 3 in mobile bar to "Call Us" / `tel:+919824144670` (prevents broken anchor)
- [x] Verify: Grep returns zero matches for comparison strings across active site; page renders clean; zero console errors

---

## Stage 2: Navigation & Discovery Core (F1 & F2) [DONE]
- [x] **F1. Header**:
  - Utility top bar (Phone +91 98241 44670 / Experience Centres / Order Samples / Architect & Trade Portal / Search trigger)
  - Sticky header with shrink animation on scroll
  - Mega menu with promo panel (image + short existing text + CTA to sample request)
  - Mobile drawer with accessible accordions (< 991px)
- [x] **F2. Search Overlay**:
  - Fullscreen overlay, Esc to close, focus trap
  - Live categorized results (Products, Projects, Pages, Articles)
  - "No results" state with 3 fallback buttons (Products, Colours, Experience Centre)
  - Powered by client-side `search-index.json`

---

## Stage 3: Product Exploration & Brand Showcase (F3 – F8) [DONE]
- [x] **F3. Hero Promo Banners**: Auto-rotating promotional cards (pause on hover/touch, swipeable, dots+arrows, respects prefers-reduced-motion)
- [x] **F4. Category Tabs**: Decking, Cladding, Beams, Deck Tile, Fencing, Railing, Planter Box with swatch thumbnails, color counts, and crossfade image preview
- [x] **F5. Color Explorer**: Swatch selection swaps finished-project image with crossfade; displays name, code, series; "Order a sample" button connects to F9
- [x] **F6. Count-Up Stats**: Scroll-triggered numeric easeOut counter (1.5s) using existing site figures ("30+", "10M+", "25 Years", "95%")
- [x] **F7. Board Anatomy Hotspots**: Interactive SVG UltraShield board diagram with clickable hotspots displaying benefit tooltips
- [x] **F8. Testimonial Slider & Partner Logo Strip**: Slider with arrows/swipe; infinite smooth logo marquee (pauses on hover) using verified standards

---

## Stage 4: Conversion & Engagement Engines (F9 & F10) [DONE]
- [x] **F9. Sample / Quote Popup Form**:
  - Modal with Name, Phone, Email, City, Product, Color (prefilled from F5), Project Size, Timeline, optional plan upload, honeypot
  - "Save and resume later" via localStorage
  - WhatsApp click-to-chat fallback submit (`https://wa.me/919824144670`)
- [x] **F10. Newsletter Signup**: Email, Name, Indian State dropdown with inline validation and animated confirmation

---

## Stage 5: Tools, Architecture & Technical Hub (F11 – F17) [DONE]
- [x] **F11. Material Calculator (BOQ Only)**:
  - Technical material estimation ONLY: inputs = area, profile type, wastage %; outputs = board count, clips, billed area
  - Formula: $\text{planks} = \lceil \frac{\text{area} \times (1 + \text{wastage})}{\text{plank area}} \rceil$
  - STRICTLY ZERO cost, price, or wood comparison
  - Seamless "Transfer BOQ to Sample / Quote Request" action
- [x] **F12. Brochure Block & In-House Flipbook**: Direct PDF download CTAs to official repository PDFs + lightweight in-house CSS 3D page-flip viewer (no 3rd party embeds)
- [x] **F13. Favourites System**: Heart toggle on project and product cards; saved to localStorage; "Saved Finishes" slide-out drawer with sample transfer
- [x] **F14. Experience Centre & Dealer Finder**: State filter chips (Delhi, Karnataka, Rajasthan, Gujarat, Punjab) + search box + Google Map & Call actions
- [x] **F15. Project & Gallery Filters**: All / International / National tabs + product-type chips with URL hash state and empty state
- [x] **F16. Pro Resources**: Downloads library for catalogs, architectural specs, installation guides, and test certificates
- [x] **F17. Sticky Mobile Bar + WhatsApp**: Bottom safe-area bar (Centres | WhatsApp | Free Sample | Call) with zero UI overlap

---

## Stage 6: Polish & Motion Design (F18) [DONE]
- [x] **F18. Micro-Interactions Framework**:
  - Scroll-reveal (fade-up, 32px, 0.6s) via IntersectionObserver
  - Card hover zoom and elevation shadow
  - Button hover effects & smooth anchor scrolling with header offset
  - Automatic disable under `@media (prefers-reduced-motion: reduce)`

---

## Stage 7: Multi-Agent QA, Security & Verification [DONE]
- [x] Task R0 Removal Audit: Verified 0 matches for cost/maintenance comparison anywhere on active site
- [x] Content Freeze Compliance: 0 invented claims, 0 fake testimonials, official specs only
- [x] Input Security & Sanitization: Honeypot spam defense, HTML entity escaping, safe event listeners
- [x] End-to-End Test Suite: `scratch/test_complete_suite.py` passed 100% with exit code 0
- [x] Console Errors: Verified ZERO uncaught JavaScript errors or broken anchors
