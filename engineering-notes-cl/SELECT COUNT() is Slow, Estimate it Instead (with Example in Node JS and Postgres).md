# SELECT COUNT() is Slow, Estimate it Instead (with Example in Node JS and Postgres)

> Source: `SELECT COUNT() is Slow, Estimate it Instead (with Example in Node JS and Postgres).txt` · Transcript 30 of 43

## 📝 Description
A Node.js + Postgres demo showing that counting a **300-million-row** table takes about **two minutes**, while an estimate from `EXPLAIN` takes about **300 ms**.

## ⚠️ Problem
An app can't wait minutes to show a single number (e.g. a view count), and many parallel counts tie up database connections.

## ✅ Solution
Run `EXPLAIN` on the query and parse the planner's row estimate instead of counting.

## 🔍 Explanation
1. **Baseline:** exact `COUNT(*)` on 300M rows took roughly two minutes.
2. **Bucket counts** such as "grades between 10 and 20" take just as long or longer.
3. **Estimate function:** run `EXPLAIN` through the same Postgres client and read the estimated rows from the plan text.
4. **Comparison:** the app ran many queries at once. Exact counts were slow, and estimates returned in about 300 ms total.
5. **Accuracy:** some buckets were very close, but one was off by roughly 800k. Whether that's acceptable depends on the use case.
6. **Bonus:** the estimate avoids long-running queries that hold connections.

## 💻 Relevant Code
```js
async function countEstimate(query) {
  const res = await pool.query("EXPLAIN " + query);
  for (const row of res.rows) {
    const m = /rows=(\d+)/.exec(row["QUERY PLAN"]);
    if (m) return parseInt(m[1], 10);     // first (top) node's estimate
  }
  return 0;
}

const n = await countEstimate("SELECT * FROM grades WHERE g BETWEEN 10 AND 20");
```

## 🤖 Claude's Notes
- Only build the SQL from trusted input. `EXPLAIN` with string concatenation is an injection risk.
- Refresh statistics (`ANALYZE`) regularly so estimates stay reasonable.

## 🎯 Key Takeaways
- Exact counts scale linearly with rows.
- Planner estimates are fast but approximate.
- Check the error margin against the product need.

## ❓ Questions
1. How is the estimate extracted from `EXPLAIN` output?
2. What can make the estimate inaccurate?
3. Why is the estimate faster?

## 🔁 Follow-up Questions
1. What alternatives exist, such as counter tables or HyperLogLog?
2. How would you choose between an estimate and a cached exact count?

## 🤔 Questions to Think About
- Would your users notice a 3% error in a count?
- What if the estimate is wildly wrong after a bulk load?
