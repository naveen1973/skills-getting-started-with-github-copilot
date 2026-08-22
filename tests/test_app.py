"""API tests for the Mergington High School FastAPI backend."""

from fastapi.testclient import TestClient


class TestRootEndpoint:
    """Test the root endpoint behavior."""

    def test_root_redirect(self, client: TestClient):
        """Test that the root endpoint redirects to /static/index.html."""
        # Arrange: No setup needed for this simple test

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Test the activities listing endpoint."""

    def test_get_activities_returns_data(self, client: TestClient):
        """Test that GET /activities returns the full activity list."""
        # Arrange: No setup needed; reset_activities fixture handles state

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert data["Chess Club"]["max_participants"] == 12


class TestSignupEndpoint:
    """Test the activity signup endpoint."""

    def test_signup_success(self, client: TestClient):
        """Test successful signup for a new student to an activity."""
        # Arrange: Get baseline participant count
        response = client.get("/activities")
        baseline_count = len(response.json()["Chess Club"]["participants"])

        # Act
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert "newstudent@mergington.edu" in response.json()["message"]

        # Verify the participant was added
        response = client.get("/activities")
        assert len(response.json()["Chess Club"]["participants"]) == baseline_count + 1

    def test_signup_duplicate_email_returns_400(self, client: TestClient):
        """Test that signing up with a duplicate email returns a 400 error."""
        # Arrange: Use an existing participant
        duplicate_email = "michael@mergington.edu"

        # Act
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": duplicate_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_missing_activity_returns_404(self, client: TestClient):
        """Test that signing up for a non-existent activity returns a 404 error."""
        # Arrange: Use an invalid activity name

        # Act
        response = client.post(
            "/activities/Unknown Activity/signup",
            params={"email": "newstudent@mergington.edu"}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_signup_multiple_students_succeeds(self, client: TestClient):
        """Test that multiple different students can sign up for the same activity."""
        # Arrange: Two new students
        emails = ["alice@mergington.edu", "bob@mergington.edu"]
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()["Programming Class"]["participants"])

        # Act & Assert
        for email in emails:
            response = client.post(
                "/activities/Programming Class/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Verify both were added
        response = client.get("/activities")
        final_count = len(response.json()["Programming Class"]["participants"])
        assert final_count == initial_count + len(emails)
