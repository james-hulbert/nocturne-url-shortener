import os
import pytest
from fastapi.testclient import TestClient

# 1. Point to a separate test database file so we don't mess up real data
os.environ["DB_FILE"] = "test_url_shortener.db"

from app.main import app
from app.database import init_db

# Initialize a test client that simulates user requests
client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    """Setup and teardown: Create a fresh test database before every test."""
    init_db()
    yield
    # Cleanup test database file after test finishes
    if os.path.exists("test_url_shortener.db"):
        os.remove("test_url_shortener.db")


def test_read_root():
    """Test our root health-check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Micro URL Shortener is running"}


def test_create_short_url():
    """Test creating a short code from a long URL."""
    response = client.post("/url", json={"target_url": "https://www.gothic-example.com"})
    assert response.status_code == 201
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://www.gothic-example.com"


def test_redirect_and_analytics():
    """Test full cycle: Create link, visit/redirect it, and verify click count increments."""
    # 1. Create the short link
    create_response = client.post("/url", json={"target_url": "https://www.gothic-example.com"})
    short_code = create_response.json()["short_code"]

    # 2. Check stats before clicking (should be 0)
    stats_before = client.get(f"/stats/{short_code}")
    assert stats_before.status_code == 200
    assert stats_before.json()["clicks"] == 0

    # 3. Simulate a user visiting the short link (follow_redirects=False so we catch the redirect status)
    redirect_response = client.get(f"/{short_code}", follow_redirects=False)
    assert redirect_response.status_code == 307  # Temporary redirect
    assert redirect_response.headers["location"] == "https://www.gothic-example.com"

    # 4. Check stats after clicking (should now be 1)
    stats_after = client.get(f"/stats/{short_code}")
    assert stats_after.status_code == 200
    assert stats_after.json()["clicks"] == 1


def test_url_not_found():
    """Test handling of invalid or non-existent short codes."""
    response = client.get("/doesnotexist99")
    assert response.status_code == 404
    assert response.json()["detail"] == "Short URL not found"