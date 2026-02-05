import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestActivitiesEndpoints:
    """Tests for the /activities endpoints"""

    def test_get_activities(self, client):
        """Test getting all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all activities are present
        assert "Basketball Team" in data
        assert "Soccer Club" in data
        assert "Chess Club" in data
        
        # Verify structure
        assert "description" in data["Basketball Team"]
        assert "schedule" in data["Basketball Team"]
        assert "max_participants" in data["Basketball Team"]
        assert "participants" in data["Basketball Team"]

    def test_get_activities_contains_initial_participants(self, client):
        """Test that activities contain initial participants"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Chess Club should have initial participants
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


class TestSignupEndpoint:
    """Tests for the signup endpoint"""

    def test_signup_for_activity(self, client):
        """Test successful signup for an activity"""
        response = client.post(
            "/activities/Basketball Team/signup?email=student@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up student@mergington.edu for Basketball Team" in data["message"]

    def test_signup_adds_participant(self, client):
        """Test that signup actually adds the participant"""
        client.post("/activities/Art Club/signup?email=new@mergington.edu")
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert "new@mergington.edu" in data["Art Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client):
        """Test signup for activity that doesn't exist"""
        response = client.post(
            "/activities/Nonexistent Club/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self, client):
        """Test that duplicate signups are rejected"""
        email = "student@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(f"/activities/Basketball Team/signup?email={email}")
        assert response1.status_code == 200
        
        # Second signup with same email should fail
        response2 = client.post(f"/activities/Basketball Team/signup?email={email}")
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]

    def test_signup_multiple_activities(self, client):
        """Test that a student can sign up for multiple activities"""
        email = "multi@mergington.edu"
        
        # Sign up for two activities
        response1 = client.post(f"/activities/Basketball Team/signup?email={email}")
        response2 = client.post(f"/activities/Soccer Club/signup?email={email}")
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both signups
        response = client.get("/activities")
        data = response.json()
        assert email in data["Basketball Team"]["participants"]
        assert email in data["Soccer Club"]["participants"]


class TestUnregisterEndpoint:
    """Tests for the unregister endpoint"""

    def test_unregister_from_activity(self, client):
        """Test successful unregistering from an activity"""
        email = "remove@mergington.edu"
        
        # First sign up
        client.post(f"/activities/Basketball Team/signup?email={email}")
        
        # Then unregister
        response = client.delete(
            f"/activities/Basketball Team/unregister?email={email}"
        )
        assert response.status_code == 200
        assert f"Unregistered {email} from Basketball Team" in response.json()["message"]

    def test_unregister_removes_participant(self, client):
        """Test that unregister actually removes the participant"""
        email = "remove@mergington.edu"
        
        # Sign up
        client.post(f"/activities/Art Club/signup?email={email}")
        
        # Verify signup
        response = client.get("/activities")
        assert email in response.json()["Art Club"]["participants"]
        
        # Unregister
        client.delete(f"/activities/Art Club/unregister?email={email}")
        
        # Verify removal
        response = client.get("/activities")
        assert email not in response.json()["Art Club"]["participants"]

    def test_unregister_from_nonexistent_activity(self, client):
        """Test unregister from activity that doesn't exist"""
        response = client.delete(
            "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404

    def test_unregister_not_signed_up(self, client):
        """Test unregister when student is not signed up"""
        response = client.delete(
            "/activities/Basketball Team/unregister?email=notsignup@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_from_activity_with_initial_participants(self, client):
        """Test unregistering from an activity with initial participants"""
        response = client.delete(
            "/activities/Chess Club/unregister?email=michael@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify removal
        response = client.get("/activities")
        data = response.json()
        assert "michael@mergington.edu" not in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


class TestIntegrationScenarios:
    """Integration tests for complex scenarios"""

    def test_signup_and_unregister_workflow(self, client):
        """Test complete signup and unregister workflow"""
        email = "workflow@mergington.edu"
        activity = "Programming Class"
        
        # Get initial state
        response = client.get("/activities")
        initial_count = len(response.json()[activity]["participants"])
        
        # Sign up
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify signup
        response = client.get("/activities")
        assert len(response.json()[activity]["participants"]) == initial_count + 1
        assert email in response.json()[activity]["participants"]
        
        # Unregister
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        assert response.status_code == 200
        
        # Verify unregister
        response = client.get("/activities")
        assert len(response.json()[activity]["participants"]) == initial_count
        assert email not in response.json()[activity]["participants"]

    def test_multiple_signups_and_unregisters(self, client):
        """Test multiple students signing up and unregistering"""
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        activity = "Soccer Club"
        
        # Sign up multiple students
        for email in emails:
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all signed up
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        for email in emails:
            assert email in participants
        
        # Unregister one student
        client.delete(f"/activities/{activity}/unregister?email={emails[1]}")
        
        # Verify only the unregistered one is removed
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        assert emails[0] in participants
        assert emails[1] not in participants
        assert emails[2] in participants
