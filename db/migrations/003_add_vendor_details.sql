-- Migration 003: Add Vendor Details and Permissions
-- Applied: 2026-10-10

ALTER TABLE users ADD COLUMN vendor_id TEXT;
ALTER TABLE users ADD COLUMN phone TEXT;
ALTER TABLE users ADD COLUMN permissions TEXT;

-- Update existing default users with proper vendor IDs and permission scopes
UPDATE users SET vendor_id = 'ADMIN-001', phone = '+91 99999 00001', permissions = 'all' WHERE id = 'admin';
UPDATE users SET vendor_id = 'ADMIN-002', phone = '+91 99999 00002', permissions = 'all' WHERE id = 'admin_user';
UPDATE users SET vendor_id = 'SAL-2026-001', phone = '+91 98333 45678', permissions = 'pipeline,orders,meetings,visitors' WHERE id = 'sales_01';
UPDATE users SET vendor_id = 'VND-2026-001', phone = '+91 98200 12345', permissions = 'gopro_cad,pipeline_specs,meetings,invitations' WHERE id = 'arch_01';
UPDATE users SET vendor_id = 'DLR-902-IND', phone = '+91 98111 67890', permissions = 'waltz_orders,wholesale_catalog,invitations' WHERE id = 'dlr_01';
