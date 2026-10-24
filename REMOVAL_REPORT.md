# TASK R0 REMOVAL REPORT (REMOVAL_REPORT.md)

## 1. Summary of Identified Target Occurrences
Total matching lines found: **11** across the repository.

| File | Line | Matched Pattern | Line Snippet |
|---|:---:|---|---|
| [`FEATURE_RECON.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/FEATURE_RECON.md) | 40 | `wood-vs` | `- **Strictly No Cost Comparison**: The material calculator (F11) computes plank count and clips from area and profile dimensions o` |
| [`LOOP_LOG.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/LOOP_LOG.md) | 7 | `cost-calculator` | `\| **F2** \| 1 \| Build & Verification \| PASS \| `/assets/ntw-v2/features/cost-calculator.css` & `.js` mounted in `index.html`; node m` |
| [`REVIEW.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/REVIEW.md) | 27 | `ntw-cost-calculator` | `\| **F2** \| **Wood vs Composite Cost Calculator** \| [`cost-calculator.css`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodin` |
| [`REVIEW.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/REVIEW.md) | 57 | `cost-calculator` | `- File: [`assets/ntw-v2/features/cost-calculator.js`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/assets/ntw-v2/feat` |
| [`TASKS.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/TASKS.md) | 17 | `Cost & Maintenance Comparison` | `## Stage 1: Task R0 Execution (Removal of Cost & Maintenance Comparison)` |
| [`TASKS.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/TASKS.md) | 18 | `ntw-cost-calculator` | `- [ ] Remove `#ntw-cost-calculator` HTML block from `index.html` (lines 1282-1288)` |
| [`TASKS.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/TASKS.md) | 19 | `cost-calculator` | `- [ ] Remove `cost-calculator.css` link from `index.html` (line 279)` |
| [`TASKS.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/TASKS.md) | 20 | `cost-calculator` | `- [ ] Remove `cost-calculator.js` script tag from `index.html` (line 1719)` |
| [`TASKS.md`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/TASKS.md) | 21 | `cost-calculator` | `- [ ] Delete dead assets: `/assets/ntw-v2/features/cost-calculator.css` & `.js`` |
| [`blog/composite-vs-wood-which-builds-the-better-deck/index.html`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/blog/composite-vs-wood-which-builds-the-better-deck/index.html) | 594 | `wood-vs` | `<p>At first glance, natural wood decks often win in cost comparisons. Generally, they are cheaper to install than composite decks.` |
| [`wp-json/wp/v2/posts/2214/index.html`](file:///C:/Users/amanr/OneDrive/Documents/newtechwoodintl/wp-json/wp/v2/posts/2214/index.html) | 1 | `wood-vs` | `{"id":2214,"date":"2021-01-07T00:00:00","date_gmt":"2021-01-07T00:00:00","guid":{"rendered":"https:\/\/test.newtechwoodintl.com\/b` |

## 2. Breakdown by Category & Proposed Removal Plan

### A. HTML Mount Points
- **`index.html`**:
  - Line 279: `<link rel="stylesheet" href="/assets/ntw-v2/features/cost-calculator.css">`
  - Lines 1275-1288: `<div id="ntw-cost-calculator">...</div>`
  - Line 1718: `<script src="/assets/ntw-v2/features/cost-calculator.js" defer></script>`

### B. Cross-Feature References & Links
- **`assets/ntw-v2/features/search-index.json`**:
  - Entry for "Wood vs Composite Cost Calculator" pointing to `/#ntw-cost-calculator`.
- **`assets/ntw-v2/features/search-overlay.js`**:
  - POPULAR_ITEMS entry: `{ title: 'Cost Calculator', url: '/#ntw-cost-calculator', category: 'Tool' }`.
- **`assets/ntw-v2/features/whatsapp-floating.js`**:
  - Mobile action bar button 3 (#ntw-mab-calc-btn): Click handler scrolling to `#ntw-cost-calculator`.
  - *Replacement for mobile bar button*: Change Action 3 to "Call Us" (`tel:+919824144670`) or "Experience Centre" (`/#experience-centre`) so mobile users retain 3 high-value actions without broken anchors.

### C. Dead Feature Assets (To be removed/depleted)
- **`assets/ntw-v2/features/cost-calculator.css`** (to be deleted)
- **`assets/ntw-v2/features/cost-calculator.js`** (to be deleted)

### D. Project Documentation / Logs (References in audit logs)
- `FEATURE_AUDIT.md`, `TASKS.md`, `LOOP_LOG.md`, `REVIEW.md` contain historical log entries which will be updated/scrubbed to reflect the removal.

## 3. Human Approval Checkpoint
Per task instructions: **WAIT FOR USER APPROVAL** before deleting or modifying the files above.
