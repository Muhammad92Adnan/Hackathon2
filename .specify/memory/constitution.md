<!--
Sync Impact Report:
- Version change: N/A → 1.0.0 (initial constitution for Hackathon II - Todo App Evolution)
- List of modified principles: None (new constitution)
- Added sections: All sections (new constitution created)
- Removed sections: None
- Templates requiring updates: ⚠ pending - plan-template.md, spec-template.md, tasks-template.md need alignment with new principles
- Follow-up TODOs: None
-->
# Hackathon II - Todo App Evolution Constitution

## Core Principles

### Spec-Driven Development (NON-NEGOTIABLE)
All code must be generated via Claude Code from specs, no manual coding. All code changes must map back to spec/plan/tasks and be traceable through the development workflow.

### Phase-Based Evolution
Development follows 5 sequential phases: Console → Web → Chatbot → Local K8s → Cloud. Each phase must be completed before advancing to the next, with deployed applications and demo videos under 90 seconds for each phase submission.

### Monorepo Organization with Clean Code Standards
Single repository with frontend/backend separation, using descriptive names, docstrings, and proper structure. Technology stack is fixed per phase as defined in the project requirements.

### AI-First Development with Security
Use OpenAI Agents SDK, MCP tools for conversational interface, and Claude Code Subagents for reusable intelligence. Security & Secrets managed through environment variables, no hardcoded credentials, Better Auth with JWT for frontend/backend communication.

### Cloud-Native Architecture
Use Docker, Kubernetes, event-driven architecture with Kafka and Dapr. Neon PostgreSQL for database (Phase II+), OpenAI ChatKit for chatbot UI (Phase III+). WSL 2 required for Windows users for all development commands.

### Traceability and Compliance
All phases must have working applications with specs/plan/tasks traceable for every feature. Success criteria include completed phases with deployed applications and demo videos demonstrating features.

## Technology Stack Requirements

Phase I: Python 3.13+, uv, Claude Code, Spec-Kit Plus, in-memory storage
Phase II: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth with JWT
Phase III: OpenAI ChatKit, OpenAI Agents SDK, Official MCP SDK, stateless chat endpoint
Phase IV: Docker, Minikube, Helm charts, kubectl-ai, Kagent, Gordon (Docker AI)
Phase V: Kafka (Redpanda/Strimzi), Dapr, DigitalOcean DOKS/Azure AKS/Google GKE, event-driven architecture

## Development Workflow

Spec-Driven Development (NON-NEGOTIABLE) - All code must be generated via Claude Code from specs, no manual coding
Monorepo Organization - Single repository with frontend/backend separation
Clean Code Standards - Descriptive names, docstrings, proper structure
WSL 2 for Windows - Use WSL 2 for all development commands
Security & Secrets - Environment variables, no hardcoded credentials
AI-First Development - OpenAI Agents SDK, MCP tools for conversational interface
Cloud-Native Architecture - Docker, Kubernetes, event-driven with Kafka and Dapr

## Governance

This constitution supersedes all other development practices for the Hackathon II - Todo App Evolution project. All code changes must map back to spec/plan/tasks. Amendments require documentation, team approval, and migration plan. All PRs/reviews must verify compliance with Spec-Driven Development and Phase-Based Evolution requirements. No manual coding is allowed - must use spec-driven workflow. All phases must be completed in order with deployed applications and demo videos.

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08