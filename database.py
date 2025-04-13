import sqlite3
import aiosqlite
import json
from datetime import datetime

DB_NAME = "nutrition_survey.db"

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица пользователей
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            registration_date TEXT,
            is_paid BOOLEAN DEFAULT FALSE
        )
        ''')
        
        # Таблица ответов на опрос
        await db.execute('''
        CREATE TABLE IF NOT EXISTS survey_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question_number INTEGER,
            answer TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Таблица для хранения полных опросов
        await db.execute('''
        CREATE TABLE IF NOT EXISTS completed_surveys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            survey_data TEXT,
            completion_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        # Таблица платежей
        await db.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            payment_date TEXT,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        
        await db.commit()

async def register_user(user_id, username, first_name, last_name):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, registration_date) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, first_name, last_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()

async def save_answer(user_id, question_number, answer):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO survey_results (user_id, question_number, answer, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, question_number, answer, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()

async def save_completed_survey(user_id, survey_data):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO completed_surveys (user_id, survey_data, completion_date) VALUES (?, ?, ?)",
            (user_id, json.dumps(survey_data, ensure_ascii=False), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        await db.commit()

async def record_payment(user_id, amount, status="pending"):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO payments (user_id, amount, payment_date, status) VALUES (?, ?, ?, ?)",
            (user_id, amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status)
        )
        await db.commit()

async def update_payment_status(user_id, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE payments SET status = ? WHERE user_id = ? AND status = 'pending'",
            (status, user_id)
        )
        await db.execute(
            "UPDATE users SET is_paid = ? WHERE user_id = ?",
            (status == "completed", user_id)
        )
        await db.commit()

async def is_user_paid(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT is_paid FROM users WHERE user_id = ?", (user_id,))
        result = await cursor.fetchone()
        if result:
            return bool(result[0])
        return False

async def get_user_survey_results(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT question_number, answer FROM survey_results WHERE user_id = ? ORDER BY question_number",
            (user_id,)
        )
        results = await cursor.fetchall()
        return {row[0]: row[1] for row in results}

async def get_all_completed_surveys():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT cs.id, u.user_id, u.username, u.first_name, u.last_name, cs.survey_data, cs.completion_date "
            "FROM completed_surveys cs JOIN users u ON cs.user_id = u.user_id "
            "ORDER BY cs.completion_date DESC"
        )
        results = await cursor.fetchall()
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "username": row[2],
                "first_name": row[3],
                "last_name": row[4],
                "survey_data": json.loads(row[5]),
                "completion_date": row[6]
            }
            for row in results
        ]
