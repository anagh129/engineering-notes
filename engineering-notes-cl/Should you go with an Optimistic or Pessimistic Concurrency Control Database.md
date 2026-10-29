# Should you go with an Optimistic or Pessimistic Concurrency Control Database

> Source: `Should you go with an Optimistic or Pessimistic Concurrency Control Database.txt` · Transcript 31 of 43

## 📝 Description
Compares **optimistic and pessimistic concurrency control** in databases and why the choice shapes which database fits your workload.

## ⚠️ Problem
When many transactions touch the same data, you must prevent lost updates and inconsistent reads without crippling performance.

## ✅ Solution
Choose between **locking first** (pessimistic) and **detecting conflicts at commit** (optimistic), depending on how often conflicts happen.

## 🔍 Explanation
1. **Pessimistic:** lock the rows before using them. Others wait. Safe, but lock management is expensive and can cause waits and deadlocks.
2. **Optimistic:** don't lock. Do the work, then check at commit (e.g. a version or timestamp) whether someone else changed the data. If so, abort and retry. Works well when conflicts are rare.
3. **Cost of locks:** the database must track every locked row, usually in memory. A transaction touching a million rows needs a million lock records, and memory is not free. So many databases avoid row-level locks or escalate them (e.g. to a table lock).
4. **Why it matters:** this choice often decides which database you pick.
5. **Host note:** engines evolve (e.g. MongoDB changes) and viewer comments keep sharpening the discussion.

## 💻 Relevant Code
Pessimistic (Postgres):
```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;   -- lock
UPDATE accounts SET bal = bal - 10 WHERE id = 1;
COMMIT;
```
Optimistic (version column):
```sql
UPDATE accounts SET bal = bal - 10, version = version + 1
WHERE id = 1 AND version = 7;     -- 0 rows updated => someone else changed it, retry
```

## 🤖 Claude's Notes
- High contention favors pessimistic locking. Low contention favors optimistic.
- MVCC databases (Postgres, MySQL InnoDB) already give readers snapshots without read locks, and then add locks for writers.

## 🎯 Key Takeaways
- Pessimistic = lock now, optimistic = check later.
- Locks cost memory and concurrency.
- Pick by expected conflict rate.

## ❓ Questions
1. How does an optimistic update detect a conflict?
2. Why are row-level locks expensive?
3. When does pessimistic locking win?

## 🔁 Follow-up Questions
1. What is lock escalation?
2. How does MVCC relate to these two strategies?

## 🤔 Questions to Think About
- For a collaborative editor, which strategy fits and why?
- How many retries before optimistic control becomes worse than locking?
