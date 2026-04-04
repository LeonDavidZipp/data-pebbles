from collections.abc import Generator
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies import projects_dep
from src.main import app
from src.postgres import ProjectMetadata

NOW = datetime.now(timezone.utc)


@pytest.fixture
def mock_interactor() -> AsyncMock:
	return AsyncMock()


@pytest.fixture
def client(mock_interactor: AsyncMock) -> Generator[TestClient, None, None]:
	app.dependency_overrides[projects_dep] = lambda: mock_interactor
	yield TestClient(app)  # type: ignore[misc]
	app.dependency_overrides.clear()


class TestListProjects:
	def test_list_empty(self, client: TestClient, mock_interactor: AsyncMock) -> None:
		mock_interactor.get_all.return_value = []
		resp = client.get("/projects/")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json() == []
		mock_interactor.get_all.assert_awaited_once()

	def test_list_returns_items(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		project = ProjectMetadata(
			id=1,
			name="My Project",
			description="A test project",
			created_at=NOW,
			updated_at=NOW,
		)
		mock_interactor.get_all.return_value = [project]
		resp = client.get("/projects/")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["name"] == "My Project"
		assert data[0]["description"] == "A test project"

	def test_list_multiple_items(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		projects = [
			ProjectMetadata(
				id=i,
				name=f"Project {i}",
				description=None,
				created_at=NOW,
				updated_at=NOW,
			)
			for i in range(1, 4)
		]
		mock_interactor.get_all.return_value = projects
		resp = client.get("/projects/")
		assert resp.status_code == status.HTTP_200_OK
		assert len(resp.json()) == 3


class TestCreateProject:
	def test_create_success(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		project = ProjectMetadata(
			id=5,
			name="New Project",
			description=None,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_interactor.create.return_value = project
		resp = client.post("/projects/", json={"name": "New Project"})
		assert resp.status_code == status.HTTP_201_CREATED
		assert resp.json()["project_id"] == 5
		mock_interactor.create.assert_awaited_once_with("New Project", None)

	def test_create_with_description(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		project = ProjectMetadata(
			id=6,
			name="Described",
			description="With desc",
			created_at=NOW,
			updated_at=NOW,
		)
		mock_interactor.create.return_value = project
		resp = client.post(
			"/projects/", json={"name": "Described", "description": "With desc"}
		)
		assert resp.status_code == status.HTTP_201_CREATED
		assert resp.json()["project_id"] == 6
		mock_interactor.create.assert_awaited_once_with("Described", "With desc")


class TestGetProject:
	def test_get_found(self, client: TestClient, mock_interactor: AsyncMock) -> None:
		project = ProjectMetadata(
			id=1,
			name="proj",
			description=None,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_interactor.get.return_value = project
		resp = client.get("/projects/1")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["id"] == 1
		mock_interactor.get.assert_awaited_once_with(1)

	def test_get_not_found(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		mock_interactor.get.return_value = None
		resp = client.get("/projects/999")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateProject:
	def test_update_found(self, client: TestClient, mock_interactor: AsyncMock) -> None:
		project = ProjectMetadata(
			id=1,
			name="updated",
			description="new desc",
			created_at=NOW,
			updated_at=NOW,
		)
		mock_interactor.update.return_value = project
		resp = client.patch(
			"/projects/1", json={"name": "updated", "description": "new desc"}
		)
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["name"] == "updated"
		assert resp.json()["description"] == "new desc"
		mock_interactor.update.assert_awaited_once_with(
			1, name="updated", description="new desc"
		)

	def test_update_not_found(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		mock_interactor.update.return_value = None
		resp = client.patch("/projects/1", json={"name": "x"})
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteProject:
	def test_delete_success(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		mock_interactor.delete.return_value = 1
		resp = client.delete("/projects/1")
		assert resp.status_code == status.HTTP_200_OK
		mock_interactor.delete.assert_awaited_once_with(1)

	def test_delete_response_message(
		self, client: TestClient, mock_interactor: AsyncMock
	) -> None:
		mock_interactor.delete.return_value = 1
		resp = client.delete("/projects/2")
		assert resp.json()["message"] == "Project deleted successfully."
