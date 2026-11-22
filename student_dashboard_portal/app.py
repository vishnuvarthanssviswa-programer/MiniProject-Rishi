from flask import Flask, jsonify, request, send_from_directory
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "student_portal.db"
FRONTEND = ROOT / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")

def get_db():
    conn = sqlite3.connect(DB_PATH)
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

@app.get("/")
def home():
    return send_from_directory(FRONTEND, "index.html")

@app.get("/api/dashboard")
def dashboard():
    with get_db() as db:
        tasks = db.execute("SELECT * FROM tasks ORDER BY due_date").fetchall()
        announcements = db.execute(
            "SELECT * FROM announcements ORDER BY posted_on DESC"
        ).fetchall()
    task_list = [dict(row) for row in tasks]
    return jsonify({
        "student": {
            "name": "Alex Johnson",
            "department": "Computer Science Engineering",
            "year": "3rd Year",
            "register_number": "CSE2026001",
            "attendance": 92,
            "cgpa": 8.4
        },
        "tasks": task_list,
        "announcements": [dict(row) for row in announcements],
        "stats": {
            "total_tasks": len(task_list),
            "pending_tasks": sum(t["status"] != "Completed" for t in task_list),
            "completed_tasks": sum(t["status"] == "Completed" for t in task_list)
        }
    })

@app.post("/api/tasks")
def add_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    due_date = (data.get("due_date") or "").strip()
    if not title or not due_date:
        return jsonify({"error": "Task title and due date are required."}), 400
    with get_db() as db:
        cur = db.execute(
            "INSERT INTO tasks (title, due_date, status) VALUES (?, ?, 'Pending')",
            (title, due_date)
        )
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(task)), 201

@app.patch("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in ("Pending", "In progress", "Completed"):
        return jsonify({"error": "Invalid task status."}), 400
    with get_db() as db:
        cur = db.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Task not found."}), 404
        task = db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return jsonify(dict(task))

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
