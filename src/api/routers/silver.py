from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile
from fastapi.responses import StreamingResponse

from ..dependencies import DeltaLoader, silver_dep, validate_file

silver_router = APIRouter()


@silver_router.post("/upload/{source_id}")
async def upload(
	source_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	silver: Annotated[DeltaLoader, Depends(silver_dep)],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	silver.upload(table=file.filename, lf=lf, mode="append")  # type: ignore


@silver_router.get("/download/{file_id}")
def download(
	file_id: int,
	silver: Annotated[DeltaLoader, Depends(silver_dep)],
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	df = silver.get(table=str(file_id), version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={file_id}.parquet"},
	)
