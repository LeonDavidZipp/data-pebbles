from typing import Annotated

import boto3
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, POSTGRES_URI, S3_URL
from ..loaders import BronzeLoader, DeltaLoader, GoldLoader, SilverLoader
from ..postgres import (
	BronzeResourceMetadataInteractor,
	BronzeResourceVersionInteractor,
	GoldResourceMetadataInteractor,
	GoldVersionLineageInteractor,
	SilverResourceMetadataInteractor,
	SilverVersionLineageInteractor,
)
from ..s3 import S3Interactor

ALLOWED_CONTENT_TYPES = {
	"text/csv",
	"application/json",
	"application/vnd.apache.parquet",
	"application/octet-stream",
	"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

ALLOWED_EXTENSIONS = {".csv", ".parquet", ".json", ".xlsx"}


def validate_file(file: Annotated[UploadFile, File()]):
	if not file.filename:
		raise ValueError("Filename is required.")
	ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
	if ext not in ALLOWED_EXTENSIONS:
		raise ValueError(
			f"Unsupported file extension '{ext}'. "
			+ f"Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
		)
	if file.content_type not in ALLOWED_CONTENT_TYPES:
		raise ValueError(
			f"Unsupported content type '{file.content_type}'. "
			+ f"Allowed: {', '.join(sorted(ALLOWED_CONTENT_TYPES))}"
		)
	return file


def validate_files(files: Annotated[list[UploadFile], File()]):
	for file in files:
		validate_file(file)
	return files


opts_ = {
	"endpoint_url": S3_URL,
	"AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
	"AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
	"AWS_ALLOW_HTTP": True,
	"AWS_S3_ALLOW_UNSAFE_RENAME": True,
}

engine_ = create_async_engine(POSTGRES_URI)
session_maker_ = async_sessionmaker(engine_, expire_on_commit=False)

s3_ = boto3.client(  # type: ignore
	"s3",
	endpoint_url=S3_URL,
	aws_access_key_id=AWS_ACCESS_KEY_ID,
	aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

bronze_resource_metadata_interactor_ = BronzeResourceMetadataInteractor(session_maker_)
bronze_resource_version_interactor_ = BronzeResourceVersionInteractor(session_maker_)
bronze_s3_interactor_ = S3Interactor("bronze", s3_)
bronze_loader_ = BronzeLoader(
	bronze_resource_metadata_interactor_,
	bronze_resource_version_interactor_,
	bronze_s3_interactor_,
)

silver_metadata_interactor_ = SilverResourceMetadataInteractor(session_maker_)
silver_lineage_interactor_ = SilverVersionLineageInteractor(session_maker_)
silver_delta_loader_ = DeltaLoader("silver", storage_options=opts_)
silver_loader_ = SilverLoader(
	silver_metadata_interactor_,
	silver_lineage_interactor_,
	silver_delta_loader_,
)

gold_metadata_interactor_ = GoldResourceMetadataInteractor(session_maker_)
gold_lineage_interactor_ = GoldVersionLineageInteractor(session_maker_)
gold_delta_loader_ = DeltaLoader("gold", storage_options=opts_)
gold_loader_ = GoldLoader(
	gold_metadata_interactor_,
	gold_lineage_interactor_,
	gold_delta_loader_,
)


def bronze_dep() -> BronzeLoader:
	return bronze_loader_


def silver_dep() -> SilverLoader:
	return silver_loader_


def gold_dep() -> GoldLoader:
	return gold_loader_
