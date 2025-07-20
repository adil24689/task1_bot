import sqlite3

DB_NAME = "taskbot.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.executescript(open("schema.sql").read())
        conn.commit()

def add_user(user_id, name):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT OR IGNORE INTO users (id, name) VALUES (?, ?)", (user_id, name))

def get_user(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

def add_task(title, desc, slots):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO tasks (title, description, slots) VALUES (?, ?, ?)", (title, desc, slots))

def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM tasks").fetchall()

def submit_proof(user_id, task_id, proof):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO submissions (user_id, task_id, proof, status) VALUES (?, ?, ?, 'pending')", (user_id, task_id, proof))

def get_pending_submissions():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM submissions WHERE status='pending'").fetchall()

def approve_submission(sub_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE submissions SET status='approved' WHERE id=?", (sub_id,))

def get_stats():
    with sqlite3.connect(DB_NAME) as conn:
        u = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        t = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        s = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
        return u, t, s

def add_recharge(user_id, method, amount):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO recharges (user_id, method, amount, status) VALUES (?, ?, ?, 'pending')", (user_id, method, amount))

def get_recharges():
    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("SELECT * FROM recharges").fetchall()