# Skills Index

## Job Search

### [gmail-job-search](skills/gmail-job-search/SKILL.md)

Filters job alert emails and recruiter outreach from Gmail against your personal job criteria.

**What it does:**
- Searches Gmail for job alerts from LinkedIn, Indeed, Glassdoor, FlexJobs, and other sources
- Evaluates each posting against your criteria file
- Cross-references your application tracker to exclude roles already applied to
- Identifies recruiter outreach and flags follow-ups on existing applications
- Formats results as Strong match / Possible match with fit reasoning

**Requires:**
- Gmail MCP configured and connected ([setup guide](https://github.com/robinsjm2/jobsearch-harness/blob/main/docs/gmail-mcp-setup.md))
- `~/.jobsearch/job-criteria.md` — your personal job criteria (see [template](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/job-criteria.md))
- `~/.jobsearch/applications.md` — your application tracker (see [template](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/applications.md))

**Invoke with:**
```
check my email for job alerts from the last 3 days
```
or
```
were there any recruiter reach-outs this week?
```

In Kiro, prefix with `#job-criteria` if your workspace has the [job-criteria steering file](https://github.com/robinsjm2/jobsearch-harness/blob/main/.kiro/steering/job-criteria.md).

---

### [job-search-sweep](skills/job-search-sweep/SKILL.md)

Searches Indeed for new openings that match your personal job criteria, then checks each promising posting in full.

**What it does:**
- Runs several targeted Indeed searches built from your criteria's role types and strengths
- Fetches full postings to confirm the real remote status, pay, and requirements (a remote search still returns on-site roles)
- Skips roles you have already applied to, or that were presented in a previous sweep
- Checks employer ratings for top matches
- Formats results as Strong match / Possible match and saves a short sweep record

**Requires:**
- Indeed MCP connected ([Indeed MCP docs](https://docs.indeed.com/mcp/)); in Claude, add the Indeed connector at claude.ai
- `~/.jobsearch/job-criteria.md` — your personal job criteria (see [template](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/job-criteria.md))
- `~/.jobsearch/applications.md` — your application tracker (see [template](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/applications.md))

**Invoke with:**
```
find new remote jobs that match my criteria
```
or `/job-search-sweep`

---

*More skills coming. Topics in progress: Tyme sprint review, LinkedIn post drafting, technical interview prep.*
