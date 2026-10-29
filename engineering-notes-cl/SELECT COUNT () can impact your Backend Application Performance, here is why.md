# SELECT COUNT () can impact your Backend Application Performance, here is why

> Source: `SELECT COUNT () can impact your Backend Application Performance, here is why.txt` · Transcript 29 of 43

## 📝 Description
Explains why **`SELECT COUNT()`** gets slow on big tables, why even index-only scans can be slow, and when an **estimate** is a good alternative. The demo table is `grades` with about 60 million rows.

## ⚠️ Problem
Counting means the database must walk many index entries or heap rows. On large tables this is slow, and running it often hurts the database and the app.

## ✅ Solution
If you don't need an exact number, take the planner's **estimated row count** from `EXPLAIN` instead.

## 🔍 Explanation
1. **Exact counts:** `SELECT COUNT(g) FROM grades WHERE id BETWEEN 1000 AND 4000` looks fast only because of caching.
2. **Index-only scan still hits the heap:** Postgres checks the **visibility map**. If rows may have been updated or deleted, the scan must go back to the table to verify them. This is the extra work, which can run to thousands of heap fetches.
3. **Estimate:** `EXPLAIN` returns the planner's estimated row count, which comes from table statistics.
4. **UX argument:** if the real number is in the millions, nobody needs "60,000,320". Showing about 60 million is enough.
5. **Guideline:** use exact counts for small tables, and estimates when the table can grow into the millions.

## 💻 Relevant Code
```sql
-- exact (slow on huge tables)
SELECT COUNT(*) FROM grades WHERE g BETWEEN 10 AND 20;

-- estimate
EXPLAIN SELECT * FROM grades WHERE g BETWEEN 10 AND 20;   -- read "rows=" from the plan
```

## 🤖 Claude's Notes
- `VACUUM` updates the visibility map, which makes index-only scans cheaper.
- For whole-table totals, `SELECT reltuples FROM pg_class WHERE relname='grades'` is an even cheaper estimate.

## 🎯 Key Takeaways
- COUNT is O(rows touched), and it's expensive at scale.
- Index-only scans may still visit the table.
- Often an estimate is good enough.

## ❓ Questions
1. Why can an index-only scan still read the table?
2. What produces the estimate?
3. When is an exact count still needed?

## 🔁 Follow-up Questions
1. How does `ANALYZE` affect estimates?
2. What does `VACUUM` do for index-only scans?

## 🤔 Questions to Think About
- Where in your product are users shown an exact count they don't need?
- How would you keep a cached count in sync?
