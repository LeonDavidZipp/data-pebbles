from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel
from sqlalchemy import (
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
		async with self.session_maker() as db:
			source = BronzeSourceMetadata(name=name)
			db.add(source)
			await db.commit()
			await db.refresh(source)
			return BronzeSourceMetadataRead.model_validate(source)

	async def get(self, id: int) -> BronzeSourceMetadataRead | None:
		async with self.session_maker() as db:
			source = await db.get(BronzeSourceMetadata, id)
			if source is None:
				return None
			return BronzeSourceMetadataRead.model_validate(source)

	async def update(
		self, id: int, name: str | None = None
	) -> BronzeSourceMetadataRead | None:
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
	) -> BronzeSourceVersionRead:
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
			await db.refresh(entry)
			return BronzeSourceVersionRead.model_validate(entry)

	async def activate_version(
		self, source_id: int, version: int
	) -> BronzeSourceVersionRead | None:
		"""
		Activate a specific version for a source, archiving any currently active
		version.

		Args:
			source_id: ID of the source.
			version: Version number to activate.

		Returns:
			The activated BronzeSourceVersionRead object, or None if the specified
				version does not exist.
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
				return None
			await db.commit()
			return BronzeSourceVersionRead.model_validate(entry)

	async def get(self, id: int) -> BronzeSourceVersionRead | None:
		async with self.session_maker() as db:
			entry = await db.get(BronzeSourceVersion, id)
			if entry is None:
				return None
			return BronzeSourceVersionRead.model_validate(entry)

	async def get_by_source(
		self, source_id: int, limit: int | None = None
	) -> list[BronzeSourceVersionRead]:
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

	async def update(
		self, id: int, s3_key: str | None = None
	) -> BronzeSourceVersionRead | None:
		async with self.session_maker() as db:
			entry = await db.get(BronzeSourceVersion, id)
			if entry is None:
				return None
			if s3_key is not None:
				entry.s3_key = s3_key
			await db.commit()
			await db.refresh(entry)
			return BronzeSourceVersionRead.model_validate(entry)

	async def delete(self, id: int) -> int:
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(BronzeSourceVersion).where(BronzeSourceVersion.id == id)
			)
			await db.commit()
			return result.rowcount
