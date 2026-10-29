# Horizontal vs Vertical Database Partitioning

> Source: `Horizontal vs Vertical Database Partitioning.txt` · Transcript 14 of 43

## 📝 Description
A short vlog on **database partitioning**: the difference between horizontal and vertical partitioning and why you would use each.

## ⚠️ Problem
A huge table is slow to query and maintain. Queries scan more data than they need, and wide rows (e.g. big blob columns) bloat every read.

## ✅ Solution
Split the table into smaller parts. **Horizontal** partitioning splits by rows and **vertical** partitioning splits by columns.

## 🔍 Explanation
1. **Horizontal:** slice the table across rows. Each partition holds a subset of rows, chosen by range, list, hash or a composite rule. Queries that target a subset read only that partition.
2. **Same machine:** partitioning keeps the pieces on the same instance and disk. This is different from **sharding**, which distributes pieces across machines.
3. **Vertical:** split columns. Move a rarely-used, heavy column (like a large blob) with its row ids into another table, so frequent queries stay fast.
4. **List example:** rows with a given city or country value go in their own partition.

## 💻 Relevant Code
Postgres declarative partitioning (illustrative):
```sql
CREATE TABLE orders (id bigint, country text, total numeric)
  PARTITION BY LIST (country);

CREATE TABLE orders_fr PARTITION OF orders FOR VALUES IN ('FR');
CREATE TABLE orders_us PARTITION OF orders FOR VALUES IN ('US');
```
Vertical split:
```sql
CREATE TABLE user_core (id int PRIMARY KEY, name text);
CREATE TABLE user_photo (id int PRIMARY KEY REFERENCES user_core, photo bytea);
```

## 🤖 Claude's Notes
- Partition pruning only helps if queries filter on the partition key.
- Too many tiny partitions add planning overhead.

## 🎯 Key Takeaways
- Horizontal = split rows, vertical = split columns.
- Partitioning ≠ sharding.
- Choose the partition key to match your query filters.

## ❓ Questions
1. Which type of partitioning separates a blob column from the rest?
2. How does partitioning differ from sharding?
3. Name four horizontal partitioning strategies.

## 🔁 Follow-up Questions
1. What is partition pruning?
2. How would you partition a table of time-series events?

## 🤔 Questions to Think About
- What happens to queries that don't filter on the partition key?
- When would sharding become necessary?
