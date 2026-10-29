# Uber’s new Backend Architecture for Processing Payments

> Source: `Uber’s new Backend Architecture for Processing Payments.txt` · Transcript 35 of 43

## 📝 Description
Reviews Uber Engineering's article on **moving money at scale with strong data consistency**. The host likes it because it explains architecture, not tools.

## ⚠️ Problem
Payments must be strongly consistent: debit one account and credit another without losing, duplicating or half-applying money, across a global system. A trip involves fares, service fees, tips and adjustments.

## ✅ Solution
Model the work as **jobs → orders → order entries**, executed by processors and schedulers that can safely retry and reconcile.

## 🔍 Explanation
1. **The classic way:** a single ACID database where one transaction debits and credits (atomicity, isolation). Simple and strong on one instance.
2. **At global scale:** options include strongly consistent global databases (Spanner uses atomic clocks to order transactions, FaunaDB writes slowly for strong guarantees) or relaxing guarantees (but you don't want eventual consistency for money).
3. **Uber's approach:** a **job/order-based** system. A *job* is something like a trip, an *order* is a payment that needs to happen, and *order entries* are the individual pieces.
4. **Order tray and processors:** work sits in a queue-like order tray, and processors execute it. A **settlement scheduler** picks up money that was never paid or settled.
5. **Similarity to sagas:** breaking work into steps with managed states reaches consistency by finishing the whole series, though the article doesn't mention microservices or sagas.
6. **Host's praise:** it names no Kafka, RabbitMQ or Kubernetes. Any computer-science professor could understand it. His belief: you should understand how every component in your system works, within your role.

## 💻 Relevant Code
No code in the article or video. A minimal idempotent-order sketch:
```sql
-- each order has a unique key so retries can't double-charge
INSERT INTO orders (idempotency_key, job_id, amount, state)
VALUES ($1, $2, $3, 'PENDING')
ON CONFLICT (idempotency_key) DO NOTHING;
```

## 🤖 Claude's Notes
- The core ideas for money systems: **idempotency**, **an append-only ledger**, **state machines** for each order, and **reconciliation** jobs.
- Don't copy this design without understanding its failure modes. Uber's details are far richer than this summary.

## 🎯 Key Takeaways
- Money needs strong consistency.
- Break work into jobs, orders and entries with explicit states.
- Retry-safe processing and schedulers recover unfinished work.
- Explain architecture without hiding behind tools.

## ❓ Questions
1. Why is eventual consistency risky for payments?
2. What are a job, an order and an order entry?
3. What does the settlement scheduler do?

## 🔁 Follow-up Questions
1. How does an idempotency key prevent double charging?
2. How does Spanner's approach differ from Uber's?

## 🤔 Questions to Think About
- Where would you place the boundary of a single ACID transaction in a payments system?
- How would you audit that no money was lost?
