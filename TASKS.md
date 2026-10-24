# ORDERED IMPLEMENTATION WORKFLOW

## Stage 0: Audit & Baseline Verification
- [x] Create git branch `features-v1`
- [x] Discover data sources (products.json, colors, locations, projects, tokens)
- [x] Verify API endpoints in `/api/` (no public submission endpoint; WhatsApp fallback confirmed)
- [x] Complete `FEATURE_AUDIT.md`
- [ ] **HUMAN-IN-THE-LOOP CHECKPOINT: PLAN SUMMARY APPROVAL**

---

## Stage 1: Feature Implementation Pipeline (Sequential — Strict QA Loop)
- [x] **F1. Color Swatch Explorer**
  - [x] Implement `/assets/ntw-v2/features/color-swatch-explorer.css` & `.js`
  - [x] Read existing colors from `products.json` (Antique, Teak, IPE, Maple + series codes)
  - [x] Large image swap, preloading, ARIA keyboard navigation (arrows/Enter), zero layout shift
  - [x] Connect "Order this color" hook for F3
  - [x] QA Loop: Console check, keyboard test, 375/768/1440 responsiveness, log to `LOOP_LOG.md`
- [x] **F2. Wood vs Composite Cost Calculator**
  - [x] Implement `/assets/ntw-v2/features/cost-calculator.css` & `.js`
  - [x] Config object at top marked `TODO-VERIFY` with 3 presets in INR + "Use my own number"
  - [x] Years slider 1 to 25 (ticks at 1, 5, 10, 15, 20, 25)
  - [x] Two columns: Real Wood upkeep & weekends vs UltraShield (0 upkeep, 25-yr warranty)
  - [x] Indian currency formatting (Lakh grouping / Rs 6,750), custom input validation
  - [x] QA Loop: Math verification tests (e.g., 450 x 15 = 6,750), responsive check, log to `LOOP_LOG.md`
- [x] **F3. Free Sample Request Band + Form**
  - [x] Implement `/assets/ntw-v2/features/sample-request.css` & `.js`
  - [x] "Feel it before you build it" section + modal form (name, phone, email, city, product, color prefill from F1, message)
  - [x] Honeypot spam trap, client-side validation, error/success states
  - [x] WhatsApp fallback submit payload (since no public `/api` endpoint exists)
  - [x] QA Loop: Form validation check, honeypot test, modal accessibility, log to `LOOP_LOG.md`
- [x] **F4. Experience Centre Filter**
  - [x] Implement `/assets/ntw-v2/features/experience-centre-filter.css` & `.js`
  - [x] Filter chips: Delhi, Karnataka, Rajasthan, Gujarat, Punjab + All
  - [x] Preserve all existing addresses and phone numbers; Punjab shows "Coming Soon" badge
  - [x] QA Loop: Filter click tests, keyboard accessibility, map link checks, log to `LOOP_LOG.md`
- [x] **F5. Project Filter**
  - [x] Implement `/assets/ntw-v2/features/project-filter.css` & `.js`
  - [x] Tabs: All / International / National (India) with URL hash synchronization (`#national`, `#international`)
  - [x] Smooth transitions, counter updates, empty-state fallback
  - [x] QA Loop: Hash state change test, back/forward button test, responsive check, log to `LOOP_LOG.md`
- [x] **F6. Client-Side Search Overlay**
  - [x] Build search index generator script (`scratch/build_search_index.py` -> `/assets/ntw-v2/features/search-index.json`)
  - [x] Implement `/assets/ntw-v2/features/search-overlay.css` & `.js`
  - [x] Full-screen overlay, Esc to close, focus trap, popular links (Decking, Cladding, Colors, Visualizer, Experience Centre)
  - [x] Instant client-side fuzzy search over generated index
  - [x] QA Loop: Focus trap verification, keyboard navigation, Esc close check, log to `LOOP_LOG.md`
- [x] **F7. WhatsApp Floating Button + Mobile Action Bar**
  - [x] Implement `/assets/ntw-v2/features/whatsapp-floating.css` & `.js`
  - [x] Verified WhatsApp business number with pre-filled message
  - [x] Non-overlapping placement respecting mobile bottom sticky bar and viewport safe-areas
  - [x] QA Loop: Viewport test on 375px/768px/1440px, scroll test, log to `LOOP_LOG.md`

---

## Stage 2: Final Multi-Agent QA & Security Review
- [x] Run complete test suite (existing pytest 16/16 passed, verification script passed)
- [x] Security Review (XSS escaping, honeypot spam protection, zero console data leaks)
- [x] Cross-browser & responsive layout audit (375px mobile action bar, 768px tablet, 1440px desktop)
- [x] Write `REVIEW.md` and `TODO-VERIFY` list
- [ ] **HUMAN-IN-THE-LOOP CHECKPOINT: FINAL APPROVAL BEFORE PUSH/MERGE/DEPLOY**

