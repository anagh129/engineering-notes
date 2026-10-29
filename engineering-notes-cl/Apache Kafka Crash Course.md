# Apache Kafka Crash Course

> Source: `Apache Kafka Crash Course.txt` · Transcript 4 of 43

## 📝 Description
A crash course on **Apache Kafka**: its components built up one at a time, then a hands-on demo with Docker and Node.js (kafkajs) covering a cluster, producers, consumers, load balancing and rebalancing, and a summary of pros and cons.

## ⚠️ Problem
You need to move a very large stream of events between systems, durably and in order, and let many different consumers read it at their own pace (and even re-read it). A classic queue deletes messages after delivery, which doesn't fit.

## ✅ Solution
Kafka is a **distributed, partitioned, replicated log**. Producers append messages to topics, and consumers pull them using offsets.

## 🔍 Explanation
1. **Broker:** a Kafka server that stores data. A cluster has several brokers.
2. **Topic and partitions:** a topic is split into partitions. Each partition is an ordered, append-only log, and the message key decides which partition a message goes to. Ordering is guaranteed only within a partition.
3. **Producer:** writes messages to a topic.
4. **Consumer and consumer group:** consumers in a group share a topic's partitions, and each partition goes to exactly one consumer in the group. Adding consumers spreads the load, and extra consumers beyond the partition count sit idle.
5. **Offsets:** each consumer tracks how far it has read, which is why it can resume or replay.
6. **Rebalancing:** when a consumer joins or leaves, Kafka reassigns partitions in the group.
7. **ZooKeeper:** in the older architecture shown, it holds cluster metadata and coordination. Kafka defaults assume three brokers, so a single-broker demo must set the offsets topic replication factor to 1.
8. **Pros/cons:** huge throughput, durability and replay vs. operational complexity.

## 💻 Relevant Code
Single-broker demo settings (the replication-factor fix mentioned above) and a kafkajs producer/consumer:
```yaml
# docker-compose excerpt (confluentinc images)
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```
```js
const { Kafka } = require("kafkajs");
const kafka = new Kafka({ clientId: "demo", brokers: ["localhost:9092"] });

// producer
const producer = kafka.producer();
await producer.connect();
await producer.send({ topic: "users", messages: [{ key: "u1", value: "hello" }] });

// consumer
const consumer = kafka.consumer({ groupId: "g1" });
await consumer.connect();
await consumer.subscribe({ topic: "users", fromBeginning: true });
await consumer.run({ eachMessage: async ({ partition, message }) =>
  console.log(partition, message.value.toString()) });
```

## 🤖 Claude's Notes
- Newer Kafka versions can run without ZooKeeper (KRaft mode), so check which version you deploy.
- Choose message keys carefully: all messages with the same key land in one partition, which gives ordering for that entity but can cause "hot partitions".

## 🎯 Key Takeaways
- Kafka is a log, not a queue. Messages stay until retention expires.
- Partitions give parallelism; the key gives ordering per key.
- Consumer groups scale reads, and rebalancing handles membership changes.

## ❓ Questions
1. Why is ordering guaranteed only within a partition?
2. What is an offset, and why does it enable replay?
3. What happens to a consumer group when a new consumer joins?

## 🔁 Follow-up Questions
1. What happens if you have more consumers in a group than partitions?
2. How does the replication factor affect durability?
3. What delivery guarantees does Kafka offer (at-most, at-least, exactly once)?

## 🤔 Questions to Think About
- When is a simple queue like RabbitMQ the better choice than Kafka?
- How would you choose the number of partitions for a new topic?
