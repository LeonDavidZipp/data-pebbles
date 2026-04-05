from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP  # type: ignore[stub-not-found]

from .api import bronze_router, gold_router, projects_router, raw_router, silver_router
from .api.exceptions import register_exception_handlers

tags_metadata = [
	{
		"name": "projects",
		"description": "Manage projects that group related resources across the"
		+ " medallion architecture layers.",
	},
	{
		"name": "raw",
		"description": "Raw layer (medallion architecture). Ingest and version raw"
		+ " source files stored in S3.",
	},
	{
		"name": "bronze",
		"description": "Bronze layer (medallion architecture). Cleaned data derived"
		+ " from raw resources, stored as Delta Lake tables.",
	},
	{
		"name": "silver",
		"description": "Silver layer (medallion architecture). Refined data derived"
		+ " from bronze resources, stored as Delta Lake tables.",
	},
	{
		"name": "gold",
		"description": "Gold layer (medallion architecture). Aggregated/business-ready"
		+ " data derived from silver resources, stored as Delta Lake tables.",
	},
]

app = FastAPI(openapi_tags=tags_metadata)
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
	tags=["projects"],
)
app.include_router(
	raw_router,
	prefix="/raw",
	tags=["raw"],
)
app.include_router(
	bronze_router,
	prefix="/bronze",
	tags=["bronze"],
)
app.include_router(
	silver_router,
	prefix="/silver",
	tags=["silver"],
)
app.include_router(
	gold_router,
	prefix="/gold",
	tags=["gold"],
)

mcp = FastApiMCP(
	app,
	name="Layer API MCP",
	description="MCP server for the Data Pebbles API",
	describe_full_response_schema=True,
	describe_all_responses=True,
)
mcp.mount_http()
