# Is EventStoreDB the First Native gRPC Database

> Source: `Is EventStoreDB the First Native gRPC Database.txt` · Transcript 19 of 43

## 📝 Description
Looks at **EventStoreDB**, an event-sourcing database that exposes a **native gRPC** interface, and why that matters for database client protocols.

## ⚠️ Problem
Each database speaks its own wire protocol (Postgres, Redis, etc.), so every language needs a hand-built client that understands it. That's hard to write and hard to upgrade. Also, database connections are expensive and non-multiplexed, which is why we need pools.

## ✅ Solution
Use a database whose API is **gRPC** (built on HTTP/2): clients are generated from a schema in many languages, and HTTP/2 supports multiplexing.

## 🔍 Explanation
1. **gRPC:** Google's RPC protocol over HTTP/2, language-neutral, with generated clients.
2. **Event sourcing:** instead of storing just the current state, store the stream of events that led to it.
3. **Client pain:** protocol semantics (XMPP, Postgres, Redis wire protocols) require custom clients that are hard to maintain.
4. **Pooling digression:** because a database connection handles one query at a time, apps use a pool of connections. Multiplexing could reduce that need.
5. **The host's wish:** a database with a natively multiplexed protocol, and he admits he knows little about event sourcing and asks the audience.

## 💻 Relevant Code
No code in the video. Typical gRPC client shape (illustrative):
```js
const client = new EventStoreClient("esdb://localhost:2113?tls=false");
await client.appendToStream("orders", jsonEvent({ type: "OrderPlaced", data: { id: 1 } }));
```

## 🤖 Claude's Notes
- Whether it is "the first native gRPC database" is the host's belief. Check current claims yourself.
- gRPC runs on HTTP/2, so it still inherits TCP head-of-line blocking.

## 🎯 Key Takeaways
- gRPC lowers the cost of writing clients.
- Event sourcing stores changes, not only state.
- Multiplexed DB protocols could shrink connection pools.

## ❓ Questions
1. Why is writing a client for a custom DB protocol hard?
2. What is event sourcing?
3. Why does a database need connection pools today?

## 🔁 Follow-up Questions
1. What are the downsides of event sourcing?
2. How does gRPC streaming differ from request/response?

## 🤔 Questions to Think About
- Would you trade a hand-tuned binary protocol for a generated gRPC client?
- What breaks if one multiplexed connection carries many queries?
