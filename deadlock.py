import time
from threading import Thread, Event

from initialization import *
from balance_commands import *

def deadlock():
    print("-----DEADLOCK DEMONSTRATION-----\n")
    tx_1_update = Event()
    tx_2_update = Event()

    def transaction_1(conn_str):
        conn = get_connection(conn_str)
        try:
            print(f"\n[Tx1-{conn_str}] Starting transaction 1.")
            conn.start_transaction()

            update_balance(conn, "Alice", 100, f"Tx1-{conn_str}");
            print(f"\n[Tx1-{conn_str}] Alice's balance updated. Not commited.")
            tx_1_update.set()

            tx_2_update.wait()
            tx_1_update.clear()

            update_balance(conn, "Bob", 300, f"Tx1-{conn_str}");
            print(f"\n[Tx1-{conn_str}] Bob's balance updated. Not commited.")
            tx_1_update.set()

            tx_2_update.wait()

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

            tx_1_update.wait();
            update_balance(conn, "Bob", 200, f"Tx2-{conn_str}");
            print(f"\n[Tx2-{conn_str}] Bob's balance updated. Not commited.")

            tx_2_update.set()

            tx_1_update.wait()
            tx_2_update.clear()
            update_balance(conn, "Alice", 150, f"Tx2-{conn_str}");
            print(f"\n[Tx2-{conn_str}] Alice's balance updated. Not commited.")

            tx_2_update.set()

            conn.commit()
            print(f"\n[Tx2-{conn_str}] Transaction 2 commited.")

        except mysql.connector.Error as e:
            print(f"[ERROR] Error starting transaction 2: {e}")
            conn.rollback()
            print("Transaction 2 rollbacked")

        finally:
            conn.close()

    def executing():
        reset_database()

        thread1 = Thread(target=transaction_1, args=("REPEATABLE READ",))
        thread2 = Thread(target=transaction_2, args=("REPEATABLE READ",))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    executing()