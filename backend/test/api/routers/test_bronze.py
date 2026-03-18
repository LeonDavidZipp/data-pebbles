from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies import bronze_dep
from src.loaders import BronzeFileResult, BronzeLoader
from src.main import app
from src.postgres import (
	BronzeResourceMetadataRead,
	BronzeResourceVersionRead,
	VersionStatus,
)
from test.conftest import NOW


@pytest.fixture
def mock_bronze() -> MagicMock:
	loader = MagicMock(spec=BronzeLoader)
	loader.metadata_interactor = AsyncMock()
	loader.version_interactor = AsyncMock()
	loader.get_metadata = AsyncMock()
	loader.download_version = AsyncMock()
	loader.upload = AsyncMock()
	loader.delete_version = AsyncMock()
	return loader


@pytest.fixture
def client(mock_bronze: MagicMock) -> Generator[TestClient, None, None]:
	app.dependency_overrides[bronze_dep] = lambda: mock_bronze
	yield TestClient(app)  # type: ignore[misc]
	app.dependency_overrides.clear()


class TestListResources:
	def test_list_empty(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.metadata_interactor.get_all.return_value = []
		resp = client.get("/bronze/")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json() == []

	def test_list_returns_items(
		self, client: TestClient, mock_bronze: MagicMock
	) -> None:
		meta = BronzeResourceMetadataRead(
			id=1,
			name="res",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_bronze.metadata_interactor.get_all.return_value = [meta]
		resp = client.get("/bronze/")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["id"] == 1
		assert data[0]["name"] == "res"


class TestCreateResource:
	def test_create_success(self, client: TestClient, mock_bronze: MagicMock) -> None:
		meta = BronzeResourceMetadataRead(
			id=5,
			name="new",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_bronze.metadata_interactor.create.return_value = meta
		resp = client.post("/bronze/", json={"name": "new", "project_id": 1})
		assert resp.status_code == status.HTTP_201_CREATED
		assert resp.json()["resource_id"] == 5


class TestGetResource:
	def test_get_found(self, client: TestClient, mock_bronze: MagicMock) -> None:
		meta = BronzeResourceMetadataRead(
			id=1,
			name="res",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_bronze.get_metadata.return_value = meta
		resp = client.get("/bronze/1")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["id"] == 1

	def test_get_not_found(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.get_metadata.return_value = None
		resp = client.get("/bronze/999")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteResource:
	def test_delete_success(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.metadata_interactor.delete.return_value = 1
		resp = client.delete("/bronze/1")
		assert resp.status_code == status.HTTP_200_OK


class TestUpdateResource:
	def test_update_found(self, client: TestClient, mock_bronze: MagicMock) -> None:
		meta = BronzeResourceMetadataRead(
			id=1,
			name="updated",
			description=None,
			project_id=1,
			created_at=NOW,
			updated_at=NOW,
		)
		mock_bronze.metadata_interactor.update.return_value = meta
		resp = client.patch("/bronze/1", json={"name": "updated"})
		assert resp.status_code == status.HTTP_200_OK
		assert resp.json()["name"] == "updated"

	def test_update_not_found(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.metadata_interactor.update.return_value = None
		resp = client.patch("/bronze/1", json={"name": "x"})
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestListVersions:
	def test_list_versions(self, client: TestClient, mock_bronze: MagicMock) -> None:
		ver = BronzeResourceVersionRead(
			id=1,
			resource_id=1,
			version=1,
			status=VersionStatus.ACTIVE,
			s3_key="bronze/key.csv",
			created_at=NOW,
			updated_at=NOW,
		)
		mock_bronze.version_interactor.get_by_resource.return_value = [ver]
		resp = client.get("/bronze/1/versions")
		assert resp.status_code == status.HTTP_200_OK
		data = resp.json()
		assert len(data) == 1
		assert data[0]["version"] == 1


class TestActivateVersion:
	def test_activate_success(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.version_interactor.activate_version.return_value = 1
		resp = client.patch("/bronze/1/versions/1")
		assert resp.status_code == status.HTTP_200_OK

	def test_activate_not_found(
		self, client: TestClient, mock_bronze: MagicMock
	) -> None:
		mock_bronze.version_interactor.activate_version.return_value = 0
		resp = client.patch("/bronze/1/versions/99")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteVersion:
	def test_delete_version_success(
		self, client: TestClient, mock_bronze: MagicMock
	) -> None:
		mock_bronze.delete_version.return_value = 1
		resp = client.delete("/bronze/1/versions/1")
		assert resp.status_code == status.HTTP_200_OK

	def test_delete_version_not_found(
		self, client: TestClient, mock_bronze: MagicMock
	) -> None:
		mock_bronze.delete_version.return_value = 0
		resp = client.delete("/bronze/1/versions/99")
		assert resp.status_code == status.HTTP_404_NOT_FOUND


class TestDownloadVersion:
	def test_download_success(self, client: TestClient, mock_bronze: MagicMock) -> None:
		mock_bronze.download_version.return_value = BronzeFileResult(
			content=b"hello", name="file.csv"
		)
		resp = client.get("/bronze/1/versions/1")
		assert resp.status_code == status.HTTP_200_OK
		assert resp.content == b"hello"
		assert "file.csv" in resp.headers["content-disposition"]

	def test_download_not_found(
		self, client: TestClient, mock_bronze: MagicMock
	) -> None:
		mock_bronze.download_version.return_value = None
		resp = client.get("/bronze/1/versions/99")
		assert resp.status_code == status.HTTP_404_NOT_FOUND
