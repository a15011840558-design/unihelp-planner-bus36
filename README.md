# UniHelp Planner

Flask + SQLite + Bootstrap prototype for Challenge 3: Student Help - A University Student Support Platform.

## Product scope

The prototype focuses on one clear opportunity: students often face academic pressure, fragmented support information, and late wellbeing intervention. UniHelp Planner gives students one place to:

- add coursework tasks and receive priority guidance;
- find relevant university support resources;
- complete a wellbeing check-in and receive a support recommendation.

## User stories implemented

| ID | User story | Acceptance criteria | Prototype evidence |
| --- | --- | --- | --- |
| S1 | As a student, I want to add coursework tasks with deadlines so that I can see what I should work on first. | Given I enter a task, deadline, estimated hours, and difficulty, when I submit the form, then the system shows the task in a prioritised list with advice. | `/tasks` |
| S2 | As a student, I want to choose the type of problem I am facing so that I can find relevant university support quickly. | Given I select a support category and urgency, when I search, then the system shows matching resources and contact routes. | `/resources` |
| S3 | As a student, I want to complete a wellbeing check-in so that I can receive basic guidance on what support action to take. | Given I submit mood, stress, and sleep values, when the check-in is saved, then the system stores it and displays a risk-level recommendation. | `/wellbeing` |

## Run locally

```bash
cd student_help_platform
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

## Run tests

```bash
cd student_help_platform
pytest -q
```

## Suggested video script

1. Start on the dashboard and state the product vision.
2. Story S1: add a coursework task, show priority advice, change status.
3. Story S2: select wellbeing or academic support, show recommended resources.
4. Story S3: submit a high-stress wellbeing check-in, show the support recommendation.
5. End by explaining that each flow demonstrates input, processing, output, and acceptance criteria.

## Portfolio notes

Suggested class diagram entities:

- `Student`
- `Task`
- `SupportResource`
- `ResourceQuery`
- `WellbeingCheckIn`
- `RecommendationService`

Suggested sequence diagrams:

- Add task and calculate priority recommendation.
- Submit wellbeing check-in and show support recommendation.

The app stores data in SQLite at `instance/student_help.sqlite` when run locally. The database is created automatically and seeded with support resources.
