-- Migration 004: Phase 1 Security & Schema Fixes
-- Applied: 2026-10-14

-- Cleanup: delete expired sessions
DELETE FROM sessions WHERE expires_at < datetime('now');

-- Record this migration
INSERT OR IGNORE INTO schema_migrations (version) VALUES ('004_phase1_security');
