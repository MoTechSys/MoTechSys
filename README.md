<div align="center">

<h1>م. معين العباسي · Moain Al-Abbasi</h1>

**Full-stack & applied-AI engineer** — Arabic-first products, deterministic verification systems, offline-first mobile apps.
<br/>
مهندس برمجيات وذكاء اصطناعي تطبيقي — أبني منتجات عربية أولًا: أنظمة تحقق حتمية، تطبيقات تعمل بلا إنترنت، ومنصات ويب فاخرة.

<br/>

[![Basira](https://img.shields.io/badge/Live-basirapp.site-2EF2C2?style=for-the-badge&labelColor=12183F)](https://basirapp.site)
[![Telegram Bot](https://img.shields.io/badge/Telegram-@BasiraCheckBot-6150EA?style=for-the-badge&logo=telegram&logoColor=white&labelColor=12183F)](https://t.me/BasiraCheckBot)
[![GitHub](https://img.shields.io/badge/GitHub-MoTechSys-12183F?style=for-the-badge&logo=github)](https://github.com/MoTechSys)

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

| Project | What it is | Stack |
|---|---|---|
| [**Project-Basira**](https://github.com/MoTechSys/Project-Basira) | Deterministic Quran & Hadith quotation checker — web, API, MCP, Telegram | Python · FastAPI · NumPy · React 19 · TypeScript |
| [**mohanad-web-app-2**](https://github.com/MoTechSys/mohanad-web-app-2) | دفتر البقالة — offline-first Android accounting for small groceries: append-only ledgers, shifts, barcode, PDF/Excel, 157 tests | Flutter · Dart · Hive |
| [**Sijilati**](https://github.com/MoTechSys/Sijilati) | سجلاتي — digital debt ledger for Yemeni shops, works without internet | Flutter · Dart |
| [**ghaida**](https://github.com/MoTechSys/ghaida) | غيداء — smart guide that trains domestic workers in their own language with AI voice, video and tailored schedules | TypeScript · Python |
| [**S-ACM-Project**](https://github.com/MoTechSys/S-ACM-Project) | Smart Academic Content Management System | TypeScript · Hono · PostgreSQL · Drizzle |
| [**keif-aldiafa-web**](https://github.com/MoTechSys/keif-aldiafa-web) | كيف الضيافة — production website for a Saudi hospitality business (CRO, SEO/GEO, PDPL) | Next.js · TypeScript |
| [**electricity-billing-pwa-v2**](https://github.com/MoTechSys/electricity-billing-pwa-v2) | Electricity billing PWA, fully local (IndexedDB), no server | TypeScript · PWA |

---

## 🛠️ Toolbox

- **Languages** · Python · TypeScript · JavaScript · Dart · Go · SQL
- **Backend** · FastAPI · Pydantic · Hono · Node.js · PostgreSQL · Drizzle · REST · Model Context Protocol (MCP)
- **Frontend & mobile** · React 19 · Next.js · Vite · Tailwind CSS · Flutter · PWA · RTL / Arabic-first UX · accessibility (axe)
- **AI & NLP** · Arabic text normalisation · information retrieval (BM25, n-grams, RRF) · fuzzy matching · LLM integration with constrained outputs · OCR pipelines · model benchmarking
- **Quality & ops** · pytest · vitest · Playwright · ruff · mypy strict · Docker · Caddy · GitHub Actions CI/CD · VPS deployment

---

## 🤖 How I build

I work with frontier AI coding agents — **Claude Opus 5.5 · Claude Fable 5.1 · GPT-6 Astra** via **Genspark** — under strict
engineering rules: every safety invariant has a named test, every number is measured and dated, every decision is
recorded, and nothing ships without passing the gates.

<div align="center">

<sub>Arabic-first · measured, not claimed · بصيرة: تعرض أين وُجد النص… ولا تحكم عليه</sub>

</div>
