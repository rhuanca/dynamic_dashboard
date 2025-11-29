-- Equipment Inventory Database Schema
-- Business-realistic equipment tracking system
-- Main Equipment Table
CREATE TABLE IF NOT EXISTS equipment (
    -- Identity
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_tag TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    manufacturer TEXT,
    model_number TEXT,
    serial_number TEXT,
    -- Financial
    purchase_date DATE,
    purchase_price REAL,
    current_value REAL,
    depreciation_rate REAL,
    -- Location & Assignment
    department TEXT NOT NULL,
    location TEXT,
    assigned_to TEXT,
    -- Status & Maintenance
    status TEXT DEFAULT 'Active',
    condition TEXT,
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    maintenance_interval_days INTEGER,
    warranty_expiry_date DATE,
    -- Metadata
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_department ON equipment(department);
CREATE INDEX IF NOT EXISTS idx_status ON equipment(status);
CREATE INDEX IF NOT EXISTS idx_category ON equipment(category);
CREATE INDEX IF NOT EXISTS idx_next_maintenance ON equipment(next_maintenance_date);
CREATE INDEX IF NOT EXISTS idx_asset_tag ON equipment(asset_tag);
-- Maintenance Log Table
CREATE TABLE IF NOT EXISTS maintenance_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id INTEGER NOT NULL,
    maintenance_date DATE NOT NULL,
    maintenance_type TEXT,
    performed_by TEXT,
    cost REAL,
    description TEXT,
    next_scheduled_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_maintenance_equipment ON maintenance_log(equipment_id);
CREATE INDEX IF NOT EXISTS idx_maintenance_date ON maintenance_log(maintenance_date);
-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action TEXT NOT NULL,
    equipment_id INTEGER,
    user_query TEXT,
    agent_name TEXT,
    changes TEXT,
    success BOOLEAN
);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_equipment ON audit_log(equipment_id);