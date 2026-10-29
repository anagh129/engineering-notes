# Fail-over and High-Availability (Explained by Example)

> Source: `Fail-over and High-Availability (Explained by Example).txt` · Transcript 12 of 43

## 📝 Description
Explains **failover** (switching to a redundant backup when a machine dies) as a technique for high availability, and the networking pieces that make it work: ARP, Virtual IP and VRRP.

## ⚠️ Problem
Clients connect to one IP. If the machine behind it dies, the service is down, and you don't want clients to reconfigure anything.

## ✅ Solution
Give the service a **Virtual IP (VIP)** that is owned by whichever node is currently active. When the active node dies, the standby takes over the VIP, and clients keep using the same IP.

## 🔍 Explanation
1. **ARP (Address Resolution Protocol):** maps an IP to a MAC address on the local network. A machine broadcasts "who has this IP?" and the owner answers with its MAC. Everyone caches the answer.
2. **Virtual IP:** not a real IP of one machine. The active node advertises it as its own.
3. **VRRP (Virtual Router Redundancy Protocol):** nodes exchange heartbeats and elect a master. Keepalived implements it.
4. **Failover:** when the master stops responding, the standby claims the VIP and tells the network "this IP now belongs to my MAC" (a gratuitous ARP). Switches and hosts update their tables.
5. **Timing:** it happens in a fraction of a second, but some clients may briefly hold a stale ARP entry and keep sending to the dead MAC.
6. **Combine** with L4/L7 load balancing (e.g. HAProxy + keepalived) for production setups.

## 💻 Relevant Code
Keepalived on two proxy nodes (illustrative):
```conf
vrrp_instance VI_1 {
  state MASTER            # BACKUP on the other node
  interface eth0
  virtual_router_id 51
  priority 101            # lower on BACKUP
  advert_int 1
  virtual_ipaddress { 192.168.1.100 }
}
```
Check which MAC owns an IP:
```bash
arp -n 192.168.1.100
```

## 🤖 Claude's Notes
- Failover is not instant. Expect a short blip, and design clients with retries.
- Beware **split brain**: if the heartbeat network fails but both nodes are alive, both may claim the VIP.

## 🎯 Key Takeaways
- Clients use a stable VIP, and the active node changes behind it.
- ARP/gratuitous ARP is the trick that moves the VIP.
- VRRP/keepalived automates election and takeover.

## ❓ Questions
1. What does ARP do?
2. What does a VIP decouple?
3. Why might a client briefly still reach the dead node?

## 🔁 Follow-up Questions
1. What is a gratuitous ARP?
2. How would you prevent split brain?

## 🤔 Questions to Think About
- What state is lost when the active node dies, and how can the standby get it?
- Does a VIP help across different data centers or only the same L2 network?
