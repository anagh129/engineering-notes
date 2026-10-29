# Microservices Explained and their Pros & Cons

> Source: `Microservices Explained and their Pros & Cons.txt` · Transcript 24 of 43

## 📝 Description
Explains **microservices** by example: what they are, why companies like Twitter and Netflix adopted them, and the pros and cons.

## ⚠️ Problem
A large monolith, one codebase running on one port, becomes hard to change, deploy and scale, and forces everyone onto the same language and database.

## ✅ Solution
Break it into small services that communicate over the network (HTTP/REST or gRPC), each owned by a team and deployable on its own.

## 🔍 Explanation
1. **From call to network call:** what used to be a function call now goes over a network via GET/POST or gRPC.
2. **Pros:**
   - Teams pick their own language and database.
   - Independent deployment and scaling.
   - Smaller code bases that are easier to understand.
   - The common contract is HTTP, so anyone can call any service.
3. **Cons:**
   - Network latency and partial failures.
   - Harder debugging, tracing and testing.
   - Distributed data consistency.
   - More infrastructure: service discovery, proxying, monitoring.
4. **Not free:** a call that took nanoseconds can now take milliseconds and fail.

## 💻 Relevant Code
Monolith vs microservice call:
```js
// monolith
const price = pricing.calculate(cart);

// microservice
const price = await (await fetch("http://pricing-service/calculate", {
  method: "POST", body: JSON.stringify(cart)
})).json();
```

## 🤖 Claude's Notes
- Start with a well-structured monolith, and split services when team or scaling pain justifies it.
- Add timeouts, retries and circuit breakers to every network call.

## 🎯 Key Takeaways
- Microservices trade simplicity for independence.
- Every service boundary is a network boundary.
- Operational complexity grows quickly.

## ❓ Questions
1. What replaces a method call in a microservice architecture?
2. Name two benefits and two costs.
3. Why can each team choose its own language?

## 🔁 Follow-up Questions
1. How do services find each other?
2. How would you trace a request across ten services?

## 🤔 Questions to Think About
- At what team size does a monolith start to hurt?
- What would you split out first?
