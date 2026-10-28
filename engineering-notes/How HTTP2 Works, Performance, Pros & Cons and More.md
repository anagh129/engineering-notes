# How HTTP2 Works, Performance, Pros & Cons and More

## Description
A deep dive into HTTP/2 architectural mechanisms: binary framing, stream multiplexing over a single TCP connection, HPACK header compression, ALPN negotiation, and benchmark comparisons with HTTP/1.1.

---

## The Problem
HTTP/1.1 suffers from Head-of-Line (HoL) blocking at the application layer: only one request/response can be processed per TCP connection at a time. Browsers hack around this by opening up to 6 parallel TCP connections per host, causing socket bloat, high server memory usage, uncoordinated TCP slow starts, and massive latency on high-RTT networks.

---

## The Solution
HTTP/2 introduces a binary framing layer that multiplexes concurrent bidirectional streams over a single persistent TCP connection, compresses headers via HPACK, negotiates protocols during TLS handshake via ALPN, and supports server push.

---

## Detailed Explanation
1. **Binary Framing Layer**: Replaces plaintext ASCII HTTP/1.1 verbs and headers with typed binary frames (`HEADERS`, `DATA`, `SETTINGS`, `RST_STREAM`, etc.).
2. **Multiplexing & Stream IDs**:
   - Multiple requests and responses interleave concurrently over one TCP socket.
   - Each stream is tagged with an integer Stream ID (client-initiated streams use odd IDs, server-initiated use even IDs).
   - Eliminates application-layer Head-of-Line blocking.
3. **HPACK Compression**:
   - Maintains synchronized static tables (common headers like `:method: GET`) and dynamic tables (frequently repeated cookies/tokens) between client and server.
   - Drastically cuts header overhead compared to verbose ASCII headers repeated on every HTTP/1.1 request.
4. **ALPN (Application-Layer Protocol Negotiation)**:
   - HTTP/2 is negotiated inside the TLS handshake using ALPN extension bytes (`h2`), eliminating the need for an extra HTTP `Upgrade` round-trip and avoiding SSL-stripping attacks.
5. **Empirical Benchmarks**:
   - Loading 100 images on Fast 3G: HTTP/1.1 took ~10s; HTTP/2 finished in **~2.7s** (~73% faster).
   - On Slow 3G: HTTP/1.1 took ~35s; HTTP/2 finished in **~10s** (~71% faster).
6. **Drawbacks**:
   - **TCP-Level HoL Blocking**: Because HTTP/2 multiplexes everything over a single TCP pipe, dropping a single packet halts the entire TCP sliding window, stalling all concurrent HTTP/2 streams until retransmission completes.
   - **Server Push Complexities**: Often pushes resources already in browser cache, wasting bandwidth.

---

## Relevant Code & Configurations
```
// Node.js HTTP/2 Server Demonstration with TLS & Multiplexing
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt'),
  allowHTTP1: true // Fallback support
});

server.on('error', (err) => console.error(err));

server.on('stream', (stream, headers) => {
  const path = headers[':path'];
  const method = headers[':method'];

  console.log(`Received ${method} for ${path} on stream ID: ${stream.id}`);

  if (path === '/') {
    // Optionally initiate Server Push for critical assets
    if (stream.pushAllowed) {
      stream.pushStream({ ':path': '/style.css' }, (err, pushStream) => {
        if (!err) {
          pushStream.respond({ ':status': 200, 'content-type': 'text/css' });
          pushStream.end('body { background: #f0f0f0; }');
        }
      });
    }

    stream.respond({
      'content-type': 'text/html; charset=utf-8',
      ':status': 200
    });
    stream.end('<h1>HTTP/2 Multiplexed Response</h1>');
  } else {
    stream.respond({ ':status': 404 });
    stream.end('Not Found');
  }
});

server.listen(8443, () => console.log('HTTP/2 server listening on port 8443'));
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Why HTTP/2 Suffers on Lossy Networks (The QUIC Justification)
In clean network environments (fiber, modern broadband), HTTP/2 outperforms HTTP/1.1 massively. However, on lossy cellular networks with 2%+ packet drop rates, HTTP/2 can perform *worse* than HTTP/1.1. Why?
- Under HTTP/1.1 (with 6 parallel TCP connections), a dropped packet only blocks the 1 connection it belongs to; the other 5 continue streaming data.
- Under HTTP/2, all streams share 1 TCP stream buffer. The TCP stack cannot deliver byte $N+1$ to the application until byte $N$ is received in order. This single transport-level bottleneck stalled the entire multiplexed stream, motivating Google and the IETF to create **QUIC / HTTP/3** over UDP.

### Server Push Deprecation
Chrome and major browser engines formally disabled HTTP/2 Server Push by default in 2022. It suffered from "cache blindness" (servers pushing assets clients already cached) and prioritization contention. The modern replacement is RFC 8297 (`103 Early Hints`).

---

## Key Takeaways
- HTTP/2 solves application-layer Head-of-Line blocking by multiplexing binary frames over a single TCP socket using Stream IDs.
- HPACK compresses redundant headers using shared static and dynamic state tables.
- ALPN negotiates protocol version inside the TLS handshake, saving 1 RTT and preventing protocol downgrade attacks.
- TCP-level Head-of-Line blocking remains HTTP/2's primary Achilles heel, resolved only by HTTP/3 over UDP.

---

## Technical Interview Question
**Question**: What is the difference between Application-Layer Head-of-Line blocking in HTTP/1.1 and Transport-Layer Head-of-Line blocking in HTTP/2?

---

## Follow-up Question
**Follow-up**: How does HPACK maintain state between client and server, and why was gzip header compression in SPDY abandoned due to the CRIME vulnerability?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: If HTTP/2 multiplexes all requests onto a single connection, how should backend engineers size connection pools when communicating between microservices using gRPC/HTTP/2?
