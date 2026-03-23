"""PawPal+ backend: Task, Pet, Owner, Scheduler."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional, List


@dataclass
class Task:
    """A single pet care activity."""
    title: str
    time: str          # "HH:MM" 24-hour format
    duration_minutes: int
    priority: str      # "low" | "medium" | "high"
    frequency: str     # "once" | "daily" | "weekly"
    pet_name: str
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark task done; return next occurrence for recurring tasks, else None."""
        self.completed = True
        if self.frequency == "daily":
            return Task(self.title, self.time, self.duration_minutes,
                        self.priority, self.frequency, self.pet_name,
                        self.due_date + timedelta(days=1))
        if self.frequency == "weekly":
            return Task(self.title, self.time, self.duration_minutes,
                        self.priority, self.frequency, self.pet_name,
                        self.due_date + timedelta(weeks=1))
        return None


@dataclass
class Pet:
    """A pet with a list of care tasks."""
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return number of tasks."""
        return len(self.tasks)


@dataclass
class Owner:
    """An owner who manages one or more pets."""
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def all_tasks(self) -> list[Task]:
        """Return all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, sorts, filters, and checks tasks for an Owner."""

    def __init__(self, owner: Owner):
        """Initialize with an Owner instance."""
        self.owner = owner

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted chronologically by HH:MM time string."""
        tasks = tasks if tasks is not None else self.owner.all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_tasks(self, pet_name: Optional[str] = None,
                     completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        tasks = self.owner.all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return warning strings for tasks sharing the same pet and time."""
        seen: dict = {}
        warnings = []
        for task in self.owner.all_tasks():
            key = (task.pet_name, task.time)
            if key in seen:
                warnings.append(
                    f"[CONFLICT] '{seen[key].title}' and '{task.title}' "
                    f"both scheduled at {task.time} for {task.pet_name}"
                )
            else:
                seen[key] = task
        return warnings

    def mark_task_complete(self, task: Task, pet: Pet) -> None:
        """Complete a task and add its next recurrence to the pet if applicable."""
        next_task = task.mark_complete()
        if next_task:
            pet.add_task(next_task)

    def daily_schedule(self) -> List[Task]:
        """Return today's incomplete tasks sorted by time."""
        today = date.today()
        tasks = [t for t in self.owner.all_tasks()
                 if not t.completed and t.due_date == today]
        return self.sort_by_time(tasks)
