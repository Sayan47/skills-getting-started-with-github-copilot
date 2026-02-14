import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client):
    """Test that root redirect to static/index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "Basketball Team" in data
    assert "Programming Class" in data
    
    # Check activity structure
    tennis = data["Tennis Club"]
    assert "description" in tennis
    assert "schedule" in tennis
    assert "max_participants" in tennis
    assert "participants" in tennis
    assert isinstance(tennis["participants"], list)


def test_signup_for_activity(client):
    """Test signing up for an activity"""
    response = client.post("/activities/Tennis%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Tennis Club" in data["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert "newstudent@mergington.edu" in activities["Tennis Club"]["participants"]


def test_signup_duplicate_email(client):
    """Test that a student cannot sign up twice for the same activity"""
    # First signup
    response1 = client.post("/activities/Tennis%20Club/signup?email=test@mergington.edu")
    assert response1.status_code == 200
    
    # Second signup with same email
    response2 = client.post("/activities/Tennis%20Club/signup?email=test@mergington.edu")
    assert response2.status_code == 400
    
    data = response2.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/Nonexistent%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_full_activity(client):
    """Test that students can still sign up even if activity is at capacity"""
    # This test verifies the current behavior - no validation against max_participants
    response = client.post("/activities/Chess%20Club/signup?email=newcomer@mergington.edu")
    assert response.status_code == 200
    assert "Sign up successful" in response.json().get("message", "") or "Signed up" in response.json().get("message", "")


def test_unregister_from_activity(client):
    """Test unregistering a student from an activity"""
    # First, ensure participant is registered
    activities_before = client.get("/activities").json()
    assert "alex@mergington.edu" in activities_before["Tennis Club"]["participants"]
    
    # Unregister
    response = client.delete("/activities/Tennis%20Club/unregister?email=alex@mergington.edu")
    assert response.status_code == 200
    
    data = response.json()
    assert "Unregistered" in data["message"] or "unregistered" in data["message"].lower()
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    assert "alex@mergington.edu" not in activities_after["Tennis Club"]["participants"]


def test_unregister_not_registered_student(client):
    """Test unregistering a student who is not registered"""
    response = client.delete("/activities/Tennis%20Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


def test_unregister_nonexistent_activity(client):
    """Test unregistering from a non-existent activity"""
    response = client.delete("/activities/Nonexistent%20Club/unregister?email=student@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_participant_count_updates(client):
    """Test that participant counts are correctly updated"""
    activity_name = "Art%20Studio"
    
    # Get initial count
    initial = client.get("/activities").json()
    initial_count = len(initial["Art Studio"]["participants"])
    
    # Add participant
    client.post(f"/activities/{activity_name}/signup?email=newcomer1@mergington.edu")
    
    # Check count increased
    after_signup = client.get("/activities").json()
    assert len(after_signup["Art Studio"]["participants"]) == initial_count + 1
    
    # Remove participant
    client.delete(f"/activities/{activity_name}/unregister?email=newcomer1@mergington.edu")
    
    # Check count decreased back
    after_unregister = client.get("/activities").json()
    assert len(after_unregister["Art Studio"]["participants"]) == initial_count
