from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from polars.exceptions import ComputeError, PolarsError, SchemaError, ShapeError

from ..logger import logger

# ============================================================================
# Custom Exceptions
# ============================================================================


class MissingFileNameError(Exception):
	"""Raised when an uploaded file has no filename."""

	def __init__(self) -> None:
		super().__init__("Filename is required.")


class UnsupportedFileExtensionError(Exception):
	"""Raised when an uploaded file has a disallowed extension."""

	def __init__(self, ext: str, allowed: set[str]) -> None:
		allowed_str = ", ".join(sorted(allowed))
		super().__init__(f"Unsupported file extension '{ext}'. Allowed: {allowed_str}")


class UnsupportedContentTypeError(Exception):
	"""Raised when an uploaded file has a disallowed content type."""

	def __init__(self, content_type: str | None, allowed: set[str]) -> None:
		allowed_str = ", ".join(sorted(allowed))
		super().__init__(
			f"Unsupported content type '{content_type}'. Allowed: {allowed_str}"
		)


class ResourceNotFoundError(Exception):
	"""Raised when a resource metadata entry does not exist."""

	def __init__(self, resource_id: int) -> None:
		super().__init__(f"Resource {resource_id} not found.")


class VersionNotFoundError(Exception):
	"""Raised when a resource version or lineage entry does not exist."""

	def __init__(self, resource_id: int, version: int) -> None:
		super().__init__(f"Version {version} of resource {resource_id} not found.")


# ============================================================================
# Exception Handlers
# ============================================================================


async def missing_file_name_handler(
	request: Request, exc: MissingFileNameError
) -> JSONResponse:
	logger.info("MissingFileNameError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": "Filename is required."},
	)


async def unsupported_file_extension_handler(
	request: Request, exc: UnsupportedFileExtensionError
) -> JSONResponse:
	logger.info("UnsupportedFileExtensionError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": "Unsupported file type."},
	)


async def unsupported_content_type_handler(
	request: Request, exc: UnsupportedContentTypeError
) -> JSONResponse:
	logger.info("UnsupportedContentTypeError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": "Unsupported content type."},
	)


async def resource_not_found_handler(
	request: Request, exc: ResourceNotFoundError
) -> JSONResponse:
	logger.info("ResourceNotFoundError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_404_NOT_FOUND,
		content={"detail": "Resource not found."},
	)


async def version_not_found_handler(
	request: Request, exc: VersionNotFoundError
) -> JSONResponse:
	logger.info("VersionNotFoundError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_404_NOT_FOUND,
		content={"detail": "Version not found."},
	)


# ============================================================================
# Polars Exception Handlers
# ============================================================================


async def polars_schema_error_handler(
	request: Request, exc: SchemaError
) -> JSONResponse:
	logger.warning("Polars SchemaError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": "Data processing error."},
	)


async def polars_shape_error_handler(request: Request, exc: ShapeError) -> JSONResponse:
	logger.warning("Polars ShapeError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_400_BAD_REQUEST,
		content={"detail": "Data processing error."},
	)


async def polars_compute_error_handler(
	request: Request, exc: ComputeError
) -> JSONResponse:
	logger.warning("Polars ComputeError: %s", exc)
	return JSONResponse(
		status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
		content={"detail": "Data processing error."},
	)


async def polars_error_handler(request: Request, exc: PolarsError) -> JSONResponse:
	logger.error("Polars error: %s", exc, exc_info=True)
	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={"detail": "An unexpected error occurred."},
	)


async def fallback_exception_handler(request: Request, exc: Exception) -> JSONResponse:
	logger.error("Unhandled exception: %s", exc, exc_info=True)
	return JSONResponse(
		status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
		content={"detail": "An unexpected error occurred."},
	)


# ============================================================================
# Registration
# ============================================================================


def register_exception_handlers(app: FastAPI) -> FastAPI:
	# Custom exceptions
	app.add_exception_handler(MissingFileNameError, missing_file_name_handler)  # type: ignore[arg-type]
	app.add_exception_handler(
		UnsupportedFileExtensionError,
		unsupported_file_extension_handler,  # type: ignore[arg-type]
	)
	app.add_exception_handler(
		UnsupportedContentTypeError,
		unsupported_content_type_handler,  # type: ignore[arg-type]
	)
	app.add_exception_handler(ResourceNotFoundError, resource_not_found_handler)  # type: ignore[arg-type]
	app.add_exception_handler(VersionNotFoundError, version_not_found_handler)  # type: ignore[arg-type]

	# Polars exceptions
	app.add_exception_handler(SchemaError, polars_schema_error_handler)  # type: ignore[arg-type]
	app.add_exception_handler(ShapeError, polars_shape_error_handler)  # type: ignore[arg-type]
	app.add_exception_handler(ComputeError, polars_compute_error_handler)  # type: ignore[arg-type]
	app.add_exception_handler(PolarsError, polars_error_handler)  # type: ignore[arg-type]
	app.add_exception_handler(Exception, fallback_exception_handler)

	return app
