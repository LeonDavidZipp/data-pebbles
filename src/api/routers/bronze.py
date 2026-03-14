from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from ..dependencies import BronzeLoader, bronze_dep, validate_file

bronze_router = APIRouter()


class CreateSourceRequest(BaseModel):
	name: str


@bronze_router.post("/")
async def create_source(
	body: CreateSourceRequest,
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> JSONResponse:
	res = await bronze.metadata_interactor.create(body.name)
	return JSONResponse(
		content={"message": "Source created successfully.", "source_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


class MetadataResponse(BaseModel):
	id: int
	name: str
	created_at: str


@bronze_router.get("/{source_id}/metadata", status_code=status.HTTP_200_OK)
async def get_source_metadata(
	source_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> MetadataResponse:
	res = await bronze.get_metadata(source_id)
	if res is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, detail="Source not found."
		)
	return MetadataResponse(
		id=res.id,
		name=res.name,
		created_at=res.created_at.isoformat(),
	)


@bronze_router.delete("/{source_id}")
async def delete_source(
	source_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> JSONResponse:
	await bronze.metadata_interactor.delete(source_id)
	return JSONResponse(
		content={"message": "Source deleted successfully."},
		status_code=status.HTTP_200_OK,
	)


@bronze_router.post("/upload/{source_id}")
async def upload(
	file: Annotated[UploadFile, Depends(validate_file)],
	source_id: Annotated[int, Path()],
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
) -> JSONResponse:
	content = await file.read()
	await bronze.upload(source_id, content, file.filename)  # type: ignore
	return JSONResponse(
		content={"message": "File uploaded successfully."},
		status_code=status.HTTP_201_CREATED,
	)


@bronze_router.get("/download/{source_id}")
async def download(
	bronze: Annotated[BronzeLoader, Depends(bronze_dep)],
	source_id: Annotated[int, Path()],
	version: Annotated[int | None, Query()] = None,
) -> StreamingResponse:
	result = await bronze.download_version(source_id, version)
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
