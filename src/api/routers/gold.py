from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi.responses import StreamingResponse

from ..dependencies import DeltaLoader, gold_dep, validate_file

gold_router = APIRouter()


@gold_router.post("/upload")
async def upload(
	file: Annotated[UploadFile, Depends(validate_file)],
	gold: Annotated[DeltaLoader, Depends(gold_dep)],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	gold.upload_lazy(table=file.filename, lf=lf, mode="append")  # type: ignore


@gold_router.get("/download/{file_id}")
def download(
	gold: Annotated[DeltaLoader, Depends(gold_dep)],
	file_id: int,
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	df = gold.get(table=str(file_id), version=version)
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={file_id}.parquet"},
	)
