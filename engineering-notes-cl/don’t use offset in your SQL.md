# don’t use “offset” in your SQL

> Source: `don’t use “offset” in your SQL.txt` · Transcript 43 of 43

## 📝 Description
Explains why SQL **`OFFSET`** is a bad way to implement paging and shows a faster alternative. It is inspired by the *Use The Index, Luke* blog. Demo: a Postgres `news` table with an index on `id`.

## ⚠️ Problem
A paging API turns "page 10 with 10 items" into `OFFSET 100 LIMIT 10`. The database must fetch and **discard** the first 100 rows, and the cost grows with the page number. Offset can also return duplicates when rows are inserted between page requests.

## ✅ Solution
Use **keyset (seek) pagination**: the client sends the last id it saw, and the query uses `WHERE id < :last_id ORDER BY id DESC LIMIT 10`.

## 🔍 Explanation
1. **Why offset is slow:** `OFFSET n LIMIT 10` reads n+10 rows and throws away n.
2. **Duplicates:** if a new row is inserted after page 10 is read, `OFFSET 110` can push an already-seen row into the next page.
3. **Demo results (explain analyze):**
   - Offset 0 → 10 rows read, about 0.2 ms.
   - Offset 1,000 → 1,010 index rows read, about 1 ms.
   - Offset 100,000 → 100,010 rows read, about 79 ms (cached). After a restart (cold cache) it went to several hundred ms or even seconds.
4. **Keyset fix:** use the indexed `id` as the page marker: `WHERE id < last_seen ORDER BY id DESC LIMIT 10`. The database reads only ~10 rows, even for very old pages.
5. **Limit forms:** `LIMIT 10` (or `FETCH FIRST 10 ROWS ONLY`) is fine. The expensive part is the OFFSET.
6. **Less I/O:** only 10 index entries and then the heap fetch for those 10 rows.

## 💻 Relevant Code
```sql
-- slow at depth: reads and discards 100,000 rows
EXPLAIN ANALYZE SELECT title FROM news ORDER BY id DESC OFFSET 100000 LIMIT 10;

-- fast at any depth: keyset pagination
SELECT id, title FROM news ORDER BY id DESC LIMIT 10;                 -- first page
SELECT id, title FROM news WHERE id < 99990 ORDER BY id DESC LIMIT 10; -- next page (99990 = last id seen)
```

## 🤖 Claude's Notes
- Keyset pagination needs a **stable, unique sort key**. If you sort by a non-unique column (e.g. date), add the id as a tiebreaker: `WHERE (date, id) < (:d, :id)`.
- Trade-off: you can't jump straight to "page 500". It suits infinite scroll and "next/previous".

## 🎯 Key Takeaways
- OFFSET does work proportional to the offset.
- Keyset pagination uses the index to jump straight to the right place.
- Keyset avoids duplicates when rows are inserted.
- You lose random page jumps.

## ❓ Questions
1. Why does OFFSET get slower on later pages?
2. How does `WHERE id < last_id` avoid the extra work?
3. How can OFFSET return duplicate rows?

## 🔁 Follow-up Questions
1. How do you paginate on a non-unique sort column?
2. How would you support "go to page N" efficiently enough?

## 🤔 Questions to Think About
- Which of your API endpoints use OFFSET, and how deep do users really page?
- Would an estimated total page count be enough for your UI?
