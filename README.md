# Koi

Koi is an evolving banking copilot that moves from a secure read-only banking API toward an agentic fintech assistant with persistent conversation, governed tools, modern product UI, and production-oriented orchestration.

Koi is an authenticated, read-only banking co-pilot featuring a decoupled backend, data persistence, a chat feature, an agent-based roadmap, and an initial UI that is already connected to the API.

The project is designed as a progressive architecture: first a reliable banking backend, then a conversational layer, then real LLM integration, then stateful orchestration, and finally specialist and advanced agent systems. This staged evolution keeps the platform understandable, testable, and safe while allowing increasingly capable AI features.

## Vision

Koi aims to become a fintech copilot capable of understanding banking questions, maintaining conversational context, using trusted banking tools, retrieving grounded knowledge, and progressively evolving toward orchestrated agent workflows.

The platform starts from deterministic and controlled foundations, then adds semantic understanding, memory, retrieval, observability, graph orchestration, specialist agents, and later experimentation with more advanced agent architectures.

## Current direction

Koi follows a layered stack:

- FastAPI as backend application and API surface.
- Streamlit as temporary product UI and validation layer.
- LangChain as the composable LLM application layer.
- LangSmith as the observability and evaluation layer.
- LangServe as the deployment exposure layer for chains, graphs, and agents.
- LangGraph as the stateful orchestration layer for agent workflows.
- Next.js as the target professional frontend in later stages.
- CrewAI and Deep Agents as later experimentation layers, not as the initial product core.

## Architectural evolution

The project does not jump directly into multi-agent complexity. Instead, it evolves in a sequence of increasing capability.

1. Secure banking API and persistence.
2. Conversational chat UX and session continuity.
3. LLM-ready semantic contracts.
4. First real LLM calls with structured output.
5. Retrieval and grounding.
6. Stateful orchestration with LangGraph.
7. Product-grade frontend and deployment split.
8. Specialist agents and governed tools.
9. Advanced agent experimentation.

## LangChain ecosystem in Koi

Koi uses the LangChain ecosystem as a progressive stack rather than as a single isolated library.

### Sequential LangChain adoption

| Stage | Capability | Usage in Koi | Outcome |
|---|---|---|---|
| 1 | LangChain core | Base abstractions for prompts, chat models, output parsing, retrievers, and composable chains | Provides a modular LLM application foundation |
| 2 | Runnables / LCEL | Composition of prompt-model-parser and retriever-model flows with `invoke`, `batch`, and `stream` patterns | Makes pipelines composable, testable, and easier to evolve |
| 3 | Structured output | Intent classification, entity extraction, clarification state, and machine-usable contracts | Replaces fragile free-form parsing with reliable schemas |
| 4 | Tools | Banking operations, retrieval functions, and external capabilities exposed as callable tools | Prepares the system for controlled tool usage |
| 5 | Agents | Model-driven decision making and tool selection beyond deterministic routing | Moves Koi from chat app toward agentic copilot |
| 6 | LangServe | Exposure of chains, graphs, and agents through API endpoints such as `/invoke` and `/stream` | Separates backend execution from frontend consumption |
| 7 | LangSmith | Tracing, evaluations, monitoring, and run inspection for LLM workflows | Makes the system observable and safer to evolve |
| 8 | LangGraph | Stateful orchestration with nodes, edges, branching, retries, and checkpoints | Enables robust, controllable agent workflows |
| 9 | Multi-agent expansion | Specialist agents, governed tools, and controlled handoffs | Extends Koi into modular agent systems |
| 10 | Deep agent experimentation | Exploration of deeper reasoning and complex multi-step workflows | Adds a path toward more advanced agent architectures |

### LangChain capabilities used or planned

#### LangChain core

LangChain provides the core abstractions for prompts, chat models, retrievers, output parsing, and chain composition. In Koi, this layer is the base from which the conversational and agentic capabilities evolve.

#### Runnables and LCEL

Koi progressively adopts the Runnable interface to standardize execution through `invoke`, `batch`, and `stream`. This makes the system easier to compose and extend as new retrieval, classification, and orchestration steps are added.

#### Structured output

A key evolution in Koi is the move from free-form responses toward structured outputs for intent detection, entities, clarification flags, and planner-friendly machine-readable state.

#### Tools

Koi evolves toward a tool-oriented architecture where banking capabilities and retrieval functions are represented as explicit callable tools. These tools later become typed and governed for safer execution.

#### Agents

Agent capabilities are introduced gradually. Koi starts with controlled routing and later moves toward model-based decision making, tool use, and specialist execution paths.

#### LangServe

LangServe exposes chains, graphs, and agent flows as API endpoints. This layer allows the frontend to consume a stable agent interface while backend execution remains decoupled.

#### LangSmith

LangSmith is the observability and evaluation layer of Koi. It enables tracing, evaluation datasets, inspection of runs, and safer iteration on prompts, chains, tools, and graphs.

#### LangGraph

LangGraph is the framework used when Koi moves from composable LLM pipelines into stateful orchestrated workflows. It provides explicit state, routing, branching, retries, and controlled execution for more advanced banking flows.

#### CrewAI and Deep Agents

CrewAI and Deep Agents are placed in later stages as experimentation layers for more advanced collaborative or deeper reasoning workflows. They are not the initial architectural core of Koi.

## Roadmap

Koi evolves from a read-only banking API into a stateful, observable, agentic fintech copilot through a staged roadmap that introduces conversational UX, LLM features, retrieval, orchestration, and advanced agent capabilities in sequence.[cite:2061]

| Sprint | Version | Goal | Key deliverables | Architectural value |
|---|---|---|---|---|
| 1 | v0.1.0 | Base project scaffolding | Poetry, FastAPI, health check, initial modular structure, environment configuration | Maintainable foundation prepared for growth |
| 2 | v0.2.0 | Authenticated read-only banking baseline | Mock auth, demo users, `/auth/me`, accounts, balance, transactions, and mock Bizum endpoints | First functional contract for a read-only banking API |
| 3 | v0.3.0 | Chat endpoint with rule-based banking routing | Protected `/chat`, `ChatIntent`, deterministic router, unit tests | Separates intent, handlers, and response layer |
| 4 | v0.4.0 | API hardening, persistence, and quality | HTTPBearer/JWT, SQLite persistence with SQLModel for banking data and chat messages, robust errors, expanded tests, README and CHANGELOG | Serious backend base for product evolution |
| 5 | v0.5.0 | Conversational banking core and LLM-ready semantic architecture | Closed taxonomy of banking intents and entities; structured contract for `intent_agent` (`intent`, `confidence`, `entities`, `missing_entities`, `needs_clarification`, `tool_candidates`); read-only banking tools (`get_balance`, `get_accounts`, `get_recent_transactions`, `get_recent_bizum`); entity resolution across message and context; real multi-turn clarification; minimal deterministic validation; basic persistence of decisions and traces | First production-grade conversational banking core that leaves the system ready for real LLM semantic classification without relying on scattered ad hoc logic |
| 6 | v0.6.0 | Professional product UI / frontend MVP | First product frontend for login, accounts, balance, movements, Bizum, and chat connected to the API; persistent sessions with `session_id`; Streamlit remains as temporary validation UI | Enables a real product demo without relying on Swagger and establishes Streamlit as temporary UI |
| 7 | v0.7.0 | Conversational UX, session state, and persistent chat history | Real `ChatSession` handling; persistent history by user and session; recovery of previous messages; continuity of pending clarifications; sidebar or session list; improved chat UX | Introduces real conversational continuity and prepares the base for memory and reusable context |
| 8 | v0.8.0 | First real LLM integration and observability foundations | First real LLM call for `intent_agent` with structured output (`intent`, `confidence`, `entities`, `missing_entities`, `needs_clarification`); deterministic fallback on low confidence; initial LangSmith integration for traces, evaluation dataset, and classification and clarification metrics | Marks the real start of the LLM layer in Koi, moving from LLM-ready design to observable semantic inference |
| 9 | v0.9.0 | Guardrails and safe fintech interaction | Input validation, output control, anti prompt-injection, stronger read-only mode, safe interaction policies | Separates a functional conversational core from a safer fintech system |
| 10 | v1.0.0 | Deployment-ready MVP with LangServe | Docker, CI/CD, environment-based deployment, release checklist, publication of chains or agent capabilities through LangServe, initial `/invoke` and `/stream` integration | Transforms Koi from a local project into a deployable MVP with API exposure for LLM workflows |
| 11 | v1.1.0 | Memory architecture and user context | Short-term and long-term memory, user preferences, retention and deletion policies, reusable operational context, conversational persistence design over DynamoDB | Separates memory, profile, and operational context and prepares scalable conversation persistence |
| 12 | v1.2.0 | Retrieval and banking knowledge layer | RAG for FAQs, policies, glossary, and banking content; retrieval refinement; grounding; retrieval evaluation; S3 storage for source documents and artifacts; OpenSearch as vector store | Adds grounded banking knowledge and consolidates retrieval as a core capability |
| 13 | v1.3.0 | LangGraph orchestration architecture | Explicit graph with LangGraph, planner or router, synthesis, retries, fallbacks, branching, node separation by responsibility, PostgreSQL for technical checkpoint persistence | Marks the explicit move from chain-based application to graph-based agent system |
| 14 | v1.4.0 | Frontend product bridge | Product UI connected to API and agent, auth, persistent sessions, visible history, working end-to-end chat; Streamlit remains as transitional frontend while migration to Next.js is prepared | Turns Koi into a demonstrable product experience and prepares migration toward a professional web frontend |
| 15 | v1.5.0 | Next.js professional frontend | New professional frontend in Next.js inspired by modern digital banking UX: Tailwind, shadcn/ui, app shell, session sidebar, topbar, premium chat, account cards, empty states, consistent banking UX | Introduces a real product-grade web frontend separated from the backend |
| 16 | v1.6.0 | Frontend-backend split and typed client | Separate frontend server and backend server deployment; typed client generated from OpenAPI; stable contracts for chat and session APIs; streaming-ready interfaces; repository abstraction to decouple local and cloud persistence | Formalizes the architectural split between client and server and stabilizes full-stack integration |
| 17 | v1.7.0 | LangChain runnables and composable execution layer | Explicit adoption of Runnable-based composition for prompt-model-parser and retriever-model flows; standardization around `invoke`, `batch`, and `stream`; better separation between business endpoints and LLM execution components | Makes the LLM layer composable, reusable, and easier to test and evolve |
| 18 | v1.8.0 | Governed and structured tools layer | Catalog of typed and auditable tools for accounts, balance, transactions, Bizum, cards, FAQs, and documents; timeouts, contracts, structured inputs, and logs per tool; S3 for long execution artifacts | Converts capabilities into governed tools that can be safely reused by agents |
| 19 | v1.9.0 | Specialist agents with LangGraph | Orchestrator plus specialist agents for Accounts, Transactions, Cards, Bizum or Payments, Information or RAG, Clarification, and Safety or Compliance, implemented on LangGraph with controlled handoffs | Introduces a modular specialist-agent architecture with control and traceability |
| 20 | v2.0.0 | Enterprise-grade fintech copilot showcase | Stable end-to-end demo, documented architecture, premium frontend, real tools, memory, observability, graph orchestration, and advanced storytelling of the system | Presents Koi as a mature fintech copilot platform |
| 21 | v2.1.0 | CrewAI experimentation layer | Evaluation of CrewAI for collaborative multi-agent scenarios, delegation experiments, and comparison with LangGraph-based specialist orchestration | Explores a more collaborative multi-agent approach without changing the product core too early |
| 22 | v2.2.0 | Deep Agents experimentation layer | Evaluation of deeper-reasoning agent approaches for hierarchical planning, complex multi-step execution, and advanced workflow reasoning; comparison with LangGraph and CrewAI in banking scenarios | Opens a path toward more advanced deep agent architectures while preserving the main system design |

## Framework adoption path across sprints

To make the evolution explicit, the LangChain ecosystem enters Koi in this sequence:[cite:2061]

- **LangChain core** becomes visible from the moment composable prompt and model logic is formalized.
- **LLM-ready semantic contracts** are introduced in Sprint 5.
- **Real LLM calls with structured output** arrive in Sprint 8.
- **LangServe** becomes part of the deployable stack in Sprint 10.
- **Memory and retrieval architecture** expand in Sprints 11 and 12.
- **LangGraph** becomes explicit in Sprint 13.
- **Runnable-based composition** is made explicit as an architectural layer in Sprint 17.
- **Governed structured tools** arrive in Sprint 18.
- **Specialist agents** arrive in Sprint 19.
- **CrewAI** and **Deep Agents** are explored only in later experimental stages.

## Technology direction

### Backend

- FastAPI
- SQLModel / SQLite in early stages
- DynamoDB for scalable conversation and memory persistence
- S3 for document and artifact storage
- OpenSearch for vector retrieval
- PostgreSQL for technical workflow persistence and checkpointing

### AI and orchestration

- LangChain core
- Runnable-based LLM execution
- Structured outputs
- Typed and governed tools
- LangServe
- LangSmith
- LangGraph
- Specialist agents
- CrewAI experimentation
- Deep Agents experimentation

### Frontend

- Streamlit as temporary POC UI
- Next.js as target professional frontend
- Tailwind CSS
- shadcn/ui

## Status philosophy

Koi is intentionally built in stages.

The early stages prioritize correctness, persistence, and banking API foundations. The middle stages introduce conversational continuity, real LLM calls, observability, retrieval, and orchestration. The later stages introduce specialist-agent systems and more advanced experiments such as CrewAI and Deep Agents.

This roadmap keeps the project coherent while making the progression toward a more capable agentic fintech copilot explicit.[cite:2061][cite:2066]