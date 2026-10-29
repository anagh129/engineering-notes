# B-tree vs B+ tree in Database Systems

> Source: `B-tree vs B+ tree in Database Systems.txt` · Transcript 6 of 43

## 📝 Description
A deep dive into **B-trees and B+ trees**, the data structures behind most database indexes: how they differ and what problems and limits each has.

## ⚠️ Problem
A database must find one row among millions or billions without scanning everything, and it reads from disk in fixed-size pages. Searching a huge sorted list from scratch is too slow.

## ✅ Solution
Use a balanced, wide tree where each node is one disk page. A lookup touches only a few pages. B+ trees improve on B-trees by keeping values only in leaves.

## 🔍 Explanation
1. **B-tree:** every node (internal and leaf) holds keys **and their values** (e.g. a tuple id in Postgres, or the primary key in MySQL).
2. **Problem with that:** values take space, so fewer keys fit per page, the tree is deeper, and more I/O is needed.
3. **B+ tree:** internal nodes hold **only keys**, and the **leaves hold the values**. More keys per page → shallower tree → fewer page reads.
4. **Linked leaves:** leaf nodes are linked together, so a **range scan** finds the start and then just walks along the leaves.
5. **MySQL note:** secondary indexes store the primary key as the value, so a large primary key makes every index big. Postgres stores the tuple id.
6. **Degree:** a database doesn't pick a fixed degree. It derives how many keys fit from the size of the indexed data type.

## 💻 Relevant Code
Seeing an index and a range query in Postgres:
```sql
CREATE INDEX idx_grades_g ON grades (g);
EXPLAIN ANALYZE SELECT * FROM grades WHERE g BETWEEN 80 AND 90;  -- walks the leaf level
```

## 🤖 Claude's Notes
- The key insight is that depth ≈ number of disk reads. A B+ tree with thousands of keys per page can index billions of rows in 3–4 levels.
- Random UUID primary keys cause page splits and fragmented inserts, while sequential keys append cheaply.

## 🎯 Key Takeaways
- B-trees keep values everywhere, while B+ trees keep them only in leaves.
- B+ trees give shallower trees and fast range scans.
- Primary key size affects every secondary index in MySQL.

## ❓ Questions
1. Why do B+ trees need fewer page reads than B-trees?
2. Why are linked leaves good for range queries?
3. How does a wide primary key affect MySQL secondary indexes?

## 🔁 Follow-up Questions
1. What is a page split and when does it happen?
2. How does an index-only scan relate to what a B+ tree leaf stores?

## 🤔 Questions to Think About
- Would a hash index beat a B+ tree for any workload? What would you lose?
- How might random vs sequential primary keys change insert performance?
