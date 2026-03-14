from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile
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
	gold.upload(table=file.filename, lf=lf, mode="append")  # type: ignore


@gold_router.get("/download/{source_id}")
def download(
	gold: Annotated[DeltaLoader, Depends(gold_dep)],
	source_id: Annotated[int, Path()],
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	df = gold.get(table=str(source_id), version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={source_id}.parquet"},
	)
