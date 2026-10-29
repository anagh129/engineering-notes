# Traefik Crash Course (Without docker)

> Source: `Traefik Crash Course (Without docker).txt` · Transcript 34 of 43

## 📝 Description
A crash course on **Traefik**, an open-source reverse proxy / "edge router" written in Go, demoed **without Docker**, including L4 and L7 proxying and TLS version hardening.

## ⚠️ Problem
You need a reverse proxy that routes traffic to several backends, supports HTTPS and HTTP/2 easily and can update routes dynamically.

## ✅ Solution
Use Traefik with static configuration for entrypoints and dynamic configuration for routers and services.

## 🔍 Explanation
1. **Pattern:** as with other proxies, the host starts with the current architecture, then the desired architecture, then the demo.
2. **Building blocks:** **entrypoints** (ports Traefik listens on), **routers** (match rules), **services** (backend groups and load balancing) and **middlewares**.
3. **Round robin demo:** requests alternate across four backend servers.
4. **Path routing:** `/app1` is sent to servers 1 and 2, and `/app2` to servers 3 and 4.
5. **Proxy modes:** it supports Layer 4 (TCP) and Layer 7 (HTTP) proxying.
6. **TLS:** enable TLS 1.3, 1.2, 1.1 and 1.0, then harden by disabling 1.1 and 1.0.

## 💻 Relevant Code
Illustrative dynamic file configuration:
```yaml
http:
  routers:
    app1:
      rule: "PathPrefix(`/app1`)"
      service: app1
      entryPoints: [web]
  services:
    app1:
      loadBalancer:
        servers:
          - url: "http://127.0.0.1:1111"
          - url: "http://127.0.0.1:2222"
```
Minimum TLS version:
```yaml
tls:
  options:
    default:
      minVersion: VersionTLS12
```

## 🤖 Claude's Notes
- Traefik's strength is dynamic discovery (Docker, Kubernetes), which this "without Docker" demo purposely sets aside.
- Exact YAML keys differ between Traefik v2 and v3, so check the docs for your version.

## 🎯 Key Takeaways
- Entrypoint → router → service (+ middleware).
- Supports TCP and HTTP routing.
- Disable old TLS versions for security.

## ❓ Questions
1. How do routers, services and entrypoints relate?
2. Why disable TLS 1.0 and 1.1?
3. How is path-based routing configured?

## 🔁 Follow-up Questions
1. How does Traefik discover services in Docker or Kubernetes?
2. What are middlewares used for?

## 🤔 Questions to Think About
- When would Traefik's auto-discovery beat a static HAProxy config?
- What belongs at the edge proxy vs. inside the app?
