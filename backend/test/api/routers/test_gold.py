from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies import gold_dep
from src.loaders import GoldLoader
from src.main import app
from src.postgres import GoldResourceMetadataRead, GoldVersionLineageRead
from test.conftest import NOW


@pytest.fixture
def mock_gold() -> MagicMock:
	loader = MagicMock(spec=GoldLoader)
	loader.metadata_interactor = AsyncMock()
	loader.get_metadata = AsyncMock()
	loader.get_lineage = AsyncMock()
	loader.get = MagicMock()
	loader.upload = AsyncMock()
	return loader


@pytest.fixture
def client(mock_gold: MagicMock) -> TestClient:
	app.dependency_overrides[gold_dep] = lambda: mock_gold
	yield TestClient(app)  # type: ignore[misc]
	app.dependency_overrides.clear()


class TestListResources:
	def test_list_empty(self, client: TestClient, mock_gold: MagicMock) -> None:
		mock_gold.metadata_interactor.get_all.return_value = []
		resp = client.get("/gold/")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json() == []

	def test_list_returns_items(self, client: TestClient, mock_gold: MagicMock) -> None:
		meta = GoldResourceMetadataRead(
			id=1, name="gold_res", created_at=NOW, updated_at=NOW
		)
		mock_gold.metadata_interactor.get_all.return_value = [meta]
		resp = client.get("/gold/")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["name"] == "gold_res"


class TestCreateResource:
	def test_create_success(self, client: TestClient, mock_gold: MagicMock) -> None:
		meta = GoldResourceMetadataRead(
			id=5, name="new_gold", created_at=NOW, updated_at=NOW
		)
		mock_gold.metadata_interactor.create.return_value = meta
		resp = client.post("/gold/", json={"name": "new_gold"})
		assert resp.status_code == status.HTTP_201_CREATED
		assert resp.json()["resource_id"] == 5


class TestGetResource:
	def test_get_found(self, client: TestClient, mock_gold: MagicMock) -> None:
		meta = GoldResourceMetadataRead(id=1, name="g", created_at=NOW, updated_at=NOW)
		mock_gold.get_metadata.return_value = meta
		resp = client.get("/gold/1")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["id"] == 1

	def test_get_not_found(self, client: TestClient, mock_gold: MagicMock) -> None:
		mock_gold.get_metadata.return_value = None
		resp = client.get("/gold/999")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteResource:
	def test_delete_success(self, client: TestClient, mock_gold: MagicMock) -> None:
		mock_gold.metadata_interactor.delete.return_value = 1
		resp = client.delete("/gold/1")
		assert resp.status_code == status.HTTP_200_OK


class TestUpdateResource:
	def test_update_found(self, client: TestClient, mock_gold: MagicMock) -> None:
		meta = GoldResourceMetadataRead(
			id=1, name="updated", created_at=NOW, updated_at=NOW
		)
		mock_gold.metadata_interactor.update.return_value = meta
		resp = client.patch("/gold/1", json={"name": "updated"})
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["name"] == "updated"

	def test_update_not_found(self, client: TestClient, mock_gold: MagicMock) -> None:
		mock_gold.metadata_interactor.update.return_value = None
		resp = client.patch("/gold/1", json={"name": "x"})
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestListVersions:
	def test_list_versions(self, client: TestClient, mock_gold: MagicMock) -> None:
		lineage = GoldVersionLineageRead(
			id=1, resource_id=1, delta_version=0, from_resource_id=5, created_at=NOW
		)
		mock_gold.get_lineage.return_value = [lineage]
		resp = client.get("/gold/1/versions")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["delta_version"] == 0
		assert data[0]["from_resource_id"] == 5
