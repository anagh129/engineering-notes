# Active-Active vs Active-Passive Cluster to Achieve High Availability in Scaling Systems

> Source: `Active-Active vs Active-Passive Cluster to Achieve High Availability in Scaling Systems.txt` · Transcript 3 of 43

## 📝 Description
Compares **Active-Active** and **Active-Passive** cluster setups for high availability, using a proxy in front of two servers and keepalived for failover.

> ⚠️ **Transcript quality warning:** the auto-generated transcript for this video is badly garbled, so this summary comes from the title and the topic, not from the text of the video.

## ⚠️ Problem
A single server (or a single proxy) is a single point of failure. If it dies, the application goes down.

## ✅ Solution
Run more than one node. Either keep one idle standby ready (**Active-Passive**) or have all nodes serve traffic at the same time (**Active-Active**).

## 🔍 Explanation
1. **Active-Passive:** one node serves traffic while a standby waits. If the active node dies, the standby takes over a shared **virtual IP** (via VRRP/keepalived). Simple, but half your capacity is idle.
2. **Active-Active:** every node is serving. A load balancer spreads traffic across them. Better utilization and scale, but you must handle shared state and consistency.
3. **Capacity risk:** in Active-Active, when one node dies the others must absorb its load. If they were each near 100%, they overload too.
4. **The balancer itself** is often a single point of failure, so it is usually run as an Active-Passive pair in front of the Active-Active servers.

## 💻 Relevant Code
A typical keepalived snippet for the Active-Passive proxy pair:
```conf
vrrp_instance VI_1 {
    state MASTER          # BACKUP on the standby
    interface eth0
    virtual_router_id 51
    priority 100          # lower on the standby
    virtual_ipaddress { 192.168.1.100 }
}
```

## 🤖 Claude's Notes
- Active-Active is not automatically "better". It costs more in design (session state, data replication, split brain).
- For databases, Active-Active means multi-writer, which is much harder than for stateless web servers.

## 🎯 Key Takeaways
- Active-Passive: simple, idle standby, brief failover gap.
- Active-Active: efficient and scalable, but needs spare capacity and state handling.
- Remove single points of failure at every layer, including the load balancer.

## ❓ Questions
1. What is idle in Active-Passive that is not idle in Active-Active?
2. Why must Active-Active clusters keep spare capacity?

## 🔁 Follow-up Questions
1. How does a VIP make failover invisible to clients?
2. What is "split brain" and how can it occur in an Active-Passive pair?

## 🤔 Questions to Think About
- For a stateless API versus a database, which model would you choose and why?
- Is a few seconds of failover gap acceptable for your application?
