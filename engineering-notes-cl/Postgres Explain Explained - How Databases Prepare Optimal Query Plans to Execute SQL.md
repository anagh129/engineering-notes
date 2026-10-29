# Postgres Explain Explained - How Databases Prepare Optimal Query Plans to Execute SQL

> Source: `Postgres Explain Explained - How Databases Prepare Optimal Query Plans to Execute SQL.txt` · Transcript 27 of 43

## 📝 Description
Explains the Postgres **`EXPLAIN`** command on a ~200-million-row `grades` table (columns: id, grade, name) with indexes on id and grade but not on name.

## ⚠️ Problem
You don't know how Postgres will execute a query or why it is slow.

## ✅ Solution
Use `EXPLAIN` to see the **query plan** the planner chose, including scan types and cost estimates.

## 🔍 Explanation
1. **Purpose:** `EXPLAIN` shows the plan for a statement without running it.
2. **Read plans inside-out:** start from the innermost node and move up, not from the top line.
3. **Node types:** Seq Scan, **Parallel Seq Scan**, Index Scan, Index Only Scan, Sort.
4. **Cost numbers:** startup cost, total cost, estimated rows and row width. These are estimates in planner units, not milliseconds.
5. **Example `SELECT *`:** the "worst query", which reads the entire table.
6. **Sort on an unindexed column (`name`):** the planner must scan the heap, pull everything, then sort, which is expensive.
7. **Next step:** `EXPLAIN ANALYZE` actually runs the query and shows real timings (planned for another video).

## 💻 Relevant Code
```sql
EXPLAIN SELECT * FROM grades;
EXPLAIN SELECT * FROM grades WHERE id = 100;               -- index scan
EXPLAIN SELECT * FROM grades ORDER BY name;                -- parallel seq scan + sort
EXPLAIN ANALYZE SELECT * FROM grades WHERE id < 1000;      -- real timings
```

## 🤖 Claude's Notes
- Compare estimated vs actual rows in `EXPLAIN ANALYZE`. A large gap usually means stale statistics (run `ANALYZE`).
- `EXPLAIN ANALYZE` on INSERT/UPDATE/DELETE really executes them, so wrap in a transaction and roll back.

## 🎯 Key Takeaways
- Read the plan from the inside out.
- Costs are relative estimates.
- Unindexed sorts and scans are the usual culprits.

## ❓ Questions
1. What does `EXPLAIN` do without `ANALYZE`?
2. Why read plans bottom-up/inside-out?
3. Why is sorting by an unindexed column expensive?

## 🔁 Follow-up Questions
1. What is the difference between Index Scan and Index Only Scan?
2. What does `EXPLAIN (ANALYZE, BUFFERS)` add?

## 🤔 Questions to Think About
- When would the planner pick a sequential scan even if an index exists?
- How would you decide whether to add an index on `name`?
