# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A multi-agent AI system built with [CrewAI](https://crewai.com) (v1.3.0) that researches a topic and generates a blog post. Two agents run sequentially: **Report Generator** (produces a ~2000 word research report) → **Blog Writer** (converts it into a ~500 word blog post). Output goes to `blogs/blog.md`.

## Commands

```bash
# Install dependencies
crewai install

# Run the crew
crewai run
# or with uv directly (recommended when using Ants Platform observability)
uv run run_crew

# Test crew (n = number of iterations)
crewai test -n 3

# Train crew
crewai train -n 5

# Replay execution from a specific task
crewai replay

# Reset all agent memories
crewai reset-memories -a
```

## Architecture

This is a standard CrewAI project using the `@CrewBase` decorator pattern:

- **`src/research_and_blog_crew/crew.py`** — `ResearchAndBlogCrew` class: defines agents, tasks, and crew orchestration. Agents and tasks are loaded from YAML configs and wired together via decorators (`@agent`, `@task`, `@crew`). The crew runs in `Process.sequential` mode.
- **`src/research_and_blog_crew/main.py`** — Entry point. Sets up Ants Platform observability, defines the `topic` input, and kicks off the crew. Change the `topic` variable here to research a different subject.
- **`src/research_and_blog_crew/config/agents.yaml`** — Agent definitions (role, goal, backstory). Uses `{topic}` placeholder.
- **`src/research_and_blog_crew/config/tasks.yaml`** — Task definitions (description, expected_output, agent assignment). Uses `{topic}` placeholder.
- **`src/research_and_blog_crew/tools/custom_tool.py`** — Scaffold for custom tools (extend `BaseTool` from crewai).
- **`knowledge/user_preference.txt`** — User context injected as knowledge for the agents.

## Key Details

- **Python**: >=3.10, <3.14. Uses `uv` as package manager and `hatchling` as build backend.
- **Entry points** defined in `pyproject.toml`: `run_crew`, `train`, `replay`, `test`, `run_with_trigger`.
- **Ants Platform SDK** is integrated for observability (LLM calls, agent steps, tool usage, costs). Requires `ANTS_PLATFORM_PUBLIC_KEY`, `ANTS_PLATFORM_SECRET_KEY`, and `ANTS_PLATFORM_HOST` env vars. The SDK is sourced from GitHub via `[tool.uv.sources]` in `pyproject.toml`.
- **Environment variables** needed: `OPENAI_API_KEY`, `OPENAI_MODEL_NAME` (e.g., `gpt-4o-mini`) in a `.env` file.
