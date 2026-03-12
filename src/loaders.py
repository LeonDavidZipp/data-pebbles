from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Literal

import polars as pl

from .postgres import (
	BronzeSourceMetadataInteractor,
	BronzeSourceVersionInteractor,
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
		storage_options = self.storage_options
		if version is not None and storage_options is not None:
			storage_options["version"] = version
		return pl.read_delta(path, storage_options=storage_options)  # type: ignore

	def upload(
		self,
		table: str,
		df: pl.DataFrame,
		mode: Literal["error", "append", "overwrite", "ignore"] = "append",
	) -> None:
		write_opts = {"schema_mode": "overwrite"}
		df.write_delta(  # type: ignore
			f"{self.base_path}/{table}",
			mode=mode,
			storage_options=self.storage_options,
			delta_write_options=write_opts,
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

	async def get_version(
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
