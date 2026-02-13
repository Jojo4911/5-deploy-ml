import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import the application, the database and the get_db function
from app import app, get_db
from database import Base

# 1. Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 2. Fixture for preparing the database before each test
@pytest.fixture()
def test_db():
    # Creating tables before test
    Base.metadata.create_all(bind=engine)
    yield
    # Destructing tables after test
    Base.metadata.drop_all(bind=engine)


# 3. Fixture for the test client
@pytest.fixture()
def client(test_db):

    # Function to replace the real database
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Telling FastAPI to replace get_db by override_get_db
    app.dependency_overrides[get_db] = override_get_db

    # Returning the test client
    with TestClient(app) as c:
        yield c
