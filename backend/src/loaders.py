from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Literal

import polars as pl
from deltalake import DeltaTable

from .postgres import (
	BronzeResourceMetadataInteractor,
	BronzeResourceMetadataRead,
	BronzeResourceVersionInteractor,
	GoldResourceMetadataInteractor,
	GoldResourceMetadataRead,
	GoldVersionLineageInteractor,
	GoldVersionLineageRead,
	SilverResourceMetadataInteractor,
	SilverResourceMetadataRead,
	SilverVersionLineageInteractor,
	SilverVersionLineageRead,
)
from .s3 import S3Interactor


class DeltaLoader:
	def __init__(
		self,
		layer: Literal["silver", "gold"],
		base_path: str = "s3://",
		storage_options: dict[str, Any] | None = None,
	):
		self.base_path = f"{base_path}/{layer}"
		self.storage_options = storage_options

	def get(self, table: str, version: int | None = None) -> pl.LazyFrame:
		path = f"{self.base_path}/{table}"
		return pl.scan_delta(
			path, version=version, storage_options=self.storage_options
		)

	def upload(
		self,
		table: str,
		lf: pl.LazyFrame,
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> int:
		path = f"{self.base_path}/{table}"
		write_opts = {"schema_mode": "overwrite"}
		lf.sink_delta(  # type: ignore
			path,
			mode=mode,
			storage_options=self.storage_options,
			delta_write_options=write_opts,
		)
		return DeltaTable(path, storage_options=self.storage_options).version()


class SilverLoader:
	def __init__(
		self,
		metadata_interactor: SilverResourceMetadataInteractor,
		lineage_interactor: SilverVersionLineageInteractor,
		delta_loader: DeltaLoader,
	):
		self.metadata_interactor = metadata_interactor
		self.lineage_interactor = lineage_interactor
		self.delta_loader = delta_loader

	async def get_metadata(self, resource_id: int) -> SilverResourceMetadataRead | None:
		"""Get silver resource metadata by ID.

		Args:
			resource_id (int): ID of the silver resource.

		Returns:
			SilverResourceMetadataRead | None: The resource metadata if found,
				else None.
		"""
		return await self.metadata_interactor.get(resource_id)

	def get(self, resource_id: int, version: int | None = None) -> pl.LazyFrame:
		"""Get data from a silver Delta table.

		Args:
			resource_id (int): ID of the silver resource (used as table name).
			version (int | None): Delta version to read. If None, reads latest.

		Returns:
			pl.DataFrame: The data from the Delta table.
		"""
		return self.delta_loader.get(table=str(resource_id), version=version)

	async def upload(
		self,
		resource_id: int,
		lf: pl.LazyFrame,
		from_resource_id: int,
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> SilverVersionLineageRead:
		"""Upload data to a silver Delta table and record lineage.

		Args:
			resource_id (int): ID of the silver resource (used as table name).
			lf (pl.LazyFrame): Data to write.
			from_resource_id (int): Bronze resource version ID this data derives from.
			mode (Literal["error", "append", "overwrite", "ignore"]): Delta write mode.

		Returns:
			SilverVersionLineageRead: The created lineage entry.
		"""
		delta_version = self.delta_loader.upload(
			table=str(resource_id), lf=lf, mode=mode
		)
		return await self.lineage_interactor.create(
			resource_id=resource_id,
			delta_version=delta_version,
			from_resource_id=from_resource_id,
		)

	async def get_lineage(self, resource_id: int) -> list[SilverVersionLineageRead]:
		"""Get all lineage entries for a silver resource.

		Args:
			resource_id (int): ID of the silver resource.

		Returns:
			list[SilverVersionLineageRead]: All lineage entries ordered by delta
				version.
		"""
		return await self.lineage_interactor.get_by_resource(resource_id)

	async def get_version_lineage(
		self, resource_id: int, delta_version: int
	) -> SilverVersionLineageRead | None:
		"""Get the lineage entry for a specific silver delta version.

		Args:
			resource_id (int): ID of the silver resource.
			delta_version (int): Delta version number.

		Returns:
			SilverVersionLineageRead | None: The lineage entry if found, else None.
		"""
		return await self.lineage_interactor.get_by_delta_version(
			resource_id, delta_version
		)


class GoldLoader:
	def __init__(
		self,
		metadata_interactor: GoldResourceMetadataInteractor,
		lineage_interactor: GoldVersionLineageInteractor,
		delta_loader: DeltaLoader,
	):
		self.metadata_interactor = metadata_interactor
		self.lineage_interactor = lineage_interactor
		self.delta_loader = delta_loader

	async def get_metadata(self, resource_id: int) -> GoldResourceMetadataRead | None:
		"""Get gold resource metadata by ID.

		Args:
			resource_id (int): ID of the gold resource.

		Returns:
			GoldResourceMetadataRead | None: The resource metadata if found, else None.
		"""
		return await self.metadata_interactor.get(resource_id)

	def get(self, resource_id: int, version: int | None = None) -> pl.LazyFrame:
		"""Get data from a gold Delta table.

		Args:
			resource_id (int): ID of the gold resource (used as table name).
			version (int | None): Delta version to read. If None, reads latest.

		Returns:
			pl.DataFrame: The data from the Delta table.
		"""
		return self.delta_loader.get(table=str(resource_id), version=version)

	async def upload(
		self,
		resource_id: int,
		lf: pl.LazyFrame,
		resources: list[int],
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> list[GoldVersionLineageRead]:
		"""Upload data to a gold Delta table and record lineage.

		Args:
			resource_id (int): ID of the gold resource (used as table name).
			lf (pl.LazyFrame): Data to write.
			resources (list[int]): Silver version lineage row IDs this data derives
				from.
			mode (Literal["error", "append", "overwrite", "ignore"]): Delta write mode.

		Returns:
			list[GoldVersionLineageRead]: The created lineage entries.
		"""
		delta_version = self.delta_loader.upload(
			table=str(resource_id), lf=lf, mode=mode
		)
		return await self.lineage_interactor.create_many(
			resource_id=resource_id,
			delta_version=delta_version,
			resources=resources,
		)

	async def get_lineage(self, resource_id: int) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a gold resource.

		Args:
			resource_id (int): ID of the gold resource.

		Returns:
			list[GoldVersionLineageRead]: All lineage entries ordered by delta version.
		"""
		return await self.lineage_interactor.get_by_resource(resource_id)

	async def get_version_lineage(
		self, resource_id: int, delta_version: int
	) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a specific gold delta version.

		Args:
			resource_id (int): ID of the gold resource.
			delta_version (int): Delta version number.

		Returns:
			list[GoldVersionLineageRead]: The lineage entries.
		"""
		return await self.lineage_interactor.get_by_delta_version(
			resource_id, delta_version
		)


@dataclass
class BronzeFileResult:
	content: bytes
	name: str


class BronzeLoader:
	def __init__(
		self,
		metadata_interactor: BronzeResourceMetadataInteractor,
		version_interactor: BronzeResourceVersionInteractor,
		s3_interactor: S3Interactor,
	):
		self.metadata_interactor = metadata_interactor
		self.version_interactor = version_interactor
		self.s3_interactor = s3_interactor

	async def get_metadata(self, resource_id: int) -> BronzeResourceMetadataRead | None:
		return await self.metadata_interactor.get(resource_id)

	async def download_version(
		self, resource_id: int, version: int | None = None
	) -> BronzeFileResult | None:
		resource = await self.version_interactor.get_version_by_resource(
			resource_id, version
		)
		if resource is None:
			return None
		data = self.s3_interactor.download_file(resource.s3_key)
		if data is None:
			return None
		name = PurePosixPath(resource.s3_key).name
		return BronzeFileResult(content=data, name=name)

	async def upload(
		self, resource_id: int, file: bytes, filename: str, set_as_active: bool = False
	) -> int:
		s3_key = self.s3_interactor.upload_file(file, filename)
		return await self.version_interactor.create(resource_id, s3_key, set_as_active)

	async def delete_version(self, resource_id: int, version: int) -> int:
		resource = await self.version_interactor.get_version_by_resource(
			resource_id, version
		)
		if resource is not None:
			self.s3_interactor.delete_file(resource.s3_key)
		return await self.version_interactor.delete_version_by_resource(
			resource_id, version
		)
