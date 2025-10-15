import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from app.utils import env
from app.utils import setup_logging
from app.routes import version_router


logging.basicConfig(level=logging.INFO)

LOG_FILE = setup_logging(app_name="app", keep_days=30)

logger = logging.getLogger(__name__)
logger.info("Logger is ready.")

ORIGINS = env.get("ORIGINS") or []
HOST_SERVER = env.get("HOST_SERVER") or "127.0.0.1"
PORT_SERVER = int(env.get("PORT_SERVER") or 8000)

# Ganti startup_event dengan lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App startup: WORKLOG WEGE")
    yield  # lanjutkan lifecycle FastAPI tanpa shutdown event

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)
app.include_router(version_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_SERVER, port=PORT_SERVER)
