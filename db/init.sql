-- types

CREATE TYPE version_status AS ENUM ('active', 'archived', 'deleted');

-- projects

CREATE SCHEMA IF NOT EXISTS projects;

-- stores metadata about the project, e.g. project name, description, etc. This allows us to group related resources together under a common project and also to store any additional metadata specific to the project if needed.
CREATE TABLE IF NOT EXISTS projects.project_metadata (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL UNIQUE,
    description VARCHAR(512),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- raw layer

CREATE SCHEMA IF NOT EXISTS raw;

-- stores metadata about the resource, e.g. "customer_data", "sales_data", etc.
CREATE TABLE IF NOT EXISTS raw.resource_metadata (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(512),
    project_id BIGINT NOT NULL REFERENCES projects.project_metadata (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_resource_metadata_name ON raw.resource_metadata (name);

-- stores metadata about each version of the resource, e.g. version number, S3 key, etc. This allows us to keep track of multiple versions of the same resource and their statuses (active, archived, deleted).
CREATE TABLE IF NOT EXISTS raw.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    resource_id BIGINT NOT NULL REFERENCES raw.resource_metadata (id) ON DELETE CASCADE,
    version BIGINT NOT NULL,
    status version_status NOT NULL DEFAULT 'archived',
    s3_key TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (resource_id, version)
);

CREATE INDEX IF NOT EXISTS idx_version_lineage_resource_id ON raw.version_lineage (resource_id);

CREATE INDEX IF NOT EXISTS idx_version_lineage_status ON raw.version_lineage (status);

-- bronze layer

CREATE SCHEMA IF NOT EXISTS bronze;

-- stores metadata about the resource in the bronze layer, e.g. "customer_data", "sales_data", etc. This allows us to keep track of the lineage from silver to bronze, and also to store any additional metadata specific to the bronze layer if needed.
CREATE TABLE IF NOT EXISTS bronze.resource_metadata (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(512),
    project_id BIGINT NOT NULL REFERENCES projects.project_metadata (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bronze_resource_metadata_name ON bronze.resource_metadata (name);

-- stores the lineage information from raw to bronze, i.e. which version of the raw resource was used to create which version of the bronze resource. This allows us to trace back the lineage and also to keep track of multiple versions of the bronze resource and their corresponding raw versions.
CREATE TABLE bronze.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    resource_id BIGINT NOT NULL REFERENCES bronze.resource_metadata (id) ON DELETE CASCADE,
    delta_version BIGINT NOT NULL, -- bronze's Delta Lake version
    from_resource_id BIGINT NOT NULL REFERENCES raw.version_lineage (id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_bronze_version_lineage_resource_id ON bronze.version_lineage (resource_id);

CREATE INDEX IF NOT EXISTS idx_bronze_version_lineage_from_resource_id ON bronze.version_lineage (from_resource_id);

-- silver layer

CREATE SCHEMA IF NOT EXISTS silver;

-- stores metadata about the resource in the silver layer, e.g. "customer_data", "sales_data", etc. This allows us to keep track of the lineage from bronze to silver, and also to store any additional metadata specific to the silver layer if needed.
CREATE TABLE IF NOT EXISTS silver.resource_metadata (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(512),
    project_id BIGINT NOT NULL REFERENCES projects.project_metadata (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_silver_resource_metadata_name ON silver.resource_metadata (name);

-- stores the lineage information from bronze to silver, i.e. which version of the bronze resource was used to create which version of the silver resource. This allows us to trace back the lineage and also to keep track of multiple versions of the silver resource and their corresponding bronze versions.
CREATE TABLE silver.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    resource_id BIGINT NOT NULL REFERENCES silver.resource_metadata (id) ON DELETE CASCADE,
    delta_version BIGINT NOT NULL,
    from_resource_id BIGINT NOT NULL REFERENCES bronze.version_lineage (id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_silver_version_lineage_resource_id ON silver.version_lineage (resource_id);

CREATE INDEX IF NOT EXISTS idx_silver_version_lineage_from_resource_id ON silver.version_lineage (from_resource_id);

-- gold layer

CREATE SCHEMA IF NOT EXISTS gold;

-- stores metadata about the resource in the gold layer, e.g. "customer_data", "sales_data", etc. This allows us to keep track of the lineage from silver to gold, and also to store any additional metadata specific to the gold layer if needed.
CREATE TABLE IF NOT EXISTS gold.resource_metadata (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    description VARCHAR(512),
    project_id BIGINT NOT NULL REFERENCES projects.project_metadata (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gold_resource_metadata_name ON gold.resource_metadata (name);

-- stores the lineage information from silver to gold, i.e. which version of the silver resource was used to create which version of the gold resource. This allows us to trace back the lineage and also to keep track of multiple versions of the gold resource and their corresponding silver versions.
CREATE TABLE gold.version_lineage (
    id BIGSERIAL PRIMARY KEY,
    resource_id BIGINT NOT NULL REFERENCES gold.resource_metadata (id) ON DELETE CASCADE,
    delta_version BIGINT NOT NULL, -- gold's Delta Lake version
    from_resource_id BIGINT NOT NULL REFERENCES silver.version_lineage (id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_gold_version_lineage_resource_id ON gold.version_lineage (resource_id);

CREATE INDEX IF NOT EXISTS idx_gold_version_lineage_from_resource_id ON gold.version_lineage (from_resource_id);