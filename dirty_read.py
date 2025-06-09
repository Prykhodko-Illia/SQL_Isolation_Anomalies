import time
from threading import Thread, Event

from initialization import *
from balance_commands import *

def dirty_read():
    print("-----DIRTY READ DEMONSTRATION-----\n")
    tx_1_update = Event()
    tx_2_read = Event()

    def transaction_1(conn_str):
        conn = get_connection(conn_str)
        try:
            print(f"\n[Tx1-{conn_str}] Starting transaction 1.")
            conn.start_transaction()

            update_balance(conn, "Alice", 100, f"Tx1-{conn_str}");
            print(f"\n[Tx1-{conn_str}] Alice balance updated. Not commited.")
            tx_1_update.set()

            tx_2_read.wait()

            conn.commit()
            print(f"\n[Tx1-{conn_str}] Transaction 1 commited.")

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

            tx_1_update.wait()

            fetch_balance(conn, "Alice", f"Tx2-{conn_str} (first read)")
            tx_2_read.set()

            time.sleep(1)

            fetch_balance(conn, "Alice", f"Tx2-{conn_str} (second read)")

        except mysql.connector.Error as e:
            print(f"[ERROR] Error starting transaction 2: {e}")

        finally:
            conn.close()

    def executing():
        reset_database()

        thread1 = Thread(target=transaction_1, args=("READ UNCOMMITTED",))
        thread2 = Thread(target=transaction_2, args=("READ UNCOMMITTED",))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    executing()