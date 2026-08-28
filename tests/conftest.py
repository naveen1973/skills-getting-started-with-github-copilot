"""Shared test fixtures and configuration for the FastAPI backend tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a known state before and after each test."""
    original_activities = {
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
        },
        "Soccer Team": {
            "description": "Practice and compete in soccer matches against other schools",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Develop basketball skills and play friendly matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and other visual arts techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "amelia@mergington.edu"]
        },
        "Drama Society": {
            "description": "Rehearse and perform plays and theatrical productions",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["ethan@mergington.edu", "charlotte@mergington.edu"]
        },
        "Debate Team": {
            "description": "Research topics and compete in debate tournaments",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["james@mergington.edu", "harper@mergington.edu"]
        },
        "Math Olympiad": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["benjamin@mergington.edu", "evelyn@mergington.edu"]
        }
    }
    
    # Clear and reset activities before the test
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after the test
    activities.clear()
    activities.update(original_activities)
