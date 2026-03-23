"""CLI demo: verify PawPal+ backend logic."""

from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Jordan")

mochi = Pet("Mochi", "dog")
mochi.add_task(Task("Evening walk",   "18:00", 30, "high",   "daily",  "Mochi"))
mochi.add_task(Task("Morning walk",   "07:30", 20, "high",   "daily",  "Mochi"))
mochi.add_task(Task("Flea treatment", "09:00", 5,  "medium", "weekly", "Mochi"))

luna = Pet("Luna", "cat")
luna.add_task(Task("Feeding",  "08:00", 5,  "high",   "daily",  "Luna"))
luna.add_task(Task("Playtime", "17:00", 15, "medium", "once",   "Luna"))
luna.add_task(Task("Grooming", "08:00", 10, "low",    "weekly", "Luna"))  # conflict!

owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner)

print("=== Today's Schedule (sorted) ===")
for t in scheduler.sort_by_time():
    status = "[x]" if t.completed else "[ ]"
    print(f"  {status} [{t.time}] {t.pet_name}: {t.title} ({t.duration_minutes} min, {t.priority})")

print("\n=== Conflict Detection ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for w in conflicts:
        print(" ", w)
else:
    print("  No conflicts found.")

print("\n=== Completing 'Morning walk' (daily -> recurs tomorrow) ===")
scheduler.mark_task_complete(mochi.tasks[1], mochi)
print(f"  Morning walk completed: {mochi.tasks[1].completed}")
print(f"  New task added for tomorrow: {mochi.tasks[-1].title} on {mochi.tasks[-1].due_date}")

print("\n=== Filter: incomplete tasks for Mochi ===")
for t in scheduler.filter_tasks(pet_name="Mochi", completed=False):
    print(f"  [{t.time}] {t.title}")
