from typing import Annotated

import boto3
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from ..config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, POSTGRES_URI, S3_URL
from ..loaders import BronzeLoader, DeltaLoader
from ..postgres import (
	BronzeSourceMetadataInteractor,
	BronzeSourceVersionInteractor,
	GoldSourceMetadataInteractor,
	GoldVersionLineageInteractor,
	SilverSourceMetadataInteractor,
	SilverVersionLineageInteractor,
)
from ..s3 import S3Interactor


def validate_file(file: Annotated[UploadFile, File()]):
	if not file.filename:
		raise ValueError("Filename is required.")
	if not file.content_type == "application/octet-stream":
		raise ValueError("Invalid content type. Expected application/octet-stream.")
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

bronze_source_metadata_interactor_ = BronzeSourceMetadataInteractor(session_maker_)
bronze_source_version_interactor_ = BronzeSourceVersionInteractor(session_maker_)
bronze_s3_interactor_ = S3Interactor("bronze", s3_)
bronze_loader_ = BronzeLoader(
	bronze_source_metadata_interactor_,
	bronze_source_version_interactor_,
	bronze_s3_interactor_,
)

silver_loader_ = DeltaLoader("silver", storage_options=opts_)
silver_metadata_interactor_ = SilverSourceMetadataInteractor(session_maker_)
silver_lineage_interactor_ = SilverVersionLineageInteractor(session_maker_)

gold_loader_ = DeltaLoader("gold", storage_options=opts_)
gold_metadata_interactor_ = GoldSourceMetadataInteractor(session_maker_)
gold_lineage_interactor_ = GoldVersionLineageInteractor(session_maker_)


def bronze_dep() -> BronzeLoader:
	return bronze_loader_


def silver_dep() -> DeltaLoader:
	return silver_loader_


def gold_dep() -> DeltaLoader:
	return gold_loader_
