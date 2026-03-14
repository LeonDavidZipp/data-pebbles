-- bronze layer

CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TYPE bronze.file_status AS ENUM ('active', 'archived', 'deleted');

-- stores metadata about the source, e.g. "customer_data", "sales_data", etc.
CREATE TABLE IF NOT EXISTS bronze.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_source_metadata_name ON bronze.source_metadata (name);

-- stores metadata about each version of the source, e.g. version number, S3 key, etc. This allows us to keep track of multiple versions of the same source and their statuses (active, archived, deleted).
CREATE TABLE IF NOT EXISTS bronze.source_versions (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES bronze.source_metadata (id) ON DELETE CASCADE,
    version BIGINT NOT NULL,
    status file_status NOT NULL DEFAULT 'active',
    s3_key TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_id, version)
);

CREATE INDEX IF NOT EXISTS idx_source_versions_source_id ON bronze.source_versions (source_id);

CREATE INDEX IF NOT EXISTS idx_source_versions_status ON bronze.source_versions (status);

-- silver layer

CREATE SCHEMA IF NOT EXISTS silver;

-- stores metadata about the source in the silver layer, e.g. "customer_data", "sales_data", etc. This allows us to keep track of the lineage from bronze to silver, and also to store any additional metadata specific to the silver layer if needed.
CREATE TABLE IF NOT EXISTS silver.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_silver_source_metadata_name ON silver.source_metadata (name);

-- stores the lineage information from bronze to silver, i.e. which version of the bronze source was used to create which version of the silver source. This allows us to trace back the lineage and also to keep track of multiple versions of the silver source and their corresponding bronze versions.
CREATE TABLE silver.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES silver.source_metadata (id) ON DELETE CASCADE,
    delta_version BIGINT NOT NULL,
    from_source_id BIGINT NOT NULL REFERENCES bronze.source_versions (id) ON DELETE RESTRICT, -- TODO: is this actually correct?
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_silver_version_lineage_source_id ON silver.version_lineage (source_id);

CREATE INDEX IF NOT EXISTS idx_silver_version_lineage_from_source_id ON silver.version_lineage (from_source_id);

-- gold layer

CREATE SCHEMA IF NOT EXISTS gold;

-- stores metadata about the source in the gold layer, e.g. "customer_data", "sales_data", etc. This allows us to keep track of the lineage from silver to gold, and also to store any additional metadata specific to the gold layer if needed.
CREATE TABLE IF NOT EXISTS gold.source_metadata (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gold_source_metadata_name ON gold.source_metadata (name);

-- stores the lineage information from silver to gold, i.e. which version of the silver source was used to create which version of the gold source. This allows us to trace back the lineage and also to keep track of multiple versions of the gold source and their corresponding silver versions.
CREATE TABLE gold.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES gold.source_metadata (id) ON DELETE CASCADE,
    delta_version BIGINT NOT NULL, -- gold's Delta Lake version
    from_source_id BIGINT NOT NULL REFERENCES silver.source_metadata (id) ON DELETE RESTRICT,
    from_delta_version BIGINT NOT NULL, -- silver's Delta Lake version used
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gold_version_lineage_source_id ON gold.version_lineage (source_id);

CREATE INDEX IF NOT EXISTS idx_gold_version_lineage_from_source_id ON gold.version_lineage (from_source_id);