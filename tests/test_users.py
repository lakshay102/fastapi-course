import jwt
import pytest
from app.schemas import Token, UserOut
# from .database import client,session
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     # print(res.json().get('message'))
#     assert res.status_code == 200
#     assert res.json().get("message") == "Hello world"

def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"}
    )

    new_user = UserOut(**res.json())
    # print(res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']} )
    login_res = Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ("hello@gmail.com", "password", 403),
    (None, 'password', 403),
    ("hello@gmail.com", None, 403),
    ("user@gmail.com", "password123", 403),
    ("wrongemail@gmail.com", "password123", 403),
    ("hello123@gmail.com", "wrongPassword", 403),
    ("wrongemail@gmail.com", "wrongPassword", 403)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data= {"username" : email, "password" : password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid credentials'