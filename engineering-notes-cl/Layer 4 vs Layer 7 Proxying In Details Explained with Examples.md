# Layer 4 vs Layer 7 Proxying In Details Explained with Examples

> Source: `Layer 4 vs Layer 7 Proxying In Details Explained with Examples.txt` · Transcript 20 of 43

## 📝 Description
A detailed comparison of **Layer 4 vs Layer 7 reverse proxying**, using a proxy with two backends. Layer 7 is explained first, then Layer 4.

## ⚠️ Problem
You must decide how a proxy should handle traffic: just forward bytes, or understand the application protocol. Each choice affects speed, features and security.

## ✅ Solution
Pick the proxy layer according to what you need. L4 for speed and simplicity, L7 for smart routing and manipulation.

## 🔍 Explanation
1. **Terminology:** HAProxy `mode tcp` = L4 and `mode http` = L7. nginx `stream` context = L4 and `http` context = L7.
2. **Layer 7 (application):** the proxy terminates the client connection, reads the whole HTTP request, then opens its own connection to a backend. It can route by path/headers/cookies, cache, rewrite and inspect. It must buffer and parse, so it costs more CPU and memory, and TLS is decrypted at the proxy.
3. **Layer 4 (transport):** the proxy picks a backend per TCP connection and forwards the stream without understanding HTTP. Faster and simpler, but no content-based routing. Because one connection maps to one backend, all requests on that connection hit the same server.
4. **TLS:** L4 can pass encrypted traffic straight through, while L7 must terminate it to read content.
5. **The host's stance:** both have pros and cons, and he invites disagreement.

## 💻 Relevant Code
```conf
# HAProxy L4
frontend tcp_in
    mode tcp
    bind *:80
    default_backend app
backend app
    mode tcp
    server s1 127.0.0.1:2222

# nginx L4 (stream context)
stream { server { listen 80; proxy_pass 127.0.0.1:2222; } }
```

## 🤖 Claude's Notes
- With L4 and HTTP keep-alive, load can become unbalanced because balancing happens per connection, not per request.
- L7 gives you rate limiting, auth, WAF rules and path routing.

## 🎯 Key Takeaways
- L4 = bytes and connections, L7 = application requests.
- L7 flexibility costs CPU and exposes decrypted data.
- Know each tool's naming (tcp/http, stream/http).

## ❓ Questions
1. Which layer can route /api and /images separately?
2. Why is L4 usually faster?
3. Why must L7 terminate TLS?

## 🔁 Follow-up Questions
1. Why can L4 balancing be uneven with HTTP/2 or keep-alive?
2. Can you chain an L4 proxy in front of an L7 proxy?

## 🤔 Questions to Think About
- Is the security of encrypted pass-through worth losing L7 features?
- Which layer fits a database proxy?
