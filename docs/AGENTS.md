# AI Agent & Vibe Coding Governance

This file defines what AI coding agents (Claude Code, Cursor, Windsurf, GitHub Copilot, etc.) are permitted to do in this repository. It is a contract, not a suggestion. If an agent-generated change violates a rule here, the change must be rejected and the rule must be referenced in the rejection reason.

---

## Source of Truth Hierarchy

When sources conflict, this order applies:

1. `docs/SECURITY_AND_COMPLIANCE.md` — security and compliance rules are never overridden
2. `docs/DATA_MODEL.md` — schema is the ground truth for data structures
3. `docs/ARCHITECTURE.md` — ADR table decisions are final for the stated phase
4. `docs/V1_SCOPE.md` — V1 feature boundaries are fixed
5. `PRODUCT_ROADMAP_v4.md` — phase sequence and exit gates
6. This file (`AGENTS.md`) — coding governance
7. Everything else

An agent may not override a higher-priority document to satisfy a lower-priority one.

---

## What Agents Can Do

- Read any file in the repository
- Propose new feature code in `app/`, `components/`, `lib/` (excluding restricted directories below)
- Write or edit Drizzle schema files in `lib/db/schema/` and propose the migration (`drizzle-kit generate`)
- Write unit tests and integration tests
- Write or edit Tailwind and shadcn/ui component files
- Propose changes to `app/api/` Route Handlers and Server Actions
- Write AI wrapper functions in `lib/ai/` following the PII boundary rule
- Propose changes to `turbo.json`, `package.json`, `tsconfig.json`

---

## What Agents Must Not Do

### Never, Under Any Circumstances

- Generate or print secrets, API keys, connection strings, or tokens in any file, comment, or log
- Run any command against the production database (no direct `psql`, no `drizzle-kit migrate --env production` without explicit human approval)
- Run database migrations without a rollback plan written in the same PR
- Create or modify Supabase RLS policies without a corresponding integration test
- Weaken any existing security control (removing an auth check, broadening an RLS policy, disabling a CI step)
- Add a dependency that is not on the allowlist below without getting human approval first
- Make architectural changes without an ADR entry in `docs/ARCHITECTURE.md`
- Send customer PII (names, phone numbers, order history) to any external API

### Restricted Directories — Human Review Required

Changes to these paths require explicit human review and approval before merge:

- `supabase/migrations/` — all schema changes
- `.github/workflows/` — all CI/CD changes
- `lib/auth/` — all auth logic
- `lib/db/service-role.ts` — service-role Supabase client usage
- `middleware.ts` — route protection
- `app/api/webhooks/` — webhook handlers (Moyasar, Unifonic)
- `lib/money/` — monetary conversion utilities

---

## Dependency Allowlist

Adding a new `npm` package requires it to appear here or have explicit human approval. This list reflects packages appropriate for V1.

**Approved:**
- next, react, react-dom (framework)
- typescript, @types/* (types)
- tailwindcss, @tailwindcss/*, postcss (styling)
- drizzle-orm, drizzle-kit (ORM)
- @supabase/supabase-js, @supabase/ssr (Supabase client)
- zod (validation)
- react-hook-form, @hookform/resolvers (forms)
- zustand (client state)
- shadcn/ui components (via `npx shadcn@latest add`)
- papaparse (CSV parsing)
- xlsx (Excel parsing)
- qrcode (QR generation)
- @mistralai/mistralai (Mistral SDK)
- groq-sdk (Groq SDK)
- resend (email)
- vitest, @vitest/*, testing-library/* (testing)
- eslint, prettier, lint-staged, husky (tooling)
- clsx, tailwind-merge, class-variance-authority (UI utilities)

**Not approved without discussion:**
- Any Google SDK (exception: `@googleapis/walletobjects` in V2 with documented rationale)
- Any analytics SDK that sends data to third parties
- Any logging SDK that sends data to third-party servers
- Axios (use native fetch)
- Moment.js (use date-fns or native Intl)
- Lodash (use native JS)
- Any image processing library that runs server-side without memory limits defined

---

## Maximum Change Size Per PR

- **Production code:** 500 lines changed (added + removed)
- **Tests:** no limit, but every PR that adds production code must include tests
- **Schema migrations:** one migration per PR; never combine feature code and migration in the same PR

If a feature requires more than 500 lines, split it into sequential PRs. Each PR must be independently deployable (no broken intermediate state).

---

## Mandatory Tests for Sensitive Areas

The following must have tests before any related code merges. "I'll add tests later" is not accepted for these areas:

| Area | Required Test Type |
|---|---|
| RLS policies | Integration test using two separate org users; verify Org A cannot read Org B's data |
| Authentication | Unit test for session validation; integration test for protected route rejection |
| Allergen confirmation flow | Unit test that `allergens_confirmed = false` items do not appear in public menu query |
| CSV import rollback | Integration test that rollback within 24 hours removes all imported items |
| Price changes | Unit test that price is stored in halalas; display converts correctly |
| Webhook handlers | Unit test with mock payload; idempotency test with duplicate event |
| AI audit events | Integration test that every AI call creates a row in `ai_audit_events` |

---

## AI-Specific Rules for Allergens and Pricing

1. An allergen returned by an AI model must be stored with `allergens_confirmed = false`
2. The UI must show the suggested allergens with a Confirm button — not auto-apply them
3. The public menu must query `WHERE allergens_confirmed = true` for allergen display
4. A price generated or suggested by an AI model (e.g., from a CSV mapping) must be shown to the user in the import review step before being written to the database
5. The word "confirmed" in UI copy must always mean a human explicitly clicked a confirm button — not auto-inferred

---

## Definition of Done (AI-Generated Code)

A PR generated by an AI agent is done when all of the following are true:

- [ ] `tsc --noEmit` passes with zero errors
- [ ] `eslint` passes with zero warnings (`--max-warnings 0`)
- [ ] All new and existing Vitest tests pass
- [ ] RLS integration tests pass (if data access was changed)
- [ ] Semgrep SAST finds no new HIGH or CRITICAL findings
- [ ] TruffleHog finds no secrets in the diff
- [ ] No restricted directory was changed without a human review note in the PR description
- [ ] If a migration was added: rollback SQL is included as a comment in the migration file
- [ ] If a new dependency was added: it appears on the allowlist or has explicit approval noted in PR
- [ ] If AI generates content: `ai_audit_events` write is included in the implementation
- [ ] If an ADR was changed: the change appears in `docs/ARCHITECTURE.md`
- [ ] PR description includes: what changed, why, how to test it, and what the rollback plan is

---

## No Direct Production Database Access

Agents must never run commands that connect to the production database directly. The only approved path for schema changes:

1. Write migration in `supabase/migrations/` via `drizzle-kit generate`
2. Test migration against local Supabase (`supabase start`)
3. Deploy to staging via CI and verify
4. Merge to `main` → CI deploys to production after 10-minute gate

There is no "just run this SQL quickly" path. If an emergency fix is needed in production, it goes through this pipeline with an expedited staging test.
