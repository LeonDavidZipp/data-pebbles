from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ..dependencies import GoldLoader, gold_dep, validate_file

gold_router = APIRouter()


class CreateGoldSourceRequest(BaseModel):
	name: str


class UpdateGoldSourceRequest(BaseModel):
	name: str


class GoldMetadataResponse(BaseModel):
	id: int
	name: str
	created_at: str


class GoldLineageResponse(BaseModel):
	id: int
	source_id: int
	delta_version: int
	from_source_id: int
	created_at: str


@gold_router.get("/", status_code=status.HTTP_200_OK)
async def list_sources(
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> list[GoldMetadataResponse]:
	sources = await gold.metadata_interactor.get_all()
	return [
		GoldMetadataResponse(
			id=s.id,
			name=s.name,
			created_at=s.created_at.isoformat(),
		)
		for s in sources
	]


@gold_router.post("/")
async def create_source(
	body: CreateGoldSourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> JSONResponse:
	res = await gold.metadata_interactor.create(body.name)
	return JSONResponse(
		content={"message": "Source created successfully.", "source_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@gold_router.get("/{source_id}", status_code=status.HTTP_200_OK)
async def get_source(
	source_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	res = await gold.get_metadata(source_id)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Source not found."
		)
	return GoldMetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@gold_router.delete("/{source_id}")
async def delete_source(
	source_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> JSONResponse:
	await gold.metadata_interactor.delete(source_id)
	return JSONResponse(
		content={"message": "Source deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@gold_router.patch("/{source_id}")
async def update_source(
	source_id: Annotated[int, Path()],
	body: UpdateGoldSourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	res = await gold.metadata_interactor.update(source_id, name=body.name)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Source not found."
		)
	return GoldMetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@gold_router.get("/{source_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	source_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> list[GoldLineageResponse]:
	entries = await gold.get_lineage(source_id)
	return [
		GoldLineageResponse(
			id=e.id,
			source_id=e.source_id,
			delta_version=e.delta_version,
			from_source_id=e.from_source_id,
			created_at=e.created_at.isoformat(),
		)
		for e in entries
	]


@gold_router.post("/{source_id}/versions")
async def upload_version(
	source_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
	sources: Annotated[list[int], Query()],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	await gold.upload(
		source_id=source_id,
		lf=lf,
		sources=sources,
		mode="append",
	)


@gold_router.get("/{source_id}/versions/{version}")
def download_version(
	source_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> StreamingResponse:
	df = gold.get(source_id=source_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={source_id}.parquet"},
	)
