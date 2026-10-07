from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import app
from app.db.session import get_db
from sqlalchemy.pool import NullPool
import os

test_db = create_engine(
    os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+psycopg://postgres:Enger123@localhost:5432/shop_api_test"
    ),
    poolclass=NullPool
)

TestSession = sessionmaker(test_db)

def get_test_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_test_db



