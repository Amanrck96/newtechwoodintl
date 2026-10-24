# REMOVAL REPORT: "Architectural Planning Tool / Material BOQ & Quantity Estimator"

## 1. Summary of Identified Target Occurrences
The section matching:
- **Eyebrow**: *"Architectural Planning Tool"*
- **Title**: *"Material BOQ & Quantity Estimator"*
- **Subtitle**: *"Calculate the exact number of UltraShield planks, fasteners, and substructure requirements based on your project dimensions."*

Corresponds to **Feature F11 (`material-calculator`)** mounted dynamically at `#ntw-material-calculator`.

---

## 2. Exact Files & Lines to be Removed / Modified

| File | Line(s) | Role | Proposed Change |
|---|:---:|---|---|
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 287 | CSS Link | Remove `<link rel="stylesheet" href="/assets/ntw-v2/features/material-calculator.css">` |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1033–1039 | Resources Mega Menu Card | Remove `<a href="/#ntw-material-calculator" class="ntw-resources-dropdown-card">` |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1815–1816 | JS Script Tag | Remove `<script src="/assets/ntw-v2/features/material-calculator.js" defer></script>` |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 73–76 | Utility Bar Link | Remove Material Calculator link (`#ntw-utility-calc-link`) from utility header |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 649 | Mobile Drawer Link | Remove `<a href="/#ntw-material-calculator">` from mobile drawer accordion |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 877 | Smooth Scroll Selector | Remove `a[href*="#ntw-material-calculator"]` from smooth scroll query selector |
| [`assets/ntw-v2/features/brochure-viewer.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/brochure-viewer.js) | 117 | Fallback Anchor | Update mount anchor from `#ntw-material-calculator` to `#ntw-color-swatch-explorer` / `#ntw-sample-request` |
| [`assets/ntw-v2/features/material-calculator.css`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/material-calculator.css) | 1–254 (all) | Dead Feature CSS | Delete file |
| [`assets/ntw-v2/features/material-calculator.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/material-calculator.js) | 1–193 (all) | Dead Feature JS | Delete file |
| [`scratch/test_nav_upgrades.py`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/scratch/test_nav_upgrades.py) | 122–125 | Test Case | Update test N3 to verify calculator link cleanly removed |

---

## 3. Impact & Verification Plan
1. **Zero broken anchors**: Removing all utility bar, mega-menu, and drawer links ensures no user encounters a broken `#ntw-material-calculator` target.
2. **Anchor Fallback Safety**: `brochure-viewer.js` automatically mounts to the next available block (`#ntw-sample-request` / `#ntw-color-swatch-explorer`) without interruption.
3. **Automated Regression**: Run `test_nav_upgrades.py` with 100% pass rate.
4. **Clean Git Commit**: Record changes on branch `features-v2`.

---

# REMOVAL REPORT 2: "Technical Downloads / Architectural Catalogues & Spec Sheets"

## 1. Summary of Identified Target Occurrences
The section matching:
- **Eyebrow**: *"Technical Downloads"*
- **Title**: *"Architectural Catalogues & Spec Sheets"*
- **Subtitle**: *"Download comprehensive product brochures, profile cross-sections, span tables, and installation manuals directly."*

Corresponds to **Feature F12 (`brochure-viewer`)** mounted dynamically at `#ntw-brochures-block`.

---

## 2. Exact Files & Lines Removed / Modified

| File | Line(s) | Role | Change Made |
|---|:---:|---|---|
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 287 | CSS Link | Removed `<link rel="stylesheet" href="/assets/ntw-v2/features/brochure-viewer.css">` |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1032–1038 | Resources Mega Menu Card | Updated link target from `/#ntw-brochures-block` to `/downloads/` |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1807–1808 | JS Script Tag | Removed `<script src="/assets/ntw-v2/features/brochure-viewer.js" defer></script>` |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 645 | Mobile Drawer Link | Updated link target from `/#ntw-brochures-block` to `/downloads/` |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 873 | Smooth Scroll Selector | Removed `a[href*="#ntw-brochures-block"]` selector |
| [`assets/ntw-v2/features/brochure-viewer.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/brochure-viewer.js) | All | Feature JS | Retired/disabled |
| [`assets/ntw-v2/features/brochure-viewer.css`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/brochure-viewer.css) | All | Feature CSS | Retired/disabled |

---

## 3. Impact & Status
- **Zero dead DOM elements**: No orphaned brochure viewer markup rendered.
- **Resources links preserved**: External and portal visitors can still access technical files via `/downloads/`.
- **Status**: COMPLETE ✅

---

# REMOVAL REPORT 3: "Top Dark Green Utility Bar (.ntw-utility-bar)"

## 1. Summary of Identified Target Occurrences
The section matching:
- **Element**: `.ntw-utility-bar` / `#ntw-utility-bar`
- **Content**: Phone number `+91 98241 44670`, partner badge `OFFICIAL INDIA PARTNER: LUMBER LIFE`, links `Experience Centres`, `Favourites (0)`, `Architect & Trade Portal`, and search trigger `Search Ctrl K`.
- **User Instruction**: *"REMOVE THIS IT LOOK BAD"*

---

## 2. Exact Files & Lines Removed / Modified

| File | Line(s) | Role | Change Made |
|---|:---:|---|---|
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 35, 50–53 | Nav Engine | Replaced utility bar render with `removeUtilityBar()`, purged utility bar HTML insertion |
| [`assets/ntw-v2/features/header.css`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.css) | 9–11 | Header Styles | Set `.ntw-utility-bar { display: none !important; }` to prevent any display |
| [`scratch/test_nav_upgrades.py`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/scratch/test_nav_upgrades.py) | Nav suite | E2E Test Suite | Updated assertions to verify `#ntw-utility-bar` is absent (`count == 0`) and header sits flush at top |

---

## 3. Impact & Status
- **Zero layout shifts / zero dead DOM**: `#ntw-utility-bar` is completely unmounted.
- **Clean white header**: The site now starts cleanly with the official white NewTechWood brand navigation header.
- **Search & Favourites**: Remain fully accessible via drawer, shortcuts (Ctrl+K), and header CTA.
- **Status**: COMPLETE ✅

