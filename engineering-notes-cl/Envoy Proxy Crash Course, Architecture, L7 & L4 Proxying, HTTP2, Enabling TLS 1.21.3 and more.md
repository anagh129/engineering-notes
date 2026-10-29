# Envoy Proxy Crash Course, Architecture, L7 & L4 Proxying, HTTP2, Enabling TLS 1.21.3 and more

> Source: `Envoy Proxy Crash Course, Architecture, L7 & L4 Proxying, HTTP2, Enabling TLS 1.21.3 and more.txt` · Transcript 11 of 43

## 📝 Description
A crash course on **Envoy**, an open-source Layer 7 proxy and "communication bus" created at Lyft to help move from a monolith to microservices. It covers architecture, L4 and L7 proxying, HTTP/2, TLS and a YAML-heavy demo.

## ⚠️ Problem
Clients talk straight to a single app or a few servers. You need load balancing, routing, TLS and observability in front of backends, and ideally a flexible, programmable proxy for microservices.

## ✅ Solution
Put Envoy in front of the backends and configure **listeners, routes, clusters and endpoints**.

## 🔍 Explanation
1. **Listener:** the address and port where Envoy accepts connections.
2. **Filter chain:** processes the traffic. An L4 TCP proxy filter forwards bytes, and the L7 HTTP connection manager understands HTTP.
3. **Routes:** match requests (path, header) and send them to a cluster.
4. **Cluster:** a named group of upstream servers. **Endpoints** are the individual addresses (socket address + port).
5. **Load balancing:** round robin across endpoints in the demo, defined by adding endpoints one by one.
6. **TLS:** Envoy can terminate TLS 1.2/1.3 and speak HTTP/2.
7. **Humor and lesson:** the config is verbose YAML. The host's closing advice: security features must be enabled on both the proxy and the backend, and keep your strategy focused on one thing.

## 💻 Relevant Code
Minimal static Envoy config (illustrative):
```yaml
static_resources:
  listeners:
  - name: main
    address: { socket_address: { address: 0.0.0.0, port_value: 8080 } }
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          stat_prefix: ingress
          route_config:
            virtual_hosts:
            - name: app
              domains: ["*"]
              routes: [{ match: { prefix: "/" }, route: { cluster: app_cluster } }]
          http_filters: [{ name: envoy.filters.http.router, typed_config: { "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router } }]
  clusters:
  - name: app_cluster
    type: STATIC
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: app_cluster
      endpoints:
      - lb_endpoints:
        - endpoint: { address: { socket_address: { address: 127.0.0.1, port_value: 1111 } } }
        - endpoint: { address: { socket_address: { address: 127.0.0.1, port_value: 2222 } } }
```

## 🤖 Claude's Notes
- Envoy shines with a control plane (xDS) in service meshes like Istio. Static YAML is the "hello world" way.
- Validate configs with `envoy --mode validate -c file.yaml` before running.

## 🎯 Key Takeaways
- Listener → filter chain → route → cluster → endpoint.
- Envoy supports both L4 and L7.
- TLS needs configuring on both sides of the proxy.

## ❓ Questions
1. How are a cluster and an endpoint related?
2. What is the difference between the TCP proxy filter and the HTTP connection manager?
3. What does a listener do?

## 🔁 Follow-up Questions
1. What is xDS and why does it matter for dynamic config?
2. How would you add a health check to a cluster?

## 🤔 Questions to Think About
- When is Envoy's flexibility worth its configuration complexity over HAProxy or nginx?
- How does a sidecar proxy change latency for each service call?
