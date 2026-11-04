import streamlit as st
import json
import os
from datetime import date

FILE = "tasks.json"

# --- Load saved tasks ---
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(FILE, "w") as f:
        json.dump(st.session_state.tasks, f)

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "dark" not in st.session_state:
    st.session_state.dark = False

# --- Dark Mode ---
if st.session_state.dark:
    st.markdown("""
    <style>
    .stApp { background-color: #1E1E1E; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="My To-Do List", page_icon="✅")
st.title("✅ My To-Do List")

# Dark mode button
if st.button("🌙 Dark Mode" if not st.session_state.dark else "☀️ Light Mode"):
    st.session_state.dark = not st.session_state.dark
    st.rerun()

st.write("Organize your day!")

# --- Add new task ---
col_a, col_b = st.columns(2)
with col_a:
    new_task = st.text_input("New task:")
with col_b:
    priority = st.selectbox("Priority:", ["🔴 Important", "🟡 Normal", "🟢 Low"])

task_date = st.date_input("Date:", value=date.today())

if st.button("➕ Add Task"):
    if new_task:
        st.session_state.tasks.append({
            "task": new_task,
            "priority": priority,
            "date": str(task_date),
            "done": False
        })
        save_tasks()
        st.rerun()

st.divider()

# --- Filter ---
filter_option = st.selectbox("Show:", ["All", "Not Done", "Done", "🔴 Important"])
st.divider()

# --- Show tasks ---
shown = 0
for i, item in enumerate(st.session_state.tasks):
    if filter_option == "Not Done" and item["done"]:
        continue
    if filter_option == "Done" and not item["done"]:
        continue
    if filter_option == "🔴 Important" and "Important" not in item["priority"]:
        continue
    
    shown += 1
    c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
    with c1:
        checked = st.checkbox("", value=item["done"], key=f"check_{i}")
        if checked != item["done"]:
            st.session_state.tasks[i]["done"] = checked
            save_tasks()
            st.rerun()
    with c2:
        text = f"{item['task']}  -  {item['priority']}  -  📅 {item['date']}"
        if item["done"]:
            st.markdown(f"~~{text}~~")
        else:
            st.write(text)
    with c3:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            save_tasks()
            st.rerun()

if shown == 0:
    st.info("No tasks here!")

# --- Progress ---
if len(st.session_state.tasks) > 0:
    done = sum(1 for t in st.session_state.tasks if t["done"])
    total = len(st.session_state.tasks)
    st.progress(done / total)
    st.success(f"You finished {done} / {total} tasks! Keep going 💪")

if st.button("🗑️ Delete All Done"):
    st.session_state.tasks = [t for t in st.session_state.tasks if not t["done"]]
    save_tasks()
    st.rerun()