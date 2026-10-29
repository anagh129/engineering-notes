# How timeouts can make or break your Backend load balancers

> Source: `How timeouts can make or break your Backend load balancers.txt` · Transcript 17 of 43

## 📝 Description
Why **timeouts** on load balancers and proxies are critical, with examples from nginx and HAProxy and a reference to the 2021 Slack outage and the Amazon Kinesis outage.

## ⚠️ Problem
Without proper timeouts, dead or very slow requests keep consuming CPU, RAM and connections. Failures pile up and can turn a small problem into an outage.

## ✅ Solution
Configure timeouts at each stage of a proxied request so useless work is killed quickly and resources go to fresh requests.

## 🔍 Explanation
1. **Where timers apply:** connecting to the backend, waiting for the client's request, waiting for the backend's response, idle time between requests, and time to send headers/body.
2. **Keep-alive:** TCP keep-alive keeps the transport alive. HTTP keep-alive is about how long to wait between *logical* requests. They are different.
3. **Proxy differences:** nginx and HAProxy name and scope timers differently (e.g. client/server/connect timeouts in HAProxy). Fine-grained control is a mark of a good proxy.
4. **Danger of none:** requests wait forever, pools exhaust and retries amplify the load.
5. **A proxy is not a web server:** if you need a proxy, avoid making it also do everything else.

## 💻 Relevant Code
HAProxy timeouts:
```conf
defaults
    timeout connect 5s    # connecting to the backend
    timeout client  30s   # waiting for data from the client
    timeout server  30s   # waiting for the backend's response
    timeout http-keep-alive 10s
```
nginx equivalents:
```nginx
proxy_connect_timeout 5s;
proxy_read_timeout 30s;
keepalive_timeout 10s;
```

## 🤖 Claude's Notes
- Pair timeouts with **bounded retries** and backoff. Retrying everything on timeout can create a retry storm.
- Choose values from measured p99 latency, not guesses.

## 🎯 Key Takeaways
- Every hop needs explicit timeouts.
- TCP keep-alive ≠ HTTP keep-alive.
- Missing timeouts can amplify outages.

## ❓ Questions
1. What does a server timeout protect against?
2. How is HTTP keep-alive different from TCP keep-alive?
3. Why can retries make an outage worse?

## 🔁 Follow-up Questions
1. How should timeouts be ordered from client to proxy to backend?
2. What is a circuit breaker?

## 🤔 Questions to Think About
- What is the right timeout for an endpoint whose p99 is 2 s?
- What should the user see when a timeout fires?
