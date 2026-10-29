# Watch out before Adding Indexes to Your Table, Your Database Optimizer Might not Use them

> Source: `Watch out before Adding Indexes to Your Table, Your Database Optimizer Might not Use them.txt` · Transcript 36 of 43

## 📝 Description
Shows how a database **optimizer chooses between multiple single-column indexes**, and why adding an index doesn't guarantee it will be used. The example is a table `t(f1, f2)` with an index on each, queried with `WHERE f1 = 1 AND f2 = 4`.

## ⚠️ Problem
You add indexes expecting faster queries, but the optimizer may ignore them, so you pay storage and write costs for nothing.

## ✅ Solution
Understand the optimizer's three typical choices and keep table **statistics** fresh.

## 🔍 Explanation
1. **Case 1, use both indexes:** search `f1_idx` for 1 and collect matching row ids. Search `f2_idx` for 4 and collect row ids. For an AND, intersect them, then fetch rows from the table. Worth it when each index returns a moderate number of rows.
2. **Case 2, use one index then filter:** use `f1_idx` only, fetch those rows, then check `f2 = 4` on them. Chosen when one index is very selective (a primary key is the extreme case) and the other returns many rows. Searching a B-tree isn't free.
3. **Case 3, ignore the indexes:** if the conditions match a large share of the table (e.g. three quarters), a table scan, possibly with parallel workers in Postgres, is cheaper.
4. **How it knows:** **table statistics**, approximate counts of values in the table. They aren't perfect and can be refreshed with `ANALYZE` (Oracle: gather statistics).
5. **Stale stats trap:** a fresh table has near-zero stats. If you bulk-insert millions of rows and query immediately without updating statistics, the optimizer plans as if the table were nearly empty and chooses badly.
6. **Scope:** this video excludes composite (multi-column) indexes.

## 💻 Relevant Code
```sql
CREATE TABLE t (f1 int, f2 int);
CREATE INDEX f1_idx ON t(f1);
CREATE INDEX f2_idx ON t(f2);

EXPLAIN SELECT * FROM t WHERE f1 = 1 AND f2 = 4;   -- Bitmap And, one index + filter, or Seq Scan
ANALYZE t;                                         -- refresh statistics after bulk loads
```

## 🤖 Claude's Notes
- In Postgres the "use both" plan appears as a **BitmapAnd** of two bitmap index scans.
- If you often filter by both columns, a **composite index** `(f1, f2)` is usually better than two separate ones.

## 🎯 Key Takeaways
- The optimizer may use both, one, or no indexes.
- Selectivity and statistics decide.
- Run `ANALYZE` after big data changes.

## ❓ Questions
1. When will the optimizer skip all indexes?
2. What are statistics and how are they refreshed?
3. Why might it use one index and filter on the other column?

## 🔁 Follow-up Questions
1. How is a bitmap AND different from a composite index?
2. How would you spot a bad plan caused by stale stats?

## 🤔 Questions to Think About
- Which indexes in your database are never used?
- What would the cost be of dropping them?
