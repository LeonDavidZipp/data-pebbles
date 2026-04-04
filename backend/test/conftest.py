from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.loaders import BronzeLoader, GoldLoader, SilverLoader
from src.postgres import (
	BronzeResourceMetadata,
	BronzeVersionLineage,
	GoldResourceMetadata,
	GoldVersionLineage,
	RawResourceMetadata,
	RawVersionLineage,
	SilverResourceMetadata,
	SilverVersionLineage,
	VersionStatus,
)

NOW = datetime.now(timezone.utc)


@pytest.fixture
def raw_metadata() -> RawResourceMetadata:
	return RawResourceMetadata(
		id=1,
		name="test_resource",
		description=None,
		project_id=1,
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def raw_version() -> RawVersionLineage:
	return RawVersionLineage(
		id=1,
		resource_id=1,
		version=1,
		status=VersionStatus.ACTIVE,
		s3_key="raw/test_20250101T000000_abc.csv",
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def bronze_metadata() -> BronzeResourceMetadata:
	return BronzeResourceMetadata(
		id=1,
		name="bronze_resource",
		description=None,
		project_id=1,
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def bronze_lineage() -> BronzeVersionLineage:
	return BronzeVersionLineage(
		id=1, resource_id=1, delta_version=0, from_resource_id=1, created_at=NOW
	)


@pytest.fixture
def silver_metadata() -> SilverResourceMetadata:
	return SilverResourceMetadata(
		id=1,
		name="silver_resource",
		description=None,
		project_id=1,
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def silver_lineage() -> SilverVersionLineage:
	return SilverVersionLineage(
		id=1, resource_id=1, delta_version=0, from_resource_id=1, created_at=NOW
	)


@pytest.fixture
def gold_metadata() -> GoldResourceMetadata:
	return GoldResourceMetadata(
		id=1,
		name="gold_resource",
		description=None,
		project_id=1,
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def gold_lineage() -> GoldVersionLineage:
	return GoldVersionLineage(
		id=1, resource_id=1, delta_version=0, from_resource_id=1, created_at=NOW
	)


@pytest.fixture
def mock_bronze_loader() -> MagicMock:
	loader = MagicMock(spec=BronzeLoader)
	loader.metadata_interactor = AsyncMock()
	loader.version_interactor = AsyncMock()
	loader.s3_interactor = MagicMock()
	loader.get_metadata = AsyncMock()
	loader.download_version = AsyncMock()
	loader.upload = AsyncMock()
	loader.delete_version = AsyncMock()
	return loader


@pytest.fixture
def mock_silver_loader() -> MagicMock:
	loader = MagicMock(spec=SilverLoader)
	loader.metadata_interactor = AsyncMock()
	loader.lineage_interactor = AsyncMock()
	loader.delta_loader = MagicMock()
	loader.get_metadata = AsyncMock()
	loader.get = MagicMock()
	loader.upload = AsyncMock()
	loader.get_lineage = AsyncMock()
	loader.get_version_lineage = AsyncMock()
	return loader


@pytest.fixture
def mock_gold_loader() -> MagicMock:
	loader = MagicMock(spec=GoldLoader)
	loader.metadata_interactor = AsyncMock()
	loader.lineage_interactor = AsyncMock()
	loader.delta_loader = MagicMock()
	loader.get_metadata = AsyncMock()
	loader.get = MagicMock()
	loader.upload = AsyncMock()
	loader.get_lineage = AsyncMock()
	loader.get_version_lineage = AsyncMock()
	return loader
