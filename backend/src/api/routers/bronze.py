from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
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


@bronze_router.get("/", status_code=status.HTTP_200_OK)
async def list_resources(
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> list[MetadataResponse]:
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
) -> JSONResponse:
	res = await bronze.metadata_interactor.create(
		body.name, body.project_id, body.description
	)
	return JSONResponse(
		content={"message": "Resource created successfully.", "resource_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@bronze_router.get("/{resource_id}", status_code=status.HTTP_200_OK)
async def get_resource(
	resource_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MetadataResponse:
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
) -> JSONResponse:
	await bronze.metadata_interactor.delete(resource_id)
	return JSONResponse(
		content={"message": "Resource deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@bronze_router.patch("/{resource_id}", status_code=status.HTTP_200_OK)
async def update_resource(
	resource_id: Annotated[int, Path()],
	body: UpdateResourceRequest,
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MetadataResponse:
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
) -> JSONResponse:
	rows = await bronze.version_interactor.activate_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return JSONResponse(
		content={"message": "Version activated successfully."},
		status_code=status.HTTP_200_OK,
	)


@bronze_router.delete(
	"/{resource_id}/versions/{version}",
	status_code=status.HTTP_200_OK,
)
async def delete_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> JSONResponse:
	rows = await bronze.delete_version(resource_id, version)
	if rows == 0:
		raise VersionNotFoundError(resource_id, version)
	return JSONResponse(
		content={"message": "Version deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@bronze_router.post("/{resource_id}/versions", status_code=status.HTTP_201_CREATED)
async def upload_version(
	resource_id: Annotated[int, Path()],
	file: Annotated[UploadFile, Depends(validate_file)],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> JSONResponse:
	content = await file.read()
	await bronze.upload(resource_id, content, file.filename)  # type: ignore
	return JSONResponse(
		content={"message": "File uploaded successfully."},
		status_code=status.HTTP_201_CREATED,
	)


@bronze_router.get("/{resource_id}/versions/{version}", status_code=status.HTTP_200_OK)
async def download_version(
	resource_id: Annotated[int, Path()],
	version: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> StreamingResponse:
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
