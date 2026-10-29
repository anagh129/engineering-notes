# Load balancing in Layer 4 vs Layer 7 with HAPROXY Examples

> Source: `Load balancing in Layer 4 vs Layer 7 with HAPROXY Examples.txt` · Transcript 22 of 43

## 📝 Description
Explains **Layer 4 vs Layer 7 load balancing** and implements both with HAProxy, including the pros and cons of each.

## ⚠️ Problem
Requests must be spread across several backend machines, but the way you balance (per connection or per request) changes what you can do.

## ✅ Solution
A load balancer is a reverse proxy. Use **L4** for fast, simple, protocol-agnostic balancing, and **L7** when you need content-aware routing.

## 🔍 Explanation
1. **Load balancer = reverse proxy:** it receives requests and forwards them to backends.
2. **Layer 4:** works on TCP connections. Faster (no payload parsing), simpler, works for any protocol. But no URL/header routing, no caching, and one connection sticks to one backend.
3. **Layer 7:** understands HTTP. Can route by path/host/cookie, cache and rewrite. But more CPU, requires TLS termination, and can see decrypted data.
4. **HAProxy config parts:** global, defaults, frontend and backend.
5. **Demo:** `tcp.cfg` is the L4 configuration and an HTTP config is the L7 one, both balancing between backend servers.

## 💻 Relevant Code
```conf
# L4
frontend tcp_front
    mode tcp
    bind *:80
    default_backend servers
backend servers
    mode tcp
    server s1 127.0.0.1:1111
    server s2 127.0.0.1:2222

# L7
frontend http_front
    mode http
    bind *:80
    acl app1 path_beg /app1
    use_backend app1_servers if app1
    default_backend servers
```

## 🤖 Claude's Notes
- Rule of thumb: start with L4 if you don't need routing rules, and move to L7 when you need them.
- See also the *Layer 4 vs Layer 7 Proxying* file for the deeper flow.

## 🎯 Key Takeaways
- L4 is faster and simpler, while L7 is smarter.
- HAProxy has four config sections: global, defaults, frontend, backend.
- Choose based on required routing features.

## ❓ Questions
1. What can L7 do that L4 cannot?
2. What costs does L7 add?
3. What is a load balancer in terms of proxies?

## 🔁 Follow-up Questions
1. What balancing algorithms does HAProxy support?
2. How does sticky-session routing work at L7?

## 🤔 Questions to Think About
- Which layer would you choose for a gRPC service and why?
- Where does security inspection (WAF) belong?
