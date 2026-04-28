import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect():
    """Test GET / redirects to static index.html"""
    # Arrange - TestClient is initialized above

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200  # Serves the static file directly
    # Note: FastAPI TestClient may follow redirects or serve static files


def test_get_activities():
    """Test GET /activities returns all activities"""
    # Arrange - No special setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Based on current activities
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Basketball"  # Empty activity
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" == data["message"]


def test_signup_duplicate_email():
    """Test signup with duplicate email returns 400"""
    # Arrange
    activity_name = "Chess Club"  # Has participants
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_nonexistent_activity():
    """Test signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_remove_participant_success():
    """Test successful removal of a participant"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity_name}" == data["message"]


def test_remove_participant_not_found():
    """Test removing non-existent participant returns 404"""
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_remove_from_nonexistent_activity():
    """Test removing from non-existent activity returns 404"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()