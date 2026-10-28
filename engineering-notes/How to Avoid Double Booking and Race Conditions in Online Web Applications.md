# How to Avoid Double Booking and Race Conditions in Online Web Applications

## Description
Comprehensive guide to preventing double-booking and race conditions in concurrent web systems using PostgreSQL transactions, pessimistic row-level locking (`SELECT ... FOR UPDATE`), and optimistic concurrency controls.

---

## The Problem
In concurrent booking applications (seat reservations, inventory checkouts, hotel booking), two users simultaneously check out the exact same resource. The naive 'Check-then-Act' pattern (`SELECT` to verify availability, followed by `UPDATE`) fails under concurrency because both requests see the seat available before either updates it, resulting in double booking.

---

## The Solution
Enforce atomic transaction boundaries using pessimistic row-level locking via `SELECT ... FOR UPDATE`. This locks the target row immediately, forcing concurrent requests to wait until the first transaction commits or rolls back.

---

## Detailed Explanation
1. **The Classic 'Check-Then-Act' Race Condition**:
   - User A executes: `SELECT * FROM seats WHERE id = 15 AND is_booked = 0;` (Returns 1 row - Available).
   - User B executes: `SELECT * FROM seats WHERE id = 15 AND is_booked = 0;` (Returns 1 row - Available).
   - User A executes: `UPDATE seats SET is_booked = 1, user_name = 'Alice' WHERE id = 15;`
   - User B executes: `UPDATE seats SET is_booked = 1, user_name = 'Bob' WHERE id = 15;`
   - Both receive 'Booked successfully!' messages, but Alice's reservation is overwritten by Bob.
2. **Pessimistic Locking Solution (`SELECT ... FOR UPDATE`)**:
   - Inside an explicit transaction, query the row with `FOR UPDATE`.
   - The database engine places an exclusive lock on that specific row.
   - User B's transaction is blocked at the database engine level until User A commits or rolls back.
   - When User A commits, User B unblocks and re-evaluates the query. Since `is_booked` is now `1`, the query returns 0 rows, safely rejecting User B's attempt.
3. **Optimistic Locking Alternative**:
   - Add a `version` integer column.
   - Execute: `UPDATE seats SET is_booked = 1, version = version + 1 WHERE id = 15 AND version = 3;`
   - If affected row count is 0, another process updated the record; reject or retry.

---

## Relevant Code & Configurations
```
// Resilient Booking Handler in Node.js with PostgreSQL Pessimistic Locking
const { Pool } = require('pg');
const pool = new Pool();

async function bookSeat(seatId, customerName) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');

    // 1. Acquire exclusive row lock on seat
    // Optional: Add NOWAIT or SKIP LOCKED to fail immediately without blocking
    const checkQuery = `
      SELECT id, is_booked 
      FROM seats 
      WHERE id = $1 AND is_booked = 0 
      FOR UPDATE
    `;
    const checkRes = await client.query(checkQuery, [seatId]);

    if (checkRes.rows.length === 0) {
      await client.query('ROLLBACK');
      return { success: false, message: 'Seat already booked or unavailable' };
    }

    // 2. Safe to update
    const updateQuery = `
      UPDATE seats 
      SET is_booked = 1, user_name = $1 
      WHERE id = $2
    `;
    await client.query(updateQuery, [customerName, seatId]);

    await client.query('COMMIT');
    return { success: true, message: 'Seat booked successfully' };
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Avoiding Indefinite Blocking: `NOWAIT` & `SKIP LOCKED`
By default, `SELECT ... FOR UPDATE` waits indefinitely until the lock is released. In high-traffic ticket flash sales, this can exhaust connection pools.
PostgreSQL provides two powerful modifiers:
1. `FOR UPDATE NOWAIT`: If the row is currently locked, fail immediately with an exception instead of waiting.
2. `FOR UPDATE SKIP LOCKED`: Useful for job queue processing. It skips locked rows and locks the next available unlocked row.

---

## Key Takeaways
- The 'Check-then-Act' pattern is inherently vulnerable to race conditions under concurrent load.
- Pessimistic locking with `SELECT ... FOR UPDATE` acquires an exclusive row-level database lock.
- Transactions must be committed or rolled back promptly to avoid blocking concurrent database connections.
- Use `NOWAIT` or optimistic locking to prevent connection pool exhaustion during high contention.

---

## Technical Interview Question
**Question**: What is the difference between Pessimistic Locking (`SELECT FOR UPDATE`) and Optimistic Locking (version checking), and when should each be used?

---

## Follow-up Question
**Follow-up**: How does `SKIP LOCKED` enable high-concurrency background worker queues in PostgreSQL without race conditions?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: If a distributed system uses multiple microservices to reserve a flight seat, a hotel room, and a rental car in one user checkout, how do you prevent race conditions across all three without distributed deadlocks?
