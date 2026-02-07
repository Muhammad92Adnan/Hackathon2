---
id: 1
title: "Hackathon-II Constitution Update"
stage: constitution
date_iso: "2026-02-08"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "hackathon-ii-todo-app"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Prompt History Record

## Original Prompt

```
"Project: Hackathon II - Todo App Evolution

Core principles:
- Spec-Driven Development (NON-NEGOTIABLE) - All code must be generated via Claude Code from specs, no manual coding
- Phase-Based Evolution - 5 phases in order: Console → Web → Chatbot → Local K8s → Cloud
- Monorepo Organization - Single repository with frontend/backend separation
- Clean Code Standards - Descriptive names, docstrings, proper structure
- WSL 2 for Windows - Use WSL 2 for all development commands
- Security & Secrets - Environment variables, no hardcoded credentials
- AI-First Development - OpenAI Agents SDK, MCP tools for conversational interface
- Cloud-Native Architecture - Docker, Kubernetes, event-driven with Kafka and Dapr

Key standards:
- All code changes must map back to spec/plan/tasks
- Use Claude Code Subagents for reusable intelligence
- Technology stack fixed per phase
- Better Auth with JWT for frontend/backend communication
- Neon PostgreSQL for database (Phase II+)
- OpenAI ChatKit for chatbot UI (Phase III+)

Technology Stack by Phase:
Phase I: Python 3.13+, uv, Claude Code, Spec-Kit Plus, in-memory storage
Phase II: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
Phase III: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK, stateless chat endpoint
Phase IV: Docker, Minikube, Helm charts, kubectl-ai, Kagent, Gordon (Docker AI)
Phase V: Kafka (Redpanda/Strimzi), Dapr, DigitalOcean DOKS/Azure AKS/Google GKE, event-driven architecture

Constraints:
- No manual coding allowed - must use spec-driven workflow
- All phases must be completed in order
- WSL 2 required for Windows users
- Demo video under 90 seconds for each phase submission

Success criteria:
- All phases completed with working applications
- Specs/plan/tasks traceable for every feature
- Deployed applications at each phase
- Demo videos demonstrating features"
```

## Response Summary

Created the project constitution file at `.specify/memory/constitution.md` with all the specified principles and governance structure for the Hackathon II - Todo App Evolution project. The constitution includes 6 core principles covering Spec-Driven Development, Phase-Based Evolution, Monorepo Organization, AI-First Development, Cloud-Native Architecture, and Traceability. It also includes sections for Technology Stack Requirements, Development Workflow, and Governance with version tracking.

## Outcome

Successfully created the Hackathon II - Todo App Evolution constitution with all specified principles and requirements. The constitution is now in place to guide the project's development according to the specified constraints and success criteria.