# 🤖 AI Setup 

This repo contains files and instructions for our local AI setup. It gives markdownfiles for subagents and skills, as well as setup instructions, general AI information and other stuff we find useful and want to be able to replicate easily on different systems. It's a way to share and exchange these files easily. It is also a platform where everyone who is interested can simply download the files and use it by themselves.

## 🔄 Sync Locally 

Want all the skills and subagents on your machine without copying files manually?
The `skill-sync/` folder contains a small Python script that clones this repo and
installs everything into your local AI tool config directories in one command:

```bash
cd skill-sync && bash install.sh
```

Supports Claude Code, Gemini CLI, and Codex. See [`skill-sync/README.md`](skill-sync/README.md) for full setup instructions.

## 🧭 Project Initialization

The repository now includes an `initialize` skill that can set up shared project
context for multiple coding agents at once.

Instead of writing separate context files by hand, the skill creates:

- `.ai/AI.md` as the shared project context
- `.ai/config.toml` as the per-project config file
- root-level symlinks like `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` pointing to `.ai/AI.md` when enabled

The bundled defaults live in `skills/initialize/config.toml`. They control:

- which agent symlinks should exist
- where the shared context file lives
- behavior flags for creating or removing symlinks safely
- optional sections included in the generated context file
- soft limits such as todo count and target file length

This keeps one canonical project context file while still supporting the
filename conventions expected by different agents.

## 👥 Collaboration

If you want to collaborate with us and be able to modify files, reach out to us and we can add you as a collaborator. Alternatively, you can always fork the repository and create a pull request if you want to contribute changes or improvements.

## 👨‍💻 Beginners

If you are completely new to using agents, then the `resources/` folder contains some basic guides. The file `01_setup.html` is here to help you set up the most popular coding agents in your terminal. From there you can then expand your knowledge by looking at the guides `02_subagents.html` and `03_skills.html` or by asking your AI agent of choice directly.

To practice hands-on, open `resources/workshop.html` — a task-based workshop that walks you through initializing a workspace, searching the web, creating files, spawning subagents, and writing your own custom skills, all step by step.

## 📦 Resources

**Skills & Subagents:**
- [Skills Library](https://www.skills.sh) — The original skills platform; browse and download SKILL.md files for Claude Code and other agents
- [Agents Library](https://subagents.cc/) — Curated collection of ready-to-use subagent definitions you can drop straight into your project
- [SkillsMP](https://skillsmp.com) — Skills marketplace covering Claude Code, Codex, and ChatGPT
- [Build with Claude](https://www.buildwithclaude.com/subagents) — Plugin marketplace for Claude Code (subagents, skills, commands, hooks)
- [Claude Plugins](https://claude-plugins.dev/) — Community registry with CLI installer for Claude Code plugins

**MCP Servers:**
- [mcp.so](https://mcp.so/) — Community-driven directory of 17,000+ MCP servers
- [MCP Market](https://mcpmarket.com/) — Directory of MCP servers and agent skills for Claude, Cursor, and other AI tools
- [OpenEcon Data](https://github.com/hanlulong/openecon-data) — Give your agent direct access to data from FRED, BLS, World Bank, and Census. 

**AI Coding Agents:**
- [Claude Code](https://claude.com/product/claude-code) — Anthropic's terminal-based AI coding agent, the main tool this repo is built around
- [Gemini-CLI](https://google-gemini.github.io/gemini-cli/) — Google's open-source terminal agent powered by Gemini, with a generous free tier
- [Codex](https://openai.com/codex/) — OpenAI's cloud-based coding agent that runs tasks autonomously in a sandboxed environment
- [GitHub Copilot](https://github.com/features/copilot) — AI coding assistant deeply integrated into VS Code and other IDEs
