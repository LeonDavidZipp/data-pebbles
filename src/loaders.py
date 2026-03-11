from typing import Any, Literal

import polars as pl


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
