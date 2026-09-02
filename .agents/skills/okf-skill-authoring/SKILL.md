---
name: okf-skill-authoring
description: An OKF skill is a skill whose body is an Open Knowledge Format bundle — one concept per markdown file, typed YAML frontmatter, cross-linked, with SKILL.md as the index — and this skill is the standard for authoring one. Use when creating, restructuring, renaming, or maintaining any skill in this repo. Covers SKILL.md anatomy, page structure and frontmatter, cross-linking, the index-routes-never-restates discipline, naming, and description writing.
---

# OKF Skill Authoring

## What OKF is

The Open Knowledge Format is a vendor-neutral spec (Google) that formalizes the LLM-wiki pattern: knowledge as a directory of markdown files with YAML frontmatter, cross-linked into a graph. One concept per file; the file path is the concept's identity; `type` is the only required frontmatter field. No tooling, no service — if you can read a file, you can read the bundle.

## What an OKF skill is

A standard skill directory whose body is an OKF bundle. `SKILL.md` is both the skill's entry point and the bundle's index.

## Structure

```
.agents/skills/<domain-name>/
├── SKILL.md       # frontmatter (name, description) + index body
├── <concept>.md   # one concept per page, typed frontmatter
└── <concept>.md   # ...
```

## Rules

1. **Name** the domain the skill governs (`python-development`), lowercase-hyphenated. Never an artifact word (`guide`, `docs`, `notes`) and never a name that fits every skill.
2. **Description** is three clauses in order: [What it does — teach what the thing is first, so a cold reader understands] + [When to use it] + [Key capabilities].
3. **The index routes, never restates.** The `SKILL.md` body is one line per page: what it is, when to read it. Content lives on the pages.
4. **Pages** carry one concept each, frontmatter with `type:`, and cross-link by relative path. Keep every page one link deep from `SKILL.md`.
5. **Keep `SKILL.md` small.** Pages are read on demand, at the moment of use — that is the constraint mechanism, so the index stays an index.
6. **Skip OKF's exchange apparatus** (`generated`, `verified`, `status`, `stale_after`, `sources`). Those fields exist for bundles traded across organizations; inside one repo they carry no meaning.
