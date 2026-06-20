# Prerequisites

Everything needed before writing the first line of product code.

---

## Tier 1 — Install on your machine

| Tool | Purpose | How to get it |
|---|---|---|
| **Node.js 20 LTS** | JavaScript runtime | nodejs.org → download LTS installer |
| **pnpm** | Package manager | After Node: `npm install -g pnpm` |
| **Supabase CLI** | Local DB + auth for development | `pnpm add -g supabase` |
| **VS Code** | Recommended editor | code.visualstudio.com |

**Recommended VS Code extensions:** Tailwind CSS IntelliSense, Drizzle Kit, ESLint, Prettier, TypeScript (built-in).

---

## Tier 2 — Accounts to create

### Must have before writing a line of code

| Service | Purpose | Cost | Sign-up |
|---|---|---|---|
| **GitHub Pro** | Private repo + environment protection rules (10-min deploy gate) | $4/month | github.com → Settings → Billing → upgrade existing account |
| **Supabase Cloud** | Database, auth, storage, realtime | Free (500MB, 2 projects) | supabase.com → New project → choose EU region |
| **Cloudflare** | Frontend hosting (Pages) + CDN | Free | cloudflare.com → sign up → add your domain |
| **Mistral AI** | Translation, descriptions, allergen detection fallback | Pay per use (~$0 until real traffic) | console.mistral.ai → sign up → create API key → add a card |
| **Groq** | Allergen detection (free tier) | Free | console.groq.com → sign up → create API key |
| **Resend** | Transactional email (verify, reset password, onboarding) | Free (3,000 emails/day) | resend.com → sign up → create API key → verify a sender domain |

### Set up after first deploy

| Service | Purpose | Cost | Sign-up |
|---|---|---|---|
| **UptimeRobot** | Uptime alerts (50 monitors) | Free | uptimerobot.com |
| **Sentry** | Error monitoring | Free tier | sentry.io → create a Next.js project |

---

## Tier 3 — Domain name

Required before configuring Cloudflare and sending email from Resend.

| Option | Requirements | Where to register | Time |
|---|---|---|---|
| **.com** | None | Porkbun (~$9/year, cheapest), Namecheap, GoDaddy | Same day |
| **.sa** | Saudi Commercial Registration (CR) | SaudiNIC (nic.sa) | 1–3 business days after CR verification |
| **.store / .menu** | None | Porkbun | Same day |

**Recommendation:** Buy the `.com` now so you are not blocked. Register `.sa` when your CR is ready. Point both to Cloudflare.

---

## Tier 4 — API keys to collect

Store every key in two places: **GitHub Actions Secrets** and **Cloudflare Pages environment variables**.

| Key name | Where to find it |
|---|---|
| `SUPABASE_URL` | Supabase dashboard → Project Settings → API |
| `SUPABASE_ANON_KEY` | Same page |
| `SUPABASE_SERVICE_ROLE_KEY` | Same page — never expose in client code |
| `MISTRAL_API_KEY` | console.mistral.ai → API Keys |
| `GROQ_API_KEY` | console.groq.com → API Keys |
| `RESEND_API_KEY` | resend.com → API Keys |
| `CLOUDFLARE_API_TOKEN` | Cloudflare → My Profile → API Tokens → Create Token → "Edit Cloudflare Workers" template |

---

## Tier 5 — GitHub repository configuration (one-time)

Your repo (`Zalatah/site`) already exists. Apply these settings before starting development:

1. **Make the repo private** — Settings → General (your CI structure and key names will be visible otherwise)
2. **Branch protection on `main`** — Settings → Branches → Add rule → require status checks, block direct push, require linear history
3. **Add GitHub Actions Secrets** — Settings → Secrets and Variables → Actions → add all keys from Tier 4
4. **Production environment with 10-minute gate** — Settings → Environments → New environment → name it `production` → add a wait timer of 10 minutes

---

## Do not set up yet

These are in the plan but belong to later phases. Setting them up now adds noise with no benefit.

| Service | Phase | Reason to wait |
|---|---|---|
| Moyasar (payments) | V1.3 | No billing in pilot |
| Unifonic (WhatsApp API) | V1.2 | No bot in V1 |
| Apple Developer Program ($99/year) | V2 | Wallet passes only |
| Oracle Cloud KSA VM | V2 | Self-hosted Supabase triggered by PDPL hard requirement, not before |
| fal.ai (image AI) | V1.3 | No image generation in V1 |
| Mapbox | V4 | Delivery zones only |
| MyFatoorah | Post-V3 | GCC expansion only |
| Tamara / Tabby (BNPL) | V3 advanced | Large orders only (≥ SAR 300) |

---

## First 90 minutes once everything above is ready

```bash
pnpm create next-app@latest zalatah-saas --typescript --tailwind --app
cd zalatah-saas
pnpm add drizzle-orm @supabase/supabase-js @supabase/ssr zod
pnpm add -D drizzle-kit supabase
supabase init        # creates supabase/ directory
supabase start       # starts local Postgres + Auth + Storage
```

Push to GitHub → CI runs → Cloudflare Pages deploys a blank page. Everything after that is building features against a local Supabase instance that mirrors production.
