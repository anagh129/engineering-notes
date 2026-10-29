# CQRS is probably the cause of the Microservices madness

> Source: `CQRS is probably the cause of the Microservices madness.txt` · Transcript 8 of 43

## 📝 Description
Explains **CQRS** (Command Query Responsibility Segregation) in simple terms and argues that pushing the idea too far may have produced today's microservices sprawl.

## ⚠️ Problem
A single service and database that handles both reads and writes can't be optimized for either. Writes want a transactional row-store, and reads (reports, recommendations) want different shapes and scale.

## ✅ Solution
**Separate reads from writes**, in stages: separate endpoints/services, then separate databases, scaled independently.

## 🔍 Explanation
1. **No separation:** one customer service has add/update/get/recommendation endpoints on one OLTP row-store database.
2. **Partial separation:** split into a write service and a read service.
3. **Separate databases:** writes go to the OLTP database, and reads come from an OLAP/column-store (or a replica) that suits analytics.
4. **Benefits:** security (the read service gets read-only access), performance, and scalability (e.g. 300 read instances, a few replicated or partitioned writers).
5. **Cons:** very similar to microservices: more complexity, eventual consistency between the write and read sides, more things to operate.
6. **The host's opinion:** the idea is good and he suspects it helped give birth to microservices, but the "all-the-way" version is a monster. Know it, pick what helps and don't go nuts.

## 💻 Relevant Code
No code in the video. A tiny illustration of the split:
```js
// write side: strongly consistent
app.post("/customers", async (req, res) => { await writeDb.insert(req.body); res.sendStatus(201); });

// read side: separate service/db, possibly slightly stale
app.get("/customers/:id", async (req, res) => res.json(await readDb.find(req.params.id)));
```

## 🤖 Claude's Notes
- CQRS ≠ event sourcing, though they are often combined.
- The cost to watch is **replication lag**: users may write and then read stale data from the read side.

## 🎯 Key Takeaways
- Separate reading from writing only when you have a reason.
- Different databases can serve each side best.
- Extreme separation brings microservice-style complexity.

## ❓ Questions
1. What is the simplest first step toward CQRS?
2. Why might the read side use a column-store?
3. What new consistency issue appears?

## 🔁 Follow-up Questions
1. How would you keep the read database in sync with the write database?
2. How do you handle "read your own writes" for a user?

## 🤔 Questions to Think About
- Does your app really have a reads-vs-writes imbalance big enough to justify this?
- What would you lose by going back to one database?
