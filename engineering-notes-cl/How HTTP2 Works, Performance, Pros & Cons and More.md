# How HTTP2 Works, Performance, Pros & Cons and More

> Source: `How HTTP2 Works, Performance, Pros & Cons and More.txt` · Transcript 15 of 43

## 📝 Description
A detailed explanation of **how HTTP/2 works**, its pros and cons, and a performance comparison with HTTP/1.1 using sample code.

## ⚠️ Problem
HTTP/1.1 sends one request at a time per connection, so browsers open many connections and still stall. Headers repeat on every request, and text parsing is wasteful.

## ✅ Solution
HTTP/2 is a binary protocol that **multiplexes** many request/response streams over one TCP connection and compresses headers.

## 🔍 Explanation
1. **Binary framing:** messages are split into binary frames tagged with a stream id.
2. **Multiplexing:** many streams share one connection, so there is no need for many parallel TCP connections.
3. **Header compression (HPACK):** repeated headers like cookies are compressed.
4. **Server push:** the server can send resources before the client asks, which sounds great but is rarely used well.
5. **Support requirements:** both server and client (browser or library) must understand HTTP/2. Some clients and libraries don't.
6. **Cons:** still runs on TCP, so one lost packet stalls all streams (TCP-level head-of-line blocking). HTTP/3 over QUIC fixes this.
7. **Demo:** many parallel requests are faster over HTTP/2, but results depend on the network. Real-world gains include DNS and TLS costs.

## 💻 Relevant Code
Node.js HTTP/2 server (illustrative):
```js
const http2 = require("http2");
const fs = require("fs");
const server = http2.createSecureServer({
  key: fs.readFileSync("key.pem"), cert: fs.readFileSync("cert.pem")
});
server.on("stream", (stream, headers) => {
  stream.respond({ ":status": 200, "content-type": "text/plain" });
  stream.end("hello h2");
});
server.listen(8443);
```
Check the protocol used:
```bash
curl -I --http2 -k https://localhost:8443
```

## 🤖 Claude's Notes
- Browsers only use HTTP/2 over TLS in practice.
- Server push has been removed or deprecated in some browsers, so don't rely on it.

## 🎯 Key Takeaways
- One connection, many streams.
- Binary framing and header compression reduce overhead.
- TCP-level blocking remains, which HTTP/3 targets.

## ❓ Questions
1. What is multiplexing?
2. What does HPACK do?
3. Why can HTTP/2 still suffer from head-of-line blocking?

## 🔁 Follow-up Questions
1. How does HTTP/3 change the transport?
2. What happens when an HTTP/2 client talks to an HTTP/1.1-only server?

## 🤔 Questions to Think About
- Would HTTP/2 help an API with a handful of requests per page?
- Why did server push not take off?
