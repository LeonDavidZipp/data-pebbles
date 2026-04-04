from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ..dependencies import RawLoader, raw_dep, validate_file
from ..exceptions import ResourceNotFoundError, VersionNotFoundError

raw_router = APIRouter()


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


@raw_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> list[MetadataResponse]:
	"""Return metadata for all Raw layer resources across all projects.

	Returns:
		list[MetadataResponse]: All Raw resources with id, name, description,
			project_id, and created_at.
	"""
	resources = await raw.metadata_interactor.get_all()
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


@raw_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_resource(
	body: CreateResourceRequest,
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> CreateResourceResponse:
	"""Create a new Raw layer resource.

	Args:
		body (CreateResourceRequest): name (str), project_id (int),
			description (str | None).

	Returns:
		CreateResourceResponse: Confirmation message and the new resource_id (int).
	"""
	res = await raw.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return CreateResourceResponse(
		message="Resource created successfully.",
		resource_id=res.id,
	)


@raw_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MetadataResponse:
	"""Return metadata for a single Raw layer resource.

	Args:
		resource_id (int): The id of the Raw resource.

	Returns:
		MetadataResponse: Resource id, name, description, project_id, and created_at.
			404 if not found.
	"""
	res = await raw.get_metadata(resource_id)
	if res is None:
		raise ResourceNotFoundError(resource_id)
	return MetadataResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		project_id=res.project_id,
		created_at=res.created_at.isoformat(),
	)


@raw_router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
async def delete_resource(
	resource_id: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MessageResponse:
	"""Delete a Raw layer resource and all its associated versions.

	Args:
		resource_id (int): The id of the Raw resource to delete.

	Returns:
		MessageResponse: Confirmation message.
	"""
	await raw.metadata_interactor.delete(resource_id)
	return MessageResponse(message="Resource deleted successfully.")


@raw_router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateResourceRequest,
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MetadataResponse:
	"""Update the name and/or description of a Raw layer resource.

	Args:
		resource_id (int): The id of the Raw resource to update.
		body (UpdateResourceRequest): name (str), description (str | None).

	Returns:
		MetadataResponse: Updated resource metadata. 404 if not found.
	"""
	res = await raw.metadata_interactor.update(
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


@raw_router.get("/{resource_id}/versions", status_code=status.HTTP_200_OK)
async def list_versions(
	resource_id: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> list[VersionResponse]:
	"""List all uploaded file versions for a Raw layer resource.

	Args:
		resource_id (int): The id of the Raw resource.

	Returns:
		list[VersionResponse]: Each entry contains id, resource_id, version (int),
			status ('active'/'inactive'), s3_key, created_at, and updated_at.
	"""
	versions = await raw.version_interactor.get_by_resource(resource_id)
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


@raw_router.patch("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
async def activate_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MessageResponse:
	"""Set a specific version of a Raw layer resource as the active version.

	Args:
		resource_id (int): The id of the Raw resource.
		version (int): The version number to activate.

	Returns:
		MessageResponse: Confirmation message. 404 if the version does not exist.
	"""
	rows = await raw.version_interactor.activate_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return MessageResponse(message="Version activated successfully.")


@raw_router.delete(
	"/{resource_id}/versions/{version}",
	status_code=status.HTTP_200_OK,
)
async def delete_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MessageResponse:
	"""
	Delete a specific version of a Raw layer resource, removing it from S3 and
	the database.

	Args:
		resource_id (int): The id of the Raw resource.
		version (int): The version number to delete.

	Returns:
		MessageResponse: Confirmation message. 404 if the version does not exist.
	"""
	rows = await raw.delete_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return MessageResponse(message="Version deleted successfully.")


@raw_router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> MessageResponse:
	"""
	Upload a new raw file as a new version of a Raw layer resource. Stored in S3;
	a version record is created in the database.

	Args:
		resource_id (int): The id of the Raw resource to upload to.
		file (UploadFile): The raw file to upload.

	Returns:
		MessageResponse: Confirmation message.
	"""
	content = await file.read()
	await raw.upload(resource_id, content, file.filename)  # type: ignore
	return MessageResponse(message="File uploaded successfully.")


@raw_router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
async def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	raw: Annotated[RawLoader, Depends(raw_dep)],
) -> StreamingResponse:
	"""
	Download the raw file for a specific version of a Raw layer resource.

	Args:
		resource_id (int): The id of the Raw resource.
		version (int): The version number to download.

	Returns:
		StreamingResponse: The raw file as an octet-stream attachment. 404 if the file
			is not found.
	"""
	result = await raw.download_version(resource_id, version)
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
