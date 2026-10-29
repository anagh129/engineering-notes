# Long Polling and how it differs from Push, Poll and SSE - The Backend Engineering Show

> Source: `Long Polling and how it differs from Push, Poll and SSE - The Backend Engineering Show.txt` · Transcript 23 of 43

## 📝 Description
Compares **polling, long polling, push and Server-Sent Events (SSE)** as ways for a client and server to exchange updates, and demystifies the terms.

## ⚠️ Problem
A client needs to find out when something new happens on the server (a message, a notification, a job result). Plain request/response only answers when asked.

## ✅ Solution
Choose a delivery pattern that fits: polling, long polling, push or SSE.

## 🔍 Explanation
1. **Polling:** the client repeatedly asks "anything new?". It's simple but wasteful (many empty responses) and has latency up to the interval.
2. **Push:** the server sends data the moment it is available over a persistent connection (e.g. WebSockets, AMQP). Efficient and low-latency, but needs a stateful connection.
3. **Long polling:** the client sends a request and the server **holds it open** until data arrives or a timeout hits, then the client immediately asks again. Fewer empty responses than polling, and works over normal HTTP.
4. **SSE:** a one-way stream from server to client over HTTP.
5. **Scale insight:** the YouTube bell example. Pushing a notification to every subscriber of a huge channel is expensive, which is why systems don't always notify everyone instantly.
6. **The host's point:** this is "just requests, responses and packets", so avoid hiding simple ideas behind fancy words.

## 💻 Relevant Code
Long polling client:
```js
async function poll() {
  while (true) {
    try {
      const res = await fetch("/events?since=" + lastId);   // server holds this open
      if (res.status === 200) handle(await res.json());
    } catch (e) { await new Promise(r => setTimeout(r, 1000)); }
  }
}
```
SSE client:
```js
const es = new EventSource("/stream");
es.onmessage = (e) => console.log(e.data);
```

## 🤖 Claude's Notes
- Long polling still ties up a server connection per waiting client, so the server must handle many idle connections.
- SSE gets automatic reconnect for free in browsers.

## 🎯 Key Takeaways
- Polling asks repeatedly, push delivers immediately.
- Long polling = held-open request.
- SSE = one-way server stream over HTTP.

## ❓ Questions
1. How does long polling reduce wasted requests?
2. When would you choose SSE over WebSockets?
3. What is the main cost of push?

## 🔁 Follow-up Questions
1. What timeout should a long-poll request use?
2. How do you avoid missing events between two long-poll requests?

## 🤔 Questions to Think About
- Which pattern fits a chat app, a stock ticker and a job-status page?
- How would you scale push to millions of clients?
