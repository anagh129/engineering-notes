# Why you Shouldn't Implement Features Because They are Easy - Backend Engineering

> Source: `Why you Shouldn't Implement Features Because They are Easy - Backend Engineering.txt` · Transcript 41 of 43

## 📝 Description
Explains why you should **not implement a feature just because it is easy**: every feature has hidden costs.

## ⚠️ Problem
When designing a product, the feature list starts small, but engineers get excited about what they *can* do. Easy features (even a single line, or a parameter that auto-enables extras) get added that nobody asked for.

## ✅ Solution
Add a feature only when users (or the product owner) need it. Explicitly disable side-effect features you don't want.

## 🔍 Explanation
1. **How it happens:** a design session starts with a short list, then grows because things seem simple.
2. **Hidden costs:** more code to test, document, secure and support forever, and more ways for users to be confused or harmed.
3. **Not asked for:** the team spent time defining requirements, and then extra features appear that neither users nor the owner requested.
4. **Ask:** do users need it? If not, and you can't imagine them using it, turn it off.
5. **Side effects:** enabling one parameter may automatically enable other features. Disable them explicitly, even though that is extra work.
6. **The host's confession:** he has been guilty of this in his career.

## 💻 Relevant Code
Explicitly disabling an unneeded feature that gets enabled by default (illustrative config):
```conf
server.enable_directory_listing = false   # don't ship what nobody asked for
```

## 🤖 Claude's Notes
- "It's only one line" ignores tests, docs, support and security review.
- Removing a shipped feature is much harder than not shipping it.

## 🎯 Key Takeaways
- Easy to build ≠ should be built.
- Every feature is a long-term liability.
- Audit side-effect features that turn on automatically.

## ❓ Questions
1. What hidden costs follow a "one-line" feature?
2. How can a config parameter enable unwanted features?
3. What is the first question to ask before adding a feature?

## 🔁 Follow-up Questions
1. How do you say "no" to a feature politely?
2. How do you measure whether a shipped feature is used?

## 🤔 Questions to Think About
- Which feature in your product could you remove tomorrow with no complaints?
- Who pays the maintenance cost?
