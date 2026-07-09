from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database.config import engine, Base
from app.routes import resume_routes
import os

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TalentIQ Resume Intelligence Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(resume_routes.router)

# Serve the static files from the React app
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Allow API routes to work
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
            
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend not built yet."}
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to the TalentIQ API. Frontend build not found."}
