from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies import silver_dep
from src.loaders import SilverLoader
from src.main import app
from src.postgres import SilverResourceMetadataRead, SilverVersionLineageRead
from test.conftest import NOW


@pytest.fixture
def mock_silver() -> MagicMock:
	loader = MagicMock(spec=SilverLoader)
	loader.metadata_interactor = AsyncMock()
	loader.get_metadata = AsyncMock()
	loader.get_lineage = AsyncMock()
	loader.get = MagicMock()
	loader.upload = AsyncMock()
	return loader


@pytest.fixture
def client(mock_silver: MagicMock) -> Generator[TestClient, None, None]:
	app.dependency_overrides[silver_dep] = lambda: mock_silver
	yield TestClient(app)  # type: ignore[misc]
	app.dependency_overrides.clear()


class TestListResources:
	def test_list_empty(self, client: TestClient, mock_silver: MagicMock) -> None:
		mock_silver.metadata_interactor.get_all.return_value = []
		resp = client.get("/silver/")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json() == []

	def test_list_returns_items(
		self, client: TestClient, mock_silver: MagicMock
	) -> None:
		meta = SilverResourceMetadataRead(
			id=1,
			name="silver_res",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_silver.metadata_interactor.get_all.return_value = [meta]
		resp = client.get("/silver/")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["name"] == "silver_res"


class TestCreateResource:
	def test_create_success(self, client: TestClient, mock_silver: MagicMock) -> None:
		meta = SilverResourceMetadataRead(
			id=3,
			name="new_silver",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_silver.metadata_interactor.create.return_value = meta
		resp = client.post("/silver/", json={"name": "new_silver", "project_id": 1})
		assert resp.status_code == status.HTTP_201_CREATED
		assert resp.json()["resource_id"] == 3


class TestGetResource:
	def test_get_found(self, client: TestClient, mock_silver: MagicMock) -> None:
		meta = SilverResourceMetadataRead(
			id=1,
			name="s",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_silver.get_metadata.return_value = meta
		resp = client.get("/silver/1")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["id"] == 1

	def test_get_not_found(self, client: TestClient, mock_silver: MagicMock) -> None:
		mock_silver.get_metadata.return_value = None
		resp = client.get("/silver/999")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteResource:
	def test_delete_success(self, client: TestClient, mock_silver: MagicMock) -> None:
		mock_silver.metadata_interactor.delete.return_value = 1
		resp = client.delete("/silver/1")
		assert resp.status_code == status.HTTP_200_OK


class TestUpdateResource:
	def test_update_found(self, client: TestClient, mock_silver: MagicMock) -> None:
		meta = SilverResourceMetadataRead(
			id=1,
			name="updated",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_silver.metadata_interactor.update.return_value = meta
		resp = client.patch("/silver/1", json={"name": "updated"})
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["name"] == "updated"

	def test_update_not_found(self, client: TestClient, mock_silver: MagicMock) -> None:
		mock_silver.metadata_interactor.update.return_value = None
		resp = client.patch("/silver/1", json={"name": "x"})
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestListVersions:
	def test_list_versions(self, client: TestClient, mock_silver: MagicMock) -> None:
		lineage = SilverVersionLineageRead(
			id=1, resource_id=1, delta_version=0, from_resource_id=5, created_at=NOW
		)
		mock_silver.get_lineage.return_value = [lineage]
		resp = client.get("/silver/1/versions")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["delta_version"] == 0
		assert data[0]["from_resource_id"] == 5
