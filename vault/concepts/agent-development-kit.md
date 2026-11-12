---
type: Concept
title: Agent Development Kit
description: Google's open-source framework for building, debugging and deploying AI agents in code.
resource: https://adk.dev/
tags: [adk, agents, google]
status: stable
generated: { by: human:kuanhoong, at: 2026-11-08T10:00:00Z }
verified: { by: human:kuanhoong, at: 2026-11-08T10:00:00Z }
stale_after: 2027-02-08T00:00:00Z
sources:
  - id: adk-2-0-docs
    resource: /references/adk-2-0-docs.md
    title: Welcome to ADK 2.0
---

# Summary

ADK is Google's agent framework. An agent is a model plus instructions plus tools, and plain Python functions become tools. ADK 2.0 added a Workflow Runtime that runs agents, tools and functions as nodes in a graph.[^adk-2-0-docs]

# Key points

- ADK Python 2.0 reached general availability on 19 May 2026.[^adk-2-0-docs]
- `adk web` gives a local dev UI that shows every tool call an agent makes.
- Agents run on [Gemini Models](/concepts/gemini-models.md) with an AI Studio API key.
- External tools plug in through the [Model Context Protocol](/concepts/model-context-protocol.md).

# Related

- [Open Knowledge Format](/concepts/open-knowledge-format.md)

[^adk-2-0-docs]: Welcome to ADK 2.0
