from fastapi import APIRouter

bronze_router = APIRouter()


@bronze_router.post("/upload")
def upload():
	pass


@bronze_router.get("/download")
def download():
	pass
