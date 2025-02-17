import asyncio
from fastapi import FastAPI
from typing import Optional
from database import engine
from routers import ad_router
from routers import user_router
from routers import login_router
from models import ad_model
from database import Base
from fastapi.middleware.cors import CORSMiddleware



#Base.metadata.create_all(bind=engine)

# Function to create all tables asynchronously
async def create_all_tables():
    # Use an AsyncSession with engine.begin() to perform DDL operations
    async with engine.connect() as conn:
        # Execute raw DDL statements to create all tables
        await conn.run_sync(Base.metadata.create_all)

# Lifespan event to handle startup and shutdown actions
async def lifespan(app: FastAPI):
    # Startup logic: Create tables
    await create_all_tables()
    
    # Yield control back to FastAPI
    yield

# FastAPI app with lifespan event handler
app = FastAPI(lifespan=lifespan)


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

app.include_router(login_router.router)
app.include_router(ad_router.router)
app.include_router(user_router.router)


