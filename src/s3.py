"""S3-compatible interactor for uploading and managing source files.

This module provides functionality for interacting with S3-compatible services
(AWS S3, MinIO, LocalStack, etc.) to store and retrieve source files.
"""

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
		endpoint_url: str | None = None,
	):
		"""Initialize S3 interactor.

		Args:
			bucket_name: Name of the S3 bucket.
			s3_client: Initialized boto3 S3 client.
			endpoint_url: Optional endpoint URL for S3-compatible services.
		"""
		self.bucket_name = bucket_name
		self.s3_client = s3_client
		self.endpoint_url = endpoint_url

	def upload_file(
		self,
		file_content: bytes,
		session_id: int,
		filename: str = "",
		content_type: str = "application/octet-stream",
	) -> str:
		"""Upload a file to S3.

		Args:
			file_content: File content as bytes.
			session_id: Session ID for organization.
			filename: Original filename (used to preserve extension).
			content_type: MIME type of the file.

		Returns:
			S3 URL of the uploaded file.

		Raises:
			ClientError: If S3 upload fails.
		"""
		s3_key = self._generate_s3_key(session_id, filename)

		try:
			self.s3_client.put_object(
				Bucket=self.bucket_name,
				Key=s3_key,
				Body=file_content,
				ContentType=content_type,
			)
			return self._generate_s3_url(s3_key)
		except ClientError as e:
			raise ClientError(
				e.response,
				"PutObject",
			) from e

	def upload_file_from_path(
		self,
		filepath: str,
		session_id: int,
		content_type: str = "application/octet-stream",
	) -> str:
		"""Upload a file from local path to S3.

		Args:
			filepath: Path to local file.
			session_id: Session ID for organization.
			content_type: MIME type of the file.

		Returns:
			S3 URL of the uploaded file.

		Raises:
			ClientError: If S3 upload fails.
			FileNotFoundError: If local file not found.
		"""
		try:
			with open(filepath, "rb") as f:
				file_content = f.read()
			filename = PurePosixPath(filepath).name
			return self.upload_file(file_content, session_id, filename, content_type)
		except FileNotFoundError as e:
			raise FileNotFoundError(f"File not found: {filepath}") from e

	def download_file(self, s3_key: str) -> bytes:
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
		except ClientError as e:
			raise ClientError(
				e.response,
				"GetObject",
			) from e

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

	def _generate_s3_key(self, session_id: int, filename: str = "") -> str:
		"""Generate S3 object key with folder structure.

		Args:
			session_id: Session ID.
			filename: Original filename (used to preserve extension).

		Returns:
			S3 object key.
		"""
		ext = PurePosixPath(filename).suffix
		return f"sessions/{session_id}/sources/{uuid4().hex}{ext}"

	def _generate_s3_url(self, s3_key: str) -> str:
		"""Generate HTTP URL for S3 object.

		Args:
			s3_key: S3 object key.

		Returns:
			S3 HTTP URL.
		"""
		if self.endpoint_url:
			return f"{self.endpoint_url}/{self.bucket_name}/{s3_key}"
		return f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"

	def s3_key_from_url(self, url: str) -> str:
		"""Extract the S3 object key from a full S3 URL.

		Args:
			url: Full S3 URL.

		Returns:
			The object key portion of the URL.

		Raises:
			ValueError: If the URL format is not recognised.
		"""
		if self.endpoint_url:
			prefix = f"{self.endpoint_url}/{self.bucket_name}/"
		else:
			prefix = f"https://{self.bucket_name}.s3.amazonaws.com/"

		if not url.startswith(prefix):
			raise ValueError(f"URL does not match expected S3 prefix: {url}")
		return url[len(prefix) :]
