import sqlite3

conn = sqlite3.connect("data/stress.db", check_same_thread=False)

cursor = conn.cursor()

# ---------------- USERS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ---------------- STRESS TABLE ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS stress_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    stress_level INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS questionnaire (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    sleep_hours REAL,
    study_hours REAL,
    social_interaction REAL,
    academic_pressure REAL,
    stress_level INTEGER,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()