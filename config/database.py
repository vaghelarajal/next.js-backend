import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    import warnings
    warnings.warn(
        "DATABASE_URL environment variable is not set. "
        "Database operations will fail. Please set DATABASE_URL in .env file."
    )
    # Use a dummy URL for import purposes
    DATABASE_URL = "postgresql://user:pass@localhost/db"

# Simple, fast engine configuration
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={
        "connect_timeout": 5,
        "application_name": "fastapi_auth"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
