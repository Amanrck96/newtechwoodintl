# LIVE RECONNAISSANCE REPORT (FEATURE_RECON.md)

**Reference Domains Analyzed**:
- `https://www.newtechwood.com` (US / Global flagship)
- `https://www.newtechwood.ca` (Canada regional portal)
- `https://newtechwood.com.au` (Australia portal)

---

## 1. Feature Reconnaissance Matrix

| Feature ID | Feature Name | Effect / Animation Type | Trigger (Hover / Click / Scroll) | Duration & Easing | Button / UI Labels | Mobile Behavior (< 768px) |
|---|---|---|---|---|---|---|
| **F1** | **Header (Utility, Sticky, Mega Menu)** | Slide-down & height compression (80px &rarr; 60px); mega panel fade/translateY(6px); drawer slide-in | Scroll > 50px for shrink; hover/focus for mega menu; click hamburger for drawer | `0.3s cubic-bezier(0.16, 1, 0.3, 1)` | "For Architects", "Order Samples", "Search", "Call", "Menu", "Close" | Utility bar collapses; hamburger drawer opens with vertical accordion menus |
| **F2** | **Search Overlay** | Fullscreen opacity fade (0 &rarr; 1) with modal scale (0.96 &rarr; 1); results stagger fade | Click search icon, `Ctrl+K`, `/` key; `Esc` or click outside closes | `0.25s ease-out` | "Search products, colors, projects...", "ESC", "Products", "Colours", "Experience Centre" | Fullscreen native overlay, auto-focused virtual keyboard, scroll-locked background |
| **F3** | **Hero Promo Banners** | Horizontal slide & fade carousel with auto-rotation (5s timer); pause on hover/touch | Timer, navigation arrows, dot indicators, touch swipe | `0.5s cubic-bezier(0.4, 0, 0.2, 1)`; paused under `prefers-reduced-motion` | "Explore Series &rarr;", "View Installation", "Previous", "Next" | Full touch swipe gesture, dots pagination below banner, touch-pause |
| **F4** | **Category Tabs** | Active pill background shift, crossfade image & text transition (`opacity 0 -> 1`) | Click or keyboard Tab / arrow keys | `0.35s ease-in-out` | "Decking", "Cladding", "Screening / Beams", "Deck Tiles", "Fencing", "Railing", "Planter Box" | Horizontally scrollable pill strip with scroll snap |
| **F5** | **Color Explorer** | Large finished scene crossfade (`opacity 0 -> 1`), swatch active ring pulse | Hover (desktop) / Tap (mobile) on swatch | `0.3s ease-out` | "Order a Sample", "Explore Finishes", series code pills | Grid of touch targets (44px min), auto-loads active scene without layout shift |
| **F6** | **Count-Up Stats** | Animated numeric count from 0 to target value once in viewport | IntersectionObserver threshold: 0.3 | `1.5s easeOutCubic` | Real site stats only ("30+", "10M+", "25 Years", "95%") | Triggers once on vertical mobile scroll into view |
| **F7** | **Board Anatomy Hotspots** | Pulsing SVG badge ring; tooltip bubble scale & fade-in with pointer arrow | Click or hover on hotspot dot; click outside to dismiss | `0.25s cubic-bezier(0.16, 1, 0.3, 1)` | "360° Shielding", "Core", "UV Protection", "Anti-Mold", "Stain Guard", "Eco-Core" | Tap hotspot pops up bottom card / drawer with benefit description |
| **F8** | **Testimonial Slider + Partner Strip** | Infinite smooth marquee ticker (logos); testimonial card crossfade | Marquee is continuous; slider is arrow/swipe triggered | Marquee: 35s linear infinite; Slider: `0.4s ease` | "Previous", "Next", quote text, client location | Marquee pauses on touch; testimonials swipe horizontally |
| **F9** | **Sample / Quote Popup Form** | Dialog scale & fade (`scale(0.95) -> 1`); inline validation errors shake | Click "Order Samples" / "Get a Quote" | `0.28s cubic-bezier(0.16, 1, 0.3, 1)` | "Order Free Sample Box", "Submit Request", "Save & Resume Later", "Track on WhatsApp" | Fullscreen mobile modal dialog with sticky bottom submit action |
| **F10** | **Newsletter Signup** | Inline button loading spinner; smooth expansion of success confirmation banner | Form submit | `0.3s ease-out` | "Subscribe", "Email Address", "Name", "State", "Subscribed!" | Stacked full-width input and submit button |
| **F11** | **Material BOQ Calculator** | Instant reactive calculation recalculating plank & clip quantities on input change | Input change / Wastage % slider change | Instantaneous (0ms) | "Area (Sq. Ft.)", "Product Profile", "Wastage %", "Calculate Planks", "Estimated Planks", "Clips Required" | Touch-friendly numeric inputs and large step-stepper buttons (+/-) |
| **F12** | **Brochure Block & In-House Flipbook** | CSS 3D transform page-turn effect (`perspective: 1200px`) or side-by-side flip | Click "View Brochure" / Arrow buttons | `0.45s cubic-bezier(0.25, 1, 0.5, 1)` | "Download PDF Catalog", "Preview Online", "Previous Page", "Next Page", "Close" | Modal flipbook switches to vertical swipe / scroll viewer on phones |
| **F13** | **Favourites Drawer** | Heart icon toggle fill animation (`scale(1.3) -> 1`); slide-in side drawer | Click heart icon on project/product card | `0.3s cubic-bezier(0.16, 1, 0.3, 1)` | "Save to Favourites", "Saved Items (X)", "Clear All", "Request Samples for Saved" | Slide-up bottom sheet on mobile (<768px) displaying saved cards |
| **F14** | **Experience Centre & Dealer Finder** | Filter chip toggle; real-time card visibility filter + smooth scroll | Click state chip or type in search box | `0.25s ease-out` | "All Centres", "Delhi", "Karnataka", "Rajasthan", "Gujarat", "Punjab", "View on Map", "Call" | Single-column card stack with click-to-call direct links |
| **F15** | **Project & Gallery Filter** | URL hash sync (`#national`, `#international`); card grid fade-up stagger | Click region tab or category chip | `0.28s cubic-bezier(0.16, 1, 0.3, 1)` | "All Projects", "International", "National (India)", "Decking", "Cladding" | Horizontally scrollable tab bar, grid transforms to 1-column cards |
| **F16** | **Pro Resources Library** | Card hover elevation with gold border accent; tab filtering by document type | Hover / click download card | `0.25s ease` | "Download Architectural Catalog", "CAD Details", "BIM Files", "Test Reports" | Direct tap triggers instant browser download with file size indicator |
| **F17** | **Sticky Mobile Bar + WhatsApp** | Fixed bottom safe-area bar; floating WhatsApp icon elevation | Fixed always visible on mobile; elevated when bar present | CSS fixed positioning | "Find Centre", "Get Samples", "Call Us", "WhatsApp" | Fixed 60px bottom bar with 4 touch actions; body padding-bottom 64px prevents content cutoff |
| **F18** | **Micro-Interactions** | Scroll reveal fade-up (40px, 0.6s); card hover zoom (scale 1.05, 0.4s); smooth anchor scroll | Scroll into viewport (IntersectionObserver) / hover | `0.6s cubic-bezier(0.16, 1, 0.3, 1)`; disabled under `prefers-reduced-motion` | N/A (Global subtle animation framework) | Animations gracefully disabled on low-power devices and reduced-motion settings |

---

## 2. Content Freeze & Non-Invention Policy
Per User Instructions:
- **Zero Hallucinated Content**: No invented marketing statistics, fictional client testimonials, or non-existent partner logos.
- If assets or copy are not present on the live `newtechwood.in` site, components will render using real existing site data or remain cleanly structured with placeholders logged in `MISSING_ASSETS.md` and `MISSING_CONTENT.md`.
- **New Labels Governance**: All UI micro-copy (e.g., "Search", "Close", "Next", "Filter") logged in `NEW_LABELS.md`.
- **Strictly No Cost Comparison**: The material calculator (F11) computes plank count and clips from area and profile dimensions only, with zero cost, price, or wood-vs-composite claims.
