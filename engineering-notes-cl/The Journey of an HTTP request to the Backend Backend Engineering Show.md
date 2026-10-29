# The Journey of an HTTP request to the Backend  Backend Engineering Show

> Source: `The Journey of an HTTP request to the Backend  Backend Engineering Show.txt` · Transcript 33 of 43

## 📝 Description
Follows the full **journey of an HTTP request** from the browser to the backend: DNS, TCP, TLS, how the request is delivered, and where proxies and load balancers fit.

## ⚠️ Problem
Engineers often treat "send a request" as one step, so they misdiagnose slowness and misconfigure nginx, HAProxy and other proxies.

## ✅ Solution
Understand each stage the request passes through, and what you can configure or measure at each.

## 🔍 Explanation
1. **Not only HTTP:** a front-end could use any protocol. Game developers build tiny custom protocols to avoid HTTP overhead. HTTP is just the most common.
2. **Before the request is sent:** DNS resolves the host name, a TCP connection is opened with the three-way handshake, and (for HTTPS) a TLS handshake follows.
3. **Sending:** the GET request is broken into segments, and the server acknowledges them. The backend can only process the request once the whole request arrives, so the client may wait even though the request hasn't truly been delivered yet.
4. **Proxy view:** with a load balancer or reverse proxy, the connection may be terminated and re-established, with timeouts, ciphers and buffering to configure.
5. **Why it matters:** this is the low-level knowledge you use when tuning nginx/HAProxy and diagnosing latency.

## 💻 Relevant Code
Observe each phase with curl:
```bash
curl -o /dev/null -s -w "dns:%{time_namelookup} tcp:%{time_connect} tls:%{time_appconnect} ttfb:%{time_starttransfer} total:%{time_total}\n" https://example.com
```

## 🤖 Claude's Notes
- The order is: DNS → TCP → TLS → HTTP request → server processing → response. Each can be a separate bottleneck.
- With HTTP/3 (QUIC), TCP and TLS setup are combined into fewer round trips.

## 🎯 Key Takeaways
- Several round trips happen before the server sees the request.
- A request is delivered in pieces and acknowledged.
- Proxies add their own connection, TLS and timeout behavior.

## ❓ Questions
1. List the steps before the server processes a request.
2. Why might the client wait even after sending data?
3. Where do proxies change this flow?

## 🔁 Follow-up Questions
1. How does TLS 1.3 reduce handshake round trips?
2. What does connection reuse skip?

## 🤔 Questions to Think About
- Which stage is the biggest for users far from your server?
- When would a custom protocol be worth it over HTTP?
