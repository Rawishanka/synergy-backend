from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = "postgresql+asyncpg://postgres:Rasindu@localhost:5432/testdb"
#DATABASE_URL = "postgresql://adscraperx_owner:1mYZWdiKO6tJ@ep-ancient-union-a5ivb14v.us-east-2.aws.neon.tech/adscraperx?sslmode=require"
#DATABASE_URL = "postgresql+asyncpg://adscraperx_owner:1mYZWdiKO6tJ@ep-ancient-union-a5ivb14v.us-east-2.aws.neon.tech/adscraperx"

# Create the database engine
engine = create_async_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Function to get a database session
async def get_db():
    async with SessionLocal() as session:
        yield session  # Async session
