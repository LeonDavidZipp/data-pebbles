from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from src.s3 import S3Interactor


@pytest.fixture
def s3_client() -> MagicMock:
	return MagicMock()


@pytest.fixture
def interactor(s3_client: MagicMock) -> S3Interactor:
	return S3Interactor("test-bucket", s3_client)


class TestUploadFile:
	def test_upload_returns_s3_key(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		key = interactor.upload_file(b"data", "report.csv")
		s3_client.put_object.assert_called_once()
		call_kwargs = s3_client.put_object.call_args.kwargs
		assert call_kwargs["Bucket"] == "test-bucket"
		assert call_kwargs["Body"] == b"data"
		assert key.endswith(".csv")

	def test_upload_preserves_extension(self, interactor: S3Interactor) -> None:
		key = interactor.upload_file(b"data", "file.parquet")
		assert key.endswith(".parquet")

	def test_upload_custom_content_type(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		interactor.upload_file(b"data", "f.csv", content_type="text/csv")
		call_kwargs = s3_client.put_object.call_args.kwargs
		assert call_kwargs["ContentType"] == "text/csv"

	def test_upload_raises_on_client_error(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		s3_client.put_object.side_effect = ClientError(
			{"Error": {"Code": "500", "Message": "fail"}}, "PutObject"
		)
		with pytest.raises(ClientError):
			interactor.upload_file(b"data", "f.csv")


class TestDownloadFile:
	def test_download_returns_bytes(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		body = MagicMock()
		body.read.return_value = b"file-content"
		s3_client.get_object.return_value = {"Body": body}

		result = interactor.download_file("some/key.csv")
		assert result == b"file-content"
		s3_client.get_object.assert_called_once_with(
			Bucket="test-bucket", Key="some/key.csv"
		)

	def test_download_returns_none_on_error(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		s3_client.get_object.side_effect = Exception("not found")
		result = interactor.download_file("missing/key.csv")
		assert result is None


class TestDeleteFile:
	def test_delete_calls_s3(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		interactor.delete_file("some/key.csv")
		s3_client.delete_object.assert_called_once_with(
			Bucket="test-bucket", Key="some/key.csv"
		)

	def test_delete_raises_on_client_error(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		s3_client.delete_object.side_effect = ClientError(
			{"Error": {"Code": "500", "Message": "fail"}}, "DeleteObject"
		)
		with pytest.raises(ClientError):
			interactor.delete_file("some/key.csv")


class TestFileExists:
	def test_exists_returns_true(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		assert interactor.file_exists("some/key.csv") is True
		s3_client.head_object.assert_called_once()

	def test_exists_returns_false_on_404(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		s3_client.head_object.side_effect = ClientError(
			{"Error": {"Code": "404", "Message": "Not Found"}}, "HeadObject"
		)
		assert interactor.file_exists("missing.csv") is False

	def test_exists_raises_on_other_error(
		self, interactor: S3Interactor, s3_client: MagicMock
	) -> None:
		s3_client.head_object.side_effect = ClientError(
			{"Error": {"Code": "500", "Message": "Server Error"}}, "HeadObject"
		)
		with pytest.raises(ClientError):
			interactor.file_exists("some.csv")


class TestGenerateS3Key:
	def test_key_contains_stem_and_extension(self, interactor: S3Interactor) -> None:
		key = interactor._generate_s3_key("report.csv")  # type: ignore
		assert key.startswith("bronze/report_")
		assert key.endswith(".csv")

	def test_key_unique_per_call(self, interactor: S3Interactor) -> None:
		key1 = interactor._generate_s3_key("f.csv")  # type: ignore
		key2 = interactor._generate_s3_key("f.csv")  # type: ignore
		assert key1 != key2
