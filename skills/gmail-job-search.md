# Gmail Job Search Skill

Filter job alert emails and recruiter outreach from Gmail against your personal job criteria.

## Requirements

- Gmail MCP configured and connected
- `~/.jobsearch/job-criteria.md` — your personal job criteria
- `~/.jobsearch/applications.md` — your application tracker

The skill references these files by convention. They live in a personal data directory outside any repository, so your criteria and application history are never committed. You provide the content; the skill provides the behavior.

For Gmail MCP setup instructions, see the [setup guide](https://github.com/robinsjm2/jobsearch-harness/blob/main/docs/gmail-mcp-setup.md).
For the job criteria format, see the [example criteria file](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/job-criteria.md).
For the application tracker format, see the [template](https://github.com/robinsjm2/jobsearch-harness/blob/main/templates/applications.md).

## When to activate

Activate this skill when the user asks any of the following:
- "Check my email for job alerts"
- "Were there any recruiter reach-outs?"
- "Any replies from companies I applied to?"
- "What job postings came in this week?"
- "Check my inbox for anything job-related"

## Behavior

### Checking for job alert emails

1. Load `~/.jobsearch/job-criteria.md` to get the user's job criteria.
2. Load `~/.jobsearch/applications.md` to get the list of companies and roles already applied to.
3. Search Gmail for job alert messages from known sources:
   - LinkedIn Jobs (`from:jobalerts@linkedin.com OR from:jobs-noreply@linkedin.com`)
   - Indeed (`from:indeedjobs@indeed.com OR from:alert@indeed.com`)
   - Glassdoor (`from:noreply@glassdoor.com`)
   - ZipRecruiter (`from:@ziprecruiter.com`)
   - Dice, Wellfound, Levels.fyi, or any other job board the user mentions
   - Generic: search `subject:job alert OR subject:jobs matching OR subject:new jobs`
4. Retrieve content for each alert and extract individual job postings.
5. For each posting, check whether the company + role combination already exists in `applications.md`:
   - If already applied: **skip silently** — do not include in output
   - If not yet applied: evaluate against the criteria in `~/.jobsearch/job-criteria.md`
6. Present only postings that are a **Strong match** or **Possible match** per the user's criteria.
7. Skip hard excludes entirely unless the user explicitly asks to see them.

### Checking for recruiter or company outreach

1. Load `~/.jobsearch/job-criteria.md` and `~/.jobsearch/applications.md`.
2. Search Gmail for:
   - Direct recruiter messages: `subject:opportunity OR subject:role OR subject:position OR subject:reaching out`
   - Application status replies: `subject:application OR subject:interview OR subject:next steps OR subject:thank you for applying`
   - Filter to the time window the user specified (default: last 7 days)
3. Retrieve content for each message.
4. For each message, check `applications.md`:
   - If the company matches an existing application: flag as **Follow-up on existing application** — always include regardless of fit
   - If the company is not in the applications list: treat as new inbound outreach and evaluate fit against criteria
5. Categorize each as:
   - **Follow-up on existing application** — response to something already applied to (always show)
   - **New recruiter outreach** — someone proactively reaching out (evaluate fit and show if relevant)
   - **Automated rejection** — form rejection (mention count only)
   - **Other** — flag if potentially relevant

## Output format

### Job alerts section

For each relevant posting:
```
**[Role Title] — [Company]**
- Location/Remote: [status]
- Compensation: [amount or "not disclosed"]
- Source: [job board]
- Fit: Strong match / Possible match
- Why: [2–3 sentences on alignment and any meaningful gaps]
```

### Recruiter/outreach section

For each message:
```
**[Sender name or company] — [Subject line]**
- Type: Follow-up on existing application / New recruiter outreach / Other
- Role: [title if mentioned]
- Fit: Strong match / Possible match / Below criteria / N/A (existing application)
- Action needed: [Reply, Review, No action]
```

### Summary line

```
Found X relevant job alerts (Y already applied, excluded), Z recruiter/outreach messages
(N follow-ups on existing applications). W items excluded by criteria.
```

## Updating the application tracker

When the user submits an application, add a row to `~/.jobsearch/applications.md`:
```
| [today's date] | [Company] | [Role] | [Source] | Applied | |
```

When a recruiter makes contact, add a row to the recruiter outreach log in the same file.

## What not to do

- Do not present hard-exclude roles unless the user explicitly asks
- Do not summarize every email — only relevant ones
- Do not guess at compensation when not disclosed — flag it as unknown
- Do not evaluate roles without loading both the criteria file and the applications tracker first
- If either file is missing, tell the user and point them to the templates rather than guessing at their criteria
- Do not include roles the user has already applied to in job alert output
