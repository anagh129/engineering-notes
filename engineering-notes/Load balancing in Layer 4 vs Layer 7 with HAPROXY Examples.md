# Load balancing in Layer 4 vs Layer 7 with HAPROXY Examples

## Description
Exploration of Layer 4 vs Layer 7 load balancing architectures, operational mechanics, pros and cons, and hands-on HAProxy implementation for TCP and HTTP modes.

---

## The Problem
Unbalanced backend traffic leads to server overload, socket exhaustion, and system downtime. Selecting the wrong load balancing layer results in either bloated CPU costs and TLS overhead (when L4 would suffice) or an inability to route microservice paths and cache responses (when L7 is required).

---

## The Solution
Deploy HAProxy configured with `mode tcp` for raw stream balancing using Network Address Translation (NAT) without payload decryption, or `mode http` for intelligent content-based routing, URL rewriting, ACL matching, and caching.

---

## Detailed Explanation
1. **Layer 4 Load Balancing**:
   - Operates strictly on IP and Port using NAT tables.
   - Sits on a single end-to-end TCP connection.
   - Health checking relies on TCP ping / SYN handshake timeouts.
   - Pros: Maximum throughput, lowest latency, minimal CPU/memory, highly secure (no payload decryption).
   - Cons: No smart routing, no URL rewriting, no cookie affinity, no caching, sticky per TCP connection.
2. **Layer 7 Load Balancing**:
   - Operates on HTTP headers, URLs, cookies, and methods.
   - Terminates client connection and opens separate backend connection.
   - Supports Access Control Lists (ACLs) to route `/app1` to backend pool 1 and `/app2` to backend pool 2.
   - Pros: Microservice routing, cookie-based session stickiness, edge caching, header injection (`X-Forwarded-For`).
   - Cons: Higher CPU consumption (TLS cryptographic handshakes, buffer parsing), requires centralizing certificates on the load balancer.

---

## Relevant Code & Configurations
```
# HAProxy Production Configuration: Layer 4 vs Layer 7

global
    maxconn 10000

defaults
    log global
    timeout connect 5s
    timeout client 50s
    timeout server 50s

# --- Layer 4 Ingress (TCP Mode) ---
frontend tcp_front
    bind *:8888
    mode tcp
    default_backend tcp_back

backend tcp_back
    mode tcp
    balance roundrobin
    server srv1 127.0.0.1:4444 check
    server srv2 127.0.0.1:5555 check

# --- Layer 7 Ingress (HTTP Mode) ---
frontend http_front
    bind *:9999
    mode http
    
    # ACL Definitions
    acl path_app1 path_beg /app1
    acl path_app2 path_beg /app2
    
    use_backend app1_pool if path_app1
    use_backend app2_pool if path_app2
    default_backend default_pool

backend app1_pool
    mode http
    balance roundrobin
    server app1_srv 127.0.0.1:4444 check

backend app2_pool
    mode http
    balance roundrobin
    server app2_srv1 127.0.0.1:6666 check
    server app2_srv2 127.0.0.1:7777 check

backend default_pool
    mode http
    balance roundrobin
    server def_srv 127.0.0.1:5555 check
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Stickiness Differences: L4 vs L7
- In HAProxy `mode tcp`, when a client opens a connection, all requests over that TCP session flow to the exact same backend server. Round-robin only balances *new TCP connections*, not individual HTTP requests inside keep-alive sockets.
- In HAProxy `mode http`, HAProxy analyzes each HTTP request on the persistent client socket independently. It can route Request 1 to Server A and Request 2 to Server B over the same client TCP socket.

### Backend Connection Reuse (`http-reuse`)
In Layer 7 mode, HAProxy can reuse backend connections across multiple clients using the `http-reuse` directive (`safe`, `aggressive`, `always`). This allows HAProxy to act as a connection multiplexer, shielding backend application servers from connection spikes.

---

## Key Takeaways
- L4 load balancing routes raw TCP streams via NAT; it cannot inspect HTTP paths or cookies.
- L7 load balancing terminates client connections, parses HTTP semantics, and routes based on headers, paths, and methods.
- In L4 mode, keep-alive client connections appear 'sticky' to a single server because HAProxy balances connections, not HTTP requests.
- L7 load balancers provide microservice routing and caching at the expense of higher CPU and memory overhead.

---

## Technical Interview Question
**Question**: Why does testing an L4 load balancer with a modern web browser often appear to send all traffic to a single backend despite round-robin configuration?

---

## Follow-up Question
**Follow-up**: What is the security advantage of deploying a Layer 4 load balancer in front of internal databases compared to a Layer 7 proxy?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: If modern CPUs handle TLS encryption with hardware acceleration (AES-NI), does the performance penalty of Layer 7 load balancing still justify choosing Layer 4 in web environments?
