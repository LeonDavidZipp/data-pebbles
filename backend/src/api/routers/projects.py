from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
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


class CreateProjectResponse(BaseModel):
	message: str
	project_id: int


class MessageResponse(BaseModel):
	message: str


@projects_router.get("/", status_code=status.HTTP_200_OK)
async def list_projects(
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> list[ProjectResponse]:
	"""
	Return all projects. Use project_id from the results to scope Bronze, Silver, and
	Gold resource operations.

	Returns:
		list[ProjectResponse]: All projects with id, name, description, and created_at.
	"""
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
) -> CreateProjectResponse:
	"""Create a new project.

	Args:
		body (CreateProjectRequest): name (str), description (str | None).

	Returns:
		CreateProjectResponse: Confirmation message and the new project_id (int).
	"""
	res = await interactor.create(body.name, body.description)
	return CreateProjectResponse(
		message="Project created successfully.",
		project_id=res.id,
	)


@projects_router.get("/{project_id}", status_code=status.HTTP_200_OK)
async def get_project(
	project_id: Annotated[int, Path()],
	interactor: Annotated[ProjectMetadataInteractor, Depends(projects_dep)],
) -> ProjectResponse:
	"""Return a single project by its id.

	Args:
		project_id (int): The id of the project.

	Returns:
		ProjectResponse: Project id, name, description, and created_at. 404 if
			not found.
	"""
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
	"""Update the name and/or description of a project.

	Args:
		project_id (int): The id of the project to update.
		body (UpdateProjectRequest): name (str | None), description (str | None).
			Both fields are optional.

	Returns:
		ProjectResponse: Updated project data. 404 if not found.
	"""
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
) -> MessageResponse:
	"""
	Delete a project by its id. Does not automatically delete associated Bronze,
	Silver, or Gold resources.

	Args:
		project_id (int): The id of the project to delete.

	Returns:
		MessageResponse: Confirmation message.
	"""
	await interactor.delete(project_id)
	return MessageResponse(message="Project deleted successfully.")
