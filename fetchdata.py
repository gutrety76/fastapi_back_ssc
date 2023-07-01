import psycopg2
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASSWORD")
    )

def check_cards(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()

            if user is None:
                cursor.execute("INSERT INTO card (Registered, number) VALUES (TRUE, %s) RETURNING *", (name,))
                conn.commit()
                user = cursor.fetchone()

            return user

def bancard(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE  card set Registered = FALSE WHERE number = %s", (name,))
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()
            return user

def unbancard(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE  card set Registered = TRUE WHERE number = %s", (name,))
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()
            return user
def increase_suc(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE  card set attempts_suc = attempts_suc + 1 WHERE number = %s", (name,))
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()
            return user
def increase_fail(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE  card set attempts_fail = attempts_fail + 1 WHERE number = %s", (name,))
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()
            return user