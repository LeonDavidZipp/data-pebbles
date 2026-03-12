"""S3-compatible interactor for uploading and managing source files.

This module provides functionality for interacting with S3-compatible services
(AWS S3, MinIO, LocalStack, etc.) to store and retrieve source files.
"""

from datetime import datetime, timezone
from pathlib import PurePosixPath
from uuid import uuid4

from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client


class S3Interactor:
	"""Handles S3-compatible operations for source file management."""

	def __init__(
		self,
		bucket_name: str,
		s3_client: S3Client,
	):
		"""Initialize S3 interactor.

		Args:
			bucket_name: Name of the S3 bucket.
			s3_client: Initialized boto3 S3 client.
			endpoint_url: Optional endpoint URL for S3-compatible services.
		"""
		self.bucket_name = bucket_name
		self.s3_client = s3_client

	def upload_file(
		self,
		file_content: bytes,
		filename: str,
		content_type: str = "application/octet-stream",
	) -> str:
		"""Upload a file to S3.

		Args:
			file_content: File content as bytes.
			filename: Original filename (used to preserve extension).
			content_type: MIME type of the file.

		Returns:
			S3 key of the uploaded file.

		Raises:
			ClientError: If S3 upload fails.
		"""
		s3_key = self._generate_s3_key(filename)

		try:
			self.s3_client.put_object(
				Bucket=self.bucket_name,
				Key=s3_key,
				Body=file_content,
				ContentType=content_type,
			)
			return s3_key
		except ClientError as e:
			raise ClientError(
				e.response,
				"PutObject",
			) from e

	def download_file(self, s3_key: str) -> bytes | None:
		"""Download a file from S3.

		Args:
			s3_key: S3 object key.

		Returns:
			File content as bytes.

		Raises:
			ClientError: If S3 download fails.
		"""
		try:
			response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_key)
			return response["Body"].read()
		except Exception:
			return None

	def delete_file(self, s3_key: str) -> None:
		"""Delete a file from S3.

		Args:
			s3_key: S3 object key.

		Raises:
			ClientError: If S3 delete fails.
		"""
		try:
			self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
		except ClientError as e:
			raise ClientError(
				e.response,
				"DeleteObject",
			) from e

	def file_exists(self, s3_key: str) -> bool:
		"""Check if a file exists in S3.

		Args:
			s3_key: S3 object key.

		Returns:
			True if file exists, False otherwise.
		"""
		try:
			self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
			return True
		except ClientError as e:
			if e.response.get("Error", {}).get("Code") == "404":
				return False
			raise

	def _generate_s3_key(self, filename: str) -> str:
		"""Generate S3 object key with folder structure.

		Args:
			filename: Original filename (used to preserve extension).

		Returns:
			S3 object key.
		"""
		path = PurePosixPath(filename)
		name = path.stem
		ext = path.suffix
		ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
		return f"bronze/{name}_{ts}_{uuid4().hex}{ext}"
