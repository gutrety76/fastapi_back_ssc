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

def log_attempt(card_id, attempt_result,name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO card_history (card_id, attempt_result,name) VALUES (%s, %s,%s)",
                (card_id, attempt_result,name)
            )
            conn.commit()


def get_cards():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT * FROM card ")
            user = cursor.fetchall()
            return user
def fetchStatistic(start_date,end_date):

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM card_history WHERE attempt_date BETWEEN %s AND %s", (start_date, end_date))
            stats = cursor.fetchall()
            return stats



def unbancard(name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE  card set Registered = TRUE WHERE number = %s", (name,))
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (name,))
            user = cursor.fetchone()
            return user
def increase_suc(card_number):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM card WHERE number = %s", (card_number,))
            user_name = cursor.fetchone()[0]
            cursor.execute("UPDATE card SET attempts_suc = attempts_suc + 1 WHERE number = %s RETURNING id", (card_number,))
            card_id = cursor.fetchone()[0]
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (card_number,))
            user = cursor.fetchone()
            log_attempt(card_id, True, user_name)  
            return user

def increase_fail(card_number):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM card WHERE number = %s", (card_number,))
            user_name = cursor.fetchone()[0]
            cursor.execute("UPDATE card SET attempts_fail = attempts_fail + 1 WHERE number = %s RETURNING id", (card_number,))
            card_id = cursor.fetchone()[0]
            conn.commit()
            cursor.execute("SELECT * FROM card WHERE number = %s", (card_number,))
            user = cursor.fetchone()
            log_attempt(card_id, False, user_name)  
            return user


