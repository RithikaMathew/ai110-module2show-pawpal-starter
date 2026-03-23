# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner plan and track daily care tasks for their pets.

## 📸 Demo

<a href="/course_images/ai110/pawpal_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_screenshot.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Features

### Owner and Pet Management
Register an owner and add as many pets as needed, each with a name and species (dog, cat, or other). Pets are stored in the owner's session and persist for the duration of the app session via `st.session_state`.

### Task Scheduling
Create care tasks — feedings, walks, medications, appointments, or anything else — and assign them to a specific pet. Each task captures:
- **Title** — what needs to happen
- **Time** — when it happens, in 24-hour `HH:MM` format
- **Duration** — how long it takes, in minutes
- **Priority** — `low`, `medium`, or `high`
- **Frequency** — `once`, `daily`, or `weekly`

### Chronological Daily Schedule
The `Scheduler.daily_schedule()` method filters all tasks to those due today that are not yet complete, then sorts them using `Scheduler.sort_by_time()`. Sorting uses Python's built-in `sorted()` with a `lambda t: t.time` key, which correctly orders `HH:MM` strings lexicographically. The result is displayed as a table in the UI so the owner sees their day in time order at a glance.

### Conflict Warnings
`Scheduler.detect_conflicts()` scans every task and builds a dictionary keyed on `(pet_name, time)`. If a second task maps to the same key, a plain-English warning is generated — for example: `[CONFLICT] 'Feeding' and 'Grooming' both scheduled at 08:00 for Luna`. Warnings appear as `st.warning` banners in the UI above the schedule table so they are impossible to miss. The app never crashes on a conflict — it always reports and continues.

### Automatic Recurrence
When a task is marked complete, `Task.mark_complete()` sets `completed = True` and checks the task's frequency. For `daily` tasks it returns a new `Task` with `due_date + timedelta(days=1)`; for `weekly` tasks it uses `timedelta(weeks=1)`; for `once` tasks it returns `None`. `Scheduler.mark_task_complete()` receives this return value and, if it is not `None`, immediately calls `pet.add_task()` to register the next occurrence. The UI confirms the next due date with an `st.info` message.

### Filtering
`Scheduler.filter_tasks()` accepts an optional `pet_name` and an optional `completed` boolean. Either, both, or neither can be supplied — the method chains the filters and returns the matching subset of tasks. This powers the CLI demo and can be extended to drive filter controls in the UI.

## Smarter Scheduling

- **Sorting by time** — `Scheduler.sort_by_time()` uses `sorted()` with `lambda t: t.time`; lexicographic ordering of `HH:MM` strings is equivalent to chronological ordering, so no time parsing is needed
- **Conflict detection** — `Scheduler.detect_conflicts()` uses a single-pass dictionary scan (`O(n)`) keyed on `(pet_name, time)`; returns human-readable warning strings instead of raising exceptions
- **Automatic recurrence** — `Task.mark_complete()` returns the next `Task` instance using `timedelta`; `Scheduler.mark_task_complete()` coordinates adding it back to the correct `Pet`
- **Filtering** — `Scheduler.filter_tasks()` chains `pet_name` and `completed` filters independently so either or both can be applied in one call
- **Daily schedule** — `Scheduler.daily_schedule()` combines a `due_date == today` filter with `not completed` and then calls `sort_by_time()`, giving a clean one-call API for the UI

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
