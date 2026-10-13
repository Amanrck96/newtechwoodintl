# NewTechWood CRM & Admin System - Implementation Progress

## Project Overview
Hardening security, core bug fixes, Product Price List integration, Vendor <-> Admin CRM portal, and JB Glass CRM feature parity for NewTechWood India CRM.

---

## Task Matrix & Status

### Workstream 0: Security & Core Bugs
- [x] **S1. Password Hashing**: Passwords hashed with bcrypt, legacy plain text verified/migrated, passwords never returned in API responses. *(Commit: `e84caa97`)*
- [x] **S2. Restrict Sensitive Endpoints**: `/api/users` and `/api/vendors` restricted to admin/superadmin with no password leaks. *(Commit: `e84caa97`)*
- [x] **S3. Role & Token Verification**: `require_auth` helper checks token on all protected endpoints, returning 401 (unauthorized) and 403 (forbidden). *(Commit: `e84caa97`)*
- [x] **S4. Frontend Auth Fetch Wrapper**: `admin.html` and `admin/index.html` send Bearer tokens via centralized `authFetch` / `api` helper, handling 401 redirect to `/login/`. *(Commit: `e84caa97`)*
- [x] **S5. Elimination of Hardcoded Fallback Credentials**: Removed hardcoded admin credentials and localStorage mock login fallbacks from `login/index.html` and seed scripts. *(Commit: `e84caa97`)*
- [x] **S6. Git Hygiene**: Removed tracked `db/ntw_crm.db` and `__pycache__` artifacts from git; updated `.gitignore`. *(Commit: `e84caa97`)*
- [x] **S7. XSS Mitigation**: Dynamic `esc()` helper escapes HTML values across tables and modals, exposed globally on `window.esc`.
- [x] **S8. Rate Limiting & Session Hygiene**: Added IP/account-based rate limiting on `/api/auth/login` (max 5 failed attempts in 5 mins), automatic session expiry purge, and protected session checks.
- [x] **B1. Schema & Migration Alignment**: Fixed missing columns (`stage` in `pipeline_projects`) across schema and migrations. *(Commit: `e84caa97`)*
- [x] **B2. Dynamic Analytics Date Range**: Derived date range dynamically from `financial_year` instead of hardcoding 2025/2026. *(Commit: `e84caa97`)*
- [x] **B3. Financial Year Label Standardization**: Unified UI and API on standard "FY 25-26" format. *(Commit: `e84caa97`)*
- [x] **B4. Deal Source of Truth & Analytics Maths**: Deduplicated deals between waltz_orders and pipeline_projects; excluded meetings from win-rate; mathematical accuracy certified by automated tests.
- [x] **B5. Pagination Input Clamping**: Enforced `limit` clamping (1..100) and `page` >= 1 to prevent ZeroDivisionError and negative offsets. *(Commit: `e84caa97`)*
- [x] **B6. SQL Directory Search & Min-3 Rule**: Replaced N+1 Python filtering with SQL join and enforced minimum 3 characters. *(Commit: `00f2bee2`)*
- [x] **B7. Context-Aware Location & Owner Defaults**: Default location and owner derived from logged-in user context rather than hardcoding static locations.
- [x] **B8. Sequential Order Numbers**: Collision-safe sequential numbering per financial year (e.g. `ORD-2026-0001`).
- [x] **B9. Code Duplication Cleanup & Shared Assets**: Synchronized `admin.html` and `admin/index.html` with parity and shared helpers.
- [x] **B10. Large Asset / Mirrored Directory Management**: Untracked 137 legacy crawl mirror folders (`query_p_*`), mapped in `query_p_map.json` to canonical URLs, and added HTTP 301 permanent redirects in `serve.py`. *(Commit: `f6c58c24`)*
- [x] **B11. Cloud Deployment Configuration**: Created Vercel serverless bridge (`api/index.py`), Dockerfile, and Render blueprint with PostgreSQL support toggle. *(Commit: `41a938d7`)*

---

### Workstream 1: Product Price List (TECHWOOD WPC)
- [x] **P1. Quote Calculator Formula**: Planks = `ceil(area * (1 + wastage) / plank_area)`, billed sft = `planks * plank_area`, clips = `planks * clips_per_plank`, GST per line item. *(Verified in `tests/test_workstream1.py`)*
- [x] **P2. Link Products to Orders**: Add/Edit Order product selector with quantity/area auto-filling `final_amount` and saving order lines (`order_lines`).
- [x] **P3. Product Distribution Dashboard Chart**: Feed "Product Chart by Amount / Sq.ft" from real order line data grouped by product category.
- [x] **P4. Role-Based Price Tiers**: Architect and Dealer specific pricing catalogs supported via permissions (`wholesale_catalog`).
- [x] **P5. Quotation Document Generation**: Formatted Word/HTML quotation with logo, and "Convert quote to Pipeline / Order" automated bridge.
- [x] **P6. Excel Bulk Import / Update**: Bulk import/update from `PPT - TECHWOOD (1).xlsx` with openpyxl validation and preview.
- [x] **P7. Variants, Validity & Stock**: Product color variants (Antique, Teak, IPE, Maple), price validity dates, and stock/lead time indicators.
- [x] **P8. Image Management**: Real image upload with validation, local storage in `/product-images/`, and screenshot flags ("Needs Better Image").

---

### Workstream 2: Vendor <-> Admin CRM
- [x] **Data Model (Migration 006)**: Create `vendor_requests`, `request_activity`, and `request_attachments` tables; link `vendor_user_id` to orders, meetings, invitations, pipeline projects. *(Verified in `tests/test_workstream2.py`)*
- [x] **Server-Side Scoping**: Enforce that vendor tokens can only read and write rows where `vendor_user_id == user.id`. Forbidden/not-found (403/404) for cross-vendor access. *(Verified in `tests/test_workstream2.py`)*
- [x] **Vendor Portal (`admin/vendor.html`)**: Dedicated portal for vendors: My Open Requests, New Request form, Status Timeline & reply box, My Orders, Tiered Catalog. *(Verified in `tests/test_e2e_playwright.py`)*
- [x] **Admin Request Inbox**: Request inbox with status badges, SLA traffic-light indicators (green on time, amber due soon, red overdue), assignment, comments, internal-only notes. *(Verified in `tests/test_workstream2.py` and `tests/test_e2e_playwright.py`)*
- [x] **Vendor 360 View**: Comprehensive vendor profile, all linked requests, orders, meetings, invitations, total business value, average response time. *(Verified in `tests/test_workstream2.py` and `tests/test_e2e_playwright.py`)*
- [x] **Export & Pluggable Notifications**: CSV/Excel export of requests and vendor history; pluggable notifications interface (email/WhatsApp). *(Verified in `tests/test_workstream2.py`)*

---

### Workstream 3: JB Glass CRM Feature Parity
- [x] **Dashboard Parity**: Multi-select Month with Apply, FY selector, chart filter toggles. *(Commit: `00f2bee2`)*
- [x] **Feedback Resolution**: Interactive feedback-pending workflow with live badge update. *(Commit: `b7f708f9`)*
- [x] **Directory & Meeting Parity**: Multi-sheet Excel exports, base64 meeting images upload and ZIP download (`/api/directory/meetings/images/zip`). *(Commit: `00f2bee2`)*
- [x] **Waltz Orders Parity**: Word quote `.doc` export, `/api/orders/convert` status lifecycle. *(Commit: `00f2bee2`)*
- [x] **Sortable Tables & Min-3 Search**: Table headers sortable on Meetings, Visitors, Orders; min-3 characters search enforced. *(Commit: `00f2bee2`)*

---

## Assumptions & Design Choices
1. **GST Slab**: Default 18% applied to WPC products and accessories.
2. **Clad Clips**: Default 7 clips per plank for Clads.
3. **Product Codes**: UH94 is preserved as a distinct variation/code of Twix.
4. **Backend Architecture**: Python HTTP server locally (`serve.py`), Vercel serverless entrypoint (`api/index.py`), Dockerfile container for production platforms.
5. **Session Lifetime**: 24-hour token expiry with automatic cleanup of expired records.
