from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ..dependencies import SilverLoader, silver_dep, validate_file

silver_router = APIRouter()


class CreateSilverSourceRequest(BaseModel):
	name: str


class SilverMetadataResponse(BaseModel):
	id: int
	name: str
	created_at: str


class SilverLineageResponse(BaseModel):
	id: int
	source_id: int
	delta_version: int
	from_source_id: int
	created_at: str


@silver_router.post("/")
async def create_source(
	body: CreateSilverSourceRequest,
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> JSONResponse:
	res = await silver.metadata_interactor.create(body.name)
	return JSONResponse(
		content={"message": "Source created successfully.", "source_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@silver_router.get("/{source_id}/metadata", status_code=status.HTTP_200_OK)
async def get_source_metadata(
	source_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SilverMetadataResponse:
	res = await silver.get_metadata(source_id)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Source not found."
		)
	return SilverMetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@silver_router.delete("/{source_id}")
async def delete_source(
	source_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> JSONResponse:
	await silver.metadata_interactor.delete(source_id)
	return JSONResponse(
		content={"message": "Source deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@silver_router.post("/upload/{source_id}")
async def upload(
	source_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
	from_source_id: Annotated[int, Query()],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	await silver.upload(
		source_id=source_id, lf=lf, from_source_id=from_source_id, mode="append"
	)


@silver_router.get("/download/{source_id}")
def download(
	silver: Annotated[SilverLoader, Depends(silver_dep)],
	source_id: Annotated[int, Path()],
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	df = silver.get(source_id=source_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={source_id}.parquet"},
	)


@silver_router.get("/{source_id}/lineage", status_code=status.HTTP_200_OK)
async def get_lineage(
	source_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> list[SilverLineageResponse]:
	entries = await silver.get_lineage(source_id)
	return [
		SilverLineageResponse(
			id=e.id,
			source_id=e.source_id,
			delta_version=e.delta_version,
			from_source_id=e.from_source_id,
			created_at=e.created_at.isoformat(),
		)
		for e in entries
	]
