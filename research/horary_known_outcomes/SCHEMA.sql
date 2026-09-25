PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS cases (
  case_id TEXT PRIMARY KEY,
  source_site TEXT NOT NULL,
  source_url TEXT,
  source_index_url TEXT,
  category TEXT,
  title TEXT NOT NULL,
  question_text TEXT,
  topic_house INTEGER,
  question_utc TEXT,
  latitude REAL,
  longitude REAL,
  location_label TEXT,
  reconstructibility TEXT NOT NULL DEFAULT 'unknown',
  created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS snapshots (
  snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
  case_id TEXT NOT NULL REFERENCES cases(case_id),
  kind TEXT NOT NULL,
  source_url TEXT NOT NULL,
  retrieved_at TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  storage_path TEXT NOT NULL,
  UNIQUE(case_id,kind,sha256)
);
CREATE TABLE IF NOT EXISTS outcomes (
  outcome_id INTEGER PRIMARY KEY AUTOINCREMENT,
  case_id TEXT NOT NULL REFERENCES cases(case_id),
  outcome_code TEXT NOT NULL CHECK(outcome_code IN ('YES','NO','AMBIGUOUS','UNKNOWN')),
  outcome_text TEXT,
  outcome_source_url TEXT,
  outcome_post_label TEXT,
  coded_at TEXT NOT NULL,
  coding_rule TEXT NOT NULL,
  evidence_sha256 TEXT,
  supersedes_outcome_id INTEGER REFERENCES outcomes(outcome_id)
);
CREATE TABLE IF NOT EXISTS experiment_membership (
  experiment_id TEXT NOT NULL,
  case_id TEXT NOT NULL REFERENCES cases(case_id),
  included INTEGER NOT NULL,
  exclusion_reason TEXT,
  outcome_exposed_before_prediction INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY(experiment_id,case_id)
);
CREATE TABLE IF NOT EXISTS corpus_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
