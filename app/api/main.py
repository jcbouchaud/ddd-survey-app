from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.template import router as template_router

app = FastAPI(
    title="DDD API", description="A Domain-Driven Design API", version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(template_router, prefix="/templates")


@app.get("/")
async def root():
    return {"message": "Welcome to the DDD API"}
