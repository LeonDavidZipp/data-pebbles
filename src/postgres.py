from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import (
	CursorResult,
	DateTime,
	ForeignKey,
	String,
	delete,
	select,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
	pass


class BronzeSourceMetadata(Base):
	"""Source metadata database table model."""

	__tablename__ = "source_metadata"
	__table_args__ = {"schema": "bronze"}

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String, nullable=False)
	s3_bucket: Mapped[str] = mapped_column(String, nullable=False)
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
	s3_bucket: str
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
	s3_key: str
	created_at: datetime
	updated_at: datetime

	model_config = {"from_attributes": True}


class BronzeSourceMetadataInteractor:
	"""Async interactor for source metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(self, name: str, s3_bucket: str) -> BronzeSourceMetadataRead:
		async with self.session_maker() as db:
			source = BronzeSourceMetadata(name=name, s3_bucket=s3_bucket)
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
		self, id: int, name: str | None = None, s3_bucket: str | None = None
	) -> BronzeSourceMetadataRead | None:
		async with self.session_maker() as db:
			source = await db.get(BronzeSourceMetadata, id)
			if source is None:
				return None
			if name is not None:
				source.name = name
			if s3_bucket is not None:
				source.s3_bucket = s3_bucket
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
		self, source_id: int, version: int, s3_key: str
	) -> BronzeSourceVersionRead:
		async with self.session_maker() as db:
			entry = BronzeSourceVersion(
				source_id=source_id, version=version, s3_key=s3_key
			)
			db.add(entry)
			await db.commit()
			await db.refresh(entry)
			return BronzeSourceVersionRead.model_validate(entry)

	async def get(self, id: int) -> BronzeSourceVersionRead | None:
		async with self.session_maker() as db:
			entry = await db.get(BronzeSourceVersion, id)
			if entry is None:
				return None
			return BronzeSourceVersionRead.model_validate(entry)

	async def get_by_source(self, source_id: int) -> list[BronzeSourceVersionRead]:
		async with self.session_maker() as db:
			result = await db.execute(
				select(BronzeSourceVersion)
				.where(BronzeSourceVersion.source_id == source_id)
				.order_by(BronzeSourceVersion.version)
			)
			return [
				BronzeSourceVersionRead.model_validate(v)
				for v in result.scalars().all()
			]

	async def get_latest(self, source_id: int) -> BronzeSourceVersionRead | None:
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
