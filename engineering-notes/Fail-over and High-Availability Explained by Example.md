# Fail-over and High-Availability (Explained by Example)

## Description
A comprehensive end-to-end architecture breakdown of building high-availability failover systems using Keepalived, VRRP, HAProxy, and backend application servers.

---

## The Problem
Single points of failure in production infrastructures threaten uptime. When an active load balancer fails, downstream services become inaccessible unless an automated, transparent failover mechanism switches traffic to a standby node without client disruption.

---

## The Solution
Combine Layer 2/3 VRRP clustering (Keepalived) with Layer 7 reverse proxies (HAProxy) in an active-passive topology. Keepalived monitors both node and process health, triggering VIP migration and traffic redirection instantly when faults occur.

---

## Detailed Explanation
1. **The Architecture Components**:
   - **Clients**: Connect to a single Virtual IP (`10.0.0.100`).
   - **Load Balancer 1 (Active/Master)**: Holds the VIP, runs HAProxy, balances traffic across app servers.
   - **Load Balancer 2 (Passive/Standby)**: Runs Keepalived, monitors Master heartbeats, HAProxy runs in standby.
   - **Backend Application Nodes**: Run stateless services (Node.js/Express) connected to database clusters.
2. **Process Health Tracking**:
   - Failover must trigger not just if the server OS dies, but if the HAProxy *process* crashes.
   - Keepalived executes health-check scripts (`killall -0 haproxy`). If HAProxy crashes, Keepalived reduces priority, prompting failover.
3. **The Failover Sequence**:
   - Master HAProxy fails -> Keepalived drops priority -> Standby node detects missed heartbeats -> Promotes to Master -> Binds VIP -> Issues Gratuitous ARP -> Client requests route to Standby seamlessly.

---

## Relevant Code & Configurations
```
# Keepalived tracking script to ensure HAProxy process health triggers failover

vrrp_script check_haproxy {
    script "killall -0 haproxy" # Returns 0 if process is running
    interval 2                  # Check every 2 seconds
    weight 2                    # Add 2 points if healthy
}

vrrp_instance VI_LB {
    state MASTER
    interface eth0
    virtual_router_id 52
    priority 100
    advert_int 1
    
    track_script {
        check_haproxy
    }
    
    virtual_ipaddress {
        10.0.0.100/24
    }
}
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Health Checking the Checker
A common failure mode in High Availability architectures is monitoring the machine while ignoring the application. If the server remains pingable but the HAProxy process locks up or experiences out-of-memory termination, VRRP will keep the dead master active unless a `track_script` is explicitly configured. Always tie VRRP priority to application health.

---

## Key Takeaways
- High availability requires automated detection, decision, and redirection.
- Active-passive topologies ensure one node actively processes load while standby monitors health.
- Keepalived must track process-level health (HAProxy), not just host-level ping status.
- Transparent failover preserves user experience and prevents SLA violations.

---

## Technical Interview Question
**Question**: Why is host-level ping monitoring insufficient for High Availability failover, and how does a process tracking script solve this?

---

## Follow-up Question
**Follow-up**: How do active-passive load balancers maintain TLS session cache continuity when failover occurs?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: If active-passive clusters leave 50% of your provisioned load-balancer hardware idle, at what scale does it become imperative to transition to active-active?
