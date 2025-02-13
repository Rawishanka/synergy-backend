from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DATABASE_URL = "postgresql://postgres:Rasindu@localhost:5432/testdb"
DATABASE_URL="postgresql://adscraperx_owner:1mYZWdiKO6tJ@ep-ancient-union-a5ivb14v.us-east-2.aws.neon.tech/adscraperx?sslmode=require"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
