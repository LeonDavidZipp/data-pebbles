from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..dependencies import BronzeLoader, bronze_dep, validate_file
from ..exceptions import ResourceNotFoundError, VersionNotFoundError

bronze_router = APIRouter()


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


class VersionResponse(BaseModel):
	id: int
	resource_id: int
	version: int
	status: str
	s3_key: str
	created_at: str
	updated_at: str


class CreateResourceResponse(BaseModel):
	message: str
	resource_id: int


class MessageResponse(BaseModel):
	message: str


@bronze_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> list[MetadataResponse]:
	"""Return metadata for all Bronze layer resources across all projects.

	Returns:
		list[MetadataResponse]: All Bronze resources with id, name, description,
			project_id, and created_at.
	"""
	resources = await bronze.metadata_interactor.get_all()
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


@bronze_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(
	body: CreateResourceRequest,
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> CreateResourceResponse:
	"""Create a new Bronze layer resource.

	Args:
		body (CreateResourceRequest): name (str), project_id (int),
			description (str | None).

	Returns:
		CreateResourceResponse: Confirmation message and the new resource_id (int).
	"""
	res = await bronze.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return CreateResourceResponse(
		message="Resource created successfully.",
		resource_id=res.id,
	)


@bronze_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MetadataResponse:
	"""Return metadata for a single Bronze layer resource.

	Args:
		resource_id (int): The id of the Bronze resource.

	Returns:
		MetadataResponse: Resource id, name, description, project_id, and created_at.
			404 if not found.
	"""
	res = await bronze.get_metadata(resource_id)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return MetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@bronze_router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
async def delete_resource(
	resource_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MessageResponse:
	"""Delete a Bronze layer resource and all its associated versions.

	Args:
		resource_id (int): The id of the Bronze resource to delete.

	Returns:
		MessageResponse: Confirmation message.
	"""
	await bronze.metadata_interactor.delete(resource_id)
	return MessageResponse(message="Resource deleted successfully.")


@bronze_router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateResourceRequest,
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MetadataResponse:
	"""Update the name and/or description of a Bronze layer resource.

	Args:
		resource_id (int): The id of the Bronze resource to update.
		body (UpdateResourceRequest): name (str), description (str | None).

	Returns:
		MetadataResponse: Updated resource metadata. 404 if not found.
	"""
	res = await bronze.metadata_interactor.update(
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


@bronze_router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	resource_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> list[VersionResponse]:
	"""List all uploaded file versions for a Bronze layer resource.

	Args:
		resource_id (int): The id of the Bronze resource.

	Returns:
		list[VersionResponse]: Each entry contains id, resource_id, version (int),
			status ('active'/'inactive'), s3_key, created_at, and updated_at.
	"""
	versions = await bronze.version_interactor.get_by_resource(resource_id)
	return [
		VersionResponse(
			id=v.id,
			resource_id=v.resource_id,
			version=v.version,
			status=v.status,
			s3_key=v.s3_key,
			created_at=v.created_at.isoformat(),
			updated_at=v.updated_at.isoformat(),
		)
		for v in versions
	]


@bronze_router.patch(
	"/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK
)
async def activate_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MessageResponse:
	"""Set a specific version of a Bronze layer resource as the active version.

	Args:
		resource_id (int): The id of the Bronze resource.
		version (int): The version number to activate.

	Returns:
		MessageResponse: Confirmation message. 404 if the version does not exist.
	"""
	rows = await bronze.version_interactor.activate_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return MessageResponse(message="Version activated successfully.")


@bronze_router.delete(
	"/{resource_id}/versions/{version}",
	status_code=status.HTTP_200_OK,
)
async def delete_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MessageResponse:
	"""
	Delete a specific version of a Bronze layer resource, removing it from S3 and
	the database.

	Args:
		resource_id (int): The id of the Bronze resource.
		version (int): The version number to delete.

	Returns:
		MessageResponse: Confirmation message. 404 if the version does not exist.
	"""
	rows = await bronze.delete_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return MessageResponse(message="Version deleted successfully.")


@bronze_router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MessageResponse:
	"""
	Upload a new raw file as a new version of a Bronze layer resource. Stored in S3;
	a version record is created in the database.

	Args:
		resource_id (int): The id of the Bronze resource to upload to.
		file (UploadFile): The raw file to upload.

	Returns:
		MessageResponse: Confirmation message.
	"""
	content = await file.read()
	await bronze.upload(resource_id, content, file.filename)  # type: ignore
	return MessageResponse(message="File uploaded successfully.")


@bronze_router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
async def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> StreamingResponse:
	"""
	Download the raw file for a specific version of a Bronze layer resource.

	Args:
		resource_id (int): The id of the Bronze resource.
		version (int): The version number to download.

	Returns:
		StreamingResponse: The raw file as an octet-stream attachment. 404 if the file
			is not found.
	"""
	result = await bronze.download_version(resource_id, version)
	if result is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="File not found."
		)
	content = BytesIO(result.content)
	content.seek(0)
	name = result.name
	return StreamingResponse(
		content,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={name}"},
		status_code=status.HTTP_200_OK,
	)
