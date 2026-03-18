from typing import Annotated

import polars as pl
from fastapi import APIRouter, Depends, Path, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..dependencies import SilverLoader, silver_dep, validate_file
from ..exceptions import ResourceNotFoundError

silver_router = APIRouter()


class CreateSilverResourceRequest(BaseModel):
	name: str
	project_id: int
	description: str | None = None


class UpdateSilverResourceRequest(BaseModel):
	name: str
	description: str | None = None


class SilverMetadataResponse(BaseModel):
	id: int
	name: str
	description: str | None
	project_id: int
	created_at: str


class SilverLineageResponse(BaseModel):
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


@silver_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> list[SilverMetadataResponse]:
	"""Return metadata for all Silver layer resources across all projects.

	Returns:
		list[SilverMetadataResponse]: All Silver resources with id, name, description,
			project_id, and created_at.
	"""
	resources = await silver.metadata_interactor.get_all()
	return [
		SilverMetadataResponse(
			id=s.id,
			name=s.name,
			description=s.description,
			project_id=s.project_id,
			created_at=s.created_at.isoformat(),
		)
		for s in resources
	]


@silver_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(
	body: CreateSilverResourceRequest,
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> CreateResourceResponse:
	"""Create a new Silver layer resource.

	Args:
		body (CreateSilverResourceRequest): name (str), project_id (int),
			description (str | None).

	Returns:
		CreateResourceResponse: Confirmation message and the new resource_id (int).
	"""
	res = await silver.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return CreateResourceResponse(
		message="Resource created successfully.",
		resource_id=res.id,
	)


@silver_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SilverMetadataResponse:
	"""Return metadata for a single Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource.

	Returns:
		SilverMetadataResponse: Resource id, name, description, project_id, and
			created_at. 404 if not found.
	"""
	res = await silver.get_metadata(resource_id)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return SilverMetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@silver_router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
async def delete_resource(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> MessageResponse:
	"""Delete a Silver layer resource and all its associated versions.

	Args:
		resource_id (int): The id of the Silver resource to delete.

	Returns:
		MessageResponse: Confirmation message.
	"""
	await silver.metadata_interactor.delete(resource_id)
	return MessageResponse(message="Resource deleted successfully.")


@silver_router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateSilverResourceRequest,
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SilverMetadataResponse:
	"""Update the name and/or description of a Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource to update.
		body (UpdateSilverResourceRequest): name (str), description (str | None).

	Returns:
		SilverMetadataResponse: Updated resource metadata. 404 if not found.
	"""
	res = await silver.metadata_interactor.update(
		resource_id, name=body.name, description=body.description
	)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return SilverMetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@silver_router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	resource_id: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> list[SilverLineageResponse]:
	"""List all versions (lineage entries) for a Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource.

	Returns:
		list[SilverLineageResponse]: Each entry contains id, resource_id, delta_version
			(int), from_resource_id (int, the source Bronze resource), and created_at.
	"""
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


@silver_router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
	from_resource_id: Annotated[int, Query()],
) -> MessageResponse:
	"""Upload a Parquet file as a new version of a Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource to upload to.
		file (UploadFile): The Parquet file to upload.
		from_resource_id (int): Query parameter. The source Bronze resource id used to
			record lineage.

	Returns:
		MessageResponse: Confirmation message.
	"""
	content = await file.read()
	lf = pl.scan_parquet(content)
	await silver.upload(
		resource_id=resource_id,
		lf=lf,
		from_resource_id=from_resource_id,
		mode="overwrite",
	)
	return MessageResponse(message="File uploaded successfully.")


@silver_router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> StreamingResponse:
	"""Download a specific version of a Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource.
		version (int): The Delta Lake version number to download.

	Returns:
		StreamingResponse: The data as an Arrow IPC stream file (octet-stream).
	"""
	df = silver.get(resource_id=resource_id, version=version).collect()
	buf = df.write_ipc_stream(None)
	buf.seek(0)
	return StreamingResponse(
		buf,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={resource_id}.parquet"},
	)


@silver_router.get(
	"/{resource_id}/versions/{version}/schema", status_code=status.HTTP_200_OK
)
async def get_schema(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	silver: Annotated[SilverLoader, Depends(silver_dep)],
) -> SchemaResponse:
	"""
	Return the column schema and up to the first 5 rows of data for a specific version
	of a Silver layer resource.

	Args:
		resource_id (int): The id of the Silver resource.
		version (int): The Delta Lake version number.

	Returns:
		SchemaResponse: data_schema (dict[str, str]) maps column names to lowercase type
			strings (e.g. 'int64', 'string', 'boolean'). data (dict[str, list]) contains
			up to 5 rows keyed by column name.
	"""
	df = silver.get(resource_id=resource_id, version=version).head(5).collect()
	schema = {col: type(dtype).__name__.lower() for col, dtype in df.schema.items()}
	return SchemaResponse(data_schema=schema, data=df.to_dict(as_series=False))
