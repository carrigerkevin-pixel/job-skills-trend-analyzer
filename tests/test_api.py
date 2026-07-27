import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "api"))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """The root endpoint should return a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_top_skills():
    """The top skills endpoint should return a list of skill objects."""
    response = client.get("/skills/top")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    # If there's data, check the shape of the first item
    if len(data) > 0:
        assert "skill" in data[0]
        assert "count" in data[0]


def test_get_top_skills_respects_limit():
    """The limit query parameter should control how many results come back."""
    response = client.get("/skills/top?limit=3")
    assert response.status_code == 200
    assert len(response.json()) <= 3


def test_get_categories():
    """The categories endpoint should return a list of category names."""
    response = client.get("/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_skills_by_valid_category():
    """A valid category should return skill data without error."""
    categories_response = client.get("/categories")
    categories = categories_response.json()

    if len(categories) > 0:
        first_category = categories[0]
        response = client.get(f"/skills/by-category/{first_category}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_get_skills_by_invalid_category():
    """An invalid category should return a 404, not crash or return empty data silently."""
    response = client.get("/skills/by-category/not-a-real-category")
    assert response.status_code == 404