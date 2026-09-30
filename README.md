# agent-skills

A growing library of reusable AI agent skills for Kiro and other MCP-compatible AI assistants.

Skills in this repo are generic by design. Personal configuration stays in your own data files, outside any repository. Drop any skill into your project's `.kiro/skills/` directory and provide the files it requires to get started.

## Philosophy

- Skills define *behavior*, not *preferences*
- Personal criteria and data live outside the repo (e.g. `~/.jobsearch/`), so they are never committed
- Each skill documents what data files or MCP servers it depends on
- Skills work for anyone who provides the expected context files

## Installation

Copy any skill into your project's `.kiro/skills/` directory:

```bash
cp skills/gmail-job-search.md /path/to/your/project/.kiro/skills/
```

Or install user-wide so it's available across all your projects:

```bash
cp skills/gmail-job-search.md ~/.kiro/skills/
```

Then follow the setup instructions in each skill file.

## Available Skills

See [SKILLS.md](SKILLS.md) for the full index with descriptions and requirements.

| Skill | Description | Requires |
|-------|-------------|---------|
| [gmail-job-search](skills/gmail-job-search.md) | Filter job alert emails and recruiter outreach against your personal criteria | Gmail MCP, `~/.jobsearch/job-criteria.md`, `~/.jobsearch/applications.md` |

## Related

- [robinsjm2/jobsearch-harness](https://github.com/robinsjm2/jobsearch-harness) — Harness for running a job search as AI-assisted sprints with Tyme MCP; uses these skills
- Blog: *Building a personal job search operating system with AI agents and MCP* (coming soon)
