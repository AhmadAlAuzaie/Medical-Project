"""
Database schema definition for the Baby Risk Certification System.
"""

SCHEMA_SQL = """
-- Baby table: stores basic baby information
CREATE TABLE IF NOT EXISTS babies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_of_birth TEXT NOT NULL,
    gestational_age_weeks REAL NOT NULL,
    birth_weight_grams INTEGER NOT NULL,
    medical_record_number TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Risk Assessment table: stores clinical assessments
CREATE TABLE IF NOT EXISTS risk_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    assessment_date TEXT NOT NULL,
    apgar_score_1min INTEGER NOT NULL CHECK(apgar_score_1min >= 0 AND apgar_score_1min <= 10),
    apgar_score_5min INTEGER NOT NULL CHECK(apgar_score_5min >= 0 AND apgar_score_5min <= 10),
    has_respiratory_issues BOOLEAN NOT NULL,
    has_infection BOOLEAN NOT NULL,
    requires_intensive_care BOOLEAN NOT NULL,
    additional_notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id)
);

-- Risk Certification table: stores certification records
CREATE TABLE IF NOT EXISTS risk_certifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baby_id INTEGER NOT NULL,
    assessment_id INTEGER NOT NULL,
    risk_level TEXT NOT NULL CHECK(risk_level IN ('low', 'moderate', 'high', 'critical')),
    risk_score REAL NOT NULL CHECK(risk_score >= 0 AND risk_score <= 100),
    certification_status TEXT NOT NULL CHECK(certification_status IN ('pending', 'certified', 'under_review', 'rejected')),
    certification_date TEXT NOT NULL,
    certified_by TEXT NOT NULL,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (baby_id) REFERENCES babies(id),
    FOREIGN KEY (assessment_id) REFERENCES risk_assessments(id)
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_babies_mrn ON babies(medical_record_number);
CREATE INDEX IF NOT EXISTS idx_assessments_baby ON risk_assessments(baby_id);
CREATE INDEX IF NOT EXISTS idx_certifications_baby ON risk_certifications(baby_id);
CREATE INDEX IF NOT EXISTS idx_certifications_status ON risk_certifications(certification_status);
"""
