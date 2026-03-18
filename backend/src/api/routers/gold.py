from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile, status
from fastapi.responses import StreamingResponse
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


class CreateResourceResponse(BaseModel):
	message: str
	resource_id: int


class MessageResponse(BaseModel):
	message: str


class SchemaResponse(BaseModel):
	data_schema: dict[str, str]
	data: dict[str, list[int | float | str | bool | None]]


@gold_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> list[GoldMetadataResponse]:
	"""Return metadata for all Gold layer resources across all projects.

	Returns:
		list[GoldMetadataResponse]: All Gold resources with id, name, description,
			project_id, and created_at.
	"""
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


@gold_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(
	body: CreateGoldResourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> CreateResourceResponse:
	"""Create a new Gold layer resource.

	Args:
		body (CreateGoldResourceRequest): name (str), project_id (int),
			description (str | None).

	Returns:
		CreateResourceResponse: Confirmation message and the new resource_id (int).
	"""
	res = await gold.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return CreateResourceResponse(
		message="Resource created successfully.",
		resource_id=res.id,
	)


@gold_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	"""Return metadata for a single Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource.

	Returns:
		GoldMetadataResponse: Resource id, name, description, project_id, and
			created_at. 404 if not found.
	"""
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


@gold_router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
async def delete_resource(
	resource_id: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> MessageResponse:
	"""Delete a Gold layer resource and all its associated versions.

	Args:
		resource_id (int): The id of the Gold resource to delete.

	Returns:
		MessageResponse: Confirmation message.
	"""
	await gold.metadata_interactor.delete(resource_id)
	return MessageResponse(message="Resource deleted successfully.")


@gold_router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateGoldResourceRequest,
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> GoldMetadataResponse:
	"""Update the name and/or description of a Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource to update.
		body (UpdateGoldResourceRequest): name (str), description (str | None).

	Returns:
		GoldMetadataResponse: Updated resource metadata. 404 if not found.
	"""
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
	"""List all versions (lineage entries) for a Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource.

	Returns:
		list[GoldLineageResponse]: Each entry contains id, resource_id,
			delta_version (int), from_resource_id (int, one of the source
			Silver resources), and created_at.
	"""
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


@gold_router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
	resources: Annotated[list[int], Query()],
) -> MessageResponse:
	"""Upload a Parquet file as a new version of a Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource to upload to.
		file (UploadFile): The Parquet file to upload.
		resources (list[int]): Query parameter (repeatable). The source Silver resource
			ids used to record lineage.

	Returns:
		MessageResponse: Confirmation message.
	"""
	content = await file.read()
	lf = pl.scan_parquet(content)
	await gold.upload(
		resource_id=resource_id,
		lf=lf,
		resources=resources,
		mode="overwrite",
	)
	return MessageResponse(message="File uploaded successfully.")


@gold_router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> StreamingResponse:
	"""Download a specific version of a Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource.
		version (int): The Delta Lake version number to download.

	Returns:
		StreamingResponse: The data as an Arrow IPC stream file (octet-stream).
	"""
	df = gold.get(resource_id=resource_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={resource_id}.parquet"},
	)


@gold_router.get(
	"/{resource_id}/versions/{version}/schema", status_code=status.HTTP_200_OK
)
async def get_schema(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	gold: Annotated[GoldLoader, Depends(gold_dep)],
) -> SchemaResponse:
	"""
	Return the column schema and up to the first 5 rows of data for a specific version
	of a Gold layer resource.

	Args:
		resource_id (int): The id of the Gold resource.
		version (int): The Delta Lake version number.

	Returns:
		SchemaResponse: data_schema (dict[str, str]) maps column names to lowercase
			type strings (e.g. 'int64', 'string', 'boolean'). data (dict[str, list])
			contains up to 5 rows keyed by column name.
	"""
	df = gold.get(resource_id=resource_id, version=version).head(5).collect()
	schema = {col: type(dtype).__name__.lower() for col, dtype in df.schema.items()}
	return SchemaResponse(data_schema=schema, data=df.to_dict(as_series=False))
