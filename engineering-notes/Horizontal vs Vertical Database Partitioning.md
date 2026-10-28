# Horizontal vs Vertical Database Partitioning

## Description
An architectural exploration of database partitioning, detailing row-based horizontal partitioning (sharding) vs column-based vertical partitioning, storage tiering, and performance implications.

---

## The Problem
As relational database tables swell to hundreds of millions of rows, B-Tree index structures expand beyond available memory, causing cache misses and severe disk I/O bottlenecks. Storing large, rarely accessed binary blobs alongside hot metadata degrades scanning and update speeds.

---

## The Solution
Partition the database: use Horizontal Partitioning to slice tables by rows (range, list, hash) across smaller partition tables, and Vertical Partitioning to split columns, placing hot metadata on fast SSDs and cold binary data on cheaper storage tiers.

---

## Detailed Explanation
1. **The Scaling Bottleneck**:
   - Tables with 50M+ rows suffer from bloated B-Tree indexes.
   - Memory cannot cache the full index, forcing queries to perform expensive disk reads.
2. **Horizontal Partitioning (Row Slicing / Sharding)**:
   - Slices table horizontally by rows using a **Partition Key**.
   - Strategies: **Range** (dates, ID intervals), **List** (country/region), or **Hash**.
   - Benefits: Each partition maintains a small, memory-cacheable index; partition pruning allows the database engine to skip irrelevant partitions entirely.
   - Client Transparency: Applications continue querying the master table view; the RDBMS routes to the specific partition.
3. **Vertical Partitioning (Column Slicing)**:
   - Slices table vertically by columns.
   - Separates hot, frequently queried metadata (`id`, `name`, `status`) from heavy, rarely queried payloads (`profile_photo_blob`, `pdf_data`).
   - Storage Tiering: Hot metadata table resides on fast NVMe SSDs; cold BLOB table resides on cheap high-capacity secondary storage.

---

## Relevant Code & Configurations
```
-- PostgreSQL Declarative Horizontal Range Partitioning

CREATE TABLE orders (
    order_id BIGSERIAL,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL,
    total_amount NUMERIC(10, 2),
    PRIMARY KEY (order_id, order_date)
) PARTITION BY RANGE (order_date);

-- Partitions by Quarter
CREATE TABLE orders_2026_q1 PARTITION OF orders
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE orders_2026_q2 PARTITION OF orders
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');

-- Vertical Partitioning via Schema Separation
CREATE TABLE user_profile (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
) TABLESPACE fast_nvme;

CREATE TABLE user_blob_data (
    user_id BIGINT PRIMARY KEY REFERENCES user_profile(user_id),
    raw_document_blob BYTEA
) TABLESPACE cold_storage;
```

---

## Claude Notes (Deep Dive & Real-World Context)
### Partition Pruning Optimization
The primary performance superpower of horizontal partitioning is **Partition Pruning**.
When an application issues:
```sql
SELECT * FROM orders WHERE order_date = '2026-02-15';
```
The query planner inspects the partition bounds and completely ignores `orders_2026_q2`, scanning only `orders_2026_q1`. However, if queries filter on non-partition keys, the database must execute a costly fan-out scan across *all* partitions.

---

## Key Takeaways
- Partitioning mitigates B-Tree index bloat and restores memory cache efficiency.
- Horizontal partitioning splits rows across tables via Range, List, or Hash keys.
- Vertical partitioning splits columns, separating high-frequency metadata from heavy, cold binary blobs.
- Partition pruning ensures queries only scan partitions relevant to the query filter.

---

## Technical Interview Question
**Question**: What is partition pruning, and why does a query without the partition key in its WHERE clause cause severe performance degradation on a partitioned table?

---

## Follow-up Question
**Follow-up**: How does vertical partitioning enable storage tiering between NVMe SSDs and cost-effective object/block stores?

---

## Question to Think About (System Trade-offs)
**Architectural Dilemma**: When should an engineering team transition from single-node database partitioning to distributed horizontal sharding across independent physical database clusters?
