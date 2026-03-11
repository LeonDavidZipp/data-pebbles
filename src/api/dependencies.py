from typing import Annotated

from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, POSTGRES_URI
from ..loaders import DeltaLoader
from ..postgres import BronzeSourceMetadataInteractor, BronzeSourceVersionInteractor


def validate_file(file: Annotated[UploadFile, File()]):
	if not file.filename:
		raise ValueError("Filename is required.")
	if not file.filename.endswith(".parquet"):
		raise ValueError("Only parquet files are allowed.")
	if not file.content_type == "application/octet-stream":
		raise ValueError("Invalid content type. Expected application/octet-stream.")
	return file


def validate_files(files: Annotated[list[UploadFile], File()]):
	for file in files:
		validate_file(file)
	return files


opts_ = {
	"endpoint_url": "http://minio:9000",
	"AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
	"AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
	"AWS_ALLOW_HTTP": True,
	"AWS_S3_ALLOW_UNSAFE_RENAME": True,
}

silver_loader_ = DeltaLoader("silver", storage_options=opts_)

gold_loader_ = DeltaLoader("gold", storage_options=opts_)

engine_ = create_async_engine(POSTGRES_URI)
session_maker_ = async_sessionmaker(engine_, expire_on_commit=False)

bronze_source_metadata_interactor_ = BronzeSourceMetadataInteractor(session_maker_)
bronze_source_version_interactor_ = BronzeSourceVersionInteractor(session_maker_)


def silver_dep() -> DeltaLoader:
	return silver_loader_


def gold_dep() -> DeltaLoader:
	return gold_loader_


