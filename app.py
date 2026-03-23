"""PawPal+ Streamlit UI — wired to pawpal_system backend."""

import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session state bootstrap ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("")

owner: Owner = st.session_state.owner

# --- Owner / pet setup ---
with st.sidebar:
    st.header("Owner & Pets")
    owner_name = st.text_input("Owner name", value=owner.name or "Jordan")
    owner.name = owner_name

    st.subheader("Add a pet")
    pet_name_input = st.text_input("Pet name")
    species_input = st.selectbox("Species", ["dog", "cat", "other"])
    if st.button("Add pet"):
        if pet_name_input:
            owner.add_pet(Pet(pet_name_input, species_input))
            st.success(f"Added {pet_name_input}!")

    if owner.pets:
        st.subheader("Your pets")
        for p in owner.pets:
            st.write(f"- {p.name} ({p.species})")

# --- Add task ---
st.subheader("Add a Task")
pet_names = [p.name for p in owner.pets]

if not pet_names:
    st.info("Add a pet in the sidebar first.")
else:
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        task_title = st.text_input("Title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col5:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

    selected_pet = st.selectbox("Assign to pet", pet_names)

    if st.button("Add task"):
        pet_obj = next(p for p in owner.pets if p.name == selected_pet)
        pet_obj.add_task(Task(task_title, task_time, int(duration),
                              priority, frequency, selected_pet, date.today()))
        st.success(f"Task '{task_title}' added to {selected_pet}.")

st.divider()

# --- Schedule ---
st.subheader("Generate Schedule")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("No pets added yet.")
    else:
        scheduler = Scheduler(owner)

        # Conflict warnings
        conflicts = scheduler.detect_conflicts()
        for c in conflicts:
            st.warning(c)

        # Today's sorted schedule
        schedule = scheduler.daily_schedule()
        if not schedule:
            st.info("No incomplete tasks scheduled for today.")
        else:
            st.success(f"Today's schedule for {owner.name}:")
            rows = [
                {
                    "Time": t.time,
                    "Pet": t.pet_name,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Frequency": t.frequency,
                }
                for t in schedule
            ]
            st.table(rows)

# --- Mark complete ---
st.divider()
st.subheader("Mark Task Complete")

all_incomplete = [t for t in owner.all_tasks() if not t.completed]
if all_incomplete:
    task_labels = [f"{t.time} | {t.pet_name}: {t.title}" for t in all_incomplete]
    chosen = st.selectbox("Select task to complete", task_labels)
    if st.button("Mark complete"):
        idx = task_labels.index(chosen)
        task_to_complete = all_incomplete[idx]
        pet_obj = next(p for p in owner.pets if p.name == task_to_complete.pet_name)
        Scheduler(owner).mark_task_complete(task_to_complete, pet_obj)
        st.success(f"'{task_to_complete.title}' marked complete!")
        if task_to_complete.frequency in ("daily", "weekly"):
            st.info(f"Next occurrence added for {pet_obj.tasks[-1].due_date}.")
        st.rerun()
else:
    st.info("No incomplete tasks to mark.")
