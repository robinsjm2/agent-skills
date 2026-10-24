---
name: codelikeme
description: Write code the way this user wants it, using their rules for CDK infrastructure, Python (Lambda and backend) and TypeScript, distilled from steering one project end to end. Use when writing, reviewing, or refactoring CDK, Python, or TypeScript code for this user, or when they say "code like me" or ask you to follow their coding rules.
---

# Code Like Me

The user's coding rules, as short imperatives. They come from the corrections and decisions the user made while building a serverless AWS project (CDK in TypeScript, Python Lambdas, an OpenAPI contract) with an AI agent in October 2026. Follow them without being reminded. Examples in the files come from that project.

## How to use

1. Read the shared rules below, then the file for the language you are about to touch:
   - [cdk.md](cdk.md): infrastructure (CDK is written in TypeScript, so also read the TypeScript file for CDK work)
   - [python.md](python.md): Lambda handlers, shared backend code, tests
   - [typescript.md](typescript.md): TypeScript code and its tests
2. A project's own CLAUDE.md or AGENTS.md wins when it conflicts with these rules.
3. When a rule changes how you would normally do something, do it the rule's way and say so in one line, so the user can correct the rule instead of the code.
4. When the user corrects you in a way no rule covers, finish the task, then offer to add a one- or two-line rule to the matching file.

## Rules for every language

1. **Name things in full words.** `conversation_id`, not `cid`; `request`, not `req`; `operation`, not `op`. A single letter is fine only as a throwaway counter. Rename ambiguous names too (`DataStore`, not `Store`; `db_keys.py`, not `keys.py`).
2. **No magic strings.** A string that repeats, or belongs to a closed set, becomes an enum or a named builder.
3. **Look for a standard tool before writing your own.** Check for a library or the platform's own construct first (`requests`, `geopy`, `Code.fromAsset`) and say what you found. Hand-roll only when nothing fits, and keep it small.
4. **Keep it simple.** If the design needs a fallback, a special case, or a long explanation, simplify it. "Too complicated" means remove something, not document it.
5. **Make behavior visible.** What gets deployed or run must be readable in a file in the repo. Do not assemble it in code at build time where someone troubleshooting cannot see it.
6. **Back claims with documentation.** Read the official page, link it, and quote it when asked. Never answer a docs question from memory. Say plainly when something is unverified or inferred.
7. **Test as you go, then test for real.** Every change ships with unit tests. Anything deployed gets run against the real thing (deploy to a non-prod stage, smoke test) before you call it done.
8. **Keep history clean.** Fold fixes into the one commit with an amend. No stacked "fix" or "refactor" commits unless asked. Split large work into phased PRs only when the user asks.
9. **Least privilege.** Exact resources, narrowest actions, and each environment unable to reach another.
10. **Do not build for needs you do not have.** No speculative getters, setters, wrappers, or options. Add structure when there is a reason, and state the reason.
11. **Choose numbers from evidence.** Timeouts, limits, and thresholds get a measured or documented basis, written next to the number.
12. **Do not hold what you do not need.** Hand sensitive data to a provider built for it (hosted payments, federated sign-in). Make location and similar data opt-in, and never store it exactly.
13. **Explain in words, keep code in files.** Do not paste long code into the chat; describe what changed and why.
14. **Do not show diffs the user can already see.** Their IDE's source control panel shows every change. Report outcomes, decisions and anything surprising; do not walk through each edit or paste a diff.
