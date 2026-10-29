# Your Backend is Also a Frontend (Backend vs Frontend Engineering)

> Source: `Your Backend is Also a Frontend (Backend vs Frontend Engineering).txt` · Transcript 42 of 43

## 📝 Description
Argues that **your backend is almost always a frontend for something else**, because every layer consumes the layer behind it.

## ⚠️ Problem
"Frontend" and "backend" are treated as two separate worlds, so backend engineers ignore frontend-style concerns even when they are the client of another system.

## ✅ Solution
View frontend and backend as relative roles. Anything that consumes another service is a frontend to it, and should follow good-client practices.

## 🔍 Explanation
1. **Common meaning:** frontend = web (JavaScript, CSS, HTML, React, Angular) or desktop apps. Backend = web servers, API frameworks, proxies, even databases.
2. **A backend needs a consumer:** without something consuming it, it is not really a back end.
3. **Load balancer:** it is the backend for clients but the frontend for your web servers. With several balancers layered, each is the front end of the next.
4. **App server:** a Django/REST app is the backend for browsers, but it makes calls to the database, so it is the **frontend to the database**.
5. **Practice that follows:** as a database client, ask for only what you need (`SELECT` specific columns, not `SELECT *`) and rely on indexes.
6. **Journey note:** the host mentions his growing interest in security and says he doesn't claim to be an expert.

## 💻 Relevant Code
Being a good "frontend" to the database:
```sql
-- bad: pulls every column
SELECT * FROM users WHERE id = 5;
-- better: only what the response needs
SELECT id, name FROM users WHERE id = 5;
```

## 🤖 Claude's Notes
- This reframing also explains why backend services need client-side concerns: timeouts, retries, connection pooling and error handling.
- The same idea explains the term "upstream/downstream" in proxies.

## 🎯 Key Takeaways
- Frontend/backend is a relationship, not a job title.
- Your service is a client of whatever it calls.
- Apply client best practices to your calls.

## ❓ Questions
1. Why is a load balancer both a backend and a frontend?
2. In what sense is a Django app a frontend?
3. What practice follows from being the DB's client?

## 🔁 Follow-up Questions
1. What client-side concerns (timeouts, retries, pooling) should every backend service have?
2. How does this view change how you design APIs between services?

## 🤔 Questions to Think About
- List every system your service calls. Which of those relationships are well-behaved clients?
- Who is the "frontend" of your database?
