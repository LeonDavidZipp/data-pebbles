from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ..dependencies import ProjectMetadataInteractor, projects_dep
from ..exceptions import ResourceNotFoundError

projects_router = APIRouter()


class CreateProjectRequest(BaseModel):
	name: str
	description: str | None = None


class UpdateProjectRequest(BaseModel):
	name: str | None = None
	description: str | None = None


class ProjectResponse(BaseModel):
	id: int
	name: str
	description: str | None
	created_at: str


@projects_router.get("/", status_code=status.HTTP_200_OK)
async def list_projects(
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> list[ProjectResponse]:
	projects = await interactor.get_all()
	return [
		ProjectResponse(
			id=p.id,
			name=p.name,
			description=p.description,
			created_at=p.created_at.isoformat(),
		)
		for p in projects
	]


@projects_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_project(
	body: CreateProjectRequest,
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> JSONResponse:
	res = await interactor.create(body.name, body.description)
	return JSONResponse(
		content={"message": "Project created successfully.", "project_id": res.id},
		status_code=status.HTTP_201_CREATED,
	)


@projects_router.get("/{project_id}", status_code=status.HTTP_200_OK)
async def get_project(
	project_id: Annotated[int, Path()],
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> ProjectResponse:
	res = await interactor.get(project_id)
	if res is None:
		raise ResourceNotFoundError(project_id)
	return ProjectResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		created_at=res.created_at.isoformat(),
	)


@projects_router.patch("/{project_id}", status_code=status.HTTP_200_OK)
async def update_project(
	project_id: Annotated[int, Path()],
	body: UpdateProjectRequest,
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> ProjectResponse:
	res = await interactor.update(
		project_id, name=body.name, description=body.description
	)
	if res is None:
		raise ResourceNotFoundError(project_id)
	return ProjectResponse(
		id=res.id,
		name=res.name,
		description=res.description,
		created_at=res.created_at.isoformat(),
	)


@projects_router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
	project_id: Annotated[int, Path()],
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> JSONResponse:
	await interactor.delete(project_id)
	return JSONResponse(
		content={"message": "Project deleted successfully."},
		status_code=status.HTTP_200_OK,
	)
