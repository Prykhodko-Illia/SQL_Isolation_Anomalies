# Deadlock

## Demonstration
### Starting transactions
> Happens on every isolation level
````
[Tx1-REPEATABLE READ] Starting transaction 1.
[Tx2-REPEATABLE READ] Starting transaction 2.
````
### Updating
````
[Tx1-REPEATABLE READ] Updated Alice's balance by 100.00.
[Tx1-REPEATABLE READ] Alice balance updated. Not commited.

[ERROR] Error updating balance: 1205 (HY000): Lock wait timeout exceeded; try restarting transaction

[Tx2-REPEATABLE READ] Bob's balance updated. Not commited.
[Tx1-REPEATABLE READ] Updated Bob's balance by 300.00.
...
````
### Error occured
````
[ERROR] Error updating balance: 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
````

### Order explanation
1. Transaction 1 updates Alice's balance (locking row)
2. Transaction 2 updates Bob's balance (locking row)
3. Transaction 1 can`t update Bob's balance and waits for Tx2 to finish
4. Transaction 2 can`t update Bob's balance and  waits for Tx1 to finish
5. Deadlock