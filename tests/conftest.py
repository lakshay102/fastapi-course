from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.config import settings
from alembic import command

from app.oauth2 import create_access_token
from app.models import Post

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind = engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    # run our code before we run our test
    # command.upgrade("head")
    yield TestClient(app)
    # command.downgrade("base")
    # run our code after our test finishes


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)

    # assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "abc@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)

    # assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "This is title of test post",
            "content": "This is random content",
            "owner_id": test_user["id"],
        },
        {
            "title": "This is title of test post 2",
            "content": "This is random seond content",
            "owner_id": test_user["id"],
        },
        {
            "title": "This is post 3 title",
            "content": "This is third content",
            "owner_id": test_user["id"],
        },
        {
            "title": "A new title",
            "content": "This is random content",
            "owner_id": test_user2["id"],
        }
    ]

    def create_post_model(post):
        return Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    # session.add_all(
    #     [
    #         Post(
    #             title="This is title of test post",
    #             content="This is random content",
    #             owner_id=test_user["id"],
    #         ),
    #         Post(
    #             title="This is title of test post 2",
    #             content="This is random seond content",
    #             owner_id=test_user["id"],
    #         ),
    #         Post(
    #             title="This is post 3 title",
    #             content="This is third content",
    #             owner_id=test_user["id"],
    #         ),
    #     ]
    # )

    session.commit()

    posts = session.query(Post).all()
    return posts
