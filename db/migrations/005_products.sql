-- Migration 005: Products, Price History, and Order Lines
-- Supports Workstream 1: TECHWOOD WPC Price List, Tiers, Variants, and Order Linking

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

CREATE INDEX IF NOT EXISTS idx_products_category ON products(category, status);
CREATE INDEX IF NOT EXISTS idx_price_history_product ON product_price_history(product_id, changed_at);
CREATE INDEX IF NOT EXISTS idx_order_lines_order ON order_lines(order_id);
CREATE INDEX IF NOT EXISTS idx_order_lines_product ON order_lines(product_id);
