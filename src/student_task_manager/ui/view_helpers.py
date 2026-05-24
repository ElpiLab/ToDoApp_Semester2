from datetime import date

from student_task_manager.domain.models import Task


def status_display_label(status_value: str) -> str:
    if status_value in ("pending", "open"):
        return "To do"
    return status_value.replace("_", " ").title()


TASK_STATUS_FILTER_LABELS = {
    "all": "All",
    "to_do": status_display_label("pending"),
    "in_progress": status_display_label("in_progress"),
    "done": status_display_label("done"),
}

TASK_CATEGORY_OPTIONS = [
    "Project",
    "Exam",
    "Assignment",
    "Research",
    "Reading",
    "Personal",
    "Other",
]


def task_matches_status_filter(task: Task, status_filter: str) -> bool:
    if status_filter == "to_do":
        return not task.completed and task.status.value == "pending"
    if status_filter == "in_progress":
        return not task.completed and task.status.value == "in_progress"
    if status_filter == "done":
        return task.completed or task.status.value == "done"
    return True


def filter_visible_tasks(
    tasks: list[Task],
    *,
    view: str,
    status: str,
    priority: str,
    category: str,
    query: str,
) -> list[Task]:
    visible_tasks = list(tasks)
    if view == "list":
        visible_tasks = [t for t in visible_tasks if task_matches_status_filter(t, status)]
    if priority != "all":
        visible_tasks = [t for t in visible_tasks if t.priority.value == priority]
    if category != "all":
        visible_tasks = [t for t in visible_tasks if t.category == category]
    if query:
        visible_tasks = [t for t in visible_tasks if query in t.title.lower()]
    return visible_tasks


CATEGORY_PILL_CLASSES = {
    "project": "bg-teal-100 text-teal-700",
    "exam": "bg-rose-100 text-rose-700",
    "assignment": "bg-blue-100 text-blue-700",
    "research": "bg-indigo-100 text-indigo-700",
    "reading": "bg-emerald-100 text-emerald-700",
    "personal": "bg-violet-100 text-violet-700",
    "other": "bg-slate-100 text-slate-700",
}

PRIORITY_PILL_CLASSES = {
    "low": "bg-emerald-100 text-emerald-700",
    "medium": "bg-amber-100 text-amber-700",
    "high": "bg-rose-100 text-rose-700",
}

PRIORITY_RAIL_CLASSES = {
    "low": "border-emerald-400",
    "medium": "border-amber-400",
    "high": "border-rose-400",
}

PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


def category_pill_class(value: str) -> str:
    return CATEGORY_PILL_CLASSES.get((value or "").lower(), "bg-slate-100 text-slate-700")


def priority_pill_class(value: str) -> str:
    return PRIORITY_PILL_CLASSES.get((value or "").lower(), "bg-slate-100 text-slate-700")


def priority_rail_class(value: str) -> str:
    return PRIORITY_RAIL_CLASSES.get((value or "").lower(), "border-slate-300")


def calendar_sidebar_border_class(
    priority_value: str,
    due_date: date | None,
    today: date,
    completed: bool,
) -> str:
    if due_date is not None and not completed and due_date < today:
        return "border-rose-500"
    if completed:
        return "border-slate-300"
    return priority_rail_class(priority_value)


def category_display(value: str) -> str:
    stripped = (value or "").strip()
    return stripped.title() if stripped else "Other"


def relative_due_text(due_date: date, today: date, is_done: bool) -> str:
    formatted = due_date.strftime("%d %b")
    if is_done:
        return f"Due {formatted}"
    delta = (due_date - today).days
    if delta == 0:
        return f"Due {formatted} - today"
    if delta > 0:
        plural = "s" if delta != 1 else ""
        return f"Due {formatted} - in {delta} day{plural}"
    days_late = -delta
    plural = "s" if days_late != 1 else ""
    return f"Due {formatted} - {days_late} day{plural} late"


def normalize_query(value: str | None) -> str:
    return (value or "").strip().lower()


def completion_progress_summary(
    completed_count: int,
    total_count: int,
    period_label: str | None = None,
) -> tuple[str, str]:
    if total_count <= 0:
        return "0%", f"Nothing {period_label}" if period_label else "No tasks yet"
    pct = round(completed_count / total_count * 100)
    if period_label:
        return f"{pct}%", f"{completed_count} of {total_count} {period_label}"
    plural = "s" if total_count != 1 else ""
    return f"{pct}%", f"{completed_count} of {total_count} task{plural} done"
