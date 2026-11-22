import streamlit as st
import sqlite3
from pathlib import Path
from datetime import date

st.set_page_config(page_title="StudentHub Dashboard", page_icon="🎓", layout="wide")

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "student_portal.db"

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            posted_on TEXT NOT NULL
        )""")
        if db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO tasks (title, due_date, status) VALUES (?, ?, ?)",
                [
                    ("Complete Python assignment", "2026-11-25", "Pending"),
                    ("Prepare for DBMS quiz", "2026-11-27", "In progress"),
                    ("Submit project documentation", "2026-11-30", "Completed"),
                ],
            )
        if db.execute("SELECT COUNT(*) FROM announcements").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO announcements (title, message, posted_on) VALUES (?, ?, ?)",
                [
                    ("Internal assessment schedule", "The internal assessment timetable will be shared soon.", "2026-11-20"),
                    ("Project review", "Remember to bring your project progress report for the review.", "2026-11-18"),
                ],
            )

def load_data():
    with get_db() as db:
        tasks = db.execute("SELECT * FROM tasks ORDER BY due_date").fetchall()
        announcements = db.execute("SELECT * FROM announcements ORDER BY posted_on DESC").fetchall()
    return [dict(x) for x in tasks], [dict(x) for x in announcements]

def add_task(title, due):
    with get_db() as db:
        db.execute("INSERT INTO tasks (title, due_date, status) VALUES (?, ?, 'Pending')", (title, due.isoformat()))

def update_task(task_id, status):
    with get_db() as db:
        db.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))

init_db()

# Styling is written as HTML/CSS; no frontend JavaScript is used.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#17233b; --muted:#8490a5; --blue:#4169e1; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:#f6f8fc; color:var(--ink); }
.block-container { max-width:1450px; padding-top:2rem; padding-bottom:2rem; }
[data-testid="stMetric"] { background:white; border:1px solid #edf0f6; border-radius:14px; padding:18px 20px; }
[data-testid="stMetricLabel"] { color:#748097; font-weight:600; }
[data-testid="stMetricValue"] { color:#17233b; font-family:Manrope,sans-serif; }
.hero { background:linear-gradient(110deg,#365bd2,#7188ee); border-radius:17px; padding:25px 30px; color:white; margin:8px 0 22px; }
.hero .eyebrow { color:#d4ddff; font-size:10px; letter-spacing:1.5px; font-weight:800; }
.hero h2 { color:white; font-family:Manrope,sans-serif; margin:5px 0; font-size:25px; }
.hero p { color:#e3e9ff; margin:0; }
.section-card { background:white; border:1px solid #edf0f6; border-radius:14px; padding:20px 22px; margin-bottom:14px; }
.section-kicker { color:#9aa5b8; font-size:10px; letter-spacing:1.5px; font-weight:800; margin:0 0 5px; }
.section-title { color:#17233b; font-family:Manrope,sans-serif; font-size:18px; font-weight:800; margin:0 0 14px; }
.profile { background:white; border:1px solid #edf0f6; border-radius:14px; padding:17px 22px; margin-top:12px; }
div.stButton > button, div.stFormSubmitButton > button { background:#4169e1; color:white; border:0; border-radius:8px; font-weight:700; }
div.stButton > button:hover, div.stFormSubmitButton > button:hover { background:#3154c4; color:white; border:0; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🎓 StudentHub")
    st.caption("STUDENT PORTAL")
    page = st.radio("MENU", ["Overview", "My Tasks", "Announcements"], label_visibility="visible")
    st.divider()
    st.markdown("**Alex Johnson**")
    st.caption("Student account")

tasks, announcements = load_data()
student = {
    "name": "Alex Johnson",
    "department": "Computer Science Engineering",
    "year": "3rd Year",
    "register_number": "CSE2026001",
    "attendance": 92,
    "cgpa": 8.4
}
pending = sum(t["status"] != "Completed" for t in tasks)
completed = sum(t["status"] == "Completed" for t in tasks)

st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
 <div><div class="section-kicker">STUDENT PORTAL</div><h1 style="font-family:Manrope;margin:0;color:#17233b">Dashboard</h1></div>
 <div style="color:#8490a5;font-size:13px">{date.today().strftime("%a, %b %d, %Y")}</div>
</div>
<div class="hero">
 <div class="eyebrow">YOUR ACADEMIC SPACE</div>
 <h2>Welcome back, {student["name"]}! 👋</h2>
 <p>Here’s your academic progress at a glance.</p>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Attendance", f'{student["attendance"]}%')
c2.metric("Current CGPA", f'{student["cgpa"]:.2f}')
c3.metric("Pending tasks", pending)
c4.metric("Completed tasks", completed)

if page in ("Overview", "My Tasks"):
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="section-kicker">STAY ORGANIZED</div><div class="section-title">My tasks</div>', unsafe_allow_html=True)
        with st.form("add_task_form", clear_on_submit=True):
            task_title = st.text_input("Task title", placeholder="Add a new task...")
            due_date = st.date_input("Due date", value=date.today())
            submitted = st.form_submit_button("+ Add task", use_container_width=True)
            if submitted:
                if task_title.strip():
                    add_task(task_title.strip(), due_date)
                    st.success("Task added successfully.")
                    st.rerun()
                else:
                    st.error("Please enter a task title.")
        tasks, _ = load_data()
        if not tasks:
            st.info("No tasks yet. Add your first task above.")
        for task in tasks:
            with st.container(border=True):
                row1, row2 = st.columns([2,1])
                with row1:
                    st.markdown(f"**{task['title']}**")
                    st.caption(f"Due: {task['due_date']}")
                with row2:
                    choices = ["Pending", "In progress", "Completed"]
                    current_index = choices.index(task["status"]) if task["status"] in choices else 0
                    new_status = st.selectbox("Status", choices, index=current_index, key=f"status_{task['id']}", label_visibility="collapsed")
                    if new_status != task["status"]:
                        update_task(task["id"], new_status)
                        st.rerun()
    if page == "Overview":
        with right:
            st.markdown('<div class="section-kicker">CAMPUS UPDATES</div><div class="section-title">Announcements</div>', unsafe_allow_html=True)
            for item in announcements:
                st.markdown(f"""
                <div style="padding:12px 0;border-bottom:1px solid #edf0f6">
                 <b style="font-size:13px">{item["title"]}</b>
                 <p style="font-size:12px;color:#7d899d;line-height:1.6;margin:6px 0">{item["message"]}</p>
                 <small style="color:#a0a9b8">Posted {item["posted_on"]}</small>
                </div>""", unsafe_allow_html=True)

if page == "Announcements":
    st.markdown('<div class="section-kicker">CAMPUS UPDATES</div><div class="section-title">Announcements</div>', unsafe_allow_html=True)
    for item in announcements:
        with st.container(border=True):
            st.markdown(f"**{item['title']}**")
            st.write(item["message"])
            st.caption(f"Posted {item['posted_on']}")

st.markdown(f"""
<div class="profile">
 <div class="section-kicker">STUDENT PROFILE</div>
 <b style="font-family:Manrope;font-size:15px">{student["name"]}</b>
 <div style="font-size:12px;color:#8490a5;margin-top:4px">{student["department"]} · {student["year"]}</div>
 <div style="display:flex;gap:55px;flex-wrap:wrap;margin-top:14px;font-size:12px">
  <div><span style="color:#8490a5">Register number</span><br><b>{student["register_number"]}</b></div>
  <div><span style="color:#8490a5">Portal status</span><br><b style="color:#269b68">● Active</b></div>
 </div>
</div>
""", unsafe_allow_html=True)
st.caption("StudentHub · Student Dashboard Portal")
