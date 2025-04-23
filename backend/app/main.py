from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import charts
from app.db.session import create_tables

app = FastAPI(
    title="Medical Chart Digitizer API",
    description="API for digitizing and structuring paper medical charts",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(charts.router, prefix=settings.API_V1_STR)

# Create database tables on startup if they don't exist
@app.on_event("startup")
async def startup_db_client():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Medical Chart Digitizer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
