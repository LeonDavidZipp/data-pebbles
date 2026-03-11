from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi.responses import StreamingResponse

from ..dependencies import DeltaLoader, silver_dep, validate_file

silver_router = APIRouter()


@silver_router.post("/upload")
async def upload(
	file: Annotated[UploadFile, Depends(validate_file)],
	silver: Annotated[DeltaLoader, Depends(silver_dep)],
):
	content = await file.read()
	df = pl.read_parquet(content)
	silver.upload(table=file.filename, df=df, mode="append")  # type: ignore


@silver_router.get("/download/{file_id}")
def download(
	file_id: int,
	silver: Annotated[DeltaLoader, Depends(silver_dep)],
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	df = silver.get(table=str(file_id), version=version)
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={file_id}.parquet"},
	)
