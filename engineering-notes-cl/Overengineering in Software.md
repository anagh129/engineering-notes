# Overengineering in Software

> Source: `Overengineering in Software.txt` · Transcript 26 of 43

## 📝 Description
Defines **over-engineering** (solving problems users never asked for) and discusses it at the code level and the system-architecture level.

## ⚠️ Problem
Teams add abstractions, layers and infrastructure that nobody needs, making systems hard to understand, change and run.

## ✅ Solution
Build the simplest thing that solves the real problem, and add complexity only when real requirements arrive.

## 🔍 Explanation
1. **Definition:** an over-engineered solution attempts to solve problems the user never asked to solve.
2. **In code:** premature abstraction, over-generalization and extra flexibility nobody uses.
3. **In architecture:** starting with Kubernetes, Mesos or microservices from day one for a tiny app (e.g. a parking-lot website) when a few VMs would do.
4. **Question to ask:** how many customers will you realistically have?
5. **Open discussion:** the host asks viewers for their over-engineering stories and invites disagreement.

## 💻 Relevant Code
Illustrative contrast:
```js
// over-engineered
class AbstractFactoryProviderManager { /* ... three layers to add two numbers ... */ }

// simple
const add = (a, b) => a + b;
```

## 🤖 Claude's Notes
- A useful test: "What concrete requirement forces this complexity today?" If there is none, delay it.
- Under-engineering has costs too, so aim for *appropriate* design and refactor as needs grow.

## 🎯 Key Takeaways
- Solve the problem users have, not an imagined one.
- Simple designs are easier to run and change.
- Scale infrastructure with real demand.

## ❓ Questions
1. What is over-engineering?
2. Give one example in code and one in architecture.
3. What question helps you avoid it?

## 🔁 Follow-up Questions
1. How do you tell under-engineering from over-engineering?
2. What is YAGNI?

## 🤔 Questions to Think About
- What is the most over-engineered thing you have worked on?
- What was the real cost, in time and people?
