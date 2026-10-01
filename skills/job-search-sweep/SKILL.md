---
name: job-search-sweep
description: Proactively search Indeed for new job openings that match the user's criteria in ~/.jobsearch/job-criteria.md, verify remote status and compensation from the full postings, skip roles already in ~/.jobsearch/applications.md, and present ranked matches. Use when the user asks to find, search for, or sweep for new jobs, or asks what's out there beyond their email alerts.
---

# Job Search Sweep Skill

Search Indeed for openings that fit your criteria, check each promising posting in full, and present only the roles worth your time.

This skill finds *new* openings. Reviewing job alerts and recruiter email is a separate skill ([gmail-job-search](../gmail-job-search/SKILL.md)).

## Requirements

- Indeed MCP connected (tools: `search_jobs`, `get_job_details`, `get_company_data`, `get_resume`). In Claude, add the Indeed connector at claude.ai → Settings → Connectors; see [Indeed's MCP docs](https://docs.indeed.com/mcp/).
- `~/.jobsearch/job-criteria.md`: your personal job criteria
- `~/.jobsearch/applications.md`: your application tracker

For file formats, see the templates for [criteria](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/job-criteria.md) and the [tracker](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/applications.md).

If either file is missing, tell the user and point them to the templates. Do not guess at their criteria.

**Data directory:** this skill uses `~/.jobsearch/` by default. If the project's instructions (CLAUDE.md or AGENTS.md) name a different data directory, use that path everywhere this skill says `~/.jobsearch/`. This is useful for demos and test data.

## Behavior

### 1. Load context

1. Read `~/.jobsearch/job-criteria.md` and `~/.jobsearch/applications.md`.
2. Read the most recent file in `~/.jobsearch/notes/sweeps/`, if one exists, to know which roles were already presented.
3. Optionally call `get_resume`. Use it only as background: the criteria file always takes precedence. If the Indeed resume looks outdated compared with the criteria (old employer, much older title), mention it once in the output, because Indeed personalizes results from it.

### 2. Search

Build 4–6 targeted queries rather than one broad one; each search returns only a handful of results.

- Combine the criteria's **primary role types** with its **strongest technical areas**, e.g. "senior backend engineer AWS serverless" or "staff platform engineer".
- Include secondary role types only if the user asks, or if primary searches return little.
- Use `location: "remote"` when the criteria require remote work. Otherwise use the location the criteria give.
- Use `country_code` from the criteria, or ask the user if it's not stated. Use `job_type: "fulltime"` unless the criteria say otherwise.
- If the user asks about a specific company or role, search for that directly.

### 3. Triage the results

Remove duplicates by normalized company + title. Then discard, without fetching details:

- Titles that hit a hard exclude (e.g. junior, associate, intern, or manager when management is excluded)
- Roles whose maximum listed pay is below the criteria's floor
- Company + role combinations already in `applications.md`
- Roles presented in the previous sweep, unless the user asks to see them again

Keep, but mark as stale, postings older than about 60 days.

### 4. Verify with full details

Call `get_job_details` for each remaining candidate. Cap this at about 12 per sweep, and prioritize by title fit and pay. From the full posting, determine:

- **Actual work location.** A remote search still returns on-site and hybrid roles, and the summary location is often just headquarters. Look for explicit statements such as "Work Location: Remote", "remote-first", "remote friendly", "hybrid", or "on-site", and state which one you found. If the posting never says, report remote status as **unconfirmed**. Do not assume remote.
- **Compensation**, including the full range.
- **Requirements vs. background.** Compare required years, languages and domain against the criteria's strengths.
- **Disqualifiers** hidden in the text: people management, work authorization or clearance limits, required travel or relocation.

### 5. Company check (top matches only)

For the Strong matches, call `get_company_data` (ratings plus metadata; salaries only with a job title). Look for signals the criteria care about, such as work-life balance, flexibility, and signs of return-to-office pressure. Keep this to one or two lines per company, and include the company page URL the tool provides.

### 6. Evaluate and present

Rate each verified role against the criteria as **Strong match**, **Possible match**, or **Skip**, following the criteria file's evaluation rules. Show only Strong and Possible matches, Strong first.

## Output format

Link each job title to its apply/view URL exactly as the tool returns it. Do not strip URL parameters.

```
**[Role Title — Company](apply URL)**
- Location/Remote: Remote (stated in posting) / Hybrid / On-site / Unconfirmed
- Compensation: [range or "not disclosed"]
- Posted: [date] (flag if stale)
- Fit: Strong match / Possible match
- Why: [2–3 sentences: what aligns, meaningful gaps, any risks]
- Company: [one line from get_company_data, Strong matches only]
```

Then a short **Skipped** line listing notable exclusions and why (e.g. "Jane Technologies — people-manager role").

### Summary line

```
Ran N searches, reviewed X unique roles, fetched details for Y.
Found S strong and P possible matches. Z excluded by criteria, A already applied, B seen in a previous sweep.
```

## Saving the sweep

After presenting, save a short record to `~/.jobsearch/notes/sweeps/YYYY-MM-DD.md`: the queries run, plus one line per role presented (company, title, rating, remote status, pay). The next sweep uses it to avoid repeating roles. Save only company, title and facts from the posting; no raw tool output.

## Updating the application tracker

When the user says they applied to a role from a sweep, add a row to `~/.jobsearch/applications.md`:
```
| [today's date] | [Company] | [Role] | Indeed | Applied | Submitted | |
```

## Tool notes

- `search_jobs` has no filters for pay, remote status or seniority. Apply the criteria yourself after searching.
- Job IDs (e.g. `JOBSEARCH_100002`) are temporary and only valid in the current session. Identify roles by company + title in files and the tracker.
- `get_company_data` accepts one company per call and returns salary data only when given a job title.

## What not to do

- Do not present a role as remote unless the full posting says so
- Do not present hard-exclude roles unless the user explicitly asks
- Do not guess at compensation when it is not disclosed; flag it as unknown
- Do not apply to jobs or contact employers on the user's behalf
- Do not re-present roles the user has already applied to
