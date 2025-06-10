# Dirty Read

### Starting two transactions
```
[Tx2-READ UNCOMMITTED] Starting transaction 2.
[INFO] Connection set to READ UNCOMMITTED.

[Tx1-READ UNCOMMITTED] Starting transaction 1.
```

### Updating
```
[Tx1-READ UNCOMMITTED] Updated Alice's balance by 100.00.
[Tx1-READ UNCOMMITTED] Alice balance updated. Not commited.
```

### Reading before & after *commit*
```
[Tx2-READ UNCOMMITTED (first read)] Alice's balance: 1100.00

[Tx1-READ UNCOMMITTED] Transaction 1 commited.
[Tx2-READ UNCOMMITTED (second read)] Alice's balance: 1100.00
```

### Explanation:
With **READ UNCOMMITED** isolation level it reads all changes, even not commited. 
So that it returns the same output - *1100.0*, and it is called **dirty read**.
