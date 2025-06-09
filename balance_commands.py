import mysql.connector

def fetch_balance(conn, account_holder: str, label: str = ""):
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT balance FROM accounts WHERE account_holder = %s", (account_holder,))
            balance = cur.fetchone()
            if balance:
                print(f"[{label}] {account_holder}'s balance: {balance[0]:.2f}")
            else:
                print(f"[{label}] {account_holder} not found.")
            return balance[0] if balance else None
    except mysql.connector.Error as e:
        print(f"[ERROR] Error fetching balance: {e}")
        return None


def update_balance(conn, account_holder: str, amount: float, label: str = ""):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_holder = %s",
                (amount, account_holder)
            )
            print(f"[{label}] Updated {account_holder}'s balance by {amount:.2f}.")
    except mysql.connector.Error as e:
        print(f"[ERROR] Error updating balance: {e}")