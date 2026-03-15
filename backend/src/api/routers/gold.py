from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ..dependencies import GoldLoader, gold_dep, validate_file
from ..exceptions import ResourceNotFoundError

gold_router = APIRouter()


class CreateGoldResourceRequest(BaseModel):
	name: str
	project_id: int
	description: str | None = None


class UpdateGoldResourceRequest(BaseModel):
	name: str
	description: str | None = None


class GoldMetadataResponse(BaseModel):
	id: int
	name: str
	description: str | None
	project_id: int
	created_at: str


class GoldLineageResponse(BaseModel):
	id: int
	resource_id: int
	delta_version: int
	from_resource_id: int
	created_at: str


@gold_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> list[GoldMetadataResponse]:
	resources = await gold.metadata_interactor.get_all()
	return [
		GoldMetadataResponse(
			id=s.id,
			name=s.name,
			description=s.description,
			project_id=s.project_id,
			created_at=s.created_at.isoformat(),
		)
		for s in resources
	]


@gold_router.post("/")
async def create_resource(
	body: CreateGoldResourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> JSONResponse:
	res = await gold.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return JSONResponse(
		content={"message": "Resource created successfully.", "resource_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@gold_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	res = await gold.get_metadata(resource_id)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return GoldMetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@gold_router.delete("/{resource_id}")
async def delete_resource(
	resource_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> JSONResponse:
	await gold.metadata_interactor.delete(resource_id)
	return JSONResponse(
		content={"message": "Resource deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@gold_router.patch("/{resource_id}")
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateGoldResourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	res = await gold.metadata_interactor.update(
		resource_id, name=body.name, description=body.description
	)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return GoldMetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@gold_router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	resource_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> list[GoldLineageResponse]:
	entries = await gold.get_lineage(resource_id)
	return [
		GoldLineageResponse(
			id=e.id,
			resource_id=e.resource_id,
			delta_version=e.delta_version,
			from_resource_id=e.from_resource_id,
			created_at=e.created_at.isoformat(),
		)
		for e in entries
	]


@gold_router.post("/{resource_id}/versions")
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
	resources: Annotated[list[int], Query()],
):
	content = await file.read()
	lf = pl.scan_parquet(content)
	await gold.upload(
		resource_id=resource_id,
		lf=lf,
		resources=resources,
		mode="append",
	)


@gold_router.get("/{resource_id}/versions/{version}")
def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> StreamingResponse:
	df = gold.get(resource_id=resource_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={resource_id}.parquet"},
	)
