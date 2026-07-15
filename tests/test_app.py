import copy

from fastapi.testclient import TestClient

from src.app import app, activities

initial_activities = copy.deepcopy(activities)
client = TestClient(app)


def reset_activity_state():
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))


def test_get_activities():
    reset_activity_state()

    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_for_activity():
    reset_activity_state()

    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400():
    reset_activity_state()

    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant():
    reset_activity_state()

    email = "daniel@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_delete_nonexistent_participant_returns_400():
    reset_activity_state()

    email = "ghost@mergington.edu"
    response = client.delete("/activities/Chess Club/participants", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
