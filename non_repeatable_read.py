import time
from threading import Thread, Event

from initialization import *
from balance_commands import *

def non_repeatable_read():
    print("-----NON-REPEATABLE READ DEMONSTRATION-----\n")
    tx_1_update = Event()
    tx_2_read = Event()

    def transaction_1(conn_str):
        conn = get_connection(conn_str)

        try:
            print(f"\n[Tx1-{conn_str}] Starting transaction 1.")
            conn.start_transaction()

            tx_2_read.wait()

            update_balance(conn, "Bob", 400, f"Tx1-{conn_str}")

            conn.commit()
            print(f"\n[Tx1-{conn_str}] Transaction 1 commited.")

            tx_1_update.set()


        except mysql.connector.Error as e:
            print(f"[ERROR] Error starting transaction 1: {e}")
            conn.rollback()
            print("Transaction 1 rollbacked")

        finally:
            conn.close()

    def transaction_2(conn_str):
        conn = get_connection(conn_str)

        try:
            print(f"\n[Tx2-{conn_str}] Starting transaction 2.")
            conn.start_transaction()

            alice_balance = fetch_balance(conn, "Alice", f"Tx2-{conn_str}")
            bob_balance = fetch_balance(conn, "Bob", f"Tx2-{conn_str}")

            print(f"\n[Tx2-{conn_str}] Sum balance (1): {alice_balance + bob_balance:.2f}")

            tx_2_read.set()

            tx_1_update.wait()

            bob_balance = fetch_balance(conn, "Bob", f"Tx2-{conn_str}")
            print(f"\n[Tx2-{conn_str}] Sum balance (2): {alice_balance + bob_balance:.2f}")

        except mysql.connector.Error as e:
            print(f"[ERROR] Error starting transaction 2: {e}")

        finally:
            conn.close()

    def executing(conn: str):
        if conn not in ISOLATION_LEVELS: return
        reset_database()

        thread1 = Thread(target=transaction_1, args=(conn,))
        thread2 = Thread(target=transaction_2, args=(conn,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
    executing("READ COMMITTED")

    reset_database()
    tx_1_update.clear()
    tx_2_read.clear()

    print("-----REPEATABLE READ DEMONSTRATION-----\n")
    executing("REPEATABLE READ")