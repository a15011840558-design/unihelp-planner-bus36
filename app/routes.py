from flask import Blueprint, flash, redirect, render_template, request, url_for

from .db import get_db
from .services import resource_explanation, task_priority, wellbeing_recommendation


bp = Blueprint("main", __name__)


@bp.route("/favicon.ico")
def favicon():
    return "", 204


@bp.route("/")
def index():
    database = get_db()
    tasks = database.execute(
        "SELECT * FROM tasks ORDER BY deadline ASC, difficulty DESC LIMIT 5"
    ).fetchall()
    checkins = database.execute(
        "SELECT * FROM wellbeing_checkins ORDER BY created_at DESC LIMIT 3"
    ).fetchall()
    return render_template("index.html", tasks=tasks, checkins=checkins)


@bp.route("/tasks", methods=("GET", "POST"))
def tasks():
    database = get_db()
    if request.method == "POST":
        title = request.form["title"].strip()
        module = request.form["module"].strip()
        deadline = request.form["deadline"]
        estimated_hours = float(request.form["estimated_hours"])
        difficulty = int(request.form["difficulty"])

        if not title or not module:
            flash("Task title and module are required.", "danger")
        else:
            database.execute(
                """
                INSERT INTO tasks
                    (title, module, deadline, estimated_hours, difficulty)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, module, deadline, estimated_hours, difficulty),
            )
            database.commit()
            flash("Task added and prioritised.", "success")
            return redirect(url_for("main.tasks"))

    rows = database.execute("SELECT * FROM tasks ORDER BY deadline ASC").fetchall()
    enriched_tasks = [
        {
            **dict(row),
            "priority": task_priority(
                row["deadline"], row["estimated_hours"], row["difficulty"]
            ),
        }
        for row in rows
    ]
    enriched_tasks.sort(key=lambda item: item["priority"]["score"], reverse=True)
    return render_template("tasks.html", tasks=enriched_tasks)


@bp.post("/tasks/<int:task_id>/status")
def update_task_status(task_id):
    status = request.form["status"]
    if status not in {"todo", "in_progress", "done"}:
        flash("Unknown task status.", "danger")
        return redirect(url_for("main.tasks"))

    database = get_db()
    database.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    database.commit()
    flash("Task status updated.", "success")
    return redirect(url_for("main.tasks"))


@bp.route("/resources", methods=("GET", "POST"))
def resources():
    database = get_db()
    selected_category = request.form.get("category", "academic")
    selected_urgency = request.form.get("urgency", "standard")

    if request.method == "POST":
        database.execute(
            "INSERT INTO resource_queries (category, urgency) VALUES (?, ?)",
            (selected_category, selected_urgency),
        )
        database.commit()

    if selected_urgency == "urgent":
        rows = database.execute(
            """
            SELECT * FROM support_resources
            WHERE category = ? OR urgency = 'urgent'
            ORDER BY urgency DESC, name ASC
            """,
            (selected_category,),
        ).fetchall()
    else:
        rows = database.execute(
            """
            SELECT * FROM support_resources
            WHERE category = ? AND urgency = 'standard'
            ORDER BY name ASC
            """,
            (selected_category,),
        ).fetchall()

    return render_template(
        "resources.html",
        resources=rows,
        selected_category=selected_category,
        selected_urgency=selected_urgency,
        explanation=resource_explanation(selected_category, selected_urgency),
    )


@bp.route("/wellbeing", methods=("GET", "POST"))
def wellbeing():
    recommendation = None
    database = get_db()

    if request.method == "POST":
        mood = int(request.form["mood"])
        stress = int(request.form["stress"])
        sleep_hours = float(request.form["sleep_hours"])
        notes = request.form.get("notes", "").strip()
        recommendation = wellbeing_recommendation(mood, stress, sleep_hours)
        database.execute(
            """
            INSERT INTO wellbeing_checkins
                (mood, stress, sleep_hours, notes, recommendation, risk_level)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                mood,
                stress,
                sleep_hours,
                notes,
                recommendation["message"],
                recommendation["risk_level"],
            ),
        )
        database.commit()
        flash("Check-in saved and recommendation generated.", "success")

    checkins = database.execute(
        "SELECT * FROM wellbeing_checkins ORDER BY created_at DESC LIMIT 8"
    ).fetchall()
    return render_template(
        "wellbeing.html", recommendation=recommendation, checkins=checkins
    )
