# REMOVAL REPORT: "For Architects & Specifiers / Architectural & Technical Library"

## 1. Summary of Identified Target Occurrences
The section matching:
- **Title**: *"Architectural & Technical Library"*
- **Eyebrow**: *"For Architects & Specifiers"*
- **Subtitle**: *"Access comprehensive CAD details, installation manuals, international certifications, and warranty documents for your project files."*

Corresponds to **Feature F14 (`pro-resources`)** mounted dynamically at `#ntw-pro-resources`.

---

## 2. Exact Files & Lines to be Removed / Modified

| File | Line(s) | Role | Proposed Change |
|---|:---:|---|---|
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 290 | CSS Link | Remove `<link rel="stylesheet" href="/assets/ntw-v2/features/pro-resources.css">` |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1048–1054 | Resources Mega Menu Card | Remove `<a href="/#ntw-pro-resources" class="ntw-resources-dropdown-card">` for Technical Specs & Certifications |
| [`index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html) | 1830 | JS Script Tag | Remove `<script src="/assets/ntw-v2/features/pro-resources.js" defer></script>` |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 651 | Mobile Drawer Link | Remove `<a href="/#ntw-pro-resources" class="ntw-drawer-sublink">Technical Specs &amp; Certifications</a>` |
| [`assets/ntw-v2/features/header.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/header.js) | 879 | Smooth Scroll Selector | Remove `a[href*="#ntw-pro-resources"]` from smooth scroll query selector |
| [`assets/ntw-v2/features/pro-resources.css`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/pro-resources.css) | 1–178 (all) | Dead Feature CSS | Delete file |
| [`assets/ntw-v2/features/pro-resources.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/features/pro-resources.js) | 1–222 (all) | Dead Feature JS | Delete file |

---

## 3. Impact & Verification Plan
1. **Zero broken anchors**: Removing the menu card and drawer link ensures no user navigates to a non-existent `#ntw-pro-resources` hash.
2. **Regression Testing**: Run Playwright navigation test suite (`scratch/test_nav_upgrades.py`) to confirm clean rendering with 0 console errors.
3. **Clean Git Tree**: Stage and commit removal cleanly on branch `features-v2`.

---

## 4. Human Approval Checkpoint
Per protocol: **Please confirm approval to proceed with removing this section.**
