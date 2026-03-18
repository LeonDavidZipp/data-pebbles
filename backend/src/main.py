from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP  # type: ignore[stub-not-found]

from .api import bronze_router, gold_router, projects_router, silver_router
from .api.exceptions import register_exception_handlers

app = FastAPI()
app = register_exception_handlers(app)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(
	projects_router,
	prefix="/projects",
	tags=["API Endpoints for managing projects"],
)
app.include_router(
	bronze_router,
	prefix="/bronze",
	tags=["API Endpoints for interacting with the Bronze layer"],
)
app.include_router(
	silver_router,
	prefix="/silver",
	tags=["API Endpoints for interacting with the Silver layer"],
)
app.include_router(
	gold_router,
	prefix="/gold",
	tags=["API Endpoints for interacting with the Gold layer"],
)

mcp = FastApiMCP(app)
mcp.mount_http()
