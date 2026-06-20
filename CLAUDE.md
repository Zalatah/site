# Agent Context — Zalatah Restaurant SaaS

You are building a multi-tenant restaurant SaaS platform for the Saudi Arabian market. Read the following files before making any decisions:

- `docs/AGENTS.md` — your governance contract; rules you must not violate
- `docs/V1_SCOPE.md` — the exact feature list for V1; nothing outside this ships in V1
- `docs/ARCHITECTURE.md` — all architectural decisions are final; do not re-open them
- `docs/DATA_MODEL.md` — the database schema; use it exactly as written
- `docs/SECURITY_AND_COMPLIANCE.md` — security rules including the AI safety contract
- `PRODUCT_ROADMAP_v4.md` — phase sequence and exit gates

## Non-negotiable rules

- All prices are stored as integers in halalas (1 SAR = 100 halalas). Never use floats for money.
- Every table-level data mutation writes a row to `audit_events`.
- Every AI call writes a row to `ai_audit_events` before the result is applied.
- Allergen suggestions from AI are never auto-published. They require `allergens_confirmed = true` set by a human action.
- Customer PII (names, phone numbers, order history) never goes to any external AI API.
- Authentication and authorization are always deterministic TypeScript. Never ask an AI model if a user is allowed to do something.
- `SUPABASE_SERVICE_ROLE_KEY` is used only inside `lib/db/service-role.ts`. Nowhere else.
- Migrations go in `supabase/migrations/` via `drizzle-kit generate`. Never use `supabase db push`.
- When an environment variable is missing, return a graceful error — never crash the app.

## Stack

Next.js 15 (App Router) · TypeScript strict · Drizzle ORM · Supabase (local in dev) · shadcn/ui · Tailwind CSS v4 · Zod · React Hook Form · Zustand (UI state only)

## What is in scope right now

V0 (foundation) and V1 (pilot menu). See `docs/V1_SCOPE.md` for the exact list. Do not build anything from V1.1 onward unless explicitly instructed.
