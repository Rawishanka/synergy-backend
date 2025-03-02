import asyncio
from fastapi import FastAPI
from typing import Optional
from database import engine
from routers import ad_router, user_router, login_router  # Grouped imports for cleaner code
from models import ad_model
from database import Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app first
app = FastAPI()

# Function to create all tables asynchronously
async def create_all_tables():
    # Use an AsyncSession with engine.connect() to perform DDL operations
    async with engine.begin() as conn:  # Use begin() instead of connect()
        await conn.run_sync(Base.metadata.create_all)

# Register startup event
@app.on_event("startup")
async def on_startup():
    await create_all_tables()

# Add CORS middleware
origins = [
    "http://localhost:3000",  # React app running locally
    "https://yourfrontenddomain.com",  # Add other domains if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(login_router.router)
app.include_router(ad_router.router)
app.include_router(user_router.router)
