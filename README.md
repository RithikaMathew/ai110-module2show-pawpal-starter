# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan and track daily care tasks for their pets.

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Features

- Add an owner and multiple pets (dog, cat, other)
- Add tasks with time, duration, priority, and frequency (once / daily / weekly)
- View today's schedule sorted chronologically
- Conflict warnings when two tasks share the same pet and time slot
- Automatic recurrence: completing a daily/weekly task schedules the next occurrence
- Filter tasks by pet name or completion status

## Smarter Scheduling

- **Sorting by time** — tasks are ordered by `HH:MM` string using Python's `sorted()` with a lambda key
- **Conflict detection** — the Scheduler scans all tasks and flags any two tasks for the same pet at the same time, returning a human-readable warning instead of crashing
- **Daily recurrence** — `mark_complete()` on a `daily` task returns a new `Task` with `due_date + timedelta(days=1)`; weekly tasks use `timedelta(weeks=1)`
- **Filtering** — tasks can be filtered by pet name, completion status, or both

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Running the app

```bash
streamlit run app.py
```

## CLI demo

```bash
python main.py
```

## Testing PawPal+

```bash
python -m pytest
```

The test suite (`tests/test_pawpal.py`) covers:

| Test | What it verifies |
|---|---|
| `test_mark_complete_changes_status` | `mark_complete()` sets `completed = True` |
| `test_add_task_increases_count` | Adding a task increments `pet.task_count()` |
| `test_sort_by_time_returns_chronological_order` | Tasks come back in HH:MM order |
| `test_daily_task_creates_next_occurrence` | Completing a daily task adds tomorrow's task |
| `test_once_task_does_not_recur` | One-off tasks don't spawn new tasks |
| `test_conflict_detected_for_same_pet_same_time` | Duplicate time/pet raises a warning |
| `test_no_conflict_for_different_times` | Different times produce no warnings |

**Confidence level: ★★★★☆** — core scheduling behaviors are fully covered; edge cases like overlapping durations (not just exact time matches) would be the next area to test.

## Architecture

Four classes in `pawpal_system.py`:

| Class | Responsibility |
|---|---|
| `Task` | Holds task data; handles recurrence on `mark_complete()` |
| `Pet` | Stores pet info and its list of tasks |
| `Owner` | Manages multiple pets; aggregates all tasks |
| `Scheduler` | Sorts, filters, detects conflicts, builds daily schedule |

## Suggested workflow

1. Read the scenario and identify requirements.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs.
4. Implement scheduling logic incrementally.
5. Verify with `python main.py` and `python -m pytest`.
6. Connect logic to the Streamlit UI in `app.py`.
