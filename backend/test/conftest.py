from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.loaders import BronzeLoader, GoldLoader, SilverLoader
from src.postgres import (
	BronzeResourceMetadataRead,
	BronzeResourceVersionRead,
	GoldResourceMetadataRead,
	GoldVersionLineageRead,
	SilverResourceMetadataRead,
	SilverVersionLineageRead,
	VersionStatus,
)

NOW = datetime.now(timezone.utc)


@pytest.fixture
def bronze_metadata_read() -> BronzeResourceMetadataRead:
	return BronzeResourceMetadataRead(
		id=1, name="test_resource", created_at=NOW, updated_at=NOW
	)


@pytest.fixture
def bronze_version_read() -> BronzeResourceVersionRead:
	return BronzeResourceVersionRead(
		id=1,
		resource_id=1,
		version=1,
		status=VersionStatus.ACTIVE,
		s3_key="bronze/test_20250101T000000_abc.csv",
		created_at=NOW,
		updated_at=NOW,
	)


@pytest.fixture
def silver_metadata_read() -> SilverResourceMetadataRead:
	return SilverResourceMetadataRead(
		id=1, name="silver_resource", created_at=NOW, updated_at=NOW
	)


@pytest.fixture
def silver_lineage_read() -> SilverVersionLineageRead:
	return SilverVersionLineageRead(
		id=1, resource_id=1, delta_version=0, from_resource_id=1, created_at=NOW
	)


@pytest.fixture
def gold_metadata_read() -> GoldResourceMetadataRead:
	return GoldResourceMetadataRead(
		id=1, name="gold_resource", created_at=NOW, updated_at=NOW
	)


@pytest.fixture
def gold_lineage_read() -> GoldVersionLineageRead:
	return GoldVersionLineageRead(
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
