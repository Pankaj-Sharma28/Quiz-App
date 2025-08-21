<<<<<<< HEAD
import mysql.connector
import os

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "quiz_app"),
        port=int(os.getenv("DB_PORT", 3306))
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            question TEXT,
            selected TEXT,
            correct TEXT,
            score INT,
            attempt_id INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            score INT,
            total INT,
            status VARCHAR(50)
        )
    """)

    conn.commit()
    conn.close()

    # ✅ Add attempt_id column to link results with summary
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            question TEXT,
            selected TEXT,
            correct TEXT,
            score INT,
            attempt_id INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            score INT,
            total INT,
            status VARCHAR(50)
        )
    """)

    conn.commit()
    conn.close()

def add_result(name, question, selected, correct, score, attempt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (name, question, selected, correct, score, attempt_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, question, selected, correct, score, attempt_id)
    )
    conn.commit()
    conn.close()

def add_summary(name, score, total, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quiz_summary (name, score, total, status) VALUES (%s, %s, %s, %s)",
        (name, score, total, status)
    )
    conn.commit()
    attempt_id = cur.lastrowid   # ✅ return this to link results
    conn.close()
    return attempt_id

# ✅ New: update summary at the end of quiz
def update_summary(attempt_id, score, total, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE quiz_summary SET score=%s, total=%s, status=%s WHERE id=%s",
        (score, total, status, attempt_id)
    )
    conn.commit()
    conn.close()

def fetch_summary():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM quiz_summary ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_results(name):
    """
    Return all results for latest attempt of given player.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ✅ latest attempt id for this player
    cur.execute("SELECT MAX(id) AS last_id FROM quiz_summary WHERE name = %s", (name,))
    last = cur.fetchone()
    if not last or not last["last_id"]:
        conn.close()
        return []

    attempt_id = last["last_id"]

    cur.execute("""
        SELECT question, selected, correct,
               (selected = correct) AS is_correct
        FROM results
        WHERE name = %s AND attempt_id = %s
        ORDER BY id ASC
    """, (name, attempt_id))

    rows = cur.fetchall()
    conn.close()
    return rows

# ✅ Explicit latest attempt fetcher
def fetch_latest_results(name):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT MAX(id) AS last_id FROM quiz_summary WHERE name = %s", (name,))
    row = cur.fetchone()
    last_id = row["last_id"]

    if not last_id:
        conn.close()
        return []

    cur.execute("""
        SELECT r.question, r.selected, r.correct,
               (r.selected = r.correct) AS is_correct
        FROM results r
        WHERE r.name = %s AND r.attempt_id = %s
        ORDER BY r.id ASC
    """, (name, last_id))

    rows = cur.fetchall()
    conn.close()
    return rows


=======
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          
        password="",          
        database="quiz_app"
    )

def init_db():
    """
    Initialize database and required tables if they do not exist.
    """
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""   
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS quiz_app")
    conn.commit()
    conn.close()

    conn = get_connection()
    cur = conn.cursor()

    # ✅ Add attempt_id column to link results with summary
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            question TEXT,
            selected TEXT,
            correct TEXT,
            score INT,
            attempt_id INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_summary (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            score INT,
            total INT,
            status VARCHAR(50)
        )
    """)

    conn.commit()
    conn.close()

def add_result(name, question, selected, correct, score, attempt_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO results (name, question, selected, correct, score, attempt_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, question, selected, correct, score, attempt_id)
    )
    conn.commit()
    conn.close()

def add_summary(name, score, total, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO quiz_summary (name, score, total, status) VALUES (%s, %s, %s, %s)",
        (name, score, total, status)
    )
    conn.commit()
    attempt_id = cur.lastrowid   # ✅ return this to link results
    conn.close()
    return attempt_id

# ✅ New: update summary at the end of quiz
def update_summary(attempt_id, score, total, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE quiz_summary SET score=%s, total=%s, status=%s WHERE id=%s",
        (score, total, status, attempt_id)
    )
    conn.commit()
    conn.close()

def fetch_summary():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM quiz_summary ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_results(name):
    """
    Return all results for latest attempt of given player.
    """
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    # ✅ latest attempt id for this player
    cur.execute("SELECT MAX(id) AS last_id FROM quiz_summary WHERE name = %s", (name,))
    last = cur.fetchone()
    if not last or not last["last_id"]:
        conn.close()
        return []

    attempt_id = last["last_id"]

    cur.execute("""
        SELECT question, selected, correct,
               (selected = correct) AS is_correct
        FROM results
        WHERE name = %s AND attempt_id = %s
        ORDER BY id ASC
    """, (name, attempt_id))

    rows = cur.fetchall()
    conn.close()
    return rows

# ✅ Explicit latest attempt fetcher
def fetch_latest_results(name):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT MAX(id) AS last_id FROM quiz_summary WHERE name = %s", (name,))
    row = cur.fetchone()
    last_id = row["last_id"]

    if not last_id:
        conn.close()
        return []

    cur.execute("""
        SELECT r.question, r.selected, r.correct,
               (r.selected = r.correct) AS is_correct
        FROM results r
        WHERE r.name = %s AND r.attempt_id = %s
        ORDER BY r.id ASC
    """, (name, last_id))

    rows = cur.fetchall()
    conn.close()
    return rows
>>>>>>> d295fd8 (quiz app initial commit)
