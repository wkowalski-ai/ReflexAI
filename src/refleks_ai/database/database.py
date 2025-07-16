
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config("DATABASE_URL", default="postgresql://user:password@localhost/refleks_ai")

# Use connection pooler for Neon if available
if '.us-east-2' in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('.us-east-2', '-pooler.us-east-2')

# Create engine with connection pooling and proper configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency function to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
