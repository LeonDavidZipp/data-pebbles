from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ..dependencies import SilverLoader, silver_dep, validate_file

silver_router = APIRouter()


class CreateSilverResourceRequest(BaseModel):
	name: str


class UpdateSilverResourceRequest(BaseModel):
	name: str


class SilverMetadataResponse(BaseModel):
	id: int
	name: str
	created_at: str


class SilverLineageResponse(BaseModel):
	id: int
	resource_id: int
	delta_version: int
	from_resource_id: int
	created_at: str


@silver_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> list[SilverMetadataResponse]:
	resources = await silver.metadata_interactor.get_all()
	return [
		SilverMetadataResponse(
			id=s.id,
			name=s.name,
			created_at=s.created_at.isoformat(),
		)
		for s in resources
	]


@silver_router.post("/")
async def create_resource(
	body: CreateSilverResourceRequest,
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> JSONResponse:
	res = await silver.metadata_interactor.create(body.name)
	return JSONResponse(
		content={"message": "Resource created successfully.", "resource_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@silver_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SilverMetadataResponse:
	res = await silver.get_metadata(resource_id)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found."
		)
	return SilverMetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@silver_router.delete("/{resource_id}")
async def delete_resource(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> JSONResponse:
	await silver.metadata_interactor.delete(resource_id)
	return JSONResponse(
		content={"message": "Resource deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@silver_router.patch("/{resource_id}")
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateSilverResourceRequest,
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SilverMetadataResponse:
	res = await silver.metadata_interactor.update(resource_id, name=body.name)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found."
		)
	return SilverMetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@silver_router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> list[SilverLineageResponse]:
	entries = await silver.get_lineage(resource_id)
	return [
		SilverLineageResponse(
			id=e.id,
			resource_id=e.resource_id,
			delta_version=e.delta_version,
			from_resource_id=e.from_resource_id,
			created_at=e.created_at.isoformat(),
		)
		for e in entries
	]


@silver_router.post("/{resource_id}/versions")
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
	from_resource_id: Annotated[int, Query()],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	await silver.upload(
		resource_id=resource_id, lf=lf, from_resource_id=from_resource_id, mode="append"
	)


@silver_router.get("/{resource_id}/versions/{version}")
def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> StreamingResponse:
	df = silver.get(resource_id=resource_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={resource_id}.parquet"},
	)
