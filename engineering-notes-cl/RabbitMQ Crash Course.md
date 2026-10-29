# RabbitMQ Crash Course

> Source: `RabbitMQ Crash Course.txt` · Transcript 28 of 43

## 📝 Description
A crash course on **RabbitMQ**: why it exists, its core components, and a hands-on Node.js job-queue demo with a publisher and a consumer, plus the host's thoughts on the technology.

## ⚠️ Problem
When every client talks directly to every other client you get a "spaghetti mesh" of connections (the old enterprise-bus days). It is hard to manage, and slow work blocks callers.

## ✅ Solution
Introduce a broker in the middle. RabbitMQ (open source, written in Erlang, many protocols) receives messages from publishers and delivers them to consumers.

## 🔍 Explanation
1. **AMQP:** the Advanced Message Queuing Protocol, a stateful bi-directional protocol over TCP.
2. **Connection and channel:** one TCP connection holds many lightweight channels.
3. **Publisher:** sends messages. **Consumer:** receives them.
4. **Exchange:** receives published messages and routes them to queues. **Queue:** stores messages until consumed.
5. **Demo:** run RabbitMQ in Docker. The publisher sends a job to a queue ("job sent successfully"), then closes the connection. The consumer, nearly the same code, subscribes to the queue and processes jobs. Together they form an **asynchronous job system**.
6. **Pitfall:** if you don't close the connection the process keeps running.

## 💻 Relevant Code
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
```js
// publisher.js
const amqp = require("amqplib");
(async () => {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertQueue("jobs");
  ch.sendToQueue("jobs", Buffer.from(JSON.stringify({ number: process.argv[2] })));
  console.log("Job sent successfully");
  setTimeout(() => { ch.close(); conn.close(); }, 500);
})();

// consumer.js
(async () => {
  const conn = await amqp.connect("amqp://localhost");
  const ch = await conn.createChannel();
  await ch.assertQueue("jobs");
  ch.consume("jobs", (msg) => {
    const job = JSON.parse(msg.content.toString());
    console.log("Received job", job);
    ch.ack(msg);
  });
})();
```

## 🤖 Claude's Notes
- Use `durable: true` queues and `persistent: true` messages if jobs must survive a broker restart.
- Set `ch.prefetch(n)` to limit how many unacknowledged messages a consumer holds.

## 🎯 Key Takeaways
- Publisher → exchange → queue → consumer.
- Acknowledge messages after finishing the work.
- RabbitMQ is a good fit for background job queues.

## ❓ Questions
1. What is the role of an exchange?
2. Why use channels?
3. What does `ack` tell the broker?

## 🔁 Follow-up Questions
1. What are the exchange types (direct, fanout, topic)?
2. What happens to a message if the consumer crashes before ack?

## 🤔 Questions to Think About
- How would you make the same job run exactly once?
- What do you do with jobs that keep failing (dead-letter queues)?
