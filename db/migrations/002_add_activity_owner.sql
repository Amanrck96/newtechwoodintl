-- Migration 002: Add Activity Owner and Representative Tracking
-- Applied: 2026-10-09

ALTER TABLE pipeline_projects ADD COLUMN owner_name TEXT DEFAULT 'Rohan Verma';
ALTER TABLE waltz_orders ADD COLUMN owner_name TEXT DEFAULT 'Rohan Verma';
ALTER TABLE meetings ADD COLUMN owner_name TEXT DEFAULT 'Rohan Verma';

-- Add sample owner variation for rich analytics filtering
UPDATE pipeline_projects SET owner_name = 'Super Administrator' WHERE id IN ('PRJ-101', 'PRJ-103', 'PRJ-108', 'PRJ-110', 'PRJ-118');
UPDATE pipeline_projects SET owner_name = 'Skyline Architecture Studio' WHERE id IN ('PRJ-107', 'PRJ-112', 'PRJ-115');
UPDATE pipeline_projects SET owner_name = 'Lumber Life Premier Partner' WHERE id IN ('PRJ-105', 'PRJ-114', 'PRJ-120');

UPDATE waltz_orders SET owner_name = 'Super Administrator' WHERE id IN ('ORD-W-501', 'ORD-W-504', 'ORD-W-506');
UPDATE waltz_orders SET owner_name = 'Skyline Architecture Studio' WHERE id IN ('ORD-W-502', 'ORD-W-505');
UPDATE waltz_orders SET owner_name = 'Lumber Life Premier Partner' WHERE id IN ('ORD-W-503', 'ORD-W-507');

UPDATE meetings SET owner_name = 'Super Administrator' WHERE id IN ('MTG-01', 'MTG-02');
UPDATE meetings SET owner_name = 'Skyline Architecture Studio' WHERE id IN ('MTG-04');
