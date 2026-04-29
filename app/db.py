import sqlite3

from flask import current_app, g


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    module TEXT NOT NULL,
    deadline TEXT NOT NULL,
    estimated_hours REAL NOT NULL,
    difficulty INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'todo',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS support_resources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    contact TEXT NOT NULL,
    urgency TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS resource_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    urgency TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wellbeing_checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood INTEGER NOT NULL,
    stress INTEGER NOT NULL,
    sleep_hours REAL NOT NULL,
    notes TEXT,
    recommendation TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


SEED_RESOURCES = [
    (
        "academic",
        "Academic Tutor",
        "Discuss coursework pressure, extensions guidance, and study planning.",
        "Book through your department support page",
        "standard",
    ),
    (
        "academic",
        "Study Skills Service",
        "Get help with time management, academic writing, referencing, and revision.",
        "study-skills@university.example",
        "standard",
    ),
    (
        "wellbeing",
        "Student Wellbeing Team",
        "Confidential support for stress, low mood, anxiety, or personal difficulties.",
        "wellbeing@university.example",
        "standard",
    ),
    (
        "wellbeing",
        "Urgent Support Line",
        "Same-day guidance when a student feels unable to cope safely.",
        "Call campus security or local emergency services",
        "urgent",
    ),
    (
        "social",
        "Student Union Societies",
        "Find clubs, communities, volunteering, and peer activities.",
        "studentsunion.example/societies",
        "standard",
    ),
    (
        "social",
        "Peer Mentor Scheme",
        "Talk to trained student mentors about settling in and building confidence.",
        "peer-mentors@university.example",
        "standard",
    ),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    database = g.pop("db", None)
    if database is not None:
        database.close()


def init_db():
    database = get_db()
    database.executescript(SCHEMA)
    count = database.execute("SELECT COUNT(*) FROM support_resources").fetchone()[0]
    if count == 0:
        database.executemany(
            """
            INSERT INTO support_resources
                (category, name, description, contact, urgency)
            VALUES (?, ?, ?, ?, ?)
            """,
            SEED_RESOURCES,
        )
    database.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
