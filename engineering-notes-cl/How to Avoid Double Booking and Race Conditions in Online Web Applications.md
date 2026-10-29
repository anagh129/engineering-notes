# How to Avoid Double Booking and Race Conditions in Online Web Applications

> Source: `How to Avoid Double Booking and Race Conditions in Online Web Applications.txt` · Transcript 18 of 43

## 📝 Description
How to build an online seat-booking system (Express, Node.js, Postgres) that **prevents double booking** when two people try to book the same seat at nearly the same instant, using **exclusive row locks**.

## ⚠️ Problem
The common approach is: begin a transaction, `SELECT` the seat to check it is free, then `UPDATE` it to booked. Two requests can both pass the check before either updates, so both succeed and the seat is double-booked. This is a **race condition**.

## ✅ Solution
Take an **exclusive lock** on the row as part of the read: `SELECT ... FOR UPDATE`. The second transaction must wait until the first commits, then sees that the seat is already booked.

## 🔍 Explanation
1. **Naive logic:** get a client from the pool, `BEGIN`, `SELECT * FROM seats WHERE id=$1 AND isbooked=0`; if zero rows, return "already booked"; otherwise `UPDATE`, `COMMIT`.
2. **Why it fails:** the host pauses the first request in the debugger right after the SELECT. A second client books the same seat. Releasing the first lets it also update, and both get "booked successfully".
3. **The fix:** add `FOR UPDATE` to the SELECT. Postgres locks that row, and anyone else selecting it for update waits.
4. **Demo:** the first request holds the lock. The second hangs. After the first commits, the second proceeds, finds the seat taken, and returns "couldn't book".
5. **Limitation:** in Postgres the wait is indefinite by default (the host notes Oracle lets you specify a wait time). A long lock hold means a bad user experience, though real transactions take only milliseconds.

## 💻 Relevant Code
```js
app.put("/:id/:name", async (req, res) => {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const r = await client.query(
      "SELECT * FROM seats WHERE id = $1 AND isbooked = 0 FOR UPDATE", [req.params.id]);
    if (r.rowCount === 0) { await client.query("ROLLBACK"); return res.send({ error: "Seat already booked" }); }
    await client.query("UPDATE seats SET isbooked = 1, name = $2 WHERE id = $1",
      [req.params.id, req.params.name]);
    await client.query("COMMIT");
    res.send({ ok: true });
  } catch (e) { await client.query("ROLLBACK"); res.sendStatus(500); }
  finally { client.release(); }
});
```

## 🤖 Claude's Notes
- Alternatives: `FOR UPDATE NOWAIT` / `SKIP LOCKED` (Postgres) to avoid waiting, or a single atomic statement: `UPDATE seats SET isbooked=1 WHERE id=$1 AND isbooked=0` and check the affected row count.
- A unique constraint (e.g. on seat+show) is another strong guard.

## 🎯 Key Takeaways
- Check-then-update across two statements is a race.
- `SELECT ... FOR UPDATE` serializes access to the row.
- Locks trade concurrency for correctness, so keep transactions short.

## ❓ Questions
1. Why do two users both pass the availability check?
2. What does `FOR UPDATE` do to the second transaction?
3. Why keep transactions short?

## 🔁 Follow-up Questions
1. How would `NOWAIT` change the user experience?
2. Could a single `UPDATE ... WHERE isbooked=0` replace the SELECT?

## 🤔 Questions to Think About
- What happens at huge scale when thousands try to book one seat (a hot row)?
- How would you handle a payment step that takes seconds while a seat is reserved?
