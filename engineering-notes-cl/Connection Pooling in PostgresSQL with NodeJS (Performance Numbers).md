# Connection Pooling in PostgresSQL with NodeJS (Performance Numbers)

> Source: `Connection Pooling in PostgresSQL with NodeJS (Performance Numbers).txt` · Transcript 9 of 43

## 📝 Description
Shows how to use **connection pooling** with PostgreSQL in Node.js (node-postgres), compares it with opening a connection on every request, and explains the pool settings.

## ⚠️ Problem
Opening a database connection is expensive (TCP handshake, TLS, authentication), and a database can only hold a limited number of connections. A REST API that connects, queries and disconnects on each request wastes time and may exhaust the DB.

## ✅ Solution
Create a **pool** of long-lived connections that all requests share.

## 🔍 Explanation
1. **Naive way:** each GET opens a new connection, runs a query and closes it. Slow and not scalable.
2. **Pool:** `pool.query()` borrows a free connection, runs the query and returns it automatically.
3. **When all are busy:** a client waits. **connectionTimeoutMillis** controls how long (default 0 = wait forever).
4. **Idle connections:** **idleTimeoutMillis** (default 10 s) closes connections that stay unused to free memory.
5. **Max size:** caps how many connections the pool may open.
6. **Transactions:** `pool.query` may use a different connection each call, so for multi-statement atomic work you check out one dedicated client with `pool.connect()`, run `BEGIN … COMMIT`, then `release()` it.

## 💻 Relevant Code
```js
const { Pool } = require("pg");
const pool = new Pool({
  host: "localhost", user: "postgres", database: "postgres",
  max: 20,                       // max connections
  connectionTimeoutMillis: 5000, // fail instead of waiting forever
  idleTimeoutMillis: 10000       // drop idle connections after 10 s
});

// simple query: pool picks a connection
const { rows } = await pool.query("SELECT * FROM employees LIMIT 10");

// transaction: pin one client
const client = await pool.connect();
try {
  await client.query("BEGIN");
  await client.query("UPDATE accounts SET bal = bal - 10 WHERE id = 1");
  await client.query("UPDATE accounts SET bal = bal + 10 WHERE id = 2");
  await client.query("COMMIT");
} catch (e) { await client.query("ROLLBACK"); throw e; }
finally { client.release(); }
```

## 🤖 Claude's Notes
- Always `release()` a checked-out client in a `finally` block, or the pool leaks and eventually hangs.
- Pool size should reflect what the database can handle, not what your app wants. More is not always faster.

## 🎯 Key Takeaways
- Pooling avoids repeated connection setup cost.
- Know the three settings: max, connection timeout, idle timeout.
- Use a dedicated client for transactions.

## ❓ Questions
1. What costs does a pool avoid?
2. What does a connection timeout of 0 mean?
3. Why can't `pool.query` run a transaction safely?

## 🔁 Follow-up Questions
1. How would you pick a good `max` value?
2. What happens to queued requests when the database is slow?

## 🤔 Questions to Think About
- If you run 50 app instances each with a pool of 20, what is the DB seeing?
- Would an external pooler (like PgBouncer) change your design?
