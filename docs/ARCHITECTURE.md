# Architecture

## Architecture Decision Record (ADR) Table

Each decision is final for the stated phase. A reconsideration trigger must be met before reopening.

| Topic | Decision | Rationale | Trade-off | Reconsideration Trigger |
|---|---|---|---|---|
| **Repository structure** | Single Next.js monolith through V1.3 | Monorepo with 5 packages adds CI complexity and split-deploy overhead a solo founder cannot maintain productively | Harder to extract services later, but clean module directories make it possible | Adding a second deployment target (WhatsApp Worker in V1.2) — extract then |
| **Database** | Supabase Cloud (EU region, `eu-west-1`) | Zero ops burden; managed Postgres + Auth + Storage + Realtime; no Oracle VM to maintain during pre-revenue validation | EU region means Saudi PII is outside KSA — acceptable for pre-revenue pilot; must migrate at first enterprise/PDPL-triggered hard requirement | First paying enterprise customer OR government contract OR formal PDPL audit notice |
| **ORM / Migrations** | Drizzle ORM + `drizzle-kit migrate` exclusively | Explicit migration files checked into git; type-safe queries; works identically with Supabase Cloud and self-hosted | No `supabase db push` anywhere — not in docs, not in CI, not in developer notes | Never — `supabase db push` is permanently excluded |
| **Auth** | Supabase Auth (email + password; magic link optional) | Built into Supabase; JWTs carry `org_id` claim via database hook; no additional auth service | Vendor lock-in to Supabase Auth; acceptable given full stack is already Supabase | Moving off Supabase entirely |
| **Monetary values** | Integer halalas (1 SAR = 100 halalas) | Eliminates floating-point rounding bugs in pricing and tax calculation | Display layer must divide by 100; minor but explicit | Never — float money is permanently excluded |
| **AI text provider** | Mistral direct API (primary); Groq free tier (allergen detection with Mistral fallback) | Mistral: French company, no Israeli connection, strong Arabic support, cheapest paid option. Groq free tier for high-volume allergen detection. | Groq free tier limits change without notice — fallback is mandatory in code | Groq removing free tier or Mistral raising prices > 5× |
| **AI image provider** | fal.ai FLUX (V1.3+ when image generation is added) | No Israeli connection; single API for draft and production quality; background removal included | Not needed in V1; defer until V1.3 | When image generation is added |
| **Payment gateway** | Moyasar only (V1.3–V3); no abstraction layer until V3 is built | Moyasar is Saudi-native, SAMA-licensed, covers Mada/STC Pay/Apple Pay; no second gateway justified until GCC expansion | No payment provider abstraction in V1–V2 code; refactor required at GCC expansion | First paying customer in Kuwait, UAE, or Bahrain |
| **WhatsApp / SMS** | Unifonic BSP | Saudi-founded CPaaS; one WABA per restaurant via Embedded Signup; lowest KSA-native risk | Unifonic is a single point of failure for WhatsApp; document API stability | Unifonic outage > 4 hours in any 30-day period |
| **Cloudflare** | Accept for CDN, Pages, and Workers (application use) | No viable alternative provides edge compute + CDN + zero-config deploy in one platform at this price | Israeli R&D center confirmed — documented accepted risk; Workers process business data (not PII) | A KSA-native edge platform emerges with comparable capability |
| **Google Wallet** | Accept for Android loyalty passes (V2) | No viable Android wallet alternative exists; pass content is device-local display, not data processing | Contradicts "no Google" principle — documented accepted risk with explicit rationale | A non-Google Android wallet standard with comparable adoption emerges |
| **Background jobs** | pg_cron (V1); Cloudflare Worker cron triggers (V1.2+ when Worker exists) | pg_cron is built into Supabase Postgres; no additional service for V1 cron needs | Limited to database-side jobs in V1; acceptable for scheduled cleanup and session expiry | Needing non-database computation on a schedule before V1.2 |
| **Error monitoring** | GlitchTip self-hosted on Oracle VM (or Sentry free tier pre-revenue) | GlitchTip is Sentry-compatible, open source, free. Use Sentry free tier until first Oracle VM exists | Operational overhead of self-hosted; Sentry free tier as bridge | When Oracle VM is provisioned |
| **Analytics** | Umami self-hosted | Open source, no Google Analytics, no data leaving KSA for analytics | Self-hosted maintenance | When Oracle VM is provisioned |
| **Infrastructure (V1)** | Supabase Cloud + Cloudflare Pages + GitHub Actions | Zero-infrastructure start; no VM to manage | Not KSA data-resident; acceptable for pilot | First enterprise/PDPL hard requirement |
| **Infrastructure (V2+)** | Oracle Cloud KSA Always Free VM + self-hosted Supabase | KSA data residency; free compute | Oracle Always Free is not guaranteed capacity — treat as best-effort, not SLA | Oracle reclaims VM or raises Always Free limits → migrate to paid Oracle or Hetzner KSA |

---

## V1 Tech Stack

### Application
| Layer | Choice |
|---|---|
| Framework | Next.js 15 (App Router, Server Actions, Route Handlers) |
| Language | TypeScript 5.x strict mode |
| UI | shadcn/ui + Tailwind CSS v4 |
| RTL | `tailwindcss-rtl` plugin |
| Forms | React Hook Form + Zod |
| State | Zustand (UI-only; no server state) |
| ORM | Drizzle ORM |
| Auth | Supabase Auth (server-side only) |

### Infrastructure (V1)
| Service | Provider |
|---|---|
| Database + Auth + Storage + Realtime | Supabase Cloud (EU) |
| Frontend hosting | Cloudflare Pages |
| CDN / DNS | Cloudflare |
| CI/CD | GitHub Actions (GitHub Pro, $4/month) |
| Error monitoring | Sentry free tier (pre-VM); GlitchTip self-hosted (post-VM) |
| Analytics | Umami self-hosted (post-VM); Cloudflare Analytics (pre-VM) |
| Uptime | UptimeRobot (free, 50 monitors) |
| Email | Resend (free tier: 3,000/day) |
| OTP / SMS | Unifonic (pay-per-use) |

### AI (V1)
| Task | Provider | Model | Fallback |
|---|---|---|---|
| Arabic → English translation | Mistral direct | Ministral 3B | Mistral Nemo 12B |
| Allergen detection | Groq | Llama 3.1 8B (free) | Mistral Ministral 3B |
| Description writing | Mistral direct | Ministral 3B | — |
| CSV column mapping | Mistral direct | Ministral 3B | — |

---

## Module Structure (V1 Monolith)

```
app/
  (auth)/          # login, signup, verify-email
  (dashboard)/     # protected: menu builder, settings
    [orgSlug]/
      menu/        # category + item CRUD
      settings/    # profile, hours, social links
      import/      # CSV import wizard
  [slug]/          # public menu (no auth)
    page.tsx       # SSG/ISR public menu page
  api/
    webhooks/      # Unifonic, Moyasar (V1.3)
    ai/            # Mistral proxy (server-side, no API key to client)
    wallet/        # Apple Wallet endpoints (V2)
components/
  ui/              # shadcn/ui base components
  menu/            # MenuCard, CategoryHeader, BannerStrip
  admin/           # ItemForm, CategoryForm, ImportWizard
lib/
  db/              # Drizzle client + schema
  auth/            # Supabase server client, session helpers
  ai/              # Mistral + Groq wrappers
  storage/         # Supabase Storage helpers
  money/           # halala ↔ SAR conversion utilities
supabase/
  migrations/      # All schema changes (drizzle-kit generated)
```

**Rule:** `lib/ai/` functions never receive customer names, phone numbers, or order data. They receive menu content (item names, descriptions, ingredient lists) only.

**Rule:** `lib/db/service-role.ts` exports one function per operation, named explicitly (e.g., `pushAppleWalletUpdate`, `expireWhatsAppSessions`). The service-role Supabase client is never instantiated outside this file.

---

## Data Residency Migration Path

When the PDPL hard requirement is triggered:

1. Provision Oracle Cloud KSA Always Free ARM VM (4 CPU / 24GB RAM)
2. Deploy self-hosted Supabase via Docker Compose (Supabase self-hosted guide)
3. `pg_dump` from Supabase Cloud → `pg_restore` to Oracle KSA Postgres
4. Rotate all Supabase connection strings in GitHub Secrets and Cloudflare Worker secrets
5. Smoke test in staging before switching DNS
6. Keep Supabase Cloud project alive for 30 days as rollback

**Do not pre-build this.** Build it when you need it.

---

## Staging / Production Separation

| Environment | Database | Cloudflare Pages | Secrets |
|---|---|---|---|
| Staging | Separate Supabase project | Separate Pages project (auto-deploy from `main`) | Separate GitHub environment |
| Production | Production Supabase project | Production Pages project (manual promote or auto-deploy with 10-min gate) | Separate GitHub environment |

Migrations run against staging first, then production. Never skip staging.

---

## Backup Policy

| Item | Frequency | Retention | Storage | Test |
|---|---|---|---|---|
| Supabase Cloud (V1) | Daily (managed by Supabase) | 7 days (free tier) | Supabase-managed | Monthly restore test to staging |
| Self-hosted Postgres (V2+) | Daily `pg_dump` via pg_cron | 30 days | Oracle Object Storage + off-site (Backblaze B2 encrypted) | Monthly restore drill documented |

**RPO (Recovery Point Objective):** 24 hours  
**RTO (Recovery Time Objective):** 4 hours  
These targets are acceptable for a pre-revenue pilot. Document for paying customers and revise when enterprise contracts require tighter SLAs.
