from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

from ..dependencies import BronzeLoader, bronze_dep, validate_file

bronze_router = APIRouter()


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
		raise ValueError("Source or version not found.")
	content = BytesIO(result.content)
	content.seek(0)
	name = result.name
	return StreamingResponse(
		content,
		media_type="application/octet-stream",
		headers={"Content-Disposition": f"attachment; filename={name}"},
		status_code=status.HTTP_200_OK,
	)
