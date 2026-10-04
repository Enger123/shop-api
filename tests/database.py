from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from main import app
from app.db.session import get_db
from sqlalchemy.pool import NullPool

test_db = create_engine(
    "postgresql+psycopg://postgres:Enger123@localhost:5432/shop_api_test",
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



