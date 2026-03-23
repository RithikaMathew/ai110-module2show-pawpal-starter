# PawPal+ Project Reflection

## 1. System Design

**Three core actions a user should be able to perform:**

1. **Add a pet** — The owner can register one or more pets (dog, cat, or other) by name and species so the app knows whose tasks belong to whom.
2. **Schedule a task** — The owner can create a care task (like a walk, feeding, or medication) for a specific pet, setting the time, duration, priority, and how often it repeats (once, daily, or weekly).
3. **See today's tasks** — The owner can view a chronologically sorted list of all incomplete tasks due today, with conflict warnings if two tasks overlap for the same pet.

**a. Initial design**

The system is built around four classes. `Task` is the smallest unit — it holds everything about a single care activity: its title, scheduled time, duration, priority, frequency, which pet it belongs to, its due date, and whether it has been completed. `Pet` groups a pet's basic info (name and species) with its list of tasks, and exposes simple methods to add tasks and count them. `Owner` sits above `Pet` and manages a collection of pets, with a helper method that flattens all tasks across all pets into one list. `Scheduler` is the "brain" — it takes an `Owner` and provides all the algorithmic behavior: sorting tasks by time, filtering by pet or status, detecting conflicts, handling recurrence when a task is marked complete, and building the daily schedule.

**b. Design changes**

The initial skeleton had `mark_complete()` living only on `Task`, but it had no way to add the next recurrence back to the pet's task list on its own. During implementation, `mark_task_complete()` was added to `Scheduler` so it could call `task.mark_complete()` to get the new `Task` object back and then immediately call `pet.add_task()` to register it. This kept `Task` as a pure data object while giving `Scheduler` the coordination responsibility, which is a cleaner separation of concerns.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers time (HH:MM), completion status, pet assignment, due date, and frequency. Time was treated as the most important constraint because a pet owner's day is organized around a clock — knowing what comes next is more immediately useful than knowing what is highest priority. Priority is stored on each task and displayed, but the sort order is always chronological.

**b. Tradeoffs**

The conflict detection only flags tasks that share the exact same time string for the same pet — it does not check whether a 30-minute task starting at 08:00 overlaps with a 20-minute task starting at 08:15. This is a reasonable tradeoff for a first version because exact-time conflicts are the most common scheduling mistake and are simple to detect without needing to parse durations and compute time windows. Overlap detection would require converting times to minutes, adding durations, and comparing ranges, which adds complexity that isn't necessary until the app is used with back-to-back tasks.

---

## 3. AI Collaboration

**a. How you used AI**

AI was used across every phase: brainstorming the four-class architecture, generating the initial class skeletons from the UML description, fleshing out method implementations, writing the pytest suite, and wiring the Streamlit UI to the backend. The most helpful prompts were specific and scoped — for example, asking "how should Scheduler retrieve all tasks from Owner's pets" produced a clean `all_tasks()` aggregator method, and asking for a lightweight conflict detection strategy that returns a warning string rather than raising an exception led directly to the dictionary-based approach used in `detect_conflicts()`.

**b. Judgment and verification**

The AI initially suggested using Python 3.10+ union type hint syntax (`list[Task] | None`) for method signatures. After running the code, it failed immediately on Python 3.9 with a `TypeError`. Rather than accepting the suggestion as-is, the fix was to switch to `Optional[List[Task]]` from the `typing` module, which works on Python 3.8 and above. This was verified by re-running `python main.py` and confirming no import errors before moving on.

---

## 4. Testing and Verification

**a. What you tested**

Seven behaviors were tested: that `mark_complete()` sets `completed = True`, that adding a task increments `pet.task_count()`, that `sort_by_time()` returns tasks in chronological HH:MM order, that completing a daily task adds a new task with tomorrow's date, that completing a once task does not add any new task, that two tasks for the same pet at the same time produce a conflict warning, and that two tasks at different times produce no warnings.

These tests matter because they cover the four core algorithms the app depends on — completion, sorting, recurrence, and conflict detection. If any of these break silently, the schedule shown to the user would be wrong without any obvious error.

**b. Confidence**

Confidence level: 4 out of 5 stars. All seven tests pass and cover the main happy paths and the most important edge cases. The next cases to test would be: a pet with zero tasks (does `daily_schedule()` return an empty list cleanly?), a weekly task recurrence (currently only daily recurrence is tested), and tasks with due dates in the past or future being correctly excluded from today's schedule.

---

## 5. Reflection

**a. What went well**

The CLI-first workflow worked really well. Building and verifying `pawpal_system.py` through `main.py` before touching `app.py` meant that by the time the Streamlit UI was being wired up, there was high confidence the backend was correct. Debugging in the terminal is much faster than debugging through a browser UI, so this order of operations saved a lot of time.

**b. What you would improve**

The conflict detection would be the first thing to improve in a next iteration — upgrading it from exact-time matching to duration-aware overlap detection. I would also add a `due_date` filter to `daily_schedule()` so that recurring tasks from past days that were never completed don't silently disappear from the schedule.

**c. Key takeaway**

The most important thing learned was that AI is most useful when you already have a clear mental model of what you want. When prompts were vague ("build a scheduler"), the output needed heavy editing. When prompts were specific ("write a method that returns a warning string when two tasks share the same pet and time"), the output was close to production-ready. Being the lead architect means knowing what to ask for — the AI fills in the implementation details, but the design decisions have to come from you.
