# Load Balance multiple RTMP Servers to Horizontally Scale Streaming (Node Media Server and HAProxy)

> Source: `Load Balance multiple RTMP Servers to Horizontally Scale Streaming (Node Media Server and HAProxy).txt` · Transcript 21 of 43

## 📝 Description
Builds a **horizontally scaled live-streaming setup**: multiple RTMP servers (Node Media Server), OBS pushing a stream into one server, a relay copying it to others, and **HAProxy** load balancing the viewers.

## ⚠️ Problem
One RTMP server can only serve a limited number of viewers and is a single point of failure.

## ✅ Solution
Run several RTMP servers, relay the incoming stream to all of them, and put an L4 load balancer in front for viewers.

## 🔍 Explanation
1. **RTMP:** Real-Time Messaging Protocol, widely used by OBS for streaming.
2. **Ingest:** OBS streams to the main server on port 1935 (the `live` app).
3. **Relay:** the main server uses **ffmpeg** to push the stream to the other servers (the demo uses ports 1936 and 1937).
4. **Viewers:** connect to HAProxy, which spreads them across the RTMP servers at **Layer 4** (TCP).
5. **Why L4:** RTMP is not HTTP, so a TCP-level balancer is the natural fit.
6. **Result:** capacity grows by adding edge servers. The host notes it's not perfect, and there are other options like WebSocket streaming.

## 💻 Relevant Code
Node Media Server relay config (illustrative):
```js
const NodeMediaServer = require("node-media-server");
const config = {
  rtmp: { port: 1935, chunk_size: 60000, gop_cache: true, ping: 30, ping_timeout: 60 },
  relay: { ffmpeg: "/usr/local/bin/ffmpeg", tasks: [
    { app: "live", mode: "push", edge: "rtmp://localhost:1936" },
    { app: "live", mode: "push", edge: "rtmp://localhost:1937" } ] }
};
new NodeMediaServer(config).run();
```
HAProxy TCP balancing:
```conf
frontend rtmp_in
    mode tcp
    bind *:1940
    default_backend rtmp_servers
backend rtmp_servers
    mode tcp
    server s1 127.0.0.1:1936
    server s2 127.0.0.1:1937
```

## 🤖 Claude's Notes
- The origin server is still a single point of failure for ingest. Production setups add redundant ingest.
- For large scale, CDNs and HLS/DASH are usually used instead of raw RTMP for viewers.

## 🎯 Key Takeaways
- Relay the stream to every edge so any edge can serve any viewer.
- An L4 balancer is enough for non-HTTP protocols like RTMP.
- Scale viewers by adding edge servers.

## ❓ Questions
1. Why must the ingest stream be relayed to each server?
2. Why use L4 instead of L7 here?
3. What is ffmpeg's role?

## 🔁 Follow-up Questions
1. How would you make ingest highly available?
2. How do HLS and RTMP differ for viewers?

## 🤔 Questions to Think About
- How many viewers can one edge handle, and how would you find out?
- What happens to viewers when an edge dies mid-stream?
