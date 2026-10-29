# 7 Tips to Optimize Your Backend API Without Caching

> Source: `7 Tips to Optimize Your Backend API Without Caching.txt` · Transcript 2 of 43

## 📝 Description
Seven practical tips for speeding up a backend API **without caching**. The starting observation: the server may take 3 ms to run a request, while the client sees 700 ms. The rest of the time is lost in serialization, connections, protocols, proxies and the client.

## ⚠️ Problem
You can't find where the time goes. The handler is fast, but the user-visible latency is high.

## ✅ Solution
Check seven places where hidden latency lives, and fix the ones that apply.

## 🔍 Explanation
1. **Payload format:** serialization and deserialization cost grows with payload size. XML is worst, JSON is middling, and Protocol Buffers are best (when you can accept a rigid schema).
2. **Pre-heat connections:** a new connection per request pays the TCP three-way handshake plus TLS every time. Keep client connections open and reuse them.
3. **Use HTTP/2 (or HTTP/3):** HTTP/1.1 sends one request at a time per connection. HTTP/2 multiplexes many streams on one connection. QUIC also removes the TCP handshake.
4. **TCP "meltdown" and head-of-line blocking:** if a packet is lost, the sender must retransmit and everything behind it waits. It hurts most across continents. Reuse connections, keep servers near each other, or move to QUIC.
5. **Watch the proxies:** reverse proxies, load balancers, cache layers and sidecars (Linkerd, Envoy, Istio) each add a hop. An L7 proxy may terminate and re-establish TLS, so prefer an **L4** balancer if you don't need L7 features.
6. **Avoid large payloads:** big responses break into many packets that each need acknowledging. Don't `SELECT *` 700 fields when the client needs five.
7. **Client-side processing:** transformations the client does after receiving the response (extra scripts) add to perceived latency. Sometimes client work is better, so measure.

## 💻 Relevant Code
Reusing connections in Node (keep-alive agent) instead of a fresh connection per call:
```js
const https = require("https");
const agent = new https.Agent({ keepAlive: true, maxSockets: 50 });

https.get("https://api.example.com/items", { agent }, (res) => { /* ... */ });
```

## 🤖 Claude's Notes
- The mental model is a **latency budget**: server time + serialization + connection setup + network + proxy hops + client work. Measure each one, then optimize the biggest.
- Use the browser Network waterfall (see the *DevTools Waterfall* file) to see which slice is large.

## 🎯 Key Takeaways
- A fast handler does not mean a fast API.
- Reuse connections, shrink payloads and minimize hops.
- Prefer HTTP/2 or HTTP/3 and L4 balancing where acceptable.

## ❓ Questions
1. Name three costs paid when a client opens a new connection for every request.
2. Why can an L7 proxy add more latency than an L4 proxy?
3. Why do large payloads slow things down beyond serialization?

## 🔁 Follow-up Questions
1. How would you measure how much time is spent in each of the seven areas?
2. Which tip gives the biggest win for a mobile client on a weak network?

## 🤔 Questions to Think About
- Which of these tips would you skip because it makes your code more complex than the gain is worth?
- Where would caching help, and what are its costs?
