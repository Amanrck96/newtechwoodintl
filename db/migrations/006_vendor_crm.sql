-- Migration 006: Vendor CRM Tables and Scoping Schema
-- Applied: 2026-10-14

-- 1. Vendor Requests
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

-- 2. Request Activity Log
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

-- 3. Request Attachments
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

-- 4. In-App Notifications
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

-- 5. Add vendor_user_id column to existing entity tables if not present
ALTER TABLE waltz_orders ADD COLUMN vendor_user_id TEXT;
ALTER TABLE meetings ADD COLUMN vendor_user_id TEXT;
ALTER TABLE id_invitations ADD COLUMN vendor_user_id TEXT;
ALTER TABLE pipeline_projects ADD COLUMN vendor_user_id TEXT;

-- 6. Backfill existing records with vendor IDs
UPDATE waltz_orders SET vendor_user_id = 'arch_01' WHERE owner_name = 'Skyline Architecture Studio';
UPDATE waltz_orders SET vendor_user_id = 'dlr_01' WHERE owner_name = 'Lumber Life Premier Partner';
UPDATE waltz_orders SET vendor_user_id = 'sales_01' WHERE owner_name = 'Rohan Verma';

UPDATE meetings SET vendor_user_id = 'arch_01' WHERE owner_name = 'Skyline Architecture Studio' OR guest_name LIKE '%Sanjay Puri%' OR guest_name LIKE '%Vikram%';
UPDATE meetings SET vendor_user_id = 'dlr_01' WHERE owner_name = 'Lumber Life Premier Partner' OR guest_name LIKE '%Manish%';

UPDATE pipeline_projects SET vendor_user_id = 'arch_01' WHERE owner_name = 'Skyline Architecture Studio';
UPDATE pipeline_projects SET vendor_user_id = 'dlr_01' WHERE owner_name = 'Lumber Life Premier Partner';
UPDATE pipeline_projects SET vendor_user_id = 'sales_01' WHERE owner_name = 'Rohan Verma';

UPDATE id_invitations SET vendor_user_id = 'arch_01' WHERE id IN ('INV-001', 'INV-002');
UPDATE id_invitations SET vendor_user_id = 'dlr_01' WHERE id IN ('INV-003', 'INV-004');

-- 7. Indexes
CREATE INDEX IF NOT EXISTS idx_vreq_vendor ON vendor_requests(vendor_user_id);
CREATE INDEX IF NOT EXISTS idx_vreq_status ON vendor_requests(status);
CREATE INDEX IF NOT EXISTS idx_vreq_assigned ON vendor_requests(assigned_to);
CREATE INDEX IF NOT EXISTS idx_ract_request ON request_activity(request_id);
CREATE INDEX IF NOT EXISTS idx_notif_user ON notifications(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_orders_vendor ON waltz_orders(vendor_user_id);
CREATE INDEX IF NOT EXISTS idx_meetings_vendor ON meetings(vendor_user_id);
