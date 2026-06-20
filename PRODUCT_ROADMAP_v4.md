# Zalatah → Restaurant SaaS: Product Roadmap v4

**Core value proposition:**
> Turn a restaurant's existing PDF, spreadsheet, photo, or website into a live bilingual, SFDA-aware QR menu in under 30 minutes.

**Supporting documents:** [Strategy](docs/PRODUCT_STRATEGY.md) · [V1 Scope](docs/V1_SCOPE.md) · [Architecture](docs/ARCHITECTURE.md) · [Data Model](docs/DATA_MODEL.md) · [Security & Compliance](docs/SECURITY_AND_COMPLIANCE.md) · [Vendor Register](docs/VENDOR_REGISTER.md) · [Agents & AI Governance](docs/AGENTS.md)

---

## Phase Map

| Phase | Name | Entry Gate | Primary Output | Exit Gate |
|---|---|---|---|---|
| **-1** | Validation | — | 15 interviews → 5 pilots → 3 paying | Median launch ≤ 30 min; 3 restaurants confirmed paying |
| **V0** | Platform Core | Phase -1 passed | Auth + DB + storage + CI pipeline | Green CI; staging deploys cleanly |
| **V1** | Pilot Menu | V0 done | Bilingual SFDA-compliant public menu | 5 pilots live; founder support < 2 hrs/week |
| **V1.1** | Import & Migration | V1 in active use | CSV, PDF, photo, URL import wizard | Any migration completes in < 30 min |
| **V1.2** | WhatsApp Management | V1.1 stable | Bot: add/edit/86 items via WhatsApp | 3 restaurants managing menu via bot |
| **V1.3** | Billing & Multi-user | 10+ paying restaurants | Moyasar subscriptions + staff roles | SAR 10,000 MRR |
| **V2** | Loyalty & Wallets | V1.3 stable | Stamp cards in Apple/Google Wallet | 3 restaurants running loyalty |
| **V3** | Ordering & Payments | V2 stable | Direct order checkout via Moyasar | Positive GMV for 2+ restaurants |
| **V4** | Delivery | V3 stable | Driver dispatch + live tracking | — |

---

## Phase -1 — Validation

**Before writing a single line of product code.**

### Activities
- 15 structured interviews with Saudi restaurant owners (cafes, casual dining, QSR)
- 5 pilot restaurants onboarded manually (founder creates their menu)
- 3 pilots converted to a paying commitment (letter of intent or deposit)
- Measure: time from "send us your menu" to live QR link
- Measure: weekly active usage of the menu link (QR scans)
- Measure: founder support time per restaurant per week

### Go / No-Go Gates
| Gate | Threshold | Action if missed |
|---|---|---|
| Interview signal | ≥ 10/15 cite "no time to enter data" as the friction | Pivot value prop |
| Pilot launch time | Median ≤ 30 minutes | Simplify scope further |
| Paying commitment | ≥ 3 of 5 pilots willing to pay ≥ SAR 60/month | Reduce to free tool; reassess |
| Support burden | ≤ 2 founder hours/week across all pilots | Fix before scaling |

**Entry criteria for V0:** all four gates passed.

---

## V0 — Platform Core

**Deliverables:** working authentication, database, file storage, and CI pipeline. No product features ship in V0.

### Scope
- Supabase Cloud project (EU region; migrate to KSA self-hosted when a paying enterprise customer triggers the PDPL hard requirement)
- Drizzle ORM + `drizzle-kit migrate` — all schema changes via checked-in migration files
- Next.js 15 monolith: `app/` directory, Server Actions for mutations, Route Handlers for webhooks
- GitHub Actions CI: lint → typecheck → unit tests → DB integration tests → secret scan → build
- Staging and production environments separated (different Supabase projects, different Cloudflare Pages environments)
- Encrypted off-site backup configured before production receives any data

### Excluded
Everything else.

### Exit Gate
CI is green on an empty schema. Staging deploys from `main` without manual intervention.

---

## V1 — Pilot Bilingual Menu

**Deliverables:** a restaurant owner can sign up, build their menu, and share a QR-linked public page in ≤ 30 minutes.

### In Scope
See [V1_SCOPE.md](docs/V1_SCOPE.md) for the definitive list. Summary:
- Organization profile (name AR/EN, logo, hours, social links, phone)
- Category + item CRUD (name AR/EN, description AR/EN, price in halalas, image, availability)
- SFDA fields: calories, sodium, caffeine, allergens (AI-suggested, human-confirmed)
- AI translation (Arabic → English) via Mistral, with mandatory human approval step
- Manual CSV import (papaparse, column-mapping UI)
- Public mobile menu at `/[slug]`
- QR code generation (PNG + SVG download)
- Promotional banner (one active banner per menu)
- Single owner per restaurant (no team roles in V1)

### Excluded from V1
Billing, subscriptions, multi-user access, WhatsApp bot, wallet passes, loyalty, ordering, image AI generation, PDF/photo/URL import, website scraping, analytics dashboards, white-label, custom domains.

### Exit Gate
5 pilot restaurants live. Founder support time ≤ 2 hrs/week. SFDA fields complete on ≥ 80% of items across pilots.

---

## V1.1 — Import & Migration

**Entry:** V1 in active use with ≥ 5 restaurants. At least one restaurant has requested faster onboarding.

**Deliverables:** any restaurant can migrate their full menu from an existing source in under 30 minutes without manual re-entry.

### In Scope
- CSV / Excel import with AI column mapping (Mistral)
- PDF menu extraction (Mistral Pixtral vision)
- Photo of paper menu extraction (Mistral Pixtral vision)
- Current website URL crawl: Jina Reader two-pass (homepage → menu subpage) → Mistral extraction of menu items, hours, social links, phone, address, logo
- WhatsApp photo import flow (owner sends photos to a temporary number → bot → Pixtral → review link)
- `import_jobs` table + 24-hour rollback

**Exit Gate:** any migration source completes in < 30 minutes, including review step.

---

## V1.2 — WhatsApp Management

**Entry:** V1.1 stable and ≥ 10 restaurants active. At least 3 requesting WhatsApp-based management.

**Deliverables:** restaurant owner can add, edit, 86, and re-enable menu items via WhatsApp conversation.

### In Scope
- Cloudflare Worker (WhatsApp webhook handler — first non-monolith service)
- Unifonic BSP integration; one WABA per restaurant via Embedded Signup
- Conversational flow: add / edit / remove / toggle availability
- Mistral intent parsing; Groq allergen detection (free tier with Mistral fallback)
- Session state (30-min TTL) in Supabase
- 7 pre-approved Meta templates

**Not in scope for V1.2:** AI image generation, loyalty stamps, ordering.

---

## V1.3 — Billing & Multi-user

**Entry:** ≥ 10 restaurants using V1.1 or V1.2 and willing to pay.

**Deliverables:** Moyasar subscription billing, team roles (owner / manager / staff), plan-gated features.

### Pricing (SAR/month, ex-VAT)
| Tier | Price | Limits |
|---|---|---|
| Free | 0 | 1 menu, 20 items, platform branding |
| Starter | 60 | 3 menus, 100 items |
| Pro | 150 | Unlimited menus/items, custom domain, 3 locations |
| Business | 375 | White-label, API, multi-location |
| AI image credit | SAR 5/generation; SAR 50 for 10-pack | All tiers |

---

## V2 — Loyalty & Wallets

**Entry:** V1.3 stable at SAR 10,000 MRR.

**Deliverables:** stamp and points loyalty programs with Apple Wallet + Google Wallet passes. Staff PWA for stamping. AI-assisted campaign creation.

*See docs/ for detailed design when V2 development begins. Full Apple/Google Wallet spec, Staff PWA spec, and AI campaign spec from v3 apply here without modification.*

---

## V3 — Ordering & Payments

**Entry:** V2 stable with ≥ 3 restaurants running loyalty.

**Deliverables:** direct order checkout via Moyasar (Mada, Visa/MC, Apple Pay, STC Pay). Order management. KDS. ZATCA e-invoicing (build or partner). Loyalty auto-award on order. Tamara BNPL for orders ≥ SAR 300.

---

## V4 — Delivery

**Entry:** V3 with confirmed GMV from ≥ 2 restaurants.

**Deliverables:** delivery zone setup (Mapbox), driver PWA, dispatch dashboard, Supabase Realtime live tracking, Aramex overflow, AI ETA prediction.

---

## Key Principles

1. **KSA data residency** triggers self-hosted Oracle migration at first PDPL hard requirement — not before
2. **RLS + app-layer authorization** — both always; service-role key behind named domain functions only
3. **AI outputs are suggestions** — allergens, translations, and descriptions require human confirmation before publishing
4. **Integer money** — all prices in halalas (1 SAR = 100 halalas); never store floats
5. **One migration tool** — Drizzle Kit only; no `supabase db push` in any environment
6. **Boring technology** — no framework or service added without a concrete current need
7. **Validation before code** — each phase has measurable entry and exit gates
8. **Backups before users** — encrypted off-site backups configured before production receives data
