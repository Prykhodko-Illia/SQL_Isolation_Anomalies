# Non-Repeatable Read vs Repeatable Read

## Non-repeatable Read

### Starting two transactions
```
[INFO] Connection set to READ COMMITTED.

[Tx1-READ COMMITTED] Starting transaction 1.
[Tx2-READ COMMITTED] Starting transaction 2.
```

### Showing sum at the beginning 
```
[Tx2-READ COMMITTED] Alice's balance: 1000.00
[Tx2-READ COMMITTED] Bob's balance: 500.00

[Tx2-READ COMMITTED] Sum balance (1): 1500.00
```

### Updating balance
```
[Tx1-READ COMMITTED] Updated Bob's balance by 400.00.
[Tx1-READ COMMITTED] Transaction 1 commited.
```

### Reading Bob's balance and sum it with Alice balance
```
[Tx2-READ COMMITTED] Bob's balance: 900.00

[Tx2-READ COMMITTED] Sum balance (2): 1900.00
```

### Explanation
Transaction 2 reads balance before changing, showing the sum and saving Alice's balance. \
Then, transaction 1 updates Bob's balance and commits it. \
Now, 2nd transaction find the sum again, but due to changes gives the other value (*1900* instead *1500*).\
It is called **non-repeatable read**.

## Solution: Repeatable Read

### The same transactions but different isolation level
> [INFO] Connection set to REPEATABLE READ.

### First read
````
[Tx2-REPEATABLE READ] Alice's balance: 1000.00
[Tx2-REPEATABLE READ] Bob's balance: 500.00

[Tx2-REPEATABLE READ] Sum balance (1): 1500.00
````
### Updating
````
[Tx1-REPEATABLE READ] Updated Bob's balance by 400.00.
[Tx1-REPEATABLE READ] Transaction 1 commited.
````

### Second read
````
[Tx2-REPEATABLE READ] Bob's balance: 500.00
[Tx2-REPEATABLE READ] Sum balance (2): 1500.00
````

### Explanation:
In this example it reads data that was from the start of this transaction or changed in this transaction. \
So, it prevents us from non-repeatable read.