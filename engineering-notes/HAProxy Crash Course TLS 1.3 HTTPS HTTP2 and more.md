# HAProxy Crash Course (TLS 1.3, HTTPS, HTTP2 and more)

## Description
Complete production tutorial on configuring HAProxy for High Availability: frontends, backends, health checking, dynamic ACL routing, security restrictions, Let's Encrypt TLS 1.3 termination, and HTTP/2 via ALPN.

---

## The Problem
Modern production systems require high availability, DDoS resilience, TLS encryption, and protocol upgrades. Configuring reverse proxies without understanding internal timeout models, certificate formats, and ALPN negotiations results in degraded performance, security flaws, and configuration failures.

---

## The Solution
Configure HAProxy with distinct frontend and backend blocks, tune client/server timeouts, bundle certificates into single PEM files for TLS 1.3 termination, enforce path-based ACLs for microservices, and enable HTTP/2 using ALPN negotiation.

---

## Detailed Explanation
1. **Core Architecture**:
   - `frontend`: Binds to public interfaces/ports (`bind *:80`, `bind *:443`), sets client timeouts, evaluates ACLs.
   - `backend`: Defines server pools, balancing algorithms (`roundrobin`, `leastconn`, `source`), health checks (`check`), and server timeouts.
2. **Critical Timeouts**:
   - `timeout client`: Closes idle client connections to prevent socket exhaustion.
   - `timeout connect`: Maximum time allowed to establish a TCP socket to an origin server.
   - `timeout server`: Maximum time HAProxy waits for a backend server to process and return a response.
3. **ACLs & Security**:
   - Route traffic conditionally based on URI paths (`path_beg /app1`).
   - Restrict access to internal routes: `http-request deny if { path_beg /admin }`.
4. **TLS 1.3 & Certificate Bundling**:
   - HAProxy requires merging the public certificate and private key into a single combined `.pem` file (`cat fullchain.pem privkey.pem > haproxy.pem`).
   - Use Diffie-Hellman parameters of 2048+ bits for forward secrecy.
5. **Enabling HTTP/2**:
   - Add ALPN negotiation parameters to the HTTPS bind directive: `bind *:443 ssl crt /path/to/haproxy.pem alpn h2,http/1.1`.

---

## Relevant Code & Configurations
```
# Production HAProxy Configuration File: /etc/haproxy/haproxy.cfg

global
    log /dev/log local0 info
    maxconn 20000
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5s
    timeout client 50s
    timeout server 50s

frontend public_ingress
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/haproxy.pem alpn h2,http/1.1
    
    # Force HTTPS
    redirect scheme https code 301 if !{ ssl_fc }

    # Security ACL: Block public admin access
    http-request deny if { path_beg /admin }

    # Path-based routing
    acl is_app1 path_beg /app1
    acl is_app2 path_beg /app2
    
    use_backend app1_cluster if is_app1
    use_backend app2_cluster if is_app2
    default_backend default_cluster

backend app1_cluster
    mode http
    balance roundrobin
    server srv1 127.0.0.1:2222 check
    server srv2 127.0.0.1:3333 check

backend app2_cluster
    mode http
    balance leastconn
    server srv3 127.0.0.1:4444 check
    server srv4 127.0.0.1:5555 check

backend default_cluster
    mode http
    balance roundrobin
    server srv_main 127.0.0.1:2222 check
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Why HAProxy Requires Single Combined PEM Files
Unlike Nginx or Apache, which accept separate `ssl_certificate` and `ssl_certificate_key` configuration paths, HAProxy's C codebase requires all certificate chains and the associated private RSA/ECDSA key to be concatenated into a single `.pem` file. If certificates rotate via Let's Encrypt / Certbot, you must run a post-renewal hook script to concatenate `fullchain.pem` and `privkey.pem` and reload HAProxy seamlessly via runtime socket APIs without dropping connections.

---

## Key Takeaways
- HAProxy uses clean separation between frontend listeners and backend server pools.
- ALPN negotiation is mandatory to enable HTTP/2 over TLS 1.3 without extra round-trip latency.
- ACLs in HAProxy allow fast, low-overhead path routing and security filtering at the edge.
- Tuning client and server timeouts is essential to prevent slow-client socket leaks.

---

## Technical Interview Question
**Question**: How does HAProxy negotiate HTTP/2 using ALPN inside the TLS handshake, and why is this faster than an HTTP Upgrade header?

---

## Follow-up Question
**Follow-up**: What is the difference between `balance roundrobin` and `balance source` in HAProxy, and when should `source` be avoided?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: If HAProxy terminates TLS for thousands of clients, how should you design internal network security between HAProxy and your backend microservices?
