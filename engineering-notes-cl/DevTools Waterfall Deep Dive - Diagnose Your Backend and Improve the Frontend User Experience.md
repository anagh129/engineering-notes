# DevTools Waterfall Deep Dive - Diagnose Your Backend and Improve the Frontend User Experience

> Source: `DevTools Waterfall Deep Dive - Diagnose Your Backend and Improve the Frontend User Experience.txt` · Transcript 10 of 43

## 📝 Description
A guided tour of the **Chrome DevTools Network waterfall**, using it to diagnose backend and frontend performance on several sites (plain HTTP, HTTPS, an HTTP/1.1 site and an HTTP/3/QUIC site).

## ⚠️ Problem
A page feels slow, and you don't know whether the cause is DNS, connection setup, the backend, the payload or the browser.

## ✅ Solution
Read the waterfall. Each request is a bar divided into phases, and the longest segment tells you where to look.

## 🔍 Explanation
1. **Phases:** Queueing/Stalled, DNS lookup, Initial connection (TCP), SSL (TLS), Request sent, **Waiting (TTFB)**, Content download.
2. **Plain HTTP page:** one resource, no SSL segment. **HTTPS** adds a visible SSL segment.
3. **HTTP/1.1 site:** browsers allow a limited number of parallel connections per host, so requests are queued and stalled waiting for a free TCP connection. This shows up as a stair-step pattern.
4. **New connections** show their own initial-connection and SSL time, and reused connections skip them.
5. **Long Waiting (TTFB)** points to the backend, while **long Content download** points to payload size or bandwidth.
6. **HTTP/2 and HTTP/3** multiplex requests, which flattens the stair-steps.

## 💻 Relevant Code
You can read the same timing data programmatically in the browser:
```js
const [nav] = performance.getEntriesByType("navigation");
console.log({
  dns: nav.domainLookupEnd - nav.domainLookupStart,
  tcp: nav.connectEnd - nav.connectStart,
  ttfb: nav.responseStart - nav.requestStart,
  download: nav.responseEnd - nav.responseStart,
});
```

## 🤖 Claude's Notes
- "Stalled" is often about browser connection limits, not the server.
- Test with cache disabled and also with throttling to see real-user conditions.

## 🎯 Key Takeaways
- The waterfall splits latency into phases, so you can blame the right layer.
- HTTP/1.1 queues requests, while HTTP/2 and HTTP/3 reduce that.
- TTFB ≈ backend time, download ≈ payload and network.

## ❓ Questions
1. Which phase would you check first to blame the backend?
2. Why do HTTP/1.1 requests stall?
3. What does the SSL segment represent?

## 🔁 Follow-up Questions
1. How would connection reuse change the waterfall for the second request?
2. How can a CDN change each phase?

## 🤔 Questions to Think About
- If TTFB is low but the page is still slow, what else could be happening?
- Which famous site would you profile next and what would you expect?
