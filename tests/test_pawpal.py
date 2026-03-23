"""Automated tests for PawPal+ core behaviors."""

from datetime import date, timedelta
import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def setup():
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)
    scheduler = Scheduler(owner)
    return owner, pet, scheduler


def make_task(title, time, pet_name="Mochi", frequency="once"):
    return Task(title, time, 10, "medium", frequency, pet_name)


# --- Task completion ---

def test_mark_complete_changes_status(setup):
    _, pet, _ = setup
    task = make_task("Walk", "08:00")
    pet.add_task(task)
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count(setup):
    _, pet, _ = setup
    before = pet.task_count()
    pet.add_task(make_task("Feeding", "09:00"))
    assert pet.task_count() == before + 1


# --- Sorting ---

def test_sort_by_time_returns_chronological_order(setup):
    _, pet, scheduler = setup
    pet.add_task(make_task("Evening walk", "18:00"))
    pet.add_task(make_task("Morning walk", "07:00"))
    pet.add_task(make_task("Midday meds",  "12:00"))
    times = [t.time for t in scheduler.sort_by_time()]
    assert times == sorted(times)


# --- Recurrence ---

def test_daily_task_creates_next_occurrence(setup):
    _, pet, scheduler = setup
    task = make_task("Walk", "08:00", frequency="daily")
    pet.add_task(task)
    scheduler.mark_task_complete(task, pet)
    assert task.completed is True
    next_task = pet.tasks[-1]
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_once_task_does_not_recur(setup):
    _, pet, scheduler = setup
    task = make_task("Vet visit", "10:00", frequency="once")
    pet.add_task(task)
    count_before = pet.task_count()
    scheduler.mark_task_complete(task, pet)
    assert pet.task_count() == count_before  # no new task added


# --- Conflict detection ---

def test_conflict_detected_for_same_pet_same_time(setup):
    _, pet, scheduler = setup
    pet.add_task(make_task("Feeding",  "08:00"))
    pet.add_task(make_task("Grooming", "08:00"))
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_for_different_times(setup):
    _, pet, scheduler = setup
    pet.add_task(make_task("Feeding",  "08:00"))
    pet.add_task(make_task("Grooming", "09:00"))
    assert scheduler.detect_conflicts() == []
