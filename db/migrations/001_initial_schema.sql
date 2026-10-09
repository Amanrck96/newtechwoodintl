-- Migration 001: Initial CRM Schema
-- Applied: 2026-10-09

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users & Auth
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'superadmin', 'architect', 'dealer', 'sales')),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'suspended')),
    avatar_initials TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Projects & Pipeline
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
    stage TEXT NOT NULL CHECK(stage IN ('Pipeline', 'Win', 'Lost')),
    feedback_pending BOOLEAN DEFAULT 0,
    feedback_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Directory Module
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

-- Meetings
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ID Invitations
CREATE TABLE IF NOT EXISTS id_invitations (
    id TEXT PRIMARY KEY,
    invitation_code TEXT UNIQUE NOT NULL,
    recipient_name TEXT NOT NULL,
    firm_name TEXT NOT NULL,
    recipient_email TEXT,
    mobile TEXT,
    invitation_link TEXT NOT NULL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Accepted', 'Expired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- ID Visitors
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

-- Go Pro / Education Assets
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

-- Waltz Orders
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_projects_fy ON pipeline_projects(financial_year, month);
CREATE INDEX IF NOT EXISTS idx_projects_stage ON pipeline_projects(stage);
CREATE INDEX IF NOT EXISTS idx_contacts_firm ON directory_contacts(firm_id);
CREATE INDEX IF NOT EXISTS idx_meetings_date ON meetings(meeting_date);
CREATE INDEX IF NOT EXISTS idx_visitors_event ON id_visitors(event_year);
CREATE INDEX IF NOT EXISTS idx_orders_number ON waltz_orders(order_number);
