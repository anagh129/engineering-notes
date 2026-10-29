# HAProxy Crash Course (TLS 1.3, HTTPS, HTTP2 and more)

> Source: `HAProxy Crash Course (TLS 1.3, HTTPS, HTTP2 and more).txt` · Transcript 13 of 43

## 📝 Description
A long **HAProxy crash course**: current vs desired architecture, proxy concepts, using HAProxy as a TCP (L4) and HTTP (L7) proxy, ACLs, and a demo with TLS 1.3, HTTPS and HTTP/2.

## ⚠️ Problem
Clients hit a single app server directly. You need load balancing, high availability, routing rules and TLS termination in front of multiple servers.

## ✅ Solution
Run **HAProxy**, a fast open-source L4/L7 load balancer written in C, with a frontend that accepts connections and a backend that holds the server pool.

## 🔍 Explanation
1. **Frontend:** what HAProxy listens on (bind address/port) and its mode.
2. **Backend:** the list of servers and the balancing algorithm (e.g. round robin).
3. **default_backend:** the link that says which backend a frontend sends traffic to.
4. **Modes:** `mode tcp` = Layer 4 (any TCP protocol, such as databases). `mode http` = Layer 7 (can read paths, headers and cookies).
5. **ACLs:** rules to route requests, e.g. one path to app1 servers and another to app2.
6. **Validation:** run `haproxy -c -f config.cfg` to check for errors before starting.
7. **Demo:** requests to the frontend alternate between Node servers (visible as "served by node 1/2").
8. **TLS and HTTP/2:** terminate TLS 1.3 at the proxy and enable HTTP/2 with ALPN.

## 💻 Relevant Code
```conf
frontend http_front
    bind *:80
    mode http
    acl is_app1 path_beg /app1
    use_backend app1 if is_app1
    default_backend allservers

backend allservers
    mode http
    balance roundrobin
    server s1 127.0.0.1:2222
    server s2 127.0.0.1:3333

backend app1
    server s1 127.0.0.1:1111
```
HTTPS with HTTP/2:
```conf
frontend https_front
    bind *:443 ssl crt /etc/haproxy/site.pem alpn h2,http/1.1
    default_backend allservers
```

## 🤖 Claude's Notes
- Use `option httpchk` and `check` on servers so HAProxy removes unhealthy backends automatically.
- When terminating TLS at HAProxy, the backend connection can stay plain HTTP (faster) or be re-encrypted (end-to-end security).

## 🎯 Key Takeaways
- Frontend + backend + default_backend is the core model.
- L4 is protocol-agnostic and L7 is content-aware.
- ACLs enable content-based routing.

## ❓ Questions
1. What does `default_backend` do?
2. What is the difference between `mode tcp` and `mode http`?
3. Why validate the config before starting?

## 🔁 Follow-up Questions
1. How would you add health checks?
2. How does ALPN pick HTTP/2?

## 🤔 Questions to Think About
- Where would you terminate TLS in your own architecture, and why?
- What would happen if the HAProxy server itself fails?
