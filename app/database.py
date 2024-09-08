from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

# URL-encode the password if it contains special characters
encoded_password = quote_plus(settings.database_password)

# Construct the SQLAlchemy database URL using the encoded password
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:{encoded_password}@'
    f'{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
