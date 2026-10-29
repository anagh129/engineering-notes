# When Designing a Backend System Minimize the “What If” Questions

> Source: `When Designing a Backend System Minimize the “What If” Questions.txt` · Transcript 39 of 43

## 📝 Description
Argues that backend system design should **minimize "what if?" questions** and prefer simple designs that do one thing well. The host says it's a preference, not a rule.

## ⚠️ Problem
Design sessions drift into endless "what if we need X someday?" thinking. The system grows features and abstractions nobody asked for and becomes hard to explain.

## ✅ Solution
Design for the actual requirement, keep each system small, and link systems together instead of growing one big one.

## 🔍 Explanation
1. **Context:** a single person often designs and then builds the piece of technology, driven by a requirement.
2. **Personality spectrum:** he prefers engineers who go back to the basics.
3. **Black hole:** each "what if" adds another feature, and then developers abstract ("1, 2, 3 and 4 look the same, create a new abstraction"). Users then ask "why do I need this?".
4. **Unix strategy:** do one thing well.
5. **Microservices-style linking:** build a new small thing and connect it to the existing one rather than inflating the original, though he has reservations about microservices in general.

## 💻 Relevant Code
Not applicable.

## 🤖 Claude's Notes
- "What if" thinking is useful for **failure modes** (what if the DB is down?) and harmful for **speculative features**. Separate the two.
- Keep a short list of non-goals in every design doc.

## 🎯 Key Takeaways
- Design for known requirements.
- Don't build for hypothetical futures.
- Small, focused systems are easier to reason about.

## ❓ Questions
1. How do "what if" questions inflate a design?
2. What is the Unix strategy?
3. When does abstraction become harmful?

## 🔁 Follow-up Questions
1. Which "what if" questions are worth asking?
2. How do you make a simple design easy to extend later?

## 🤔 Questions to Think About
- What was the last "what if" that you built for and never used?
- How would you push back in a design review?
