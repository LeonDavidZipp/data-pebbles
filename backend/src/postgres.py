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


class BronzeResourceMetadata(Base):
	"""Resource metadata database table model."""

	__tablename__ = "resource_metadata"
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


class BronzeResourceMetadataRead(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class BronzeResourceVersion(Base):
	"""Bronze resource version database table model."""

	__tablename__ = "resource_versions"
	__table_args__ = {"schema": "bronze"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	resource_id: Mapped[int] = mapped_column(
		ForeignKey("bronze.resource_metadata.id", ondelete="CASCADE"),
		index=True,
	)
	version: Mapped[int] = mapped_column(nullable=False)
	status: Mapped[VersionStatus] = mapped_column(
		Enum(
			VersionStatus,
			name="file_status",
			create_type=False,
			schema="bronze",
			values_callable=lambda e: [member.value for member in e],
		),
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


class BronzeResourceVersionRead(BaseModel):
	id: int
	resource_id: int
	version: int
	status: VersionStatus
	s3_key: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class BronzeResourceMetadataInteractor:
	"""Async interactor for resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[BronzeResourceMetadataRead]:
		"""Get all bronze resource metadata entries.

		Returns:
			list[BronzeResourceMetadataRead]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeResourceMetadata).order_by(BronzeResourceMetadata.name)
			)
			return [
				BronzeResourceMetadataRead.model_validate(s)
				for s in result.scalars().all()
			]

	async def create(self, name: str) -> BronzeResourceMetadataRead:
		"""Create a new bronze resource metadata entry.

		Args:
			name (str): Name of the resource.

		Returns:
			BronzeResourceMetadataRead: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = BronzeResourceMetadata(name=name)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return BronzeResourceMetadataRead.model_validate(resource)

	async def get(self, id: int) -> BronzeResourceMetadataRead | None:
		"""Get a bronze resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			BronzeResourceMetadataRead | None: The resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(BronzeResourceMetadata, id)
			if resource is None:
				return None
			return BronzeResourceMetadataRead.model_validate(resource)

	async def update(
		self, id: int, name: str | None = None
	) -> BronzeResourceMetadataRead | None:
		"""Update a bronze resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.

		Returns:
			BronzeResourceMetadataRead | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(BronzeResourceMetadata, id)
			if resource is None:
				return None
			if name is not None:
				resource.name = name
			await db.commit()
			await db.refresh(resource)
			return BronzeResourceMetadataRead.model_validate(resource)

	async def delete(self, id: int) -> int:
		"""Delete a bronze resource metadata entry.

		Args:
			id (int): ID of the resource.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeResourceMetadata).where(BronzeResourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class BronzeResourceVersionInteractor:
	"""Async interactor for bronze resource version operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self, resource_id: int, s3_key: str, set_as_active: bool = False
	) -> int:
		"""
		Create a new bronze resource version entry.

		Args:
			resource_id (int): ID of the resource.
			s3_key (str): S3 key where the file is stored.
			set_as_active (bool): Whether to set the new version as active.

		Returns:
			int: The number of rows affected by the create operation.
		"""
		async with self.session_maker() as db:
			status = VersionStatus.ACTIVE if set_as_active else VersionStatus.ARCHIVED
			next_version = (
				select(func.coalesce(func.max(BronzeResourceVersion.version), 0) + 1)
				.where(BronzeResourceVersion.resource_id == resource_id)
				.scalar_subquery()
			)
			entry = BronzeResourceVersion(
				resource_id=resource_id,
				version=next_version,
				s3_key=s3_key,
				status=status,
			)
			db.add(entry)
			await db.commit()
			return 1

	async def activate_version(self, resource_id: int, version: int) -> int:
		"""
		Activate a specific version for a resource, archiving any currently active
		version.

		Args:
			resource_id (int): ID of the resource.
			version (int): Version number to activate.

		Returns:
			int: The number of rows affected by the activation operation.
		"""
		async with self.session_maker() as db:
			await db.execute(
				update(BronzeResourceVersion)
				.where(
					BronzeResourceVersion.resource_id == resource_id,
					BronzeResourceVersion.status == VersionStatus.ACTIVE,
				)
				.values(status=VersionStatus.ARCHIVED)
			)
			result = await db.execute(
				update(BronzeResourceVersion)
				.where(
					BronzeResourceVersion.resource_id == resource_id,
					BronzeResourceVersion.version == version,
				)
				.values(status=VersionStatus.ACTIVE)
				.returning(BronzeResourceVersion)
			)
			entry = result.scalars().first()
			if entry is None:
				return 0
			await db.commit()
			return 1

	async def get(self, id: int) -> BronzeResourceVersionRead | None:
		"""
		Get a bronze resource version by ID.

		Args:
			id (int): ID of the bronze resource version.

		Returns:
			BronzeResourceVersionRead | None: BronzeResourceVersionRead object if found,
			else None.
		"""
		async with self.session_maker() as db:
			entry = await db.get(BronzeResourceVersion, id)
			if entry is None:
				return None
			return BronzeResourceVersionRead.model_validate(entry)

	async def get_by_resource(
		self, resource_id: int, limit: int | None = None
	) -> list[BronzeResourceVersionRead]:
		"""Get all versions for a bronze resource.

		Args:
			resource_id (int): ID of the resource.
			limit (int | None): Maximum number of versions to return. If None,
				returns all.

		Returns:
			list[BronzeResourceVersionRead]: List of version entries.
		"""
		async with self.session_maker() as db:
			if limit is None:
				result = await db.execute(
					select(BronzeResourceVersion)
					.where(BronzeResourceVersion.resource_id == resource_id)
					.order_by(BronzeResourceVersion.version)
				)
			else:
				result = await db.execute(
					select(BronzeResourceVersion)
					.where(BronzeResourceVersion.resource_id == resource_id)
					.order_by(BronzeResourceVersion.version.desc())
					.limit(limit)
				)
			return [
				BronzeResourceVersionRead.model_validate(v)
				for v in result.scalars().all()
			]

	async def get_version_by_resource(
		self, resource_id: int, version: int | None = None
	) -> BronzeResourceVersionRead | None:
		"""
		Get a specific version of a bronze resource, or the latest version if no version
		is specified.

		Args:
			resource_id (int): ID of the resource.
			version (int | None): Version number to retrieve. If None, retrieves the
				latest version.

		Returns:
			BronzeResourceVersionRead | None: BronzeResourceVersionRead object if found,
				else None.
		"""
		if version is None:
			return await self.get_latest_by_resource(resource_id)

		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeResourceVersion).where(
					BronzeResourceVersion.resource_id == resource_id,
					BronzeResourceVersion.version == version,
				)
			)
			entry = result.scalars().first()
			if entry is None:
				return None
			return BronzeResourceVersionRead.model_validate(entry)

	async def get_latest_by_resource(
		self, resource_id: int
	) -> BronzeResourceVersionRead | None:
		"""
		Get the latest version of a bronze resource.

		Args:
			resource_id (int): ID of the resource.

		Returns:
			BronzeResourceVersionRead | None: BronzeResourceVersionRead object for the
				latest version if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeResourceVersion)
				.where(BronzeResourceVersion.resource_id == resource_id)
				.order_by(BronzeResourceVersion.version.desc())
				.limit(1)
			)
			entry = result.scalars().first()
			if entry is None:
				return None
			return BronzeResourceVersionRead.model_validate(entry)

	async def update(self, id: int, s3_key: str | None = None) -> int:
		"""
		Update a bronze resource version entry.

		Args:
			id (int): ID of the bronze resource version.
			s3_key (str | None): New S3 key for the bronze resource version.

		Returns:
			int: The number of rows affected by the update operation.
		"""
		async with self.session_maker() as db:
			entry = await db.get(BronzeResourceVersion, id)
			if entry is None:
				return 0
			if s3_key is not None:
				entry.s3_key = s3_key
			await db.commit()
			return 1

	async def delete(self, id: int) -> int:
		"""Delete a bronze resource version by ID.

		Args:
			id (int): ID of the bronze resource version.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeResourceVersion).where(BronzeResourceVersion.id == id)
			)
			await db.commit()
			return result.rowcount

	async def delete_version_by_resource(self, resource_id: int, version: int) -> int:
		"""Delete a specific version of a bronze resource.

		Args:
			resource_id (int): ID of the resource.
			version (int): Version number to delete.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeResourceVersion).where(
					BronzeResourceVersion.resource_id == resource_id,
					BronzeResourceVersion.version == version,
				)
			)
			await db.commit()
			return result.rowcount


class SilverResourceMetadata(Base):
	"""Silver resource metadata database table model."""

	__tablename__ = "resource_metadata"
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


class SilverResourceMetadataRead(BaseModel):
	id: int
	name: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class SilverVersionLineage(Base):
	"""Silver version lineage database table model."""

	__tablename__ = "version_lineage"
	__table_args__ = {"schema": "silver"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	resource_id: Mapped[int] = mapped_column(
		ForeignKey("silver.resource_metadata.id", ondelete="CASCADE"),
		index=True,
		nullable=False,
	)
	delta_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
	from_resource_id: Mapped[int] = mapped_column(
		ForeignKey("bronze.resource_versions.id", ondelete="RESTRICT"),
		index=True,
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)


class SilverVersionLineageRead(BaseModel):
	id: int
	resource_id: int
	delta_version: int
	from_resource_id: int
	created_at: datetime

	model_config = {"from_attributes": True}


class SilverResourceMetadataInteractor:
	"""Async interactor for silver resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[SilverResourceMetadataRead]:
		"""Get all silver resource metadata entries.

		Returns:
			list[SilverResourceMetadataRead]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverResourceMetadata).order_by(SilverResourceMetadata.name)
			)
			return [
				SilverResourceMetadataRead.model_validate(s)
				for s in result.scalars().all()
			]

	async def create(self, name: str) -> SilverResourceMetadataRead:
		"""Create a new silver resource metadata entry.

		Args:
			name (str): Name of the resource.

		Returns:
			SilverResourceMetadataRead: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = SilverResourceMetadata(name=name)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return SilverResourceMetadataRead.model_validate(resource)

	async def get(self, id: int) -> SilverResourceMetadataRead | None:
		"""Get a silver resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			SilverResourceMetadataRead | None: The resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(SilverResourceMetadata, id)
			if resource is None:
				return None
			return SilverResourceMetadataRead.model_validate(resource)

	async def update(
		self, id: int, name: str | None = None
	) -> SilverResourceMetadataRead | None:
		"""Update a silver resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.

		Returns:
			SilverResourceMetadataRead | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(SilverResourceMetadata, id)
			if resource is None:
				return None
			if name is not None:
				resource.name = name
			await db.commit()
			await db.refresh(resource)
			return SilverResourceMetadataRead.model_validate(resource)

	async def delete(self, id: int) -> int:
		"""Delete a silver resource metadata entry.

		Args:
			id (int): ID of the resource.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(SilverResourceMetadata).where(SilverResourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class SilverVersionLineageInteractor:
	"""Async interactor for silver version lineage operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self, resource_id: int, delta_version: int, from_resource_id: int
	) -> SilverVersionLineageRead:
		"""Create a new silver version lineage entry.

		Args:
			resource_id (int): Silver resource metadata ID.
			delta_version (int): Silver Delta Lake version.
			from_resource_id (int): Bronze resource version ID this derives from.

		Returns:
			SilverVersionLineageRead: The created lineage entry.
		"""
		async with self.session_maker() as db:
			entry = SilverVersionLineage(
				resource_id=resource_id,
				delta_version=delta_version,
				from_resource_id=from_resource_id,
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

	async def get_by_resource(self, resource_id: int) -> list[SilverVersionLineageRead]:
		"""Get all lineage entries for a silver resource.

		Args:
			resource_id (int): Silver resource metadata ID.

		Returns:
			list[SilverVersionLineageRead]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage)
				.where(SilverVersionLineage.resource_id == resource_id)
				.order_by(SilverVersionLineage.delta_version)
			)
			return [
				SilverVersionLineageRead.model_validate(v)
				for v in result.scalars().all()
			]

	async def get_by_delta_version(
		self, resource_id: int, delta_version: int
	) -> SilverVersionLineageRead | None:
		"""Get the lineage entry for a specific silver delta version.

		Args:
			resource_id (int): Silver resource metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			SilverVersionLineageRead | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage).where(
					SilverVersionLineage.resource_id == resource_id,
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


class GoldResourceMetadata(Base):
	"""Gold resource metadata database table model."""

	__tablename__ = "resource_metadata"
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


class GoldResourceMetadataRead(BaseModel):
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
	resource_id: Mapped[int] = mapped_column(
		ForeignKey("gold.resource_metadata.id", ondelete="CASCADE"),
		index=True,
		nullable=False,
	)
	delta_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
	from_resource_id: Mapped[int] = mapped_column(
		ForeignKey("silver.version_lineage.id", ondelete="RESTRICT"),
		index=True,
		nullable=False,
	)
	created_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True),
		insert_default=lambda: datetime.now(timezone.utc),
	)


class GoldVersionLineageRead(BaseModel):
	id: int
	resource_id: int
	delta_version: int
	from_resource_id: int
	created_at: datetime

	model_config = {"from_attributes": True}


class GoldResourceMetadataInteractor:
	"""Async interactor for gold resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[GoldResourceMetadataRead]:
		"""Get all gold resource metadata entries.

		Returns:
			list[GoldResourceMetadataRead]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldResourceMetadata).order_by(GoldResourceMetadata.name)
			)
			return [
				GoldResourceMetadataRead.model_validate(s)
				for s in result.scalars().all()
			]

	async def create(self, name: str) -> GoldResourceMetadataRead:
		"""Create a new gold resource metadata entry.

		Args:
			name (str): Name of the resource.

		Returns:
			GoldResourceMetadataRead: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = GoldResourceMetadata(name=name)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return GoldResourceMetadataRead.model_validate(resource)

	async def get(self, id: int) -> GoldResourceMetadataRead | None:
		"""Get a gold resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			GoldResourceMetadataRead | None: The resource metadata if found, else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(GoldResourceMetadata, id)
			if resource is None:
				return None
			return GoldResourceMetadataRead.model_validate(resource)

	async def update(
		self, id: int, name: str | None = None
	) -> GoldResourceMetadataRead | None:
		"""Update a gold resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.

		Returns:
			GoldResourceMetadataRead | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(GoldResourceMetadata, id)
			if resource is None:
				return None
			if name is not None:
				resource.name = name
			await db.commit()
			await db.refresh(resource)
			return GoldResourceMetadataRead.model_validate(resource)

	async def delete(self, id: int) -> int:
		"""Delete a gold resource metadata entry.

		Args:
			id (int): ID of the resource.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(GoldResourceMetadata).where(GoldResourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class GoldVersionLineageInteractor:
	"""Async interactor for gold version lineage operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self,
		resource_id: int,
		delta_version: int,
		from_resource_id: int,
	) -> GoldVersionLineageRead:
		"""Create a new gold version lineage entry.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Gold Delta Lake version.
			from_resource_id (int): Silver version lineage row ID this derives from.

		Returns:
			GoldVersionLineageRead: The created lineage entry.
		"""
		async with self.session_maker() as db:
			entry = GoldVersionLineage(
				resource_id=resource_id,
				delta_version=delta_version,
				from_resource_id=from_resource_id,
			)
			db.add(entry)
			await db.commit()
			await db.refresh(entry)
			return GoldVersionLineageRead.model_validate(entry)

	async def create_many(
		self,
		resource_id: int,
		delta_version: int,
		resources: list[int],
	) -> list[GoldVersionLineageRead]:
		"""Create multiple lineage entries for a single gold delta version.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Gold Delta Lake version.
			resources (list[int]): List of silver version lineage row IDs.

		Returns:
			list[GoldVersionLineageRead]: The created lineage entries.
		"""
		async with self.session_maker() as db:
			entries = [
				GoldVersionLineage(
					resource_id=resource_id,
					delta_version=delta_version,
					from_resource_id=from_id,
				)
				for from_id in resources
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

	async def get_by_resource(self, resource_id: int) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a gold resource.

		Args:
			resource_id (int): Gold resource metadata ID.

		Returns:
			list[GoldVersionLineageRead]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage)
				.where(GoldVersionLineage.resource_id == resource_id)
				.order_by(GoldVersionLineage.delta_version)
			)
			return [
				GoldVersionLineageRead.model_validate(v) for v in result.scalars().all()
			]

	async def get_by_delta_version(
		self, resource_id: int, delta_version: int
	) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a specific gold delta version.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			list[GoldVersionLineageRead]: List of lineage entries. Multiple entries
				possible since a gold version can derive from multiple silver resources.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage).where(
					GoldVersionLineage.resource_id == resource_id,
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
