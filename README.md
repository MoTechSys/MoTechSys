<div align="center">

<h1>م. معين العباسي · Moain Al-Abbasi</h1>

**Full-stack, applied-AI & security engineer** — Arabic-first products, deterministic verification, multi-tenant platforms, offline-first apps.
<br/>
مهندس برمجيات وذكاء اصطناعي تطبيقي — أبني منتجات عربية أولًا: أنظمة تحقق حتمية، منصات متعددة المستأجرين، وكلاء ذكاء اصطناعي، تطبيقات تعمل بلا إنترنت، ومواقع فاخرة للعملاء.

<br/>

[![Basira](https://img.shields.io/badge/Live-basirapp.site-2EF2C2?style=for-the-badge&labelColor=12183F)](https://basirapp.site)
[![Telegram Bot](https://img.shields.io/badge/Telegram-@BasiraCheckBot-6150EA?style=for-the-badge&logo=telegram&logoColor=white&labelColor=12183F)](https://t.me/BasiraCheckBot)
[![GitHub](https://img.shields.io/badge/GitHub-MoTechSys-12183F?style=for-the-badge&logo=github)](https://github.com/MoTechSys)
[![GitHub 2](https://img.shields.io/badge/GitHub-moain2026-12183F?style=for-the-badge&logo=github)](https://github.com/moain2026)

</div>

---

## ⭐ Featured — بصيرة · Basira

> **Deterministic verification of Quran and Hadith quotations — before you publish.**
> Entry to the *AI in Service of Islamic Content Challenge 2026* — Track 4 (knowledge & verification tools).

Paste a post, an article, a chatbot answer or an image. Basira finds every quotation presented as Quran or Hadith,
matches it **byte-exactly** against licensed, sha256-pinned corpora (71,987 records), shows the verbatim source next to
the user's text with a **letter-level diff**, and returns one of four states. The language model only *proposes*
positions and reads images — **the deterministic engine decides**. No generated religious text, no rulings, no storage.

| Measured | Result |
|---|---|
| Evaluation (150 cases, 13 categories incl. prompt injection, 3 repeats) | **150/150**, variance 0 |
| False alarms on 500 verbatim corpus segments | **0/500** |
| IslamicEval 2025 · subtask 1B (dev) | **78.54 %**, only **2 / 100** wrong spans confirmed |
| Tests | 345 backend · 110 bot · 32 frontend · mypy `--strict` |

**Engineering highlights:** corpus-anchored seed-and-extend detection (BLAST-style) · three-tier Arabic normalisation ·
numpy positional index (< 5 ms / quote over 4.5 M tokens) · BM25 + char-3-gram + RRF retrieval · windowed
token-Levenshtein · harakat gate & rasm-uniqueness proof · 19 named safety invariants · validator that independently
re-proves every “found” · `determinism_hash` on every response · REST, **MCP server**, Guard for chatbots, Telegram bot ·
one-command run (`bash run.sh`).

**→ [Repository](https://github.com/MoTechSys/Project-Basira) · [Live site](https://basirapp.site) · [API docs](https://basirapp.site/docs)**

---

## 🧰 Selected work

### Platforms & systems

| Project | What it is | Stack |
|---|---|---|
| [**Project-Basira**](https://github.com/MoTechSys/Project-Basira) | Deterministic Quran & Hadith quotation checker — web, REST, MCP server, Telegram bot | Python · FastAPI · NumPy · React 19 |
| [**nexus-notify**](https://github.com/moain2026/nexus-notify) | Central multi-tenant, multi-channel notification & conversation platform behind one API | TypeScript |
| [**motech-platform**](https://github.com/moain2026/motech-platform) · [**motech-cli**](https://github.com/moain2026/motech-cli) | Secure remote-access management (SSH over a NetBird mesh) + a one-command cross-platform agent (Windows / Linux / macOS, amd64 + arm64) | Go · HTML |
| [**scam2027**](https://github.com/MoTechSys/scam2027) | Multi-tenant course & assessment manager for universities — PostgreSQL RLS, Auth.js, RBAC with 114 permissions | Next.js 16 · Prisma · PostgreSQL |
| [**Idhaat-Platform**](https://github.com/MoTechSys/Idhaat-Platform) | منصة إضاءات — live tutoring platform: live classes, protected 48-hour recordings, homework, messaging; installable PWA | TypeScript · PWA |
| [**hesabati**](https://github.com/moain2026/hesabati) | حساباتي — multi-business financial & accounting system with an Arabic UI | TypeScript |

### AI & security

| Project | What it is | Stack |
|---|---|---|
| [**Ai_Alabbasi**](https://github.com/moain2026/Ai_Alabbasi) | Swappable-brain autonomous coding agent: one config file switches between a strong API model and a local model | Python |
| [**telegram-mcp-2**](https://github.com/moain2026/telegram-mcp-2) | Expanded Telegram MCP server with safe tools and an HTTP wrapper — sanitized public release | Python · MCP |
| [**ghaida**](https://github.com/MoTechSys/ghaida) | غيداء — trains domestic workers in their own language with AI voice, video and tailored schedules | TypeScript · Python |
| [**my-bro**](https://github.com/MoTechSys/my-bro) | SOC graduation project — open-source Security Operations Center built on Wazuh SIEM | Python |
| [**digital-forensics-lab**](https://github.com/moain2026/digital-forensics-lab) | Hands-on digital forensics: Windows Registry, Event Log, Autopsy, FTK Imager, browser forensics — with real artifacts and tooling | PowerShell |

### Offline-first apps for real businesses

| Project | What it is | Stack |
|---|---|---|
| [**mohanad-web-app-2**](https://github.com/MoTechSys/mohanad-web-app-2) | دفتر البقالة — Android accounting for small groceries: append-only ledgers, vouchers, shifts, barcode, PDF/Excel, 157 tests | Flutter · Hive |
| [**Sijilati**](https://github.com/MoTechSys/Sijilati) | سجلاتي — digital debt ledger for Yemeni shops that works without internet | Flutter |
| [**electricity-billing-flutter**](https://github.com/MoTechSys/electricity-billing-flutter) · [**electricity-billing-pwa**](https://github.com/moain2026/electricity-billing-pwa) | Electricity billing for a power-generation company — Android app and a fully local PWA (IndexedDB, no server) | Flutter · Next.js · TypeScript |

### Web for clients

| Project | What it is | Stack |
|---|---|---|
| [**keif-aldiafa-web**](https://github.com/MoTechSys/keif-aldiafa-web) | كيف الضيافة — production site for a Saudi hospitality business (CRO, SEO/GEO, PDPL compliance) | Next.js · TypeScript |
| [**osoul-aldiafa-v2**](https://github.com/MoTechSys/osoul-aldiafa-v2) | أصول الضيافة — luxury hospitality website | Next.js 14 |
| [**royal-coffee-hospitality**](https://github.com/moain2026/royal-coffee-hospitality) | القهوة الملكية — Arabic hospitality site rebuilt with a luxury identity, native RTL, high performance | Hono · Cloudflare Pages |
| [**alabbasi-soft-site**](https://github.com/moain2026/alabbasi-soft-site) | Official website of Alabbasi Tech, a software house in Sana'a | Next.js 15 |

> Two accounts: **[@MoTechSys](https://github.com/MoTechSys)** (main) · **[@moain2026](https://github.com/moain2026)** (systems, AI agents, client work).

---

## 🛠️ Toolbox

- **Languages** · Python · TypeScript · JavaScript · Dart · Go · SQL · PowerShell
- **Backend** · FastAPI · Pydantic · Hono · Node.js · PostgreSQL · Drizzle · REST · Model Context Protocol (MCP)
- **Frontend & mobile** · React 19 · Next.js · Vite · Tailwind CSS · Flutter · PWA · RTL / Arabic-first UX · accessibility (axe)
- **AI & NLP** · Arabic text normalisation · information retrieval (BM25, n-grams, RRF) · fuzzy matching · LLM integration with constrained outputs · OCR pipelines · model benchmarking
- **Security** · SOC with Wazuh SIEM · digital forensics (Autopsy, FTK Imager, registry & event logs) · secure remote access (SSH, NetBird mesh)
- **Quality & ops** · pytest · vitest · Playwright · ruff · mypy strict · Docker · Caddy · GitHub Actions CI/CD · VPS deployment

---

## 🤖 How I build

I work with frontier AI coding agents — **Claude Opus 5.5 · Claude Fable 5.1 · GPT-6 Astra** via **Genspark** — under strict
engineering rules: every safety invariant has a named test, every number is measured and dated, every decision is
recorded, and nothing ships without passing the gates.

<div align="center">

<sub>Arabic-first · measured, not claimed · بصيرة: تعرض أين وُجد النص… ولا تحكم عليه</sub>

</div>
