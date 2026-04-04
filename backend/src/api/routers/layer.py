from collections.abc import Callable
from typing import Annotated, cast

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ...loaders import BronzeLoader, GoldLoader, SilverLoader
from ..dependencies import validate_file
from ..exceptions import ResourceNotFoundError

Loader = BronzeLoader | SilverLoader | GoldLoader


class CreateResourceRequest(BaseModel):
	name: str
	project_id: int
	description: str | None = None


class UpdateResourceRequest(BaseModel):
	name: str
	description: str | None = None


class MetadataResponse(BaseModel):
	id: int
	name: str
	description: str | None
	project_id: int
	created_at: str


class LineageResponse(BaseModel):
	id: int
	resource_id: int
	delta_version: int
	from_resource_id: int
	created_at: str


class CreateResourceResponse(BaseModel):
	message: str
	resource_id: int


class MessageResponse(BaseModel):
	message: str


class SchemaResponse(BaseModel):
	data_schema: dict[str, str]
	data: dict[str, list[int | float | str | bool | None]]


def create_layer_router(
	dep: Callable[[], Loader], *, multi_source: bool = False
) -> APIRouter:
	router = APIRouter()

	@router.get("/", status_code=status.HTTP_200_OK)
	async def list_resources(  # type: ignore
		loader: Annotated[Loader, Depends(dep)],
	) -> list[MetadataResponse]:
		resources = await loader.metadata_interactor.get_all()
		return [
			MetadataResponse(
				id=s.id,
				name=s.name,
				description=s.description,
				project_id=s.project_id,
				created_at=s.created_at.isoformat(),
			)
			for s in resources
		]

	@router.post("/", status_code=status.HTTP_201_CREATED)
	async def create_resource(  # type: ignore
		body: CreateResourceRequest,
		loader: Annotated[Loader, Depends(dep)],
	) -> CreateResourceResponse:
		res = await loader.metadata_interactor.create(
			body.name, body.project_id, body.description
		)
		return CreateResourceResponse(
			message="Resource created successfully.",
			resource_id=res.id,
		)

	@router.get("/{resource_id}", status_code=status.HTTP_200_OK)
	async def get_resource(  # type: ignore
		resource_id: Annotated[int, Path()],
		loader: Annotated[Loader, Depends(dep)],
	) -> MetadataResponse:
		res = await loader.get_metadata(resource_id)
		if res is None:
			raise ResourceNotFoundError(resource_id)
		return MetadataResponse(
			id=res.id,
			name=res.name,
			description=res.description,
			project_id=res.project_id,
			created_at=res.created_at.isoformat(),
		)

	@router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
	async def delete_resource(  # type: ignore
		resource_id: Annotated[int, Path()],
		loader: Annotated[Loader, Depends(dep)],
	) -> MessageResponse:
		await loader.metadata_interactor.delete(resource_id)
		return MessageResponse(message="Resource deleted successfully.")

	@router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
	async def update_resource(  # type: ignore
		resource_id: Annotated[int, Path()],
		body: UpdateResourceRequest,
		loader: Annotated[Loader, Depends(dep)],
	) -> MetadataResponse:
		res = await loader.metadata_interactor.update(
			resource_id, name=body.name, description=body.description
		)
		if res is None:
			raise ResourceNotFoundError(resource_id)
		return MetadataResponse(
			id=res.id,
			name=res.name,
			description=res.description,
			project_id=res.project_id,
			created_at=res.created_at.isoformat(),
		)

	@router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
	async def list_versions(  # type: ignore
		resource_id: Annotated[int, Path()],
		loader: Annotated[Loader, Depends(dep)],
	) -> list[LineageResponse]:
		entries = await loader.get_lineage(resource_id)
		return [
			LineageResponse(
				id=e.id,
				resource_id=e.resource_id,
				delta_version=e.delta_version,
				from_resource_id=e.from_resource_id,
				created_at=e.created_at.isoformat(),
			)
			for e in entries
		]

	if multi_source:

		@router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
		async def upload_version_multi(  # type: ignore
			resource_id: Annotated[int, Path()],
			file: Annotated[UploadFile, Depends(validate_file)],
			loader: Annotated[Loader, Depends(dep)],
			resources: Annotated[list[int], Query()],
		) -> MessageResponse:
			content = await file.read()
			lf = pl.scan_parquet(content)
			await cast(GoldLoader, loader).upload(
				resource_id=resource_id,
				lf=lf,
				resources=resources,
				mode="overwrite",
			)
			return MessageResponse(message="File uploaded successfully.")

	else:

		@router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
		async def upload_version_single(  # type: ignore
			resource_id: Annotated[int, Path()],
			file: Annotated[UploadFile, Depends(validate_file)],
			loader: Annotated[Loader, Depends(dep)],
			from_resource_id: Annotated[int, Query()],
		) -> MessageResponse:
			content = await file.read()
			lf = pl.scan_parquet(content)
			await cast(BronzeLoader, loader).upload(
				resource_id=resource_id,
				lf=lf,
				from_resource_id=from_resource_id,
				mode="overwrite",
			)
			return MessageResponse(message="File uploaded successfully.")

	@router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
	def download_version(  # type: ignore
		resource_id: Annotated[int, Path()],
		version: Annotated[int, Path()],
		loader: Annotated[Loader, Depends(dep)],
	) -> StreamingResponse:
		df = loader.get(resource_id=resource_id, version=version).collect()
		buf = df.write_ipc_stream(None)
		buf.seek(0)
		return StreamingResponse(
			buf,
			media_type="application/octet-stream",
			headers={
				"Content-Disposition": f"attachment; filename={resource_id}.parquet"
			},
		)

	@router.get(
		"/{resource_id}/versions/{version}/schema",
		status_code=status.HTTP_200_OK,
	)
	async def get_schema(  # type: ignore
		resource_id: Annotated[int, Path()],
		version: Annotated[int, Path()],
		loader: Annotated[Loader, Depends(dep)],
	) -> SchemaResponse:
		df = loader.get(resource_id=resource_id, version=version).head(5).collect()
		schema = {col: type(dtype).__name__.lower() for col, dtype in df.schema.items()}
		return SchemaResponse(data_schema=schema, data=df.to_dict(as_series=False))

	return router
