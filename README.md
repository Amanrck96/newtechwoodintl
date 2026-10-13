# NewTechWood India CRM & Partner Portal

A high-performance, secure, and full-featured Customer Relationship Management (CRM) and Partner Portal for **NewTechWood India** (`newtechwoodintl`). Built for enterprise reliability, high responsiveness, and complete functional parity with the JB Glass CRM reference architecture (`webapp2.jbglass.in`).

---

## 🚀 Key Features

### 1. Workstream 0: Security & Core Hardening
- **Bcrypt Password Security**: Zero plain text credentials; all user passwords hashed with salted bcrypt.
- **Strict Role-Based Access Control (RBAC)**: Enforced via `require_auth` with 401 Unauthorized / 403 Forbidden status codes.
- **Sensitive Route Protection**: `/api/users` and `/api/vendors` strictly restricted to `admin` / `superadmin` with passwords permanently excluded from queries.
- **Brute-Force & Rate Limiting**: Account and IP-based rate limiting on `/api/auth/login` (max 5 failed attempts per 5 minutes) with automatic expired session purges.
- **XSS Sanitization**: Dynamic HTML escape helper (`window.esc()`) applied universally across tables, modals, and dynamic timelines.
- **Sequential Collision-Safe Order Numbering**: Year-scoped atomic sequencing (e.g., `ORD-2026-0001`).
- **Legacy URL Canonicalization**: Permanent HTTP 301 redirects for 137 legacy crawl mirror folders (`query_p_*`) mapped to canonical paths via `query_p_map.json`.

### 2. Workstream 1: TECHWOOD WPC Product Price List
- **Automated BOQ Quote Math**:
  $$\text{Planks} = \lceil \text{Area} \times (1 + \text{Wastage}) / \text{Plank Area} \rceil$$
  $$\text{Billed Sft} = \text{Planks} \times \text{Plank Area}, \quad \text{Clips} = \text{Planks} \times \text{Clips per Plank}$$
- **Multi-Tier Price Architecture**: Distinct, automated pricing catalogs for Architects, Dealers, and Retail quotes.
- **Order-Line Product Linking**: Real-time line item breakdown (`order_lines`) directly connected to commercial orders.
- **Dashboard Category Charts**: Dynamic category-based revenue and square-footage distributions.
- **Bulk Excel Import**: Built-in importer supporting Excel catalog updates (`.xlsx`) with openpyxl validation.
- **Quotation Generation & Bridge**: Downloadable Word `.doc` quotations and 1-click conversion to CRM Pipeline Projects.

### 3. Workstream 2: Dedicated Vendor <-> Admin CRM
- **Dedicated Partner Portal (`/admin/vendor.html`)**: Tailored workspace for Architects and Dealers with real-time request tracking, quote requests, and sample requests.
- **Strict Server-Side Tenant Scoping**: Multi-tenant isolation ensuring partners can only view and manage their own records (HTTP 403 on cross-tenant attempts).
- **Admin Request Inbox**: SLA traffic-light indicators (Green: on time, Amber: due soon, Red: overdue), direct assignment to sales engineers, and internal-only note separation.
- **Vendor 360 Profile**: Unified view displaying lifetime business value, order history, active/closed requests, meetings, and average response times.
- **Multi-Channel Notification Engine**: Notification interface supporting in-app alerts, email, and WhatsApp dispatch.

### 4. Workstream 3: JB Glass CRM Parity
- **Multi-Select Month Analytics**: Dynamic month and Financial Year filters for executive revenue dashboards.
- **Feedback-Pending Resolution**: Real-time meeting follow-up resolution workflow with badge counters.
- **Multi-Sheet Excel Reporting**: Formatted `.xlsx` exports for orders, pipeline, and visitors.
- **Binary Meeting Images ZIP**: Base64 meeting attachments with dynamic on-the-fly ZIP binary streaming (`/api/directory/meetings/images/zip`).
- **Search & Sort Hygiene**: Minimum 3-character database search optimization and sortable data grids.

---

## 🛠️ Technology Stack

- **Frontend**: Vanilla ES6+ JavaScript, Responsive CSS3 Design System, SheetJS (XLSX), Chart.js.
- **Backend**: Python 3 standard library with `serve.ThreadingTCPServer` and Range Request support.
- **Database**: SQLite3 (zero-configuration local) / PostgreSQL compatible (`CRM_DB_FILE` env toggle).
- **Deployment**: Vercel Serverless bridge (`api/index.py`), Dockerfile, and Render Blueprint (`render.yaml`).

---

## 💻 Local Development Setup

### Prerequisites
- Python 3.10+
- Modern web browser (Chrome, Edge, Firefox)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
pip install pytest playwright bcrypt openpyxl
```

### 2. Run Database Migrations
```bash
python db/migrate.py
```

### 3. Start the Local Server
```bash
python serve.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.
- **Admin Portal**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Partner Portal**: [http://localhost:8000/admin/vendor.html](http://localhost:8000/admin/vendor.html)
- **Login Page**: [http://localhost:8000/login/](http://localhost:8000/login/)

---

## 🧪 Automated Test Suite

The project includes an end-to-end automated test suite covering unit math, security scoping, and full Playwright browser verification:

```bash
# Run all unit, security, and integration tests:
python -m pytest tests/test_workstream0.py tests/test_workstream1.py tests/test_workstream2.py -v

# Run the full Playwright End-to-End browser journey test:
python -m pytest tests/test_e2e_playwright.py -v -s

# Run the complete test suite together:
python -m pytest tests/ -v
```

### Test Coverage Highlights:
- **`test_workstream0.py`**: Authentication token enforcement, rate limiting, role barriers, and sequential numbering.
- **`test_workstream1.py`**: Quote calculations, GST line breakdown, price tiers, Excel bulk imports, and quote-to-pipeline conversion.
- **`test_workstream2.py`**: Multi-tenant isolation (403), request state machine, internal note privacy, SLA calculation, and Vendor 360 metrics.
- **`test_e2e_playwright.py`**: Multi-context browser simulation of Partner login, request creation, Admin inbox review, timeline conversation, Vendor 360 inspection, and verification of zero console errors.

---

## 🚢 Deployment Readiness

### Vercel Serverless
Configured via `vercel.json` and `api/index.py`:
```bash
vercel --prod
```

### Docker
```bash
docker build -t newtechwood-crm .
docker run -p 8000:8000 newtechwood-crm
```

### Render
The repository includes `render.yaml` for 1-click deployment on Render with automatic environment configuration.
