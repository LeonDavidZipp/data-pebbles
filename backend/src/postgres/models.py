from sqlalchemy import (
	BigInteger,
	DateTime,
	ForeignKeyConstraint,
	Index,
	PrimaryKeyConstraint,
	String,
	Text,
	UniqueConstraint,
	text,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class ProjectMetadata(Base):
	__tablename__ = "project_metadata"
	__table_args__ = (
		PrimaryKeyConstraint("id", name="project_metadata_pkey"),
		UniqueConstraint("name", name="project_metadata_name_key"),
		{"schema": "projects"},
	)

	id = mapped_column(BigInteger)
	name = mapped_column(String(256), nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	description = mapped_column(String(512))

	resource_metadata: Mapped[list["ResourceMetadata"]] = relationship(
		"ResourceMetadata", uselist=True, back_populates="project"
	)
	resource_metadata_: Mapped[list["ResourceMetadata_"]] = relationship(
		"ResourceMetadata_", uselist=True, back_populates="project"
	)
	resource_metadata1: Mapped[list["ResourceMetadata1"]] = relationship(
		"ResourceMetadata1", uselist=True, back_populates="project"
	)


class ResourceMetadata(Base):
	__tablename__ = "resource_metadata"
	__table_args__ = (
		ForeignKeyConstraint(
			["project_id"],
			["projects.project_metadata.id"],
			ondelete="CASCADE",
			name="resource_metadata_project_id_fkey",
		),
		PrimaryKeyConstraint("id", name="resource_metadata_pkey"),
		Index("idx_resource_metadata_name", "name"),
		{"schema": "bronze"},
	)

	id = mapped_column(BigInteger)
	name = mapped_column(String(256), nullable=False)
	project_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	description = mapped_column(String(512))

	project: Mapped["ProjectMetadata"] = relationship(
		"ProjectMetadata", back_populates="resource_metadata"
	)
	resource_versions: Mapped[list["ResourceVersions"]] = relationship(
		"ResourceVersions", uselist=True, back_populates="resource"
	)


class ResourceMetadata_(Base):
	__tablename__ = "resource_metadata"
	__table_args__ = (
		ForeignKeyConstraint(
			["project_id"],
			["projects.project_metadata.id"],
			ondelete="CASCADE",
			name="resource_metadata_project_id_fkey",
		),
		PrimaryKeyConstraint("id", name="resource_metadata_pkey"),
		Index("idx_gold_resource_metadata_name", "name"),
		{"schema": "gold"},
	)

	id = mapped_column(BigInteger)
	name = mapped_column(String(256), nullable=False)
	project_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	description = mapped_column(String(512))

	project: Mapped["ProjectMetadata"] = relationship(
		"ProjectMetadata", back_populates="resource_metadata_"
	)
	version_lineage: Mapped[list["VersionLineage_"]] = relationship(
		"VersionLineage_", uselist=True, back_populates="resource"
	)


class ResourceMetadata1(Base):
	__tablename__ = "resource_metadata"
	__table_args__ = (
		ForeignKeyConstraint(
			["project_id"],
			["projects.project_metadata.id"],
			ondelete="CASCADE",
			name="resource_metadata_project_id_fkey",
		),
		PrimaryKeyConstraint("id", name="resource_metadata_pkey"),
		Index("idx_silver_resource_metadata_name", "name"),
		{"schema": "silver"},
	)

	id = mapped_column(BigInteger)
	name = mapped_column(String(256), nullable=False)
	project_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	description = mapped_column(String(512))

	project: Mapped["ProjectMetadata"] = relationship(
		"ProjectMetadata", back_populates="resource_metadata1"
	)
	version_lineage: Mapped[list["VersionLineage"]] = relationship(
		"VersionLineage", uselist=True, back_populates="resource"
	)


class ResourceVersions(Base):
	__tablename__ = "resource_versions"
	__table_args__ = (
		ForeignKeyConstraint(
			["resource_id"],
			["bronze.resource_metadata.id"],
			ondelete="CASCADE",
			name="resource_versions_resource_id_fkey",
		),
		PrimaryKeyConstraint("id", name="resource_versions_pkey"),
		UniqueConstraint(
			"resource_id", "version", name="resource_versions_resource_id_version_key"
		),
		UniqueConstraint("s3_key", name="resource_versions_s3_key_key"),
		Index("idx_resource_versions_resource_id", "resource_id"),
		Index("idx_resource_versions_status", "status"),
		{"schema": "bronze"},
	)

	id = mapped_column(BigInteger)
	resource_id = mapped_column(BigInteger, nullable=False)
	version = mapped_column(BigInteger, nullable=False)
	status = mapped_column(
		ENUM("file_status", "active", "archived", "deleted", name="file_status"),
		nullable=False,
		server_default=text("'active'::bronze.file_status"),
	)
	s3_key = mapped_column(Text, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)

	resource: Mapped["ResourceMetadata"] = relationship(
		"ResourceMetadata", back_populates="resource_versions"
	)
	version_lineage: Mapped[list["VersionLineage"]] = relationship(
		"VersionLineage", uselist=True, back_populates="from_resource"
	)


class VersionLineage(Base):
	__tablename__ = "version_lineage"
	__table_args__ = (
		ForeignKeyConstraint(
			["from_resource_id"],
			["bronze.resource_versions.id"],
			ondelete="RESTRICT",
			name="version_lineage_from_resource_id_fkey",
		),
		ForeignKeyConstraint(
			["resource_id"],
			["silver.resource_metadata.id"],
			ondelete="CASCADE",
			name="version_lineage_resource_id_fkey",
		),
		PrimaryKeyConstraint("id", name="version_lineage_pkey"),
		Index("idx_silver_version_lineage_from_resource_id", "from_resource_id"),
		Index("idx_silver_version_lineage_resource_id", "resource_id"),
		{"schema": "silver"},
	)

	id = mapped_column(BigInteger)
	resource_id = mapped_column(BigInteger, nullable=False)
	delta_version = mapped_column(BigInteger, nullable=False)
	from_resource_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)

	from_resource: Mapped["ResourceVersions"] = relationship(
		"ResourceVersions", back_populates="version_lineage"
	)
	resource: Mapped["ResourceMetadata1"] = relationship(
		"ResourceMetadata1", back_populates="version_lineage"
	)
	version_lineage: Mapped[list["VersionLineage_"]] = relationship(
		"VersionLineage_", uselist=True, back_populates="from_resource"
	)


class VersionLineage_(Base):
	__tablename__ = "version_lineage"
	__table_args__ = (
		ForeignKeyConstraint(
			["from_resource_id"],
			["silver.version_lineage.id"],
			ondelete="RESTRICT",
			name="version_lineage_from_resource_id_fkey",
		),
		ForeignKeyConstraint(
			["resource_id"],
			["gold.resource_metadata.id"],
			ondelete="CASCADE",
			name="version_lineage_resource_id_fkey",
		),
		PrimaryKeyConstraint("id", name="version_lineage_pkey"),
		Index("idx_gold_version_lineage_from_resource_id", "from_resource_id"),
		Index("idx_gold_version_lineage_resource_id", "resource_id"),
		{"schema": "gold"},
	)

	id = mapped_column(BigInteger)
	resource_id = mapped_column(BigInteger, nullable=False)
	delta_version = mapped_column(BigInteger, nullable=False)
	from_resource_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)

	from_resource: Mapped["VersionLineage"] = relationship(
		"VersionLineage", back_populates="version_lineage"
	)
	resource: Mapped["ResourceMetadata_"] = relationship(
		"ResourceMetadata_", back_populates="version_lineage"
	)
