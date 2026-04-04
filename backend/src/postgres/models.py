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

	resource_metadata: Mapped[list["BronzeResourceMetadata"]] = relationship(
		"BronzeResourceMetadata", uselist=True, back_populates="project"
	)
	resource_metadata_: Mapped[list["GoldResourceMetadata"]] = relationship(
		"GoldResourceMetadata", uselist=True, back_populates="project"
	)
	resource_metadata1: Mapped[list["RawResourceMetadata"]] = relationship(
		"RawResourceMetadata", uselist=True, back_populates="project"
	)
	resource_metadata2: Mapped[list["SilverResourceMetadata"]] = relationship(
		"SilverResourceMetadata", uselist=True, back_populates="project"
	)


class BronzeResourceMetadata(Base):
	__tablename__ = "resource_metadata"
	__table_args__ = (
		ForeignKeyConstraint(
			["project_id"],
			["projects.project_metadata.id"],
			ondelete="CASCADE",
			name="resource_metadata_project_id_fkey",
		),
		PrimaryKeyConstraint("id", name="resource_metadata_pkey"),
		Index("idx_bronze_resource_metadata_name", "name"),
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
	version_lineage: Mapped[list["BronzeVersionLineage"]] = relationship(
		"BronzeVersionLineage", uselist=True, back_populates="resource"
	)


class GoldResourceMetadata(Base):
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
	version_lineage: Mapped[list["GoldVersionLineage"]] = relationship(
		"GoldVersionLineage", uselist=True, back_populates="resource"
	)


class RawResourceMetadata(Base):
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
		{"schema": "raw"},
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
	version_lineage: Mapped[list["RawVersionLineage"]] = relationship(
		"RawVersionLineage", uselist=True, back_populates="resource"
	)


class SilverResourceMetadata(Base):
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
		"ProjectMetadata", back_populates="resource_metadata2"
	)
	version_lineage: Mapped[list["SilverVersionLineage"]] = relationship(
		"SilverVersionLineage", uselist=True, back_populates="resource"
	)


class RawVersionLineage(Base):
	__tablename__ = "version_lineage"
	__table_args__ = (
		ForeignKeyConstraint(
			["resource_id"],
			["raw.resource_metadata.id"],
			ondelete="CASCADE",
			name="version_lineage_resource_id_fkey",
		),
		PrimaryKeyConstraint("id", name="version_lineage_pkey"),
		UniqueConstraint(
			"resource_id", "version", name="version_lineage_resource_id_version_key"
		),
		UniqueConstraint("s3_key", name="version_lineage_s3_key_key"),
		Index("idx_version_lineage_resource_id", "resource_id"),
		Index("idx_version_lineage_status", "status"),
		{"schema": "raw"},
	)

	id = mapped_column(BigInteger)
	resource_id = mapped_column(BigInteger, nullable=False)
	version = mapped_column(BigInteger, nullable=False)
	status = mapped_column(
		ENUM("version_status", "active", "archived", "deleted", name="version_status"),
		nullable=False,
		server_default=text("'archived'::projects.version_status"),
	)
	s3_key = mapped_column(Text, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)
	updated_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)

	resource: Mapped["RawResourceMetadata"] = relationship(
		"RawResourceMetadata", back_populates="version_lineage"
	)
	version_lineage: Mapped[list["BronzeVersionLineage"]] = relationship(
		"BronzeVersionLineage", uselist=True, back_populates="from_resource"
	)


class BronzeVersionLineage(Base):
	__tablename__ = "version_lineage"
	__table_args__ = (
		ForeignKeyConstraint(
			["from_resource_id"],
			["raw.version_lineage.id"],
			ondelete="RESTRICT",
			name="version_lineage_from_resource_id_fkey",
		),
		ForeignKeyConstraint(
			["resource_id"],
			["bronze.resource_metadata.id"],
			ondelete="CASCADE",
			name="version_lineage_resource_id_fkey",
		),
		PrimaryKeyConstraint("id", name="version_lineage_pkey"),
		Index("idx_bronze_version_lineage_from_resource_id", "from_resource_id"),
		Index("idx_bronze_version_lineage_resource_id", "resource_id"),
		{"schema": "bronze"},
	)

	id = mapped_column(BigInteger)
	resource_id = mapped_column(BigInteger, nullable=False)
	delta_version = mapped_column(BigInteger, nullable=False)
	from_resource_id = mapped_column(BigInteger, nullable=False)
	created_at = mapped_column(
		DateTime(True), nullable=False, server_default=text("now()")
	)

	from_resource: Mapped["RawVersionLineage"] = relationship(
		"RawVersionLineage", back_populates="version_lineage"
	)
	resource: Mapped["BronzeResourceMetadata"] = relationship(
		"BronzeResourceMetadata", back_populates="version_lineage"
	)
	version_lineage: Mapped[list["SilverVersionLineage"]] = relationship(
		"SilverVersionLineage", uselist=True, back_populates="from_resource"
	)


class SilverVersionLineage(Base):
	__tablename__ = "version_lineage"
	__table_args__ = (
		ForeignKeyConstraint(
			["from_resource_id"],
			["bronze.version_lineage.id"],
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

	from_resource: Mapped["BronzeVersionLineage"] = relationship(
		"BronzeVersionLineage", back_populates="version_lineage"
	)
	resource: Mapped["SilverResourceMetadata"] = relationship(
		"SilverResourceMetadata", back_populates="version_lineage"
	)
	version_lineage: Mapped[list["GoldVersionLineage"]] = relationship(
		"GoldVersionLineage", uselist=True, back_populates="from_resource"
	)


class GoldVersionLineage(Base):
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

	from_resource: Mapped["SilverVersionLineage"] = relationship(
		"SilverVersionLineage", back_populates="version_lineage"
	)
	resource: Mapped["GoldResourceMetadata"] = relationship(
		"GoldResourceMetadata", back_populates="version_lineage"
	)
