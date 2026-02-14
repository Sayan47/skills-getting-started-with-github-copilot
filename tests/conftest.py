import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to their initial state before each test"""
    initial_activities = {
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball training and games",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "marcus@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Participate in theatrical productions and acting workshops",
            "schedule": "Wednesdays and Saturdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["sarah@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Tuesdays, 3:30 PM - 4:45 PM",
            "max_participants": 14,
            "participants": ["aisha@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design, build, and program robots for competitions",
            "schedule": "Thursdays and Saturdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ryan@mergington.edu", "sophia@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(copy.deepcopy(initial_activities))
    
    yield
