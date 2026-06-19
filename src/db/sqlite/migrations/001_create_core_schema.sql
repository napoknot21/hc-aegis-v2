CREATE TABLE IF NOT EXISTS funds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    business_line TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS control_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS control_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    control_date TEXT NOT NULL,
    fund_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    severity TEXT,
    source TEXT,
    notes TEXT,
    created_by TEXT,
    updated_by TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fund_id) REFERENCES funds(id) ON DELETE RESTRICT,
    FOREIGN KEY (category_id) REFERENCES control_categories(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS control_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value REAL,
    threshold_value REAL,
    threshold_operator TEXT,
    unit TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    details_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES control_runs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS breaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    metric_id INTEGER,
    validation_status TEXT NOT NULL DEFAULT 'pending',
    validator TEXT,
    validation_comment TEXT,
    validated_at TEXT,
    remediation_due_date TEXT,
    remediation_comment TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES control_runs(id) ON DELETE CASCADE,
    FOREIGN KEY (metric_id) REFERENCES control_metrics(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT NOT NULL,
    entity_id INTEGER NOT NULL,
    action TEXT NOT NULL,
    before_json TEXT,
    after_json TEXT,
    user_email TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_funds_business_line ON funds(business_line);
CREATE INDEX IF NOT EXISTS idx_control_runs_date ON control_runs(control_date);
CREATE INDEX IF NOT EXISTS idx_control_runs_fund ON control_runs(fund_id);
CREATE INDEX IF NOT EXISTS idx_control_runs_category ON control_runs(category_id);
CREATE INDEX IF NOT EXISTS idx_control_metrics_run ON control_metrics(run_id);
CREATE INDEX IF NOT EXISTS idx_control_metrics_status ON control_metrics(status);
CREATE INDEX IF NOT EXISTS idx_breaches_run ON breaches(run_id);
CREATE INDEX IF NOT EXISTS idx_breaches_metric ON breaches(metric_id);
CREATE INDEX IF NOT EXISTS idx_breaches_validation_status ON breaches(validation_status);
CREATE INDEX IF NOT EXISTS idx_audit_events_entity ON audit_events(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_audit_events_action ON audit_events(action);

CREATE TRIGGER IF NOT EXISTS trg_funds_updated_at
AFTER UPDATE ON funds
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE funds SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_control_categories_updated_at
AFTER UPDATE ON control_categories
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE control_categories SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_control_runs_updated_at
AFTER UPDATE ON control_runs
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE control_runs SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_control_metrics_updated_at
AFTER UPDATE ON control_metrics
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE control_metrics SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_breaches_updated_at
AFTER UPDATE ON breaches
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE breaches SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
