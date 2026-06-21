from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import Base, engine
from .routers import auth, homepage, activities, social, literature, finance, thesis, market


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create tables on startup (dev only; use Alembic in production)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Daniellife API",
    description="Personal website backend — JWT auth + CRUD + ITIS proxy",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_ORIGIN, "http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,       prefix="/api")
app.include_router(homepage.router,   prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(social.router,     prefix="/api")
app.include_router(literature.router, prefix="/api")
app.include_router(finance.router,    prefix="/api")
app.include_router(thesis.router,     prefix="/api")
app.include_router(market.router,     prefix="/api")


_uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
_uploads_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(_uploads_dir)), name="uploads")


@app.get("/api/health")
def health():
    return {"status": "ok"}
