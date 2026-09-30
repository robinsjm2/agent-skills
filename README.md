# agent-skills

A growing library of reusable AI agent skills for Claude Code, Kiro, and other MCP-compatible AI assistants.

Skills in this repo are generic by design. Personal configuration stays in your own data files, outside any repository.

Each skill is a folder containing a `SKILL.md`, following the [Agent Skills](https://agentskills.io) format: YAML frontmatter with a `name` and a `description` (which the agent uses to decide when to apply the skill), followed by the instructions.

## Philosophy

- Skills define *behavior*, not *preferences*
- Personal criteria and data live outside the repo (e.g. `~/.jobsearch/`), so they are never committed
- Each skill documents what data files or MCP servers it depends on
- Skills work for anyone who provides the expected context files

## Installation

### Claude Code

Symlink a skill into your user skills directory so edits to this repo take effect immediately:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skills/gmail-job-search" ~/.claude/skills/gmail-job-search
```

Claude uses the skill automatically when a request matches its description, or you can invoke it with `/gmail-job-search`. For a single project, link it into that project's `.claude/skills/` instead.

### Kiro

Copy the skill into your project's `.kiro/skills/` directory, or into `~/.kiro/skills/` to make it available across projects:

```bash
cp skills/gmail-job-search/SKILL.md ~/.kiro/skills/gmail-job-search.md
```

Then follow the requirements section of each skill.

## Available Skills

See [SKILLS.md](SKILLS.md) for the full index with descriptions and requirements.

| Skill | Description | Requires |
|-------|-------------|---------|
| [gmail-job-search](skills/gmail-job-search/SKILL.md) | Filter job alert emails and recruiter outreach against your personal criteria | Gmail MCP, `~/.jobsearch/job-criteria.md`, `~/.jobsearch/applications.md` |
| [job-search-sweep](skills/job-search-sweep/SKILL.md) | Search Indeed for new openings and verify remote status, pay, and fit from the full postings | Indeed MCP, `~/.jobsearch/job-criteria.md`, `~/.jobsearch/applications.md` |

## Related

- [robinsjm2/jobsearch-harness](https://github.com/robinsjm2/jobsearch-harness) — Harness for running a job search as AI-assisted sprints with Tyme MCP; uses these skills
- Blog: *Building a personal job search operating system with AI agents and MCP* (coming soon)
