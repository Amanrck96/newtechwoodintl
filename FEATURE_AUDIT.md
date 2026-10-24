# FEATURE AUDIT & REPOSITORY DISCOVERY REPORT
**Branch**: `features-v1`  
**Repository**: `newtechwoodintl` (live at newtechwood.in)  
**Date**: October 2026  
**Auditor**: Researcher & Frontend Architect Agents  

---

## 1. Existing Data Sources Discovered

### A. Products & Color Palette Data
- **File**: [`products.json`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/products.json) & [`db/products.json`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/db/products.json)
  - Categories in catalog: Decking, Cladding, Pergola, Accessories.
  - Active core product variants in India catalog:
    - **Antique** (Code: `AT`, Roman Antique series)
    - **Teak** (Code: `TK`, Peruvian Teak series)
    - **IPE** (Code: `IP`, Brazilian IPE series)
    - **Maple** (Code: `MP`, Natural Maple series)
  - Extended UltraShield Palette ([`blog/how-to-pick-a-composite-deck-color/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/blog/how-to-pick-a-composite-deck-color/index.html)):
    - Spanish Walnut (`WN`), Hawaiian Charcoal (`CH`), Westminster Gray (`LG`), English Oak (`OK`).
- **Product Images**: [`product-images/`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/product-images/)
  - Finished deck & cladding assets: `deck.jpg`, `twix.jpg`, `clads.jpg`, `twix-uh94.jpg`, `sunshades.jpg`.
  - High-res project photos in [`wp-content/uploads/`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/wp-content/uploads/).

### B. Experience Centre Locations Data
- **Sources**: [`locations/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/locations/index.html) & [`index.html#experience-centre`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/index.html#L1252-L1345)
  - **Delhi**: Lumber Life — `1/8, Shop No. 6, WHS Kirti Nagar, Ware Housing Scheme, Kirti Nagar, Delhi, 110015` | Map: `https://share.google/0lGknO28FgU9w6Bk3`
  - **Karnataka**: Aaren Intpro — `342/8, Mysore Rd, New Guddadahalli, Guddadahalli, Bengaluru, Karnataka 560026` | Map: `https://share.google/Jgvwbz134ttl7nLnV`
  - **Rajasthan**: Badayas Kitchen — `207, Mahesh Nagar, Shri Gopal Nagar, Gopal Pura Mode, Jaipur, Rajasthan 302019` | Map: `https://share.google/vGAfCFfPVIVDNNktK`
  - **Gujarat**: PRABHUSURAT BUILDWARES PRIVATE LIMITED — `1, Maruti complex, opp. sona appt., umiyadham road, Varachha, Surat-6` | Ph: `+91 261 2543312 \ 2544281`, M: `+91 98241 44670`, Email: `rahul@prabhusurat.com` | Map: `https://share.google/rsa3gddnzRzAjWJgq`
  - **Punjab**: Upcoming Experience Centre — Status: "Coming Soon" badge.

### C. Projects Data
- **Sources**: [`projects/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/projects/index.html), [`projects/international/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/projects/international/index.html), [`projects/national/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/projects/national/index.html)
  - Categorized under:
    - **All Projects** (`/projects/`)
    - **International** (`/projects/international/`) — Landmark global architecture (USA, Europe, UAE, Asia).
    - **National (India)** (`/projects/national/`) — Luxury estates, resorts & commercial installations across India by Lumber Life.
  - Existing markup uses `.projects-grid`, `.project-card`, `.filter-btn`, `.badge-international`, `.badge-national`.

---

## 2. API Endpoints Audit (/api)
- Inspected [`api/index.py`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/api/index.py) & [`db/api_router.py`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/db/api_router.py).
- **Result**: No public sample request or quotation submission endpoint currently exists. All `/api/` endpoints are internal CRM/authenticated endpoints (`/api/auth/*`, `/api/orders/*`, `/api/projects/*`, `/api/directory/*`, `/api/vendors/*`).
- **Conclusion for F3**: Per rule F3, client-side sample requests will fall back to **WhatsApp click-to-chat** with pre-formatted payload and client-side validation. No new API endpoints will be created without explicit approval.

---

## 3. Contact & WhatsApp Audit
- Phone numbers identified in public pages:
  - Gujarat Experience Centre: `+91 98241 44670`
  - Delhi Experience Centre: `[Phone Number — to be filled]` in `contact-us/index.html`
- **Action for F7**: Pre-fill WhatsApp click-to-chat with `+91 98241 44670` (or user-confirmed primary business number).

---

## 4. Design Tokens & Styling Architecture
- Directory `/assets/ntw-v2/` will be created with `tokens.css` based on existing design variables from [`projects/index.html`](file:///c:/Users/amanr/OneDrive/Documents/newtechwoodintl/projects/index.html#L48-L61):
  ```css
  :root {
    --ll-green: #2d6a2d;
    --ll-green-light: #4a9e4a;
    --ll-gold: #c9a84c;
    --ll-dark: #121614;
    --ll-bg: #f7f6f2;
    --ll-card-bg: #ffffff;
    --ll-text: #2c302e;
    --ll-muted: #6b7280;
    --ll-shadow: 0 10px 30px rgba(0,0,0,0.08);
    --ll-shadow-hover: 0 20px 40px rgba(0,0,0,0.15);
    --ll-radius: 14px;
    --ll-transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  ```
- Typography: `'Inter', sans-serif`, `'Muli', sans-serif`, `'Butler', serif`, `'Playfair Display', serif`.
- Every feature module will reside in `/assets/ntw-v2/features/` with isolated CSS and JS, lazy-loaded and zero external dependencies.

---

## 5. Header & Footer Mount Points
- **Header**: Elementor header (`<header data-elementor-type="header">`) contains search icon / trigger placeholder and navigation menu. Search overlay hook will attach to the header search button.
- **Main Content**:
  - `index.html`: Mount points for Color Swatch Explorer (F1), Cost Calculator (F2), Sample Request Band (F3), Experience Centre Filter (F4), Floating WhatsApp & Mobile Bar (F7).
  - `projects/index.html`: Tabbed filter enhancement (F5).
  - Site-wide: Search Overlay (F6).
