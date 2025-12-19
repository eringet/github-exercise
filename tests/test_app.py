import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    # Use a known activity
    activity_name = list(client.get("/activities").json().keys())[0]
    test_email = "pytestuser@mergington.edu"

    # Ensure not already signed up
    client.post(f"/activities/{activity_name}/unregister?email={test_email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp_signup.status_code == 200
    assert "Signed up" in resp_signup.json()["message"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity_name}/signup?email={test_email}")
    assert resp_dup.status_code == 400

    # Unregister
    resp_unreg = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert resp_unreg.status_code == 200 or resp_unreg.status_code == 404
    # Unregister again should fail or be idempotent
    resp_unreg2 = client.post(f"/activities/{activity_name}/unregister?email={test_email}")
    assert resp_unreg2.status_code == 404 or resp_unreg2.status_code == 200
