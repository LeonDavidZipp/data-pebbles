from enum import StrEnum

from sqlalchemy import (
	CursorResult,
	delete,
	func,
	select,
	update,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .models import (
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


def _version_status_values(_: object) -> list[str]:
	return [s.value for s in VersionStatus]


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


class RawResourceMetadataInteractor:
	"""Async interactor for resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[RawResourceMetadata]:
		"""Get all bronze resource metadata entries.

		Returns:
			list[RawResourceMetadata]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(RawResourceMetadata).order_by(RawResourceMetadata.name)
			)
			return list(result.scalars().all())

	async def create(
		self, name: str, project_id: int, description: str | None = None
	) -> RawResourceMetadata:
		"""Create a new bronze resource metadata entry.

		Args:
			name (str): Name of the resource.
			project_id (int): ID of the project this resource belongs to.
			description (str | None): Description of the resource.

		Returns:
			RawResourceMetadata: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = RawResourceMetadata(
				name=name, project_id=project_id, description=description
			)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return resource

	async def get(self, id: int) -> RawResourceMetadata | None:
		"""Get a bronze resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			RawResourceMetadata | None: The resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(RawResourceMetadata, id)
			if resource is None:
				return None
			return resource

	async def update(
		self,
		id: int,
		name: str | None = None,
		description: str | None = None,
	) -> RawResourceMetadata | None:
		"""Update a bronze resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.
			description (str | None): New description for the resource.

		Returns:
			RawResourceMetadata | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(RawResourceMetadata, id)
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
		"""Delete a bronze resource metadata entry.

		Args:
			id (int): ID of the resource.

		Returns:
			int: The number of rows deleted.
		"""
		async with self.session_maker() as db:
			result: CursorResult = await db.execute(  # type: ignore
				delete(RawResourceMetadata).where(RawResourceMetadata.id == id)
			)
			await db.commit()
			return result.rowcount


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


class SilverResourceMetadataInteractor:
	"""Async interactor for silver resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[SilverResourceMetadata]:
		"""Get all silver resource metadata entries.

		Returns:
			list[SilverResourceMetadata]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverResourceMetadata).order_by(SilverResourceMetadata.name)
			)
			return list(result.scalars().all())

	async def create(
		self, name: str, project_id: int, description: str | None = None
	) -> SilverResourceMetadata:
		"""Create a new silver resource metadata entry.

		Args:
			name (str): Name of the resource.
			project_id (int): ID of the project this resource belongs to.
			description (str | None): Description of the resource.

		Returns:
			SilverResourceMetadata: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = SilverResourceMetadata(
				name=name, project_id=project_id, description=description
			)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return resource

	async def get(self, id: int) -> SilverResourceMetadata | None:
		"""Get a silver resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			SilverResourceMetadata | None: The resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			return await db.get(SilverResourceMetadata, id)

	async def update(
		self,
		id: int,
		name: str | None = None,
		description: str | None = None,
	) -> SilverResourceMetadata | None:
		"""Update a silver resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.
			description (str | None): New description for the resource.

		Returns:
			SilverResourceMetadata | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(SilverResourceMetadata, id)
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
	) -> SilverVersionLineage:
		"""Create a new silver version lineage entry.

		Args:
			resource_id (int): Silver resource metadata ID.
			delta_version (int): Silver Delta Lake version.
			from_resource_id (int): Bronze resource version ID this derives from.

		Returns:
			SilverVersionLineage: The created lineage entry.
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
			return entry

	async def get(self, id: int) -> SilverVersionLineage | None:
		"""Get a silver version lineage entry by ID.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			SilverVersionLineage | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			return await db.get(SilverVersionLineage, id)

	async def get_by_resource(self, resource_id: int) -> list[SilverVersionLineage]:
		"""Get all lineage entries for a silver resource.

		Args:
			resource_id (int): Silver resource metadata ID.

		Returns:
			list[SilverVersionLineage]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage)
				.where(SilverVersionLineage.resource_id == resource_id)
				.order_by(SilverVersionLineage.delta_version)
			)
			return list(result.scalars().all())

	async def get_by_delta_version(
		self, resource_id: int, delta_version: int
	) -> SilverVersionLineage | None:
		"""Get the lineage entry for a specific silver delta version.

		Args:
			resource_id (int): Silver resource metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			SilverVersionLineage | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(SilverVersionLineage).where(
					SilverVersionLineage.resource_id == resource_id,
					SilverVersionLineage.delta_version == delta_version,
				)
			)
			return result.scalars().first()

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


class GoldResourceMetadataInteractor:
	"""Async interactor for gold resource metadata operations."""

	def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
		self.session_maker = session_maker

	async def get_all(self) -> list[GoldResourceMetadata]:
		"""Get all gold resource metadata entries.

		Returns:
			list[GoldResourceMetadata]: All resource metadata entries.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldResourceMetadata).order_by(GoldResourceMetadata.name)
			)
			return list(result.scalars().all())

	async def create(
		self, name: str, project_id: int, description: str | None = None
	) -> GoldResourceMetadata:
		"""Create a new gold resource metadata entry.

		Args:
			name (str): Name of the resource.
			project_id (int): ID of the project this resource belongs to.
			description (str | None): Description of the resource.

		Returns:
			GoldResourceMetadata: The created resource metadata.
		"""
		async with self.session_maker() as db:
			resource = GoldResourceMetadata(
				name=name, project_id=project_id, description=description
			)
			db.add(resource)
			await db.commit()
			await db.refresh(resource)
			return resource

	async def get(self, id: int) -> GoldResourceMetadata | None:
		"""Get a gold resource metadata entry by ID.

		Args:
			id (int): ID of the resource.

		Returns:
			GoldResourceMetadata | None: The resource metadata if found, else None.
		"""
		async with self.session_maker() as db:
			return await db.get(GoldResourceMetadata, id)

	async def update(
		self,
		id: int,
		name: str | None = None,
		description: str | None = None,
	) -> GoldResourceMetadata | None:
		"""Update a gold resource metadata entry.

		Args:
			id (int): ID of the resource.
			name (str | None): New name for the resource.
			description (str | None): New description for the resource.

		Returns:
			GoldResourceMetadata | None: The updated resource metadata if found,
				else None.
		"""
		async with self.session_maker() as db:
			resource = await db.get(GoldResourceMetadata, id)
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
	) -> GoldVersionLineage:
		"""Create a new gold version lineage entry.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Gold Delta Lake version.
			from_resource_id (int): Silver version lineage row ID this derives from.

		Returns:
			GoldVersionLineage: The created lineage entry.
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
			return entry

	async def create_many(
		self,
		resource_id: int,
		delta_version: int,
		resources: list[int],
	) -> list[GoldVersionLineage]:
		"""Create multiple lineage entries for a single gold delta version.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Gold Delta Lake version.
			resources (list[int]): List of silver version lineage row IDs.

		Returns:
			list[GoldVersionLineage]: The created lineage entries.
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
			return entries

	async def get(self, id: int) -> GoldVersionLineage | None:
		"""Get a gold version lineage entry by ID.

		Args:
			id (int): ID of the lineage entry.

		Returns:
			GoldVersionLineage | None: The lineage entry if found, else None.
		"""
		async with self.session_maker() as db:
			return await db.get(GoldVersionLineage, id)

	async def get_by_resource(self, resource_id: int) -> list[GoldVersionLineage]:
		"""Get all lineage entries for a gold resource.

		Args:
			resource_id (int): Gold resource metadata ID.

		Returns:
			list[GoldVersionLineage]: List of lineage entries ordered by delta
				version.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage)
				.where(GoldVersionLineage.resource_id == resource_id)
				.order_by(GoldVersionLineage.delta_version)
			)
			return list(result.scalars().all())

	async def get_by_delta_version(
		self, resource_id: int, delta_version: int
	) -> list[GoldVersionLineage]:
		"""Get all lineage entries for a specific gold delta version.

		Args:
			resource_id (int): Gold resource metadata ID.
			delta_version (int): Delta Lake version number.

		Returns:
			list[GoldVersionLineage]: List of lineage entries. Multiple entries
				possible since a gold version can derive from multiple silver resources.
		"""
		async with self.session_maker() as db:
			result = await db.execute(
				select(GoldVersionLineage).where(
					GoldVersionLineage.resource_id == resource_id,
					GoldVersionLineage.delta_version == delta_version,
				)
			)
			return list(result.scalars().all())

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
