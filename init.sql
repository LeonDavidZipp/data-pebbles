CREATE SCHEMA IF NOT EXISTS bronze;

CREATE SCHEMA IF NOT EXISTS silver;

CREATE SCHEMA IF NOT EXISTS gold;

CREATE SCHEMA IF NOT EXISTS platinum;

CREATE TYPE file_status AS ENUM ('active', 'archived', 'deleted');

CREATE TABLE IF NOT EXISTS bronze.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    s3_bucket TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_source_metadata_s3_bucket ON bronze.source_metadata (s3_bucket);

CREATE TABLE IF NOT EXISTS bronze.source_versions (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES bronze.source_metadata (id) ON DELETE CASCADE,
    status file_status NOT NULL DEFAULT 'active',
    s3_key TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_id, version_number)
);

CREATE INDEX IF NOT EXISTS idx_source_versions_source_id ON internal.source_versions (source_id);

CREATE INDEX IF NOT EXISTS idx_source_versions_status ON internal.source_versions (status);

CREATE TABLE IF NOT EXISTS silver.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    from_source_ids BIGINT[] NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_silver_source_metadata_name ON silver.source_metadata (name);

CREATE TABLE IF NOT EXISTS gold.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    from_source_ids BIGINT[] NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gold_source_metadata_name ON gold.source_metadata (name);