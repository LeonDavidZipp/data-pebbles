from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Literal

import polars as pl
from deltalake import DeltaTable

from .postgres import (
	BronzeSourceMetadataInteractor,
	BronzeSourceMetadataRead,
	BronzeSourceVersionInteractor,
	GoldSourceMetadataInteractor,
	GoldSourceMetadataRead,
	GoldVersionLineageInteractor,
	GoldVersionLineageRead,
	SilverSourceMetadataInteractor,
	SilverSourceMetadataRead,
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

	def get(self, table: str, version: int | None = None) -> pl.DataFrame:
		path = f"{self.base_path}/{table}"
		return pl.read_delta(
			path, version=version, storage_options=self.storage_options
		)

	def upload(
		self,
		table: str,
		df: pl.DataFrame,
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> int:
		path = f"{self.base_path}/{table}"
		write_opts = {"schema_mode": "overwrite"}
		df.write_delta(  # type: ignore
			path,
			mode=mode,
			storage_options=self.storage_options,
			delta_write_options=write_opts,
		)
		return DeltaTable(path, storage_options=self.storage_options).version()


class SilverLoader:
	def __init__(
		self,
		metadata_interactor: SilverSourceMetadataInteractor,
		lineage_interactor: SilverVersionLineageInteractor,
		delta_loader: DeltaLoader,
	):
		self.metadata_interactor = metadata_interactor
		self.lineage_interactor = lineage_interactor
		self.delta_loader = delta_loader

	async def get_metadata(self, source_id: int) -> SilverSourceMetadataRead | None:
		"""Get silver source metadata by ID.

		Args:
			source_id (int): ID of the silver source.

		Returns:
			SilverSourceMetadataRead | None: The source metadata if found, else None.
		"""
		return await self.metadata_interactor.get(source_id)

	def get(self, source_id: int, version: int | None = None) -> pl.DataFrame:
		"""Get data from a silver Delta table.

		Args:
			source_id (int): ID of the silver source (used as table name).
			version (int | None): Delta version to read. If None, reads latest.

		Returns:
			pl.DataFrame: The data from the Delta table.
		"""
		return self.delta_loader.get(table=str(source_id), version=version)

	async def upload(
		self,
		source_id: int,
		df: pl.DataFrame,
		from_source_id: int,
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> SilverVersionLineageRead:
		"""Upload data to a silver Delta table and record lineage.

		Args:
			source_id (int): ID of the silver source (used as table name).
			df (pl.DataFrame): Data to write.
			from_source_id (int): Bronze source version ID this data derives from.
			mode (Literal["error", "append", "overwrite", "ignore"]): Delta write mode.

		Returns:
			SilverVersionLineageRead: The created lineage entry.
		"""
		delta_version = self.delta_loader.upload(table=str(source_id), df=df, mode=mode)
		return await self.lineage_interactor.create(
			source_id=source_id,
			delta_version=delta_version,
			from_source_id=from_source_id,
		)

	async def get_lineage(self, source_id: int) -> list[SilverVersionLineageRead]:
		"""Get all lineage entries for a silver source.

		Args:
			source_id (int): ID of the silver source.

		Returns:
			list[SilverVersionLineageRead]: All lineage entries ordered by delta
				version.
		"""
		return await self.lineage_interactor.get_by_source(source_id)

	async def get_version_lineage(
		self, source_id: int, delta_version: int
	) -> SilverVersionLineageRead | None:
		"""Get the lineage entry for a specific silver delta version.

		Args:
			source_id (int): ID of the silver source.
			delta_version (int): Delta version number.

		Returns:
			SilverVersionLineageRead | None: The lineage entry if found, else None.
		"""
		return await self.lineage_interactor.get_by_delta_version(
			source_id, delta_version
		)


class GoldLoader:
	def __init__(
		self,
		metadata_interactor: GoldSourceMetadataInteractor,
		lineage_interactor: GoldVersionLineageInteractor,
		delta_loader: DeltaLoader,
	):
		self.metadata_interactor = metadata_interactor
		self.lineage_interactor = lineage_interactor
		self.delta_loader = delta_loader

	async def get_metadata(self, source_id: int) -> GoldSourceMetadataRead | None:
		"""Get gold source metadata by ID.

		Args:
			source_id (int): ID of the gold source.

		Returns:
			GoldSourceMetadataRead | None: The source metadata if found, else None.
		"""
		return await self.metadata_interactor.get(source_id)

	def get(self, source_id: int, version: int | None = None) -> pl.DataFrame:
		"""Get data from a gold Delta table.

		Args:
			source_id (int): ID of the gold source (used as table name).
			version (int | None): Delta version to read. If None, reads latest.

		Returns:
			pl.DataFrame: The data from the Delta table.
		"""
		return self.delta_loader.get(table=str(source_id), version=version)

	async def upload(
		self,
		source_id: int,
		df: pl.DataFrame,
		sources: list[tuple[int, int]],
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> list[GoldVersionLineageRead]:
		"""Upload data to a gold Delta table and record lineage.

		Args:
			source_id (int): ID of the gold source (used as table name).
			df (pl.DataFrame): Data to write.
			sources (list[tuple[int, int]]): List of (silver_source_id,
				silver_delta_version)
				tuples this data derives from.
			mode (Literal["error", "append", "overwrite", "ignore"]): Delta write mode.

		Returns:
			list[GoldVersionLineageRead]: The created lineage entries.
		"""
		delta_version = self.delta_loader.upload(table=str(source_id), df=df, mode=mode)
		return await self.lineage_interactor.create_many(
			source_id=source_id,
			delta_version=delta_version,
			sources=sources,
		)

	async def get_lineage(self, source_id: int) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a gold source.

		Args:
			source_id (int): ID of the gold source.

		Returns:
			list[GoldVersionLineageRead]: All lineage entries ordered by delta version.
		"""
		return await self.lineage_interactor.get_by_source(source_id)

	async def get_version_lineage(
		self, source_id: int, delta_version: int
	) -> list[GoldVersionLineageRead]:
		"""Get all lineage entries for a specific gold delta version.

		Args:
			source_id (int): ID of the gold source.
			delta_version (int): Delta version number.

		Returns:
			list[GoldVersionLineageRead]: The lineage entries. Multiple entries possible
				since a gold version can derive from multiple silver sources.
		"""
		return await self.lineage_interactor.get_by_delta_version(
			source_id, delta_version
		)


@dataclass
class BronzeFileResult:
	content: bytes
	name: str


class BronzeLoader:
	def __init__(
		self,
		metadata_interactor: BronzeSourceMetadataInteractor,
		version_interactor: BronzeSourceVersionInteractor,
		s3_interactor: S3Interactor,
	):
		self.metadata_interactor = metadata_interactor
		self.version_interactor = version_interactor
		self.s3_interactor = s3_interactor

	async def get_metadata(self, source_id: int) -> BronzeSourceMetadataRead | None:
		return await self.metadata_interactor.get(source_id)

	async def download_version(
		self, source_id: int, version: int | None = None
	) -> BronzeFileResult | None:
		source = await self.version_interactor.get_version_by_source(source_id, version)
		if source is None:
			return None
		data = self.s3_interactor.download_file(source.s3_key)
		if data is None:
			return None
		name = PurePosixPath(source.s3_key).name
		return BronzeFileResult(content=data, name=name)

	async def upload(
		self, source_id: int, file: bytes, filename: str, set_as_active: bool = False
	) -> int:
		s3_key = self.s3_interactor.upload_file(file, filename)
		return await self.version_interactor.create(source_id, s3_key, set_as_active)

	async def delete_version(self, source_id: int, version: int) -> int:
		source = await self.version_interactor.get_version_by_source(source_id, version)
		if source is not None:
			self.s3_interactor.delete_file(source.s3_key)
		return await self.version_interactor.delete_version_by_source(
			source_id, version
		)
