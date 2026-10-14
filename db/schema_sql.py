"""Consolidated database schema for NewTechWood CRM.
Provides the complete SQLite DDL with IF NOT EXISTS for all tables and indexes.
This avoids runtime dependency on external .sql files in serverless/packaged environments.
"""

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

-- 1. Schema Migrations tracker
CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Users & RBAC
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    vendor_id TEXT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT NOT NULL CHECK(role IN ('admin', 'superadmin', 'architect', 'dealer', 'sales')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'suspended')),
    permissions TEXT,
    avatar_initials TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Sessions
CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Projects & Pipeline
CREATE TABLE IF NOT EXISTS pipeline_projects (
    id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    client_name TEXT NOT NULL,
    location TEXT,
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'India',
    financial_year TEXT NOT NULL,
    month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),
    day_bracket TEXT NOT NULL CHECK(day_bracket IN ('1-5', '6-10', '11-15', '16-20', '21-25', '26-31')),
    category TEXT,
    total_value REAL NOT NULL DEFAULT 0.0,
    sq_ft REAL NOT NULL DEFAULT 0.0,
    discount_pct REAL NOT NULL DEFAULT 0.0,
    days_pipeline_to_win INTEGER DEFAULT 0,
    stage TEXT NOT NULL DEFAULT 'Pipeline' CHECK(stage IN ('Pipeline', 'Win', 'Lost')),
    feedback_pending BOOLEAN DEFAULT 0,
    feedback_notes TEXT,
    owner_name TEXT DEFAULT 'Rohan Verma',
    vendor_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Directory Firms
CREATE TABLE IF NOT EXISTS directory_firms (
    id TEXT PRIMARY KEY,
    firm_name TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('PRO', 'Architect', 'PROPLUS')),
    city TEXT,
    state TEXT,
    country TEXT DEFAULT 'India',
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Directory Contacts
CREATE TABLE IF NOT EXISTS directory_contacts (
    id TEXT PRIMARY KEY,
    firm_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    user_type TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(firm_id) REFERENCES directory_firms(id) ON DELETE CASCADE
);

-- 7. Meetings
CREATE TABLE IF NOT EXISTS meetings (
    id TEXT PRIMARY KEY,
    meeting_date DATE NOT NULL,
    firm_name TEXT NOT NULL,
    guest_name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    user_type TEXT NOT NULL CHECK(user_type IN ('Existing', 'New')),
    guest_type TEXT NOT NULL,
    country TEXT DEFAULT 'India',
    state TEXT,
    city TEXT,
    status TEXT DEFAULT 'Completed',
    discussion_notes TEXT,
    image_urls TEXT,
    owner_name TEXT DEFAULT 'Rohan Verma',
    vendor_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. ID Invitations
CREATE TABLE IF NOT EXISTS id_invitations (
    id TEXT PRIMARY KEY,
    invitation_code TEXT UNIQUE NOT NULL,
    recipient_name TEXT NOT NULL,
    firm_name TEXT NOT NULL,
    recipient_email TEXT,
    mobile TEXT,
    invitation_link TEXT NOT NULL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Accepted', 'Expired')),
    vendor_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- 9. ID Visitors
CREATE TABLE IF NOT EXISTS id_visitors (
    id TEXT PRIMARY KEY,
    visitor_type TEXT NOT NULL,
    name TEXT NOT NULL,
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    firm TEXT NOT NULL,
    link_created_date DATE NOT NULL,
    form_submitted_date DATE,
    country TEXT DEFAULT 'India',
    state TEXT,
    city TEXT,
    event_year TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Go Pro Assets
CREATE TABLE IF NOT EXISTS go_pro_assets (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    creator TEXT NOT NULL,
    file_type TEXT NOT NULL DEFAULT 'MP4 Video',
    duration TEXT NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    category TEXT DEFAULT 'Installation Guide',
    views_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Waltz Orders
CREATE TABLE IF NOT EXISTS waltz_orders (
    id TEXT PRIMARY KEY,
    order_number TEXT UNIQUE NOT NULL,
    project_name TEXT NOT NULL,
    client_name TEXT NOT NULL,
    country TEXT DEFAULT 'India',
    state TEXT,
    city TEXT,
    order_date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Lost', 'Pipeline', 'Win')),
    final_amount REAL NOT NULL DEFAULT 0.0,
    source TEXT NOT NULL,
    notes TEXT,
    owner_name TEXT DEFAULT 'Rohan Verma',
    vendor_user_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Products (TECHWOOD WPC catalog)
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    sl_no INTEGER,
    name TEXT NOT NULL,
    code TEXT,
    category TEXT NOT NULL CHECK(category IN ('Cladding', 'Decking', 'Pergola', 'Accessories')),
    item_type TEXT NOT NULL DEFAULT 'main' CHECK(item_type IN ('main', 'accessory')),
    image_url TEXT,
    dimensions TEXT,
    length_mm REAL,
    width_mm REAL,
    thickness_mm REAL,
    price REAL NOT NULL CHECK(price >= 0),
    dealer_price REAL,
    architect_price REAL,
    price_unit TEXT NOT NULL CHECK(price_unit IN ('SFT', 'Plank', 'Clip', 'Profile')),
    gst_extra INTEGER NOT NULL DEFAULT 1,
    gst_pct REAL NOT NULL DEFAULT 18.0,
    application TEXT,
    clip_product_id TEXT,
    clips_per_plank INTEGER,
    variants TEXT DEFAULT '["Antique", "Teak", "IPE", "Maple"]',
    validity_date DATE,
    stock_status TEXT DEFAULT 'in_stock' CHECK(stock_status IN ('in_stock', 'lead_time', 'out_of_stock')),
    lead_time_days INTEGER DEFAULT 7,
    needs_better_image INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(clip_product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- 13. Product Price History
CREATE TABLE IF NOT EXISTS product_price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    old_price REAL,
    new_price REAL NOT NULL,
    tier TEXT DEFAULT 'standard',
    changed_by TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- 14. Order Lines
CREATE TABLE IF NOT EXISTS order_lines (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL,
    product_id TEXT NOT NULL,
    product_name TEXT NOT NULL,
    variant_color TEXT,
    area_sft REAL,
    qty REAL NOT NULL,
    unit TEXT NOT NULL,
    rate REAL NOT NULL,
    amount REAL NOT NULL,
    gst_pct REAL DEFAULT 18.0,
    gst_amount REAL DEFAULT 0.0,
    total_amount REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES waltz_orders(id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- 15. Vendor Requests & Activity
CREATE TABLE IF NOT EXISTS vendor_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_no TEXT UNIQUE NOT NULL,
    vendor_user_id TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN (
        'Sample request',
        'Quote / price request',
        'Technical consultation / site visit',
        'Order (PO) request',
        'CAD / specification request',
        'Support / complaint'
    )),
    title TEXT NOT NULL,
    details TEXT,
    priority TEXT NOT NULL DEFAULT 'Medium' CHECK(priority IN ('Low', 'Medium', 'High', 'Urgent')),
    status TEXT NOT NULL DEFAULT 'New' CHECK(status IN (
        'New',
        'In Review',
        'Quoted/Approved',
        'In Progress',
        'Completed',
        'Rejected',
        'Cancelled'
    )),
    assigned_to TEXT,
    due_date DATE,
    linked_product_id TEXT,
    linked_order_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    FOREIGN KEY (vendor_user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES users(id),
    FOREIGN KEY (linked_product_id) REFERENCES products(id),
    FOREIGN KEY (linked_order_id) REFERENCES waltz_orders(id)
);

CREATE TABLE IF NOT EXISTS request_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL,
    from_status TEXT,
    to_status TEXT,
    comment TEXT,
    is_internal INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES vendor_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (actor_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS request_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    file_name TEXT NOT NULL,
    file_url TEXT NOT NULL,
    file_size INTEGER DEFAULT 0,
    uploaded_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES vendor_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);

-- 16. Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    channel TEXT DEFAULT 'in_app',
    is_read INTEGER DEFAULT 0,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_projects_fy ON pipeline_projects(financial_year, month);
CREATE INDEX IF NOT EXISTS idx_projects_stage ON pipeline_projects(stage);
CREATE INDEX IF NOT EXISTS idx_contacts_firm ON directory_contacts(firm_id);
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(meeting_date);
CREATE INDEX IF NOT EXISTS idx_visitors_event ON id_visitors(event_year);
CREATE INDEX IF NOT EXISTS idx_orders_number ON waltz_orders(order_number);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category, status);
CREATE INDEX IF NOT EXISTS idx_price_history_product ON product_price_history(product_id, changed_at);
CREATE INDEX IF NOT EXISTS idx_order_lines_order ON order_lines(order_id);
CREATE INDEX IF NOT EXISTS idx_order_lines_product ON order_lines(product_id);
CREATE INDEX IF NOT EXISTS idx_vreq_vendor ON vendor_requests(vendor_user_id);
CREATE INDEX IF NOT EXISTS idx_vreq_status ON vendor_requests(status);
CREATE INDEX IF NOT EXISTS idx_vreq_assigned ON vendor_requests(assigned_to);
CREATE INDEX IF NOT EXISTS idx_ract_request ON request_activity(request_id);
CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_orders_vendor ON waltz_orders(vendor_user_id);
CREATE INDEX IF NOT EXISTS idx_meetings_vendor ON meetings(vendor_user_id);
"""
