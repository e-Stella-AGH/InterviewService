import pytest

from main import app, change_for_tests
from starlette.testclient import TestClient

client = TestClient(app)


class TestMain:

    @pytest.fixture(scope="session", autouse=True)
    def set_up(self):
        change_for_tests()

    def test_happy(self):
        response = client.get("/interview/5/1")
        assert response.status_code == 200
        result = response.json()
        assert result["admin"] == "/interview/e1177e54-d903-4e91-a299-ddc56606785b/9ff2faff-dc3f-40b0-8c02-53a67750281e"
        assert result["job_seeker"] == "/interview/e1177e54-d903-4e91-a299-ddc56606785b"

    def test_older_interview(self):
        response = client.get("/interview/5/1?which=1")
        assert response.status_code == 200
        result = response.json()
        assert result["admin"] == "/interview/cbb6b884-888a-4ec4-9446-0a25ba2f2e9e/9ff2faff-dc3f-40b0-8c02-53a67750281e"
        assert result["job_seeker"] == "/interview/cbb6b884-888a-4ec4-9446-0a25ba2f2e9e"

    def test_hrpartner_not_exists(self):
        response = client.get("/interview/1/1")
        result = response.json()
        assert response.status_code == 404
        assert result['detail'] == "This hrpartner doesn't exists"

    def test_interviews_not_exists(self):
        response = client.get("/interview/5/5")
        result = response.json()
        assert response.status_code == 404
        assert result['detail'] == "This application doesn't have got interviews"

    def test_not_enough_interviews(self):
        response = client.get("/interview/5/1?which=5")
        result = response.json()
        assert response.status_code == 404
        assert result['detail'] == f"This application doesn't have got 6 interviews"

    def test_jobseeker_not_proper_uuid(self):
        response = client.get("/interview/jobseeker/zasdafasdfsacasdfsfadfasd")
        result = response.json()
        assert response.status_code == 404
        assert result['detail'] == "This string is not valid uuid"

    def test_jobseeker_interview_not_exists(self):
        uuid = "a1177e54-d903-4e91-a299-ddc56606785b"
        response = client.get(f"/interview/jobseeker/{uuid}")
        result = response.json()
        assert response.status_code == 404
        assert result['detail'] == f"Interview with id: {uuid} doesn't exist"

    def test_jobseeker_happy(self):
        response = client.get("/interview/jobseeker/e1177e54-d903-4e91-a299-ddc56606785b")
        assert response.status_code == 200
        result = response.json()
        assert result['first_name'] == "John"
        assert result['last_name'] == "Adams"
