from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel
from sqlalchemy import (
	BigInteger,
	CursorResult,
	DateTime,
	Enum,
	ForeignKey,
	String,
	delete,
	func,
	select,
	update,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class VersionStatus(StrEnum):
	ACTIVE = "active"
	ARCHIVED = "archived"
	DELETED = "deleted"


class Base(DeclarativeBase):
	pass


class BronzeSourceMetadata(Base):
	"""Source metadata database table model."""

	__tablename__ = "source_metadata"
	__table_args__ = {"schema": "bronze"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)


class BronzeSourceMetadataRead(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class BronzeSourceVersion(Base):
	"""Bronze source version database table model."""

	__tablename__ = "source_versions"
	__table_args__ = {"schema": "bronze"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	source_id: Mapped[int] = mapped_column(
		ForeignKey("bronze.source_metadata.id", ondelete="CASCADE"),
		index=True,
	)
	version: Mapped[int] = mapped_column(nullable=False)
	status: Mapped[VersionStatus] = mapped_column(
		Enum(VersionStatus, name="file_status", create_type=False, schema="public"),
		nullable=False,
		default=VersionStatus.ACTIVE,
	)
	s3_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)


class BronzeSourceVersionRead(BaseModel):
	id: int
	source_id: int
	version: int
	status: VersionStatus
	s3_key: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class BronzeSourceMetadataInteractor:
	"""Async interactor for source metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(self, name: str) -> BronzeSourceMetadataRead:
		"""Create a new bronze source metadata entry.

		Args:
			name (str): Name of the source.

		Returns:
			BronzeSourceMetadataRead: The created source metadata.
		"""
		async with self.session_maker() as db:
			source = BronzeSourceMetadata(name=name)
			db.add(source)
			await db.commit()
			await db.refresh(source)
			return BronzeSourceMetadataRead.model_validate(source)

	async def get(self, id: int) -> BronzeSourceMetadataRead | None:
		"""Get a bronze source metadata entry by ID.

		Args:
			id (int): ID of the source.

		Returns:
			BronzeSourceMetadataRead | None: The source metadata if found, else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(BronzeSourceMetadata, id)
			if source is None:
				return None
			return BronzeSourceMetadataRead.model_validate(source)

	async def update(
		self, id: int, name: str | None = None
	) -> BronzeSourceMetadataRead | None:
		"""Update a bronze source metadata entry.

		Args:
			id (int): ID of the source.
			name (str | None): New name for the source.

		Returns:
			BronzeSourceMetadataRead | None: The updated source metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(BronzeSourceMetadata, id)
			if source is None:
				return None
			if name is not None:
				source.name = name
			await db.commit()
			await db.refresh(source)
			return BronzeSourceMetadataRead.model_validate(source)

	async def delete(self, id: int) -> int:
		"""Delete a bronze source metadata entry.

		Args:
			id (int): ID of the source.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeSourceMetadata).where(BronzeSourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class BronzeSourceVersionInteractor:
	"""Async interactor for bronze source version operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self, source_id: int, s3_key: str, set_as_active: bool = False
	) -> int:
		"""
		Create a new bronze source version entry.

		Args:
			source_id (int): ID of the source.
			s3_key (str): S3 key where the file is stored.
			set_as_active (bool): Whether to set the new version as active.

		Returns:
			int: The number of rows affected by the create operation.
		"""
		async with self.session_maker() as db:
			status = VersionStatus.ACTIVE if set_as_active else VersionStatus.ARCHIVED
			next_version = (
				select(func.coalesce(func.max(BronzeSourceVersion.version), 0) + 1)
				.where(BronzeSourceVersion.source_id == source_id)
				.scalar_subquery()
			)
			entry = BronzeSourceVersion(
				source_id=source_id,
				version=next_version,
				s3_key=s3_key,
				status=status,
			)
			db.add(entry)
			await db.commit()
			return 1

	async def activate_version(self, source_id: int, version: int) -> int:
		"""
		Activate a specific version for a source, archiving any currently active
		version.

		Args:
			source_id (int): ID of the source.
			version (int): Version number to activate.

		Returns:
			int: The number of rows affected by the activation operation.
		"""
		async with self.session_maker() as db:
			await db.execute(
				update(BronzeSourceVersion)
				.where(
					BronzeSourceVersion.source_id == source_id,
					BronzeSourceVersion.status == VersionStatus.ACTIVE,
				)
				.values(status=VersionStatus.ARCHIVED)
			)
			result = await db.execute(
				update(BronzeSourceVersion)
				.where(
					BronzeSourceVersion.source_id == source_id,
					BronzeSourceVersion.version == version,
				)
				.values(status=VersionStatus.ACTIVE)
				.returning(BronzeSourceVersion)
			)
			entry = result.scalars().first()
			if entry is None:
				return 0
			await db.commit()
			return 1

	async def get(self, id: int) -> BronzeSourceVersionRead | None:
		"""
		Get a bronze source version by ID.

		Args:
			id (int): ID of the bronze source version.

		Returns:
			BronzeSourceVersionRead | None: BronzeSourceVersionRead object if found,
			else None.
		"""
		async with self.session_maker() as db:
			entry = await db.get(BronzeSourceVersion, id)
			if entry is None:
				return None
			return BronzeSourceVersionRead.model_validate(entry)

	async def get_by_source(
		self, source_id: int, limit: int | None = None
	) -> list[BronzeSourceVersionRead]:
		"""Get all versions for a bronze source.

		Args:
			source_id (int): ID of the source.
			limit (int | None): Maximum number of versions to return. If None,
				returns all.

		Returns:
			list[BronzeSourceVersionRead]: List of version entries.
		"""
		async with self.session_maker() as db:
			if limit is None:
				result = await db.execute(
					select(BronzeSourceVersion)
					.where(BronzeSourceVersion.source_id == source_id)
					.order_by(BronzeSourceVersion.version)
				)
			else:
				result = await db.execute(
					select(BronzeSourceVersion)
					.where(BronzeSourceVersion.source_id == source_id)
					.order_by(BronzeSourceVersion.version.desc())
					.limit(limit)
				)
			return [
				BronzeSourceVersionRead.model_validate(v)
				for v in result.scalars().all()
			]

	async def get_version_by_source(
		self, source_id: int, version: int | None = None
	) -> BronzeSourceVersionRead | None:
		"""
		Get a specific version of a bronze source, or the latest version if no version
		is specified.

		Args:
			source_id (int): ID of the source.
			version (int | None): Version number to retrieve. If None, retrieves the
				latest version.

		Returns:
			BronzeSourceVersionRead | None: BronzeSourceVersionRead object if found,
				else None.
		"""
		if version is None:
			return await self.get_latest_by_source(source_id)

		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeSourceVersion).where(
					BronzeSourceVersion.source_id == source_id,
					BronzeSourceVersion.version == version,
				)
			)
			entry = result.scalars().first()
			if entry is None:
				return None
			return BronzeSourceVersionRead.model_validate(entry)

	async def get_latest_by_source(
		self, source_id: int
	) -> BronzeSourceVersionRead | None:
		"""
		Get the latest version of a bronze source.

		Args:
			source_id (int): ID of the source.

		Returns:
			BronzeSourceVersionRead | None: BronzeSourceVersionRead object for the
				latest version if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeSourceVersion)
				.where(BronzeSourceVersion.source_id == source_id)
				.order_by(BronzeSourceVersion.version.desc())
				.limit(1)
			)
			entry = result.scalars().first()
			if entry is None:
				return None
			return BronzeSourceVersionRead.model_validate(entry)

	async def update(self, id: int, s3_key: str | None = None) -> int:
		"""
		Update a bronze source version entry.

		Args:
			id (int): ID of the bronze source version.
			s3_key (str | None): New S3 key for the bronze source version.

		Returns:
			int: The number of rows affected by the update operation.
		"""
		async with self.session_maker() as db:
			entry = await db.get(BronzeSourceVersion, id)
			if entry is None:
				return 0
			if s3_key is not None:
				entry.s3_key = s3_key
			await db.commit()
			return 1

	async def delete(self, id: int) -> int:
		"""Delete a bronze source version by ID.

		Args:
			id (int): ID of the bronze source version.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeSourceVersion).where(BronzeSourceVersion.id == id)
			)
			await db.commit()
			return result.rowcount

	async def delete_version_by_source(self, source_id: int, version: int) -> int:
		"""Delete a specific version of a bronze source.

		Args:
			source_id (int): ID of the source.
			version (int): Version number to delete.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeSourceVersion).where(
					BronzeSourceVersion.source_id == source_id,
					BronzeSourceVersion.version == version,
				)
			)
			await db.commit()
			return result.rowcount


class SilverSourceMetadata(Base):
	"""Silver source metadata database table model."""

	__tablename__ = "source_metadata"
	__table_args__ = {"schema": "silver"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)


class SilverSourceMetadataRead(BaseModel):
	id: int
	name: str
	from_source_id: int
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class SilverVersionLineage(Base):
	"""Silver version lineage database table model."""

	__tablename__ = "version_lineage"
	__table_args__ = {"schema": "silver"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	source_id: Mapped[int] = mapped_column(
		ForeignKey("silver.source_metadata.id", ondelete="CASCADE"),
		index=True,
		nullable=False,
	)
	delta_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
	from_source_id: Mapped[int] = mapped_column(
		ForeignKey("bronze.source_versions.id", ondelete="RESTRICT"),
		index=True,
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)


class SilverVersionLineageRead(BaseModel):
	id: int
	source_id: int
	delta_version: int
	from_source_id: int
	created_at: datetime

	model_config = {"from_attributes": True}


class SilverSourceMetadataInteractor:
	"""Async interactor for silver source metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(self, name: str, from_source_id: int) -> SilverSourceMetadataRead:
		"""Create a new silver source metadata entry.

		Args:
			name (str): Name of the source.
			from_source_id (int): ID of the bronze source this derives from.

		Returns:
			SilverSourceMetadataRead: The created source metadata.
		"""
		async with self.session_maker() as db:
			source = SilverSourceMetadata(name=name, from_source_id=from_source_id)
			db.add(source)
			await db.commit()
			await db.refresh(source)
			return SilverSourceMetadataRead.model_validate(source)

	async def get(self, id: int) -> SilverSourceMetadataRead | None:
		"""Get a silver source metadata entry by ID.

		Args:
			id (int): ID of the source.

		Returns:
			SilverSourceMetadataRead | None: The source metadata if found, else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(SilverSourceMetadata, id)
			if source is None:
				return None
			return SilverSourceMetadataRead.model_validate(source)

	async def update(
		self, id: int, name: str | None = None
	) -> SilverSourceMetadataRead | None:
		"""Update a silver source metadata entry.

		Args:
			id (int): ID of the source.
			name (str | None): New name for the source.

		Returns:
			SilverSourceMetadataRead | None: The updated source metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(SilverSourceMetadata, id)
			if source is None:
				return None
			if name is not None:
				source.name = name
			await db.commit()
			await db.refresh(source)
			return SilverSourceMetadataRead.model_validate(source)

	async def delete(self, id: int) -> int:
		"""Delete a silver source metadata entry.

		Args:
			id (int): ID of the source.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(SilverSourceMetadata).where(SilverSourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class SilverVersionLineageInteractor:
	"""Async interactor for silver version lineage operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self, source_id: int, delta_version: int, from_source_id: int
	) -> SilverVersionLineageRead:
		"""Create a new silver version lineage entry.

		Args:
			source_id (int): Silver source metadata ID.
			delta_version (int): Silver Delta Lake version.
			from_source_id (int): Bronze source version ID this derives from.

		Returns:
			SilverVersionLineageRead: The created lineage entry.
		"""
		async with self.session_maker() as db:
			entry = SilverVersionLineage(
				source_id=source_id,
				delta_version=delta_version,
				from_source_id=from_source_id,
			)
			db.add(entry)
			await db.commit()
			await db.refresh(entry)
			return SilverVersionLineageRead.model_validate(entry)

	async def get(self, id: int) -> SilverVersionLineageRead | None:
		"""Get a silver version lineage entry by ID.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			SilverVersionLineageRead | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			entry = await db.get(SilverVersionLineage, id)
			if entry is None:
				return None
			return SilverVersionLineageRead.model_validate(entry)

	async def get_by_source(self, source_id: int) -> list[SilverVersionLineageRead]:
		"""Get all lineage entries for a silver source.

		Args:
			source_id (int): Silver source metadata ID.

		Returns:
			list[SilverVersionLineageRead]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage)
				.where(SilverVersionLineage.source_id == source_id)
				.order_by(SilverVersionLineage.delta_version)
			)
			return [
				SilverVersionLineageRead.model_validate(v)
				for v in result.scalars().all()
			]

	async def get_by_delta_version(
		self, source_id: int, delta_version: int
	) -> SilverVersionLineageRead | None:
		"""Get the lineage entry for a specific silver delta version.

		Args:
			source_id (int): Silver source metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			SilverVersionLineageRead | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage).where(
					SilverVersionLineage.source_id == source_id,
					SilverVersionLineage.delta_version == delta_version,
				)
			)
			entry = result.scalars().first()
			if entry is None:
				return None
			return SilverVersionLineageRead.model_validate(entry)

	async def delete(self, id: int) -> int:
		"""Delete a silver version lineage entry.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(SilverVersionLineage).where(SilverVersionLineage.id == id)
			)
			await db.commit()
			return result.rowcount


class GoldSourceMetadata(Base):
	"""Gold source metadata database table model."""

	__tablename__ = "source_metadata"
	__table_args__ = {"schema": "gold"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
		onupdate=datetime.now(timezone.utc),
	)


class GoldSourceMetadataRead(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class GoldVersionLineage(Base):
	"""Gold version lineage database table model."""

	__tablename__ = "version_lineage"
	__table_args__ = {"schema": "gold"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	source_id: Mapped[int] = mapped_column(
		ForeignKey("gold.source_metadata.id", ondelete="CASCADE"),
		index=True,
		nullable=False,
	)
	delta_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
	from_source_id: Mapped[int] = mapped_column(
		ForeignKey("silver.source_metadata.id", ondelete="RESTRICT"),
		index=True,
		nullable=False,
	)
	from_delta_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)


class GoldVersionLineageRead(BaseModel):
	id: int
	source_id: int
	delta_version: int
	from_source_id: int
	from_delta_version: int
	created_at: datetime

	model_config = {"from_attributes": True}


class GoldSourceMetadataInteractor:
	"""Async interactor for gold source metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(self, name: str) -> GoldSourceMetadataRead:
		"""Create a new gold source metadata entry.

		Args:
			name (str): Name of the source.

		Returns:
			GoldSourceMetadataRead: The created source metadata.
		"""
		async with self.session_maker() as db:
			source = GoldSourceMetadata(name=name)
			db.add(source)
			await db.commit()
			await db.refresh(source)
			return GoldSourceMetadataRead.model_validate(source)

	async def get(self, id: int) -> GoldSourceMetadataRead | None:
		"""Get a gold source metadata entry by ID.

		Args:
			id (int): ID of the source.

		Returns:
			GoldSourceMetadataRead | None: The source metadata if found, else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(GoldSourceMetadata, id)
			if source is None:
				return None
			return GoldSourceMetadataRead.model_validate(source)

	async def update(
		self, id: int, name: str | None = None
	) -> GoldSourceMetadataRead | None:
		"""Update a gold source metadata entry.

		Args:
			id (int): ID of the source.
			name (str | None): New name for the source.

		Returns:
			GoldSourceMetadataRead | None: The updated source metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			source = await db.get(GoldSourceMetadata, id)
			if source is None:
				return None
			if name is not None:
				source.name = name
			await db.commit()
			await db.refresh(source)
			return GoldSourceMetadataRead.model_validate(source)

	async def delete(self, id: int) -> int:
		"""Delete a gold source metadata entry.

		Args:
			id (int): ID of the source.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(GoldSourceMetadata).where(GoldSourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class GoldVersionLineageInteractor:
	"""Async interactor for gold version lineage operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self,
		source_id: int,
		delta_version: int,
		from_source_id: int,
		from_delta_version: int,
	) -> GoldVersionLineageRead:
		"""Create a new gold version lineage entry.

		Args:
			source_id (int): Gold source metadata ID.
			delta_version (int): Gold Delta Lake version.
			from_source_id (int): Silver source metadata ID this derives from.
			from_delta_version (int): Silver Delta Lake version used.

		Returns:
			GoldVersionLineageRead: The created lineage entry.
		"""
		async with self.session_maker() as db:
			entry = GoldVersionLineage(
				source_id=source_id,
				delta_version=delta_version,
				from_source_id=from_source_id,
				from_delta_version=from_delta_version,
			)
			db.add(entry)
			await db.commit()
			await db.refresh(entry)
			return GoldVersionLineageRead.model_validate(entry)

	async def create_many(
		self,
		source_id: int,
		delta_version: int,
		sources: list[tuple[int, int]],
	) -> list[GoldVersionLineageRead]:
		"""Create multiple lineage entries for a single gold delta version.

		Args:
			source_id (int): Gold source metadata ID.
			delta_version (int): Gold Delta Lake version.
			sources (list[tuple[int, int]]): List of
				(silver_source_id, silver_delta_version) tuples.

		Returns:
			list[GoldVersionLineageRead]: The created lineage entries.
		"""
		async with self.session_maker() as db:
			entries = [
				GoldVersionLineage(
					source_id=source_id,
					delta_version=delta_version,
					from_source_id=from_id,
					from_delta_version=from_dv,
				)
				for from_id, from_dv in sources
			]
			db.add_all(entries)
			await db.commit()
			for entry in entries:
				await db.refresh(entry)
			return [GoldVersionLineageRead.model_validate(e) for e in entries]

	async def get(self, id: int) -> GoldVersionLineageRead | None:
		"""Get a gold version lineage entry by ID.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			GoldVersionLineageRead | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			entry = await db.get(GoldVersionLineage, id)
			if entry is None:
				return None
			return GoldVersionLineageRead.model_validate(entry)

	async def get_by_source(self, source_id: int) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a gold source.

		Args:
			source_id (int): Gold source metadata ID.

		Returns:
			list[GoldVersionLineageRead]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage)
				.where(GoldVersionLineage.source_id == source_id)
				.order_by(GoldVersionLineage.delta_version)
			)
			return [
				GoldVersionLineageRead.model_validate(v) for v in result.scalars().all()
			]

	async def get_by_delta_version(
		self, source_id: int, delta_version: int
	) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a specific gold delta version.

		Args:
			source_id (int): Gold source metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			list[GoldVersionLineageRead]: List of lineage entries. Multiple entries
				possible since a gold version can derive from multiple silver sources.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage).where(
					GoldVersionLineage.source_id == source_id,
					GoldVersionLineage.delta_version == delta_version,
				)
			)
			return [
				GoldVersionLineageRead.model_validate(v) for v in result.scalars().all()
			]

	async def delete(self, id: int) -> int:
		"""Delete a gold version lineage entry.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(GoldVersionLineage).where(GoldVersionLineage.id == id)
			)
			await db.commit()
			return result.rowcount
