from unittest.mock import AsyncMock, MagicMock

import pytest

from src.loaders import BronzeLoader, GoldLoader, RawFileResult, RawLoader, SilverLoader
from src.postgres import (
	BronzeResourceMetadata,
	BronzeVersionLineage,
	GoldResourceMetadata,
	GoldVersionLineage,
	RawResourceMetadata,
	RawVersionLineage,
	SilverResourceMetadata,
	SilverVersionLineage,
)


class TestRawLoader:
	@pytest.fixture
	def metadata_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def version_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def s3_interactor(self) -> MagicMock:
		return MagicMock()

	@pytest.fixture
	def loader(
		self,
		metadata_interactor: AsyncMock,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
	) -> RawLoader:
		return RawLoader(metadata_interactor, version_interactor, s3_interactor)

	@pytest.mark.asyncio
	async def test_get_metadata_found(
		self,
		loader: RawLoader,
		metadata_interactor: AsyncMock,
		raw_metadata: RawResourceMetadata,
	) -> None:
		metadata_interactor.get.return_value = raw_metadata
		result = await loader.get_metadata(1)
		assert result == raw_metadata
		metadata_interactor.get.assert_awaited_once_with(1)

	@pytest.mark.asyncio
	async def test_get_metadata_not_found(
		self, loader: RawLoader, metadata_interactor: AsyncMock
	) -> None:
		metadata_interactor.get.return_value = None
		result = await loader.get_metadata(999)
		assert result is None

	@pytest.mark.asyncio
	async def test_download_version_success(
		self,
		loader: RawLoader,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
		raw_version: RawVersionLineage,
	) -> None:
		version_interactor.get_version_by_resource.return_value = raw_version
		s3_interactor.download_file.return_value = b"csv-data"

		result = await loader.download_version(1, 1)
		assert result is not None
		assert isinstance(result, RawFileResult)
		assert result.content == b"csv-data"
		assert result.name.endswith(".csv")

	@pytest.mark.asyncio
	async def test_download_version_not_found(
		self, loader: RawLoader, version_interactor: AsyncMock
	) -> None:
		version_interactor.get_version_by_resource.return_value = None
		result = await loader.download_version(1, 1)
		assert result is None

	@pytest.mark.asyncio
	async def test_download_version_s3_returns_none(
		self,
		loader: RawLoader,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
		raw_version: RawVersionLineage,
	) -> None:
		version_interactor.get_version_by_resource.return_value = raw_version
		s3_interactor.download_file.return_value = None
		result = await loader.download_version(1, 1)
		assert result is None

	@pytest.mark.asyncio
	async def test_upload(
		self,
		loader: RawLoader,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
	) -> None:
		s3_interactor.upload_file.return_value = "raw/file_key.csv"
		version_interactor.create.return_value = 1

		result = await loader.upload(1, b"data", "file.csv", set_as_active=True)
		assert result == 1
		s3_interactor.upload_file.assert_called_once_with(b"data", "file.csv")
		version_interactor.create.assert_awaited_once_with(1, "raw/file_key.csv", True)

	@pytest.mark.asyncio
	async def test_delete_version_with_existing(
		self,
		loader: RawLoader,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
		raw_version: RawVersionLineage,
	) -> None:
		version_interactor.get_version_by_resource.return_value = raw_version
		version_interactor.delete_version_by_resource.return_value = 1

		result = await loader.delete_version(1, 1)
		assert result == 1
		s3_interactor.delete_file.assert_called_once_with(raw_version.s3_key)

	@pytest.mark.asyncio
	async def test_delete_version_not_found_skips_s3(
		self,
		loader: RawLoader,
		version_interactor: AsyncMock,
		s3_interactor: MagicMock,
	) -> None:
		version_interactor.get_version_by_resource.return_value = None
		version_interactor.delete_version_by_resource.return_value = 0

		result = await loader.delete_version(1, 99)
		assert result == 0
		s3_interactor.delete_file.assert_not_called()


class TestBronzeLoader:
	@pytest.fixture
	def metadata_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def lineage_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def delta_loader(self) -> MagicMock:
		return MagicMock()

	@pytest.fixture
	def loader(
		self,
		metadata_interactor: AsyncMock,
		lineage_interactor: AsyncMock,
		delta_loader: MagicMock,
	) -> BronzeLoader:
		return BronzeLoader(metadata_interactor, lineage_interactor, delta_loader)

	@pytest.mark.asyncio
	async def test_get_metadata_found(
		self,
		loader: BronzeLoader,
		metadata_interactor: AsyncMock,
		bronze_metadata: BronzeResourceMetadata,
	) -> None:
		metadata_interactor.get.return_value = bronze_metadata
		result = await loader.get_metadata(1)
		assert result == bronze_metadata

	@pytest.mark.asyncio
	async def test_get_metadata_not_found(
		self, loader: BronzeLoader, metadata_interactor: AsyncMock
	) -> None:
		metadata_interactor.get.return_value = None
		result = await loader.get_metadata(999)
		assert result is None

	def test_get_delegates_to_delta_loader(
		self, loader: BronzeLoader, delta_loader: MagicMock
	) -> None:
		loader.get(1, version=2)
		delta_loader.get.assert_called_once_with(table="1", version=2)

	def test_get_without_version(
		self, loader: BronzeLoader, delta_loader: MagicMock
	) -> None:
		loader.get(5)
		delta_loader.get.assert_called_once_with(table="5", version=None)

	@pytest.mark.asyncio
	async def test_upload(
		self,
		loader: BronzeLoader,
		delta_loader: MagicMock,
		lineage_interactor: AsyncMock,
		bronze_lineage: BronzeVersionLineage,
	) -> None:
		delta_loader.upload.return_value = 3
		lineage_interactor.create.return_value = bronze_lineage
		lf = MagicMock()

		result = await loader.upload(resource_id=1, lf=lf, from_resource_id=10)
		assert result == bronze_lineage
		delta_loader.upload.assert_called_once_with(table="1", lf=lf, mode="overwrite")
		lineage_interactor.create.assert_awaited_once_with(
			resource_id=1, delta_version=3, from_resource_id=10
		)

	@pytest.mark.asyncio
	async def test_get_lineage(
		self,
		loader: BronzeLoader,
		lineage_interactor: AsyncMock,
		bronze_lineage: BronzeVersionLineage,
	) -> None:
		lineage_interactor.get_by_resource.return_value = [bronze_lineage]
		result = await loader.get_lineage(1)
		assert result == [bronze_lineage]
		lineage_interactor.get_by_resource.assert_awaited_once_with(1)

	@pytest.mark.asyncio
	async def test_get_version_lineage(
		self,
		loader: BronzeLoader,
		lineage_interactor: AsyncMock,
		bronze_lineage: BronzeVersionLineage,
	) -> None:
		lineage_interactor.get_by_delta_version.return_value = bronze_lineage
		result = await loader.get_version_lineage(1, 0)
		assert result == bronze_lineage
		lineage_interactor.get_by_delta_version.assert_awaited_once_with(1, 0)


class TestSilverLoader:
	@pytest.fixture
	def metadata_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def lineage_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def delta_loader(self) -> MagicMock:
		return MagicMock()

	@pytest.fixture
	def loader(
		self,
		metadata_interactor: AsyncMock,
		lineage_interactor: AsyncMock,
		delta_loader: MagicMock,
	) -> SilverLoader:
		return SilverLoader(metadata_interactor, lineage_interactor, delta_loader)

	@pytest.mark.asyncio
	async def test_get_metadata_found(
		self,
		loader: SilverLoader,
		metadata_interactor: AsyncMock,
		silver_metadata: SilverResourceMetadata,
	) -> None:
		metadata_interactor.get.return_value = silver_metadata
		result = await loader.get_metadata(1)
		assert result == silver_metadata

	@pytest.mark.asyncio
	async def test_get_metadata_not_found(
		self, loader: SilverLoader, metadata_interactor: AsyncMock
	) -> None:
		metadata_interactor.get.return_value = None
		result = await loader.get_metadata(999)
		assert result is None

	def test_get_delegates_to_delta_loader(
		self, loader: SilverLoader, delta_loader: MagicMock
	) -> None:
		loader.get(1, version=2)
		delta_loader.get.assert_called_once_with(table="1", version=2)

	def test_get_without_version(
		self, loader: SilverLoader, delta_loader: MagicMock
	) -> None:
		loader.get(5)
		delta_loader.get.assert_called_once_with(table="5", version=None)

	@pytest.mark.asyncio
	async def test_upload(
		self,
		loader: SilverLoader,
		delta_loader: MagicMock,
		lineage_interactor: AsyncMock,
		silver_lineage: SilverVersionLineage,
	) -> None:
		delta_loader.upload.return_value = 3
		lineage_interactor.create.return_value = silver_lineage
		lf = MagicMock()

		result = await loader.upload(resource_id=1, lf=lf, from_resource_id=10)
		assert result == silver_lineage
		delta_loader.upload.assert_called_once_with(table="1", lf=lf, mode="overwrite")
		lineage_interactor.create.assert_awaited_once_with(
			resource_id=1, delta_version=3, from_resource_id=10
		)

	@pytest.mark.asyncio
	async def test_get_lineage(
		self,
		loader: SilverLoader,
		lineage_interactor: AsyncMock,
		silver_lineage: SilverVersionLineage,
	) -> None:
		lineage_interactor.get_by_resource.return_value = [silver_lineage]
		result = await loader.get_lineage(1)
		assert result == [silver_lineage]
		lineage_interactor.get_by_resource.assert_awaited_once_with(1)

	@pytest.mark.asyncio
	async def test_get_version_lineage(
		self,
		loader: SilverLoader,
		lineage_interactor: AsyncMock,
		silver_lineage: SilverVersionLineage,
	) -> None:
		lineage_interactor.get_by_delta_version.return_value = silver_lineage
		result = await loader.get_version_lineage(1, 0)
		assert result == silver_lineage
		lineage_interactor.get_by_delta_version.assert_awaited_once_with(1, 0)


class TestGoldLoader:
	@pytest.fixture
	def metadata_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def lineage_interactor(self) -> AsyncMock:
		return AsyncMock()

	@pytest.fixture
	def delta_loader(self) -> MagicMock:
		return MagicMock()

	@pytest.fixture
	def loader(
		self,
		metadata_interactor: AsyncMock,
		lineage_interactor: AsyncMock,
		delta_loader: MagicMock,
	) -> GoldLoader:
		return GoldLoader(metadata_interactor, lineage_interactor, delta_loader)

	@pytest.mark.asyncio
	async def test_get_metadata_found(
		self,
		loader: GoldLoader,
		metadata_interactor: AsyncMock,
		gold_metadata: GoldResourceMetadata,
	) -> None:
		metadata_interactor.get.return_value = gold_metadata
		result = await loader.get_metadata(1)
		assert result == gold_metadata

	@pytest.mark.asyncio
	async def test_get_metadata_not_found(
		self, loader: GoldLoader, metadata_interactor: AsyncMock
	) -> None:
		metadata_interactor.get.return_value = None
		result = await loader.get_metadata(999)
		assert result is None

	def test_get_delegates_to_delta_loader(
		self, loader: GoldLoader, delta_loader: MagicMock
	) -> None:
		loader.get(1, version=2)
		delta_loader.get.assert_called_once_with(table="1", version=2)

	@pytest.mark.asyncio
	async def test_upload(
		self,
		loader: GoldLoader,
		delta_loader: MagicMock,
		lineage_interactor: AsyncMock,
		gold_lineage: GoldVersionLineage,
	) -> None:
		delta_loader.upload.return_value = 5
		lineage_interactor.create_many.return_value = [gold_lineage]
		lf = MagicMock()

		result = await loader.upload(resource_id=1, lf=lf, resources=[10, 20])
		assert result == [gold_lineage]
		delta_loader.upload.assert_called_once_with(table="1", lf=lf, mode="overwrite")
		lineage_interactor.create_many.assert_awaited_once_with(
			resource_id=1, delta_version=5, resources=[10, 20]
		)

	@pytest.mark.asyncio
	async def test_get_lineage(
		self,
		loader: GoldLoader,
		lineage_interactor: AsyncMock,
		gold_lineage: GoldVersionLineage,
	) -> None:
		lineage_interactor.get_by_resource.return_value = [gold_lineage]
		result = await loader.get_lineage(1)
		assert result == [gold_lineage]

	@pytest.mark.asyncio
	async def test_get_version_lineage(
		self,
		loader: GoldLoader,
		lineage_interactor: AsyncMock,
		gold_lineage: GoldVersionLineage,
	) -> None:
		lineage_interactor.get_by_delta_version.return_value = [gold_lineage]
		result = await loader.get_version_lineage(1, 0)
		assert result == [gold_lineage]
		lineage_interactor.get_by_delta_version.assert_awaited_once_with(1, 0)
