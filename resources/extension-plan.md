# Repository Assessment: ai-setup

## Context

This is an AI agent configuration repository for the Institute of Economics and Econometrics at the University of Geneva. It provides a curated set of specialized AI subagents (domain experts), reusable skills, and progressive educational HTML guides — all structured for use with Claude Code and similar AI CLI tools.

---

## Upsides

### 1. Clear Separation of Concerns
- `agents/` — persona/expert definitions
- `skills/` — reusable task templates
- `resources/` — educational HTML guides

Each layer is independently usable, composable, and understandable.

### 2. Strong Domain Coverage for the Target Audience
Ten well-defined agents covering a coherent academic domain (economics):
- Micro, macro, econometrics, health, labor, development economics
- Mathematical proofs expert
- Gemini-powered external research
- Code reviewer and writing critic

### 3. Consistent, Professional Agent Definitions
Every agent uses the same YAML frontmatter schema (`name`, `description`, `model`, `color`, `tools`). The definitions are detailed, cite canonical literature, and articulate clear output standards and workflows.

### 4. Thoughtful Model Assignment
- `opus` for specialist reasoning tasks (math, economics)
- `sonnet` for lighter-weight tasks (writing critique, research routing)

This shows intentional cost/capability balancing.

### 5. Educational Resources Are Self-Contained
The four HTML guides form a progressive onboarding path — from installation through subagents, skills, and a full hands-on workshop — without any external build toolchain required.

### 6. Safety-Conscious Skill Definitions
The `commit` skill explicitly encodes a git safety protocol (no force push, no `--no-verify`, no config modification), which is a good pattern for shared environments.

---

## Shortcomings

### 1. No Testing or Validation Layer
There is no way to verify that any agent or skill works as intended. No test prompts, no example outputs, no CI pipeline. A broken agent definition would only be discovered at runtime.

### 2. Agent Definitions Are Not Versioned Semantically
Files have no version field in their frontmatter. If an agent's behavior changes across Claude model generations, there is no way to track what behavior a given definition was designed for.

### 3. Overlap and Redundancy Among Economics Agents
Health, labor, and development economics share much of the same YAML structure and empirical methods (DiD, RDD, IV). There is no shared "base economist" template to avoid duplication. Updating a shared method across all three requires editing three files manually.

### 4. The Gemini Agent is Brittle
`gemini-assistant.md` assumes `gemini` is available on the PATH as a CLI tool. This is a runtime dependency that is never documented as a prerequisite. On a system where this CLI is missing, the agent will silently fail.

### 5. Resources Are Static HTML with No Build Process
The HTML guides appear to be hand-crafted. Any updates must be made by directly editing raw HTML, which is error-prone and not maintainable at scale. There is no templating, no component reuse, and no automated deployment.

### 6. No MCP Server Definitions
The README references MCP (Model Context Protocol) servers but there are none configured in the repository itself. This is a gap between the documentation's promise and what the repo actually delivers.

### 7. .gitignore Pre-hides Future Resources
`resources/04_*.html` through `resources/14_*.html` are gitignored, implying a planned roadmap of 11 additional guides that do not yet exist. This creates a confusing gap between intent and reality.

### 8. No Metadata for Discoverability
There is no `index.json` or manifest listing all agents and skills, their capabilities, or their dependencies. Finding the right agent requires reading every file manually.

---

## Recommended Extensions

### Priority 1: Add a Manifest / Index
Create `agents/index.json` and `skills/index.json` listing each component's name, description, model, and tags. This enables programmatic discovery and would power a future UI or CLI selector.

### Priority 2: Add a Shared "Base Economist" Agent Template
Extract the common structure (empirical methods, LaTeX formatting, academic writing standards) shared across health/labor/development economics agents into a documented base template. Individual agents reference and extend it. This reduces maintenance burden.

### Priority 3: Add Example Prompts and Expected Outputs
For each agent, add an `examples/` directory with canonical input prompts and example outputs. This serves both as documentation and as a manual regression test suite.

### Priority 4: Document Gemini CLI as a Prerequisite
Add a `PREREQUISITES.md` or a section in the README that clearly lists external tool dependencies (Gemini CLI, Node.js, etc.) with install instructions and version requirements.

### Priority 5: Build the Resource Guides from Markdown
Replace the hand-crafted HTML with a lightweight static site generator (e.g., 11ty or pandoc). Source content in Markdown, generate HTML as an artifact. This would make contributing new workshop tasks far less error-prone.

### Priority 6: Add CI Validation
A simple GitHub Actions workflow that:
1. Lints YAML frontmatter in all agent/skill files
2. Checks that all referenced tools exist
3. Validates that no gitignored resources are accidentally committed

### Priority 7: Add Economics Data & Code Agents
Given the audience, agents that help with:
- **Stata/R code review** — annotate or debug econometric scripts
- **Data cleaning advisor** — guide IPUMS, World Bank, Eurostat data wrangling
- **Replication advisor** — check if a paper's methodology can be replicated

### Priority 8: Add a Political Economy / Public Finance Agent
A gap in the current agent suite — fiscal policy and redistribution are covered lightly in the macroeconomics agent but warrant a dedicated expert with focus on taxation, public goods, and voting theory.
