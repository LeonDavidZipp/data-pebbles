CREATE SCHEMA IF NOT EXISTS bronze;

CREATE SCHEMA IF NOT EXISTS silver;

CREATE SCHEMA IF NOT EXISTS gold;

CREATE SCHEMA IF NOT EXISTS platinum;

CREATE TYPE file_status AS ENUM ('active', 'archived', 'deleted');

CREATE TABLE IF NOT EXISTS bronze.source_metadata (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    s3_bucket TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_source_metadata_s3_bucket ON internal.source_metadata (s3_bucket);

CREATE TABLE IF NOT EXISTS bronze.source_versions (
    id SERIAL PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES internal.source_metadata (id) ON DELETE CASCADE,
    status file_status NOT NULL DEFAULT 'active',
    s3_key TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_id, version_number)
);

CREATE INDEX IF NOT EXISTS idx_source_versions_source_id ON internal.source_versions (source_id);

CREATE INDEX IF NOT EXISTS idx_source_versions_status ON internal.source_versions (status);