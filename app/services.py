from datetime import date, datetime


def days_until(deadline):
    due = datetime.strptime(deadline, "%Y-%m-%d").date()
    return (due - date.today()).days


def task_priority(deadline, estimated_hours, difficulty):
    days_left = days_until(deadline)
    score = 0

    if days_left < 0:
        score += 6
    elif days_left <= 2:
        score += 5
    elif days_left <= 7:
        score += 3
    elif days_left <= 14:
        score += 1

    if estimated_hours >= 8:
        score += 3
    elif estimated_hours >= 4:
        score += 2
    else:
        score += 1

    score += max(1, min(int(difficulty), 5))

    if score >= 10:
        level = "High"
        advice = "Start today and split this into smaller work blocks."
    elif score >= 7:
        level = "Medium"
        advice = "Schedule a focused study block this week."
    else:
        level = "Low"
        advice = "Keep it on the plan and review after higher priority work."

    return {
        "score": score,
        "level": level,
        "days_left": days_left,
        "advice": advice,
    }


def wellbeing_recommendation(mood, stress, sleep_hours):
    mood = int(mood)
    stress = int(stress)
    sleep_hours = float(sleep_hours)

    if stress >= 8 or mood <= 2:
        return {
            "risk_level": "High",
            "message": (
                "Your check-in suggests high pressure. Contact the Student "
                "Wellbeing Team and consider speaking to your academic tutor."
            ),
        }

    if stress >= 6 or mood <= 4 or sleep_hours < 6:
        return {
            "risk_level": "Medium",
            "message": (
                "Your check-in suggests moderate pressure. Reduce today's task "
                "load, plan a break, and use wellbeing or study support if this continues."
            ),
        }

    return {
        "risk_level": "Low",
        "message": (
            "Your check-in looks stable. Keep using the planner and maintain "
            "regular breaks."
        ),
    }


def resource_explanation(category, urgency):
    labels = {
        "academic": "academic workload or study support",
        "wellbeing": "wellbeing and personal support",
        "social": "social connection and belonging",
    }
    urgency_text = "urgent" if urgency == "urgent" else "standard"
    return f"Showing {urgency_text} resources for {labels.get(category, category)}."
