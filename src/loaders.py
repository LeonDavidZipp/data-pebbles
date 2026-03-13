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
	SilverSourceMetadataInteractor,
	SilverSourceMetadataRead,
	SilverVersionLineageInteractor,
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
		return await self.metadata_interactor.get(source_id)


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
		return await self.metadata_interactor.get(source_id)


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
