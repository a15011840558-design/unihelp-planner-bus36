from pathlib import Path

import pytest

from app import create_app
from app.db import get_db
from app.services import task_priority, wellbeing_recommendation


@pytest.fixture()
def app(tmp_path):
    database = tmp_path / "test.sqlite"
    return create_app(
        {
            "TESTING": True,
            "DATABASE": str(database),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


def test_dashboard_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"UniHelp Planner" in response.data
    assert b"Story S1" in response.data


def test_task_can_be_added_and_prioritised(client, app):
    response = client.post(
        "/tasks",
        data={
            "title": "Portfolio testing section",
            "module": "Building Useable Software",
            "deadline": "2026-04-30",
            "estimated_hours": "6",
            "difficulty": "4",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Portfolio testing section" in response.data
    assert b"priority" in response.data

    with app.app_context():
        row = get_db().execute("SELECT * FROM tasks").fetchone()
        assert row["title"] == "Portfolio testing section"


def test_task_status_update(client, app):
    with app.app_context():
        database = get_db()
        database.execute(
            """
            INSERT INTO tasks
                (title, module, deadline, estimated_hours, difficulty)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("Video script", "BUS", "2026-04-30", 2, 2),
        )
        database.commit()
        task_id = database.execute("SELECT id FROM tasks").fetchone()["id"]

    response = client.post(
        f"/tasks/{task_id}/status",
        data={"status": "done"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app.app_context():
        status = get_db().execute("SELECT status FROM tasks").fetchone()["status"]
        assert status == "done"


def test_resource_finder_returns_relevant_resources(client, app):
    response = client.post(
        "/resources",
        data={"category": "wellbeing", "urgency": "urgent"},
    )
    assert response.status_code == 200
    assert b"Student Wellbeing Team" in response.data
    assert b"Urgent Support Line" in response.data

    with app.app_context():
        count = get_db().execute("SELECT COUNT(*) FROM resource_queries").fetchone()[0]
        assert count == 1


def test_wellbeing_checkin_generates_recommendation(client, app):
    response = client.post(
        "/wellbeing",
        data={"mood": "2", "stress": "9", "sleep_hours": "4", "notes": "Overloaded"},
    )
    assert response.status_code == 200
    assert b"High pressure" in response.data
    assert b"Student Wellbeing Team" in response.data

    with app.app_context():
        row = get_db().execute("SELECT * FROM wellbeing_checkins").fetchone()
        assert row["risk_level"] == "High"


def test_service_priority_and_wellbeing_rules():
    priority = task_priority("2026-04-30", 8, 5)
    assert priority["level"] in {"High", "Medium", "Low"}
    assert priority["score"] >= 0

    recommendation = wellbeing_recommendation(1, 8, 5)
    assert recommendation["risk_level"] == "High"
