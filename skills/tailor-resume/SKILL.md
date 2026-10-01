---
name: tailor-resume
description: Tailor the user's resume to a specific job posting using only verified facts from ~/.jobsearch/resume/fact-bank.md, following the rules learned in ~/.jobsearch/resume/lessons.md, and render it to .docx. Use when the user asks to tailor, customize, or write a resume for a job, or to prepare an application. Also use to record feedback or outcomes that should change how resumes are tailored.
---

# Tailor Resume Skill

Produce a resume tailored to one job posting, explain how well it covers the posting, and get better with each application.

The skill rests on two personal files:

- **Fact bank** (`~/.jobsearch/resume/fact-bank.md`): every verified claim about the user's experience. It's the *only* source of resume content.
- **Lessons** (`~/.jobsearch/resume/lessons.md`): rules learned from the user's feedback and from application outcomes, open questions, and a log of resume versions and how far each application got.

Templates for both are in the [jobsearch-harness templates](https://github.com/robinsjm2/jobsearch-harness/tree/main/templates/resume). If either file is missing, tell the user and offer to build the fact bank from their existing resumes. Never draft from memory.

## Requirements

- `~/.jobsearch/resume/fact-bank.md` and `~/.jobsearch/resume/lessons.md`
- `~/.jobsearch/job-criteria.md` (positioning) and `~/.jobsearch/applications.md` (prior applications)
- The job posting: full text from Indeed (`get_job_details`), a URL the user provides, or pasted text. Use the full posting, not a search-result summary.
- For .docx output: `uv` (or Python with `python-docx`) to run `render_docx.py` in this skill's directory.

## Behavior

### 1. Load context

1. Read `lessons.md` first. Its **Rules** override the defaults in this skill. If it has **Open questions** that affect this resume (e.g. location line, years of experience), ask the user before drafting, or use the rule's stated default and say so.
2. Read `fact-bank.md`, `job-criteria.md`, and `applications.md`. Note any earlier application to the same company, and which resume version it used.

### 2. Analyze the posting

Extract and list, briefly:

- **Must-haves** (required qualifications) and **nice-to-haves**
- **The posting's own terms** for key skills, e.g. "event-driven", "infrastructure as code", "agent orchestration". Recruiters and applicant tracking systems match on these.
- **Level and scope** signals: years, "lead", "own end to end", mentoring
- **Domain**: what the company does and the team's problem

### 3. Map requirements to facts

Build a coverage table: each must-have → the fact-bank entries that support it, rated **Strong** (direct evidence), **Partial** (related or transferable), or **Gap** (no evidence).

### 4. Confirm the user wants to continue

Present why the role fits (or doesn't) against the criteria, the coverage table, and the main risks. Then **stop and ask** a simple question such as: "Does it sound like a good fit to you? Should we continue?" Don't ask about gaps or start drafting until the user says yes. They may decide the role isn't worth the effort.

### 5. Close gaps conversationally

For each gap, ask whether the user has that experience. If they do, get specifics (what, where, when, outcome) and **add it to the fact bank** with today's date before using it. If they don't, leave it out of the resume and list it in the report.

- **With more than 2–3 gaps, ask one question at a time.** Wait for the answer, acknowledge it briefly (and say what it changes), then ask the next. Don't send a long numbered list that needs a long answer.
- Ask the highest-impact gaps first, i.e. the must-haves where an answer would most change the resume.
- Keep each question short and concrete, with an example of what counts.
- Stop asking when the remaining gaps wouldn't change the resume; tell the user how many were skipped.

### 6. Draft the resume

Write it in the Markdown format `render_docx.py` expects:

```
# Full Name
Location line | email | phone
## Summary
2–3 sentences aimed at this posting's top needs.
## Technical Skills
- **Category:** skills, ordered by relevance to the posting
## Experience
### Company, Location | Month YYYY – Month YYYY
*Job title*
- Bullet
## Education
School, Location: Degree
```

Drafting rules (unless `lessons.md` says otherwise):

- **Only fact-bank claims.** Rephrase, combine, reorder, and choose freely. Never add a skill, number, title, scope, or outcome that isn't in the fact bank. Never inflate a number or upgrade a title.
- **Use the posting's terms** wherever a fact supports them.
- **Lead with the strongest match.** The first bullet of the most recent role answers the posting's main need.
- **Prefer outcomes and numbers** from the fact bank (e.g. records processed, roles eliminated, checks shipped).
- **Order skills by relevance.** Drop skills the posting doesn't care about if space is tight. Only list skills the fact bank supports.
- **Keep it to 1–2 pages.** Give older roles one bullet each.
- **Keep facts consistent across documents.** Use the same years of experience, titles, and dates as the user's other profiles, as recorded in `lessons.md`.

### 7. Self-check

Before presenting, verify each of these and fix anything that fails:

- Every bullet traces to a fact-bank entry
- Each must-have is either covered or listed as a gap
- Each posting term used is supported by a fact
- No rule in `lessons.md` is violated
- Dates, titles, and contact details match the fact bank

### 8. Save and render

1. Save the Markdown to `~/.jobsearch/resume/tailored/YYYY-MM-DD-<company>-<role-slug>.md`.
2. Render it:
   ```
   uv run --with python-docx <this skill's directory>/render_docx.py <file>.md
   ```
   This writes a `.docx` next to the Markdown file.

### 9. Report

Show the user:

- **Coverage:** must-haves covered (Strong/Partial) vs. gaps, in a short table
- **Angle:** one line on how the resume is positioned for this posting
- **Gaps and risks:** what a screener may notice is missing, and how to address it in a cover note or interview
- **Paths:** the Markdown and .docx files
- **Questions:** any fact-bank additions you need the user to confirm

Don't paste the whole resume into chat unless asked. Point to the file.

## Learning loop

The skill improves only if feedback and outcomes are written down:

- **User feedback on a draft** (e.g. "don't lead with AppSec", "too long", "say 18+ years"): fix the draft, then add a dated rule to **Rules** in `lessons.md` if it applies to future resumes.
- **When the user applies:** add a row to **Outcomes by resume version** with the resume file and its angle. The application itself goes in `applications.md` with Stage `Submitted`; note the resume file in its Notes column.
- **When Stage changes** in `applications.md`: update the matching Outcomes row.
- **Every ~5 outcomes, or when the user asks:** review the Outcomes table for patterns, such as which angles pass the resume screen and which fail. Add an **Observations** entry and propose rule changes to the user. Don't change rules on your own from too little data.

## What not to do

- Never invent or embellish experience, numbers, titles, or skills
- Never put a "Not yet evidenced" skill on a resume
- Never remove or rewrite fact-bank entries without the user's agreement; only add confirmed facts
- Never submit applications or contact employers on the user's behalf
- Don't let tailoring drift into keyword stuffing: every term must sit in a real, readable bullet
