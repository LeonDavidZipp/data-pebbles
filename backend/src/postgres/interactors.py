from enum import StrEnum
from typing import Any, Generic, TypeVar

from sqlalchemy import (
	CursorResult,
	delete,
	func,
	select,
	update,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import (
	BronzeResourceMetadata,
	BronzeVersionLineage,
	GoldResourceMetadata,
	GoldVersionLineage,
	ProjectMetadata,
	RawResourceMetadata,
	RawVersionLineage,
	SilverResourceMetadata,
	SilverVersionLineage,
)


class VersionStatus(StrEnum):
	ACTIVE = "active"
	ARCHIVED = "archived"
	DELETED = "deleted"


T = TypeVar("T")


class BaseResourceMetadataInteractor(Generic[T]):
	model: type[Any]

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[T]:
		async with self.session_maker() as db:
			result = await db.execute(select(self.model).order_by(self.model.name))
			return list(result.scalars().all())

	async def create(
		self, name: str, project_id: int, description: str | None = None
	) -> T:
		async with self.session_maker() as db:
			resource = self.model(
				name=name, project_id=project_id, description=description
			)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return resource

	async def get(self, id: int) -> T | None:
		async with self.session_maker() as db:
			return await db.get(self.model, id)

	async def update(
		self,
		id: int,
		name: str | None = None,
		description: str | None = None,
	) -> T | None:
		async with self.session_maker() as db:
			resource = await db.get(self.model, id)
			if resource is None:
				return None
			if name is not None:
				resource.name = name
			if description is not None:
				resource.description = description
			await db.commit()
			await db.refresh(resource)
			return resource

	async def delete(self, id: int) -> int:
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(self.model).where(self.model.id == id)
			)
			await db.commit()
			return result.rowcount


class BaseVersionLineageInteractor(Generic[T]):
	model: type[Any]

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def create(
		self, resource_id: int, delta_version: int, from_resource_id: int
	) -> T:
		async with self.session_maker() as db:
			entry = self.model(
				resource_id=resource_id,
				delta_version=delta_version,
				from_resource_id=from_resource_id,
			)
			db.add(entry)
			await db.commit()
			await db.refresh(entry)
			return entry

	async def get(self, id: int) -> T | None:
		async with self.session_maker() as db:
			return await db.get(self.model, id)

	async def get_by_resource(self, resource_id: int) -> list[T]:
		async with self.session_maker() as db:
			result = await db.execute(
				select(self.model)
				.where(self.model.resource_id == resource_id)
				.order_by(self.model.delta_version)
			)
			return list(result.scalars().all())

	async def get_by_delta_version(
		self, resource_id: int, delta_version: int
	) -> T | None:
		async with self.session_maker() as db:
			result = await db.execute(
				select(self.model).where(
					self.model.resource_id == resource_id,
					self.model.delta_version == delta_version,
				)
			)
			return result.scalars().first()

	async def delete(self, id: int) -> int:
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(self.model).where(self.model.id == id)
			)
			await db.commit()
			return result.rowcount


class ProjectMetadataInteractor:
	"""Async interactor for project metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[ProjectMetadata]:
		"""Get all project metadata entries.

		Returns:
			list[ProjectMetadata]: All project metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(ProjectMetadata).order_by(ProjectMetadata.name)
			)
			return list(result.scalars().all())

	async def create(
		self, name: str, description: str | None = None
	) -> ProjectMetadata:
		"""Create a new project metadata entry.

		Args:
			name (str): Name of the project.
			description (str | None): Description of the project.

		Returns:
			ProjectMetadata: The created project metadata.
		"""
		async with self.session_maker() as db:
			resource = ProjectMetadata(name=name, description=description)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return resource

	async def get(self, id: int) -> ProjectMetadata | None:
		"""Get a project metadata entry by ID.

		Args:
			id (int): ID of the project.

		Returns:
			ProjectMetadata | None: The project metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			return await db.get(ProjectMetadata, id)

	async def update(
		self,
		id: int,
		name: str | None = None,
		description: str | None = None,
	) -> ProjectMetadata | None:
		"""Update a project metadata entry.

		Args:
			id (int): ID of the project.
			name (str | None): New name for the project.
			description (str | None): New description for the project.

		Returns:
			ProjectMetadata | None: The updated project metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(ProjectMetadata, id)
			if resource is None:
				return None
			if name is not None:
				resource.name = name
			if description is not None:
				resource.description = description
			await db.commit()
			await db.refresh(resource)
			return resource

	async def delete(self, id: int) -> int:
		"""Delete a project metadata entry.

		Args:
			id (int): ID of the project.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(ProjectMetadata).where(ProjectMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


class RawResourceMetadataInteractor(
	BaseResourceMetadataInteractor[RawResourceMetadata]
):
	model = RawResourceMetadata


class RawVersionLineageInteractor:
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
				select(func.coalesce(func.max(RawVersionLineage.delta_version), 0) + 1)
				.where(RawVersionLineage.resource_id == resource_id)
				.scalar_subquery()
			)
			entry = RawVersionLineage(
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
				update(RawVersionLineage)
				.where(
					RawVersionLineage.resource_id == resource_id,
					RawVersionLineage.status == VersionStatus.ACTIVE,
				)
				.values(status=VersionStatus.ARCHIVED)
			)
			result = await db.execute(
				update(RawVersionLineage)
				.where(
					RawVersionLineage.resource_id == resource_id,
					RawVersionLineage.version == version,
				)
				.values(status=VersionStatus.ACTIVE)
				.returning(RawVersionLineage)
			)
			entry = result.scalars().first()
			if entry is None:
				return 0
			await db.commit()
			return 1

	async def get(self, id: int) -> RawVersionLineage | None:
		"""
		Get a bronze resource version by ID.

		Args:
			id (int): ID of the bronze resource version.

		Returns:
			RawVersionLineage | None: RawVersionLineage object if found,
			else None.
		"""
		async with self.session_maker() as db:
			return await db.get(RawVersionLineage, id)

	async def get_by_resource(
		self, resource_id: int, limit: int | None = None
	) -> list[RawVersionLineage]:
		"""Get all versions for a bronze resource.

		Args:
			resource_id (int): ID of the resource.
			limit (int | None): Maximum number of versions to return. If None,
				returns all.

		Returns:
			list[RawVersionLineage]: List of version entries.
		"""
		async with self.session_maker() as db:
			if limit is None:
				result = await db.execute(
					select(RawVersionLineage)
					.where(RawVersionLineage.resource_id == resource_id)
					.order_by(RawVersionLineage.version)
				)
			else:
				result = await db.execute(
					select(RawVersionLineage)
					.where(RawVersionLineage.resource_id == resource_id)
					.order_by(RawVersionLineage.version.desc())
					.limit(limit)
				)
			return list(result.scalars().all())

	async def get_version_by_resource(
		self, resource_id: int, version: int | None = None
	) -> RawVersionLineage | None:
		"""
		Get a specific version of a bronze resource, or the latest version if no version
		is specified.

		Args:
			resource_id (int): ID of the resource.
			version (int | None): Version number to retrieve. If None, retrieves the
				latest version.

		Returns:
			RawVersionLineage | None: RawVersionLineage object if found,
				else None.
		"""
		if version is None:
			return await self.get_latest_by_resource(resource_id)

		async with self.session_maker() as db:
			result = await db.execute(
				select(RawVersionLineage).where(
					RawVersionLineage.resource_id == resource_id,
					RawVersionLineage.version == version,
				)
			)
			return result.scalars().first()

	async def get_latest_by_resource(
		self, resource_id: int
	) -> RawVersionLineage | None:
		"""
		Get the latest version of a bronze resource.

		Args:
			resource_id (int): ID of the resource.

		Returns:
			RawVersionLineage | None: RawVersionLineage object for the
				latest version if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(RawVersionLineage)
				.where(RawVersionLineage.resource_id == resource_id)
				.order_by(RawVersionLineage.version.desc())
				.limit(1)
			)
			return result.scalars().first()

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
			entry = await db.get(RawVersionLineage, id)
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
				delete(RawVersionLineage).where(RawVersionLineage.id == id)
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
				delete(RawVersionLineage).where(
					RawVersionLineage.resource_id == resource_id,
					RawVersionLineage.version == version,
				)
			)
			await db.commit()
			return result.rowcount


class BronzeResourceMetadataInteractor(
	BaseResourceMetadataInteractor[BronzeResourceMetadata]
):
	model = BronzeResourceMetadata


class BronzeVersionLineageInteractor(
	BaseVersionLineageInteractor[BronzeVersionLineage]
):
	model = BronzeVersionLineage


class SilverResourceMetadataInteractor(
	BaseResourceMetadataInteractor[SilverResourceMetadata]
):
	model = SilverResourceMetadata


class SilverVersionLineageInteractor(
	BaseVersionLineageInteractor[SilverVersionLineage]
):
	model = SilverVersionLineage


class GoldResourceMetadataInteractor(
	BaseResourceMetadataInteractor[GoldResourceMetadata]
):
	model = GoldResourceMetadata


class GoldVersionLineageInteractor(BaseVersionLineageInteractor[GoldVersionLineage]):
	model = GoldVersionLineage

	async def create_many(
		self,
		resource_id: int,
		delta_version: int,
		resources: list[int],
	) -> list[GoldVersionLineage]:
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
			return entries

	async def get_by_delta_version(  # type: ignore[override]
		self, resource_id: int, delta_version: int
	) -> list[GoldVersionLineage]:
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage).where(
					GoldVersionLineage.resource_id == resource_id,
					GoldVersionLineage.delta_version == delta_version,
				)
			)
			return list(result.scalars().all())
