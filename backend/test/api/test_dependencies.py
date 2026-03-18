from io import BytesIO

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from src.api.dependencies import validate_file, validate_files
from src.api.exceptions import (
	MissingFileNameError,
	UnsupportedContentTypeError,
	UnsupportedFileExtensionError,
)


def _upload(filename: str, content_type: str) -> UploadFile:
	headers = Headers({"content-type": content_type})
	return UploadFile(filename=filename, file=BytesIO(b""), headers=headers)


class TestValidateFile:
	def test_valid_csv(self) -> None:
		file = _upload("data.csv", "text/csv")
		result = validate_file(file)
		assert result is file

	def test_valid_parquet(self) -> None:
		file = _upload("data.parquet", "application/vnd.apache.parquet")
		result = validate_file(file)
		assert result is file

	def test_valid_json(self) -> None:
		file = _upload("data.json", "application/json")
		result = validate_file(file)
		assert result is file

	def test_valid_xlsx(self) -> None:
		file = _upload(
			"data.xlsx",
			"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
		)
		result = validate_file(file)
		assert result is file

	def test_missing_filename(self) -> None:
		file = _upload("", "text/csv")
		with pytest.raises(MissingFileNameError):
			validate_file(file)

	def test_no_filename(self) -> None:
		headers = Headers({"content-type": "text/csv"})
		file = UploadFile(file=BytesIO(b""), headers=headers)
		with pytest.raises(MissingFileNameError):
			validate_file(file)

	def test_unsupported_extension(self) -> None:
		file = _upload("data.txt", "text/plain")
		with pytest.raises(UnsupportedFileExtensionError):
			validate_file(file)

	def test_unsupported_content_type(self) -> None:
		file = _upload("data.csv", "text/plain")
		with pytest.raises(UnsupportedContentTypeError):
			validate_file(file)

	def test_no_extension(self) -> None:
		file = _upload("data", "text/csv")
		with pytest.raises(UnsupportedFileExtensionError):
			validate_file(file)


class TestValidateFiles:
	def test_all_valid(self) -> None:
		f1 = _upload("a.csv", "text/csv")
		f2 = _upload("b.json", "application/json")
		result = validate_files([f1, f2])
		assert result == [f1, f2]

	def test_one_invalid_raises(self) -> None:
		f1 = _upload("a.csv", "text/csv")
		f2 = _upload("b.txt", "text/plain")
		with pytest.raises(UnsupportedFileExtensionError):
			validate_files([f1, f2])
