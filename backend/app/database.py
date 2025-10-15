import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root
load_dotenv()

# --- Database Connection URL ---
# Constructs the database URL from environment variables.
# It's crucial to have these variables set in your .env file.
# Example: postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please create a .env file.")

# --- SQLAlchemy Engine ---
# The engine is the central point of connection to the database.
# The 'connect_args' is not typically needed for PostgreSQL unless you have
# specific SSL requirements.
engine = create_engine(DATABASE_URL)

# --- Session Maker ---
# This factory will generate new Session objects when we need to
# interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Declarative Base ---
# All of our ORM models (like the CV model in models.py) will inherit
# from this class. It allows SQLAlchemy to map our Python classes to
# database tables.
Base = declarative_base()


# --- Dependency for API Endpoints ---
def get_db():
    """
    A FastAPI dependency that provides a database session for a single request.

    This function is a generator that will:
    1. Create a new database session from SessionLocal.
    2. 'yield' this session to the API endpoint function that needs it.
    3. Ensure the session is always closed after the request is finished,
       even if an error occurs, by using a try...finally block.
    
    This pattern prevents database connections from being left open.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
