from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_authentication():
    response = client.get("/", auth=("admin", "password"))
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

    response = client.get("/", auth=("invalid_user", "wrong_password"))
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}
