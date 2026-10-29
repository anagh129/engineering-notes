# The 2021 Slack Outage - Detailed analysis of what happened to Slack on Jan 4th 2021

> Source: `The 2021 Slack Outage - Detailed analysis of what happened to Slack on Jan 4th 2021.txt` · Transcript 32 of 43

## 📝 Description
Analysis of the **January 4, 2021 Slack outage** (about five hours), summarizing the official incident report and then discussing it in depth.

## ⚠️ Problem
On the first Monday back after the holidays, Slack became unusable for many customers from about 6 AM to 11 AM PST.

## ✅ Solution (what happened and what fixed it)
The cloud provider increased network capacity, Slack added backend servers, and service returned to normal. Slack's post-mortem lists remedies for next time.

## 🔍 Explanation
1. **Architecture (approximated):** clients → load balancers → backend servers → MySQL (via Vitess), connected through **cross-boundary network routers** in the cloud provider (believed to be AWS).
2. **Trigger:** around 6 AM PST the routers between load balancers, backends and the DB began dropping packets.
3. **Cascade:** the load balancer marked backends as unhealthy and removed them from the fleet. Fewer backends meant failed requests increased, and client retries added more load.
4. **Provisioning storm:** the rising failures made the provisioning service spin up a very large number of new backend servers. But the provisioning service also suffered from the network problems, timed out, and eventually ran out of **open file handles**. New machines couldn't get far enough through provisioning to start.
5. **Timeline:** errors started ~6:00, engineers were paged ~6:46, rapid error increase ~7:00, improvement ~8:45, most customers back ~9:15, and full recovery ~10:40 (roughly 4h40m).
6. **Alerting gap:** the engineers were paged on downstream symptoms (errors), not on the root cause (packet loss).
7. **Cache note:** the host earlier guessed at client-cache issues because customers were told to hard-refresh.
8. **Host's view:** no clear fault of Slack's own, but he points to remedies such as better timeouts, alerts and headroom. He praises the non-defensive report.

## 💻 Relevant Code
Not applicable. A health-check setting involved in the "remove unhealthy backends" behavior (illustrative HAProxy):
```conf
backend app
    option httpchk GET /health
    default-server inter 2s fall 3 rise 2   # 3 failed checks => remove from fleet
```

## 🤖 Claude's Notes
- The pattern is a classic **cascading failure**: a health check removes capacity, which raises load on what's left, which fails more health checks.
- Protection tools: bounded retries with backoff, load shedding, a limit on how many backends can be marked unhealthy at once ("panic mode"), and capacity headroom.

## 🎯 Key Takeaways
- Network trouble can cascade into compute trouble.
- Autoscaling depends on the provisioning path staying healthy.
- Alert on causes, not only on symptoms.
- Blameless post-mortems are good engineering.

## ❓ Questions
1. How did packet loss lead to backends being removed?
2. Why couldn't new servers rescue the system?
3. Why was alerting on errors, not packet loss, a problem?

## 🔁 Follow-up Questions
1. How does a circuit breaker or load shedding help in a cascade?
2. What limit would you put on automatic removal of unhealthy servers?

## 🤔 Questions to Think About
- Which of your services has a provisioning step that could fail under load?
- How would you test that your system survives network packet loss?
