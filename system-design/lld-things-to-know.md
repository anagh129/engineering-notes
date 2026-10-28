# What to Keep in Mind When Starting an LLD Discussion

## First 5 minutes: don't code yet
- Repeat the problem back in your own words to confirm you understood it.
- Ask clarifying questions about scope: who the users are, what's in and out of scope, and whether concurrency matters.
- State your assumptions out loud ("I'll assume X, tell me if that's wrong") so the interview keeps moving.
- Agree on a small set of core features first (for the parking lot: park, unpark, fee). Offer extras like reservations as follow-ups.

## Next 10 minutes: design before code
- Pull the nouns from the requirements to get your classes, and the verbs to get your methods.
- Give each class one responsibility. If a class does two jobs, split it.
- Decide relationships: has-a (composition) versus is-a (inheritance). Prefer composition.
- Sketch the class diagram on paper or the whiteboard before writing code.

## While coding
- Code the core flow first (park and unpark), then extend.
- Use design patterns only where the requirements call for them. Forcing a pattern is a red flag.
- Use clear names, small methods and interfaces for the parts that will change (pricing, allocation).
- Talk while you write: explain why, not just what.

## Throughout
- Think aloud. The interviewer is grading your reasoning, not only the final code.
- Treat the interviewer's hints as guidance, not criticism, and adjust.
- Mention edge cases and concurrency before being asked.
- Stay flexible. A follow-up like "now add EV spots" tests whether your design can absorb a change.

## Common mistakes to avoid
- Jumping straight into code without clarifying requirements.
- Over-engineering with too many patterns or classes for a 45-60 minute round.
- Putting everything in one giant class.
- Ignoring extensibility, so a small new requirement forces a rewrite.
- Going silent for long stretches while thinking.

## Quick framework to remember
1. Clarify requirements
2. Identify entities (classes)
3. Define relationships
4. Pick patterns where justified
5. Code the core flow
6. Discuss extensions, edge cases and trade-offs