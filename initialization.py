import mysql.connector
from database_properties import *

def get_connection(isolation_level_str: str):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if isolation_level_str in ISOLATION_LEVELS:
            conn.autocommit = False
            conn.cmd_query(f"SET SESSION TRANSACTION ISOLATION LEVEL {isolation_level_str};")
            print(f"[INFO] Connection set to {isolation_level_str}.")
        else:
            raise ValueError(f"Unsupported isolation level: {isolation_level_str}")

        return conn

    except mysql.connector.Error as e:
        print(f"[ERROR] Could not connect to database: {e}")
        exit(1)


def reset_database():
    conn = get_connection("SERIALIZABLE")
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE accounts")
            cur.execute("INSERT INTO accounts (account_holder, balance) VALUES (%s, %s)", ("Alice", "1000.0"))
            cur.execute("INSERT INTO accounts (account_holder, balance) VALUES (%s, %s)", ("Bob", "500.0"))
            conn.commit()
            print("\n[INFO] Database reset to initial state.")

    except mysql.connector.Error as e:
        print(f"[ERROR] Error resetting database: {e}")
        conn.rollback()
    finally:
        conn.close()