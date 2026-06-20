# Zalatah Menu → Restaurant SaaS: Full Product Roadmap (v2 — Saudi-Compliant)

---

## User's Intent (Restated)

> I want to transform my existing static restaurant menu website into a SaaS platform that restaurants can use to upload and manage their digital menus. I want to plan the full product landscape across four versions so I don't have to recode or re-architect between iterations. V2 will introduce a loyalty card system (stamp-based or points-based). V3 will add online ordering. V4 will add delivery management. For each version I need both the basic (must-have) and advanced (differentiating) feature lists. I also need a cost-efficiency analysis for deployment, keeping in mind this is a one-person company. The platform will be based in Saudi Arabia — it must comply with NCA cybersecurity requirements and PDPL, and must avoid services with known ties to Israel. Local/regional alternatives are preferred where available.

---

## Current State (What Exists)

The project is a single-restaurant static site with:
- Pure HTML/CSS/Vanilla JS — zero dependencies, zero backend
- Bilingual (Arabic/English) menu rendered from `menu_bilingual.json`
- 32 products across 7 categories, all with optimized WebP images
- Python build tools for image optimization and data compilation
- Existing link to `pass2u.net` for a loyalty card stub (not built)
- Deployed as a static site on GitHub (`Zalatah/site`)
- No auth, no database, no multi-tenancy, no admin interface

The client-side rendering logic and data schema (`category → products[]`) maps directly onto a multi-tenant SaaS data model and will be ported to the new stack.

---

## Saudi Regulatory Requirements

### PDPL — Personal Data Protection Law

Enforced since **September 14, 2024** by SDAIA. **This is the most immediate legal obligation for any Saudi SaaS startup.**

| Requirement | What It Means for This SaaS |
|---|---|
| Lawful basis for processing | Explicit consent or contractual necessity before collecting customer data (name, phone, email, order history, loyalty profile) |
| Cross-border transfers | Allowed to GCC or countries with adequate protection — must be documented on the National Data Governance Platform |
| Data breach notification | Notify SDAIA within 72 hours of a breach; notify affected individuals promptly |
| Data subject rights | Customers can request access, correction, or deletion of their data — must build admin tools to handle these requests |
| Marketing consent | Cannot send promotional SMS/email without opt-in |
| **Fines** | Up to SAR 5,000,000 (~USD 1.3M) per breach; doubled for repeat violations |

**Action required from Day 1**: Privacy policy (Arabic + English), consent flows in onboarding and customer registration, documented data processing agreements with all third-party vendors.

### NCA — National Cybersecurity Authority

The **ECC-1:2018** (Essential Cybersecurity Controls) was previously mandatory only for government/CNI organizations. As of 2025, **NCNICC-1:2025** extends baseline mandatory cybersecurity obligations to the broader private sector.

The **CCC-2:2024** (Cloud Cybersecurity Controls) governs cloud service usage. Key provisions:
- A SaaS startup may use a third-party IaaS provider hosted in KSA — no requirement to own a data center
- GCC hosting (e.g., AWS Bahrain) is acceptable for general private-sector SaaS under the 2024 Transfer Regulations with documented safeguards
- KSA in-country hosting is required only if serving **government, financial (SAMA-regulated), or CNI** clients

**Priority controls relevant to this SaaS**:

| Control Domain | Requirements |
|---|---|
| Identity & Access | MFA required for admin accounts; role-based access; privileged access logging |
| Data Encryption | TLS 1.2+ in transit; AES-256 at rest; encryption key management |
| Vulnerability Management | Regular security patching; periodic penetration testing |
| Logging & Monitoring | Centralized security logs retained ≥12 months; anomaly alerting |
| Third-Party Risk | Written security agreements with all vendors; periodic vendor risk assessments |
| Incident Response | Written IR plan; CSIRT contact; breach notification within 72 hours |
| Business Continuity | Daily automated backups; tested restore procedures |

**Certification roadmap**:
- **At launch**: PDPL-compliant privacy controls, ECC basic alignment
- **At ~SAR 400K ARR**: Pursue **ISO 27001** — unlocks enterprise/government restaurant chains as customers
- **For government contracts**: Full ECC + NCA audit may be required

### SFDA Digital Menu Mandate

From **July 1, 2025**, the Saudi Food and Drug Authority (SFDA) mandates that all digital menus display:
- Calorie count per serving
- Sodium content
- Caffeine content (beverages)
- Allergen declarations

This is not optional. Any platform serving Saudi restaurants must make SFDA compliance easy and automatic. This is also a **competitive differentiator** — smaller platforms may not have built this yet.

**Implementation**: Add `calories`, `sodium`, `caffeine`, `allergens[]` fields to the `menu_items` schema from V1. Display prominently on the public menu page.

---

## Vendor Risk Assessment (Israeli Connections)

The following assessment is based on public information available as of mid-2026.

| Vendor | Connection to Israel | KSA Availability | Decision |
|---|---|---|---|
| **Vercel** | CEO posted selfie with PM Netanyahu (Sep 2025); active developer boycott campaigns | Available | **REPLACE** — use Cloudflare Pages or self-host on regional infrastructure |
| **Supabase** | None found | Available | **SAFE TO USE** — clean record, strong developer community |
| **Google Cloud / Firebase** | Project Nimbus: $1.2B contract providing cloud + AI to Israeli military; cannot suspend due to boycott pressure | Available | **AVOID** — highest risk; replace with alternative BaaS |
| **AWS** | Project Nimbus co-contractor; same restrictions as Google | Available | **HIGH RISK** — preferred: deploy to Oracle Cloud KSA or Azure KSA instead. If AWS is used, use Bahrain/UAE region, not US/EU |
| **Stripe** | Israeli entity "Stripe Israel Payments Ltd." registered; CEO visited Israel Nov 2024 | **NOT AVAILABLE IN KSA** | **CANNOT USE** — use Moyasar (Saudi-native) |
| **Cloudflare** | R&D center confirmed in Israel; also has Dubai office | Available | **MODERATE RISK** — acceptable for CDN/DNS given no alternative with equivalent performance; monitor |
| **Resend** | None found (Vercel CEO is an angel investor — indirect only) | Available | **ACCEPTABLE** — use if self-hosting email is not preferred |
| **Sentry** | None found | Available | **SAFE** — replace with self-hosted GlitchTip for full data residency |
| **Umami** | None found (open source, MIT) | Self-hosted | **SAFE — RECOMMENDED** |
| **Twilio** | No R&D office in Israel found; CPO has Israeli academic background (indirect) | Available | **LOW RISK** — replace with Unifonic (Saudi CPaaS) for SMS |
| **Mapbox** | None found | Available | **SAFE — RECOMMENDED** over Google Maps |

---

## Revised Tech Stack (Saudi-Compliant, Cost-Optimized)

### Core Services

| Layer | Choice | Replaces | Why |
|---|---|---|---|
| Frontend | Next.js 15 + Tailwind CSS | — | SSR/SSG/ISR; framework-agnostic deployment |
| Hosting/Deployment | **Cloudflare Pages** + Workers | Vercel | No CEO controversy; global CDN; $0 egress; Workers = serverless functions; competitive alternative |
| Database/BaaS | **Supabase** (self-hosted on Oracle Cloud KSA) | Managed Supabase | Clean record; PostgreSQL RLS for multi-tenancy; Auth + Storage + Realtime included; self-hosted = KSA data residency |
| Cloud Infrastructure | **Oracle Cloud KSA** (Always Free tier → paid) | AWS/GCP/Vercel | KSA data centers live; no Project Nimbus association; Always Free tier (4 Arm CPUs, 24GB RAM, 200GB storage) is generous for early stage |
| Payment Gateway | **Moyasar** | Stripe | KSA-native; SAMA-licensed; Mada + Visa/MC + Apple Pay + STC Pay; best Mada rate (1.5% + 1 SAR); Arabic dashboard; active developer API |
| Email | **Resend** (or Amazon SES on Bahrain/KSA) | — | Resend is clean; SES if full KSA residency needed |
| SMS / OTP | **Unifonic** | Twilio | Saudi CPaaS; direct carrier connections; WhatsApp + SMS + voice; Arabic-first |
| Analytics | **Umami** (self-hosted on Oracle Cloud KSA) | — | Already in use; MIT license; deploy alongside app for zero data transfer outside KSA |
| Maps (V3/V4) | **Mapbox** | Google Maps | No Israeli ties; most customizable; 50K loads/month free |
| Error Monitoring | **GlitchTip** (self-hosted) | Sentry | Open source; Sentry-compatible SDKs (zero code change); 4 Docker containers; deploy on same KSA server |
| QR Codes | `qrcode` npm package (server-side) | — | No third-party dependency |
| Auth | Supabase Auth (self-hosted) | — | Email, magic link, OAuth (Google/Apple) |
| CDN | Cloudflare (existing) | — | Accept moderate risk given no practical alternative at this performance/price point |

### Oracle Cloud KSA — Always Free Tier Details

Oracle's Always Free tier includes resources that never expire:
- 4 Arm-based Ampere A1 CPUs + 24 GB RAM (ideal for self-hosted Supabase + GlitchTip + Umami)
- 200 GB block storage
- 2 x AMD VMs
- 10 GB object storage
- Outbound data: 10 TB/month free

This means **infrastructure cost at early stage is SAR 15–50/month** (domain + any overages). The self-hosted Supabase stack runs comfortably on the Always Free tier up to hundreds of tenants.

### Architecture Summary

```
Cloudflare Pages + Workers (frontend + API routes)
    │
    └── Self-hosted Supabase on Oracle Cloud KSA (Riyadh DC)
          ├── PostgreSQL (multi-tenant, RLS)
          ├── Auth (email + magic link + OAuth)
          ├── Storage (menu images → Cloudflare CDN)
          └── Realtime (WebSocket for live order updates)
          
Self-hosted on Oracle Cloud KSA (same VM or separate):
    ├── Umami (analytics)
    └── GlitchTip (error monitoring)

External:
    ├── Moyasar (payment processing)
    ├── Unifonic (SMS/OTP/WhatsApp)
    └── Resend (transactional email)
```

---

## Deployment Cost Analysis (Saudi-Compliant Stack)

### Early Stage (0–50 restaurants, pre-revenue)

| Service | Cost/Month |
|---|---|
| Oracle Cloud KSA (Always Free) | **SAR 0** |
| Cloudflare Pages (Free tier) | SAR 0 |
| Umami (self-hosted, same VM) | SAR 0 |
| GlitchTip (self-hosted, same VM) | SAR 0 |
| Resend (Free: 3,000 emails/day) | SAR 0 |
| Unifonic SMS (pay-per-use) | ~SAR 0.25–0.50 per OTP |
| Domain | ~SAR 50/year (~SAR 4/month) |
| Moyasar | 2.2% + 1 SAR per transaction |
| **Total fixed** | **~SAR 4/month** |

### Growth Stage (SAR 3,000–15,000 MRR, 50–300 restaurants)

| Service | Cost/Month |
|---|---|
| Oracle Cloud KSA (paid compute) | SAR 150–400 |
| Cloudflare Pro | SAR 75 ($20) |
| Resend Starter | SAR 75 ($20) |
| Unifonic SMS | SAR 100–300 |
| Backup storage (Oracle Object) | SAR 50–100 |
| **Total infra** | **SAR 450–875/month** |
| Moyasar fees at SAR 10K MRR | ~SAR 225 (2.2%) |
| **Total all-in** | **~SAR 675–1,100/month** |

At SAR 15,000 MRR, infra is ~4.5–7% of revenue — well within sustainable range for a solo operator.

### Comparison: Saudi-Compliant Stack vs Original Stack

| Category | Original Stack (v1) | Saudi-Compliant Stack (v2) |
|---|---|---|
| Hosting | Vercel ($20/mo) | Cloudflare Pages ($0–20/mo) |
| Database | Managed Supabase ($25/mo) | Self-hosted Supabase on Oracle KSA ($15–50/mo compute) |
| Payments | Stripe (unavailable) | Moyasar (2.2% + 1 SAR) |
| SMS | Twilio | Unifonic |
| Error Monitoring | Sentry | GlitchTip (self-hosted) |
| Data Location | US/EU servers | **KSA data center** |
| Israeli Risk | HIGH (Vercel, Google, AWS, Stripe) | **LOW** (Cloudflare: moderate; Supabase, Oracle, Moyasar: clean) |
| Monthly cost (early) | ~$1/mo | ~SAR 4/mo |

---

## Database Schema (Forward-Compatible for All 4 Versions)

```
organizations          — tenant root (restaurant account)
  ├── users            — staff/owners (auth.users FK)
  ├── menus            — one or more menus per org (lunch/dinner/etc.)
  │     └── categories
  │           └── menu_items
  │                 ├── item_modifiers     (extras/add-ons, V3)
  │                 ├── calories, sodium, caffeine   (SFDA mandate)
  │                 └── allergens[]        (SFDA mandate)
  ├── customers        — end customers (loyalty + orders link here)
  │     ├── loyalty_cards  (V2)
  │     └── stamp_events   (V2)
  ├── orders           (V3 — stubbed in V1)
  │     └── order_items
  ├── drivers          (V4 — stubbed in V1)
  ├── delivery_zones   (V4 — stubbed in V1)
  └── subscriptions    — Moyasar/billing metadata per org
```

Every table carries `organization_id UUID NOT NULL`. Supabase RLS policies enforce tenant isolation at the database layer.

---

## V1 — Digital Menu SaaS

**Goal**: Any restaurant can sign up, build their menu, and share a QR-code-linked digital menu with customers. SFDA-compliant from day one.

### Basic Features (MVP — ship these first)

| Feature | Description |
|---|---|
| Restaurant onboarding | Sign-up flow: name, logo, slug, contact info, CR number (for PDPL/KYC) |
| Menu builder | Add/edit/delete categories and items (name, description, price, image) |
| SFDA compliance fields | Calories, sodium, caffeine, allergens per item — displayed on public menu |
| Image upload | Upload photos → stored in Supabase Storage (KSA) → served via Cloudflare CDN |
| QR code generation | Unique QR per restaurant + per table linking to public menu URL |
| Public menu page | Customer-facing at `/[slug]` — bilingual (Arabic/English), RTL, no login required |
| Basic analytics | Page views, QR scans, most-viewed items (Umami, self-hosted) |
| Multi-user access | Owner invites staff with role-based access (owner / manager / staff) |
| Plan & billing | Moyasar subscription tiers |
| Admin dashboard | Manage menu, view analytics, download QR code |
| Privacy & consent | PDPL-compliant privacy policy display; cookie/data consent banner |

### Advanced Features (Differentiators — post-MVP)

| Feature | Description |
|---|---|
| Multiple menus | Separate menus per day-part with schedule-based switching |
| Table-specific QR codes | Each table gets its own QR; table-level analytics |
| Item availability toggle | 86 items instantly — hidden on public menu in real time |
| Custom branding | Cover photo, accent color, font choice |
| Custom domain | `menu.restaurant.com` via Cloudflare for SaaS (~$0.10/domain/month) |
| White-label | Remove platform branding (premium tier) |
| Allergen filtering | Customers filter by dietary requirement (vegan, gluten-free, halal-certified, etc.) |
| Item scheduling | Items auto-show/hide by time of day |
| Multi-location | One account, multiple branches — each with own menu + QR codes |
| Export | PDF menu + printable version |
| Embed widget | `<iframe>` snippet for restaurant's own website |
| Public read-only API | Future POS integration hook |
| SFDA audit export | Export nutrition data per SFDA submission format |

### V1 Pricing Model (SAR)

| Tier | SAR/Month | Limits |
|---|---|---|
| Free | 0 | 1 menu, 20 items, platform branding, basic analytics |
| Starter | 60 (~$16) | 3 menus, 100 items, no branding, QR download |
| Pro | 150 (~$40) | Unlimited menus/items, custom domain, 3 locations, advanced analytics |
| Business | 375 (~$100) | Everything + white-label, embed, API, priority support |

*Pricing aligns with the SAR 50–200/month QR-menu-only market norm, undercutting Foodics significantly for non-POS use cases.*

---

## V2 — Loyalty Card (Stamp & Points)

**Goal**: Restaurants run digital stamp cards and/or points programs through the same platform. Customers access their card via the menu — no separate app required.

### Basic Features

| Feature | Description |
|---|---|
| Digital stamp card | Define stamp goal (e.g., "10 stamps = 1 free item") |
| Points program | Earn X points per SAR spent; redeem for rewards |
| Customer wallet | Customer sees card/points balance from public menu (phone-number lookup — no app needed) |
| Manual stamp/points award | Staff award stamps via a tap-to-stamp interface |
| Reward catalogue | Define what stamps/points unlock (free item, discount, custom reward) |
| Reward redemption | Staff mark rewards as redeemed via dashboard |
| Customer registration | Phone or email — lightweight, no app download |
| PDPL consent | Explicit opt-in before enrolling in loyalty (WhatsApp/SMS marketing requires consent) |
| Notifications | Email (Resend) or WhatsApp/SMS (Unifonic) when reward is earned |

### Advanced Features

| Feature | Description |
|---|---|
| Tiered loyalty levels | Bronze / Silver / Gold — unlock earn multipliers and perks |
| Birthday rewards | Auto-trigger reward on customer birthday |
| Referral program | Customer gets stamps for referring new customers |
| Campaign builder | Time-limited bonus events ("double stamps this weekend") |
| Customer segmentation | Target inactive customers, top spenders, lapsed visitors |
| Gamification | Progress bars, badges, mini-challenges |
| Analytics dashboard | Visit frequency, CLV per customer, redemption rates, campaign ROI |
| Physical-to-digital bridge | Scan table QR to open wallet (same URL as menu) |
| Loyalty widget on menu | Customer sees stamp card inline while browsing |
| Multi-location loyalty | Stamps/points earned at any branch of the same restaurant |
| WhatsApp CRM | Send loyalty updates via Unifonic WhatsApp (preferred channel in Saudi) |
| CSV export | Customer list export for CRM (with PDPL consent records) |

### V2 Pricing Addition (SAR)

- Starter: Loyalty locked (upsell hook visible but blurred)
- Pro: Stamp cards only, up to 500 customers
- Business: Full loyalty suite, unlimited customers, campaigns, segmentation, WhatsApp notifications

---

## V3 — Online Ordering

**Goal**: Customers place orders directly through the menu page. Restaurants receive and manage orders in a dashboard. Zero commission to third-party aggregators.

### Basic Features

| Feature | Description |
|---|---|
| Add to cart | Add items + modifiers/extras to cart while browsing menu |
| Order type selection | Dine-in (table number), pickup, or delivery (if enabled) |
| Checkout flow | Customer info, order review, payment |
| Payment | Moyasar Payment Intents — Mada, Visa/MC, Apple Pay, STC Pay |
| Order confirmation | WhatsApp/SMS (Unifonic) to customer; dashboard notification to restaurant |
| Order management dashboard | Incoming orders: accept/reject, set prep time |
| Order status updates | Customer sees: received → preparing → ready |
| Order history | Customer views past orders (via loyalty wallet session) |
| Basic order analytics | Orders/day, revenue, popular items, peak times |
| Modifier/extras | Upsell add-ons per item (already in schema) |
| VAT display | Saudi VAT (15%) applied at checkout per ZATCA requirements |

### Advanced Features

| Feature | Description |
|---|---|
| Kitchen Display System (KDS) | Web-based KDS — color-coded tickets, multi-station routing |
| Scheduled orders | Customer orders for pickup at a specific time |
| Order throttling | Limit simultaneous orders to prevent kitchen overload |
| Reorder | One-tap reorder from order history |
| Loyalty auto-award | Points/stamps awarded automatically on order completion |
| Discount & promo engine | Coupon codes, combo deals, spend-threshold discounts |
| Table QR ordering | Customer scans table QR → order tagged to table |
| Staff order portal | Staff places orders on behalf of customers |
| Third-party aggregator sync | Receive orders from Jahez, HungerStation, Talabat in same dashboard |
| ZATCA e-invoicing | Phase 2 compliant e-invoices (required for VAT-registered restaurants) |
| Revenue analytics | Channel breakdown, item margins, order frequency, cohort retention |

### ZATCA E-Invoicing Note

Saudi Arabia's Zakat, Tax and Customs Authority mandates **Phase 2 e-invoicing** (Fatoora integration) for VAT-registered businesses. As customers (restaurants) grow, they'll need compliant e-invoices. Either integrate directly or partner with a ZATCA-approved solution. Foodics handles this — it is a key Foodics loyalty feature. Building this creates significant retention.

### V3 Pricing Addition (SAR)

| Model | SAR/Month |
|---|---|
| Ordering module add-on | +100–200 SAR on existing plan (zero commission model) |
| OR commission hybrid | Lower monthly + 0.5–1% per order |
| Payment processing | Pass-through Moyasar fees (2.2% card + 1 SAR) to restaurant |

---

## V4 — Delivery Management

**Goal**: Restaurants manage their own drivers, dispatch orders, and give customers live tracking — within the platform.

### Basic Features

| Feature | Description |
|---|---|
| Delivery zone setup | Draw zones on Mapbox map; set fee per zone |
| Driver accounts | Invite drivers as `driver` role users |
| Manual dispatch | Assign delivery orders to available drivers |
| Driver mobile view | Mobile-optimized screen for assigned orders (PWA) |
| Customer tracking page | Customer gets a real-time tracking link |
| Delivery status notifications | WhatsApp/SMS at milestones (picked up / on the way / delivered) via Unifonic |
| Delivery fee calculation | Auto-calculate by distance or zone |
| Basic delivery analytics | Avg. delivery time, on-time rate, driver performance |

### Advanced Features

| Feature | Description |
|---|---|
| Auto-dispatch | Assign to nearest available driver automatically |
| Route optimization | Multi-drop routing for drivers with multiple orders |
| Driver PWA | Progressive Web App: navigation, status updates, in-app messaging |
| Geofencing triggers | Status auto-updates when driver enters/exits zones |
| Driver incentives | Leaderboard, performance bonuses, gamification |
| Third-party fleet fallback | Integrate Aramex API (KSA-native) as overflow delivery network |
| Dynamic delivery pricing | Surge pricing by demand/distance/time |
| Proof of delivery | Driver captures photo or signature |
| Live map dashboard | Restaurant sees all drivers on a Mapbox live map |
| Delivery analytics | Cost per delivery, zone profitability, driver utilization |

### V4 Pricing Addition (SAR)

- Delivery module: +115–225 SAR/month on existing plan
- Driver seats: Free up to 5 drivers, SAR 20/driver/month after

---

## Saudi Market & Competitive Landscape

### Market Size

- Saudi restaurant management software: **SAR 556M (2024)**, growing rapidly
- 70%+ of Saudi/Gulf restaurants have adopted QR menus (2024)
- **81% of Saudi customers prefer digital menus** (YouGov 2024)
- QSR market projected **SAR 62B by 2033** (from SAR 35B in 2024)

### Competitor Analysis

| Competitor | Category | SAR/Month | What They Don't Have |
|---|---|---|---|
| **Foodics** (فودكس) | Full POS/RMS | 1,500–11,000+ | Lightweight/affordable tier; standalone consumer loyalty app; deep QR dine-in focus |
| **Qlub** | QR pay-at-table layer | Not public | Full menu management; loyalty system; ordering; delivery |
| **TableQR** | QR menu only | ~50–200 | Loyalty; ordering; delivery; admin dashboard |
| **Ordable** | QR ordering (table + takeaway) | ~50–200 | Loyalty; delivery; multi-location management |
| **POSRocket** (acquired by Foodics) | POS | Being sunsetted | — |
| **Marn** (مرن) | POS | Reportedly inactive | — |

### Our Positioning

| Dimension | Our Advantage |
|---|---|
| Arabic-first | RTL, Arabic-default, localized UX vs Western tools with bolted-on Arabic |
| SFDA-compliant | Nutrition labeling built in from Day 1; competitors may lag |
| PDPL-compliant | Privacy-by-design; builds trust with Saudi restaurant owners |
| All-in-one | Menu + Loyalty + Ordering + Delivery in one platform |
| Affordable | SAR 60–375/month vs Foodics SAR 1,500+ |
| No POS hardware | Software-only (Foodics sells hardware; we don't — lower barrier to entry) |
| Clean vendor stack | No Google, no AWS Project Nimbus, no Stripe — matters to Saudi-conscious buyers |
| WhatsApp-native | Unifonic WhatsApp for notifications vs email-only competitors |

**Primary target**: Small-to-medium Saudi restaurants (1–3 branches) that want digital presence beyond a QR menu but aren't ready for the complexity/cost of Foodics.

---

## Implementation Phases (Technical Execution Order)

### Phase 0 — Foundation (Before V1 Launch)

1. Initialize Next.js 15 project (TypeScript + Tailwind CSS)
2. Provision Oracle Cloud KSA instance; install self-hosted Supabase via Docker Compose
3. Design full forward-compatible database schema (V2–V4 stub tables, SFDA fields)
4. Configure Cloudflare Pages for deployment; wildcard subdomain for `[slug].yourdomain.com`
5. Set up Moyasar account; implement subscription billing
6. Integrate Unifonic for OTP verification (Saudi phone numbers)
7. Deploy Umami + GlitchTip on Oracle KSA VM
8. Migrate Zalatah static site as the first tenant under the new system
9. Implement multi-tenant routing: `/[slug]/menu`, `/[slug]/admin`, `/[slug]/order`
10. Write PDPL-compliant privacy policy + data processing agreements with all vendors

### Phase 1 — V1 (Menu SaaS)

11. Restaurant onboarding + Moyasar subscription checkout
12. Admin dashboard: menu builder with SFDA fields (calories, allergens, sodium, caffeine)
13. Public menu page at `/[slug]` — port existing HTML/CSS/JS to React components
14. QR code generation + download (PNG + SVG)
15. Analytics: Umami event tagging (QR scans, item views, category interactions)
16. Onboarding email sequence via Resend

### Phase 2 — V2 (Loyalty)

17. Activate loyalty_cards + stamp_events tables
18. Customer registration with PDPL consent capture
19. Staff stamp/award interface (mobile-friendly)
20. Customer wallet embedded in menu page
21. Campaign builder + WhatsApp/SMS notification via Unifonic

### Phase 3 — V3 (Ordering)

22. Cart + checkout flow with Moyasar Payment Intents
23. Real-time order notifications (Supabase Realtime + Unifonic WhatsApp)
24. Order management dashboard + KDS web app
25. Loyalty auto-award on order completion
26. ZATCA e-invoice generation (or partner integration)

### Phase 4 — V4 (Delivery)

27. Delivery zone map UI (Mapbox)
28. Driver PWA (Progressive Web App)
29. Dispatch dashboard + Supabase Realtime for live driver tracking
30. Aramex API integration for third-party courier overflow

---

## Key Architectural Principles

1. **KSA data residency by default** — all customer PII stays on Oracle Cloud KSA; no cross-border transfer without documented justification
2. **RLS is the security layer** — Supabase PostgreSQL RLS enforces tenant isolation at the database layer; application code is a secondary guard
3. **PDPL consent is captured explicitly** — consent recorded with timestamp and scope; deletable on request
4. **SFDA fields are mandatory from schema Day 1** — never retrofit compliance into a live schema
5. **Stub before you need it** — V2–V4 tables exist as stubs in V1 migrations to avoid destructive future migrations
6. **Feature flags per plan** — gate features via a `plan_features` lookup table; allows plan upgrades to take effect without a deployment
7. **WhatsApp over email** — Unifonic WhatsApp is the primary notification channel; email is secondary
8. **Moyasar is the only payment processor** — never introduce Stripe (unavailable in KSA) even for international customers
9. **Cloudflare is CDN/DNS only** — sensitive data never transits Cloudflare; it serves only static assets and routes traffic

---

## Compliance Action Checklist

### Before Launch
- [ ] Draft and publish Arabic + English Privacy Policy (PDPL-compliant)
- [ ] Implement explicit consent capture on customer registration
- [ ] Sign Data Processing Agreements (DPA) with Resend, Unifonic, Cloudflare
- [ ] Document all cross-border data flows and register on National Data Governance Platform
- [ ] Enable TLS 1.2+ on all endpoints (Cloudflare handles this)
- [ ] Implement AES-256 encryption at rest (Oracle KSA block storage + Supabase)
- [ ] Set up centralized security logging (GlitchTip + Supabase audit logs) retained ≥12 months
- [ ] Configure MFA requirement for all admin accounts
- [ ] Write Incident Response Plan (IR plan) with 72-hour breach notification procedure

### At SAR 400K ARR (~100–150 restaurants)
- [ ] Begin ISO 27001 certification process (unlocks enterprise/government restaurant chain clients)
- [ ] Conduct first annual penetration test
- [ ] Implement formal vendor risk assessment process

---

## Verification Checklist (Per Version)

- [ ] New tenant can sign up, build a SFDA-compliant menu, and share a working QR-code URL end-to-end
- [ ] RLS test: authenticated as tenant A, attempt to read tenant B's data — expect 0 rows returned
- [ ] Moyasar checkout: subscription upgrade reflected in feature access within 60 seconds of webhook
- [ ] Public menu page loads in <2s on 3G (Lighthouse score >90)
- [ ] Image upload: file → resized WebP → Cloudflare CDN URL → displayed on menu within 10 seconds
- [ ] SFDA fields: calories/allergens visible on public menu; export matches SFDA format
- [ ] PDPL: customer deletion request removes all PII within 30 minutes
- [ ] V2: stamp awarded → customer wallet updates in real time (Supabase Realtime)
- [ ] V3: order placed → restaurant dashboard notification → KDS ticket within 3 seconds
- [ ] V3: Moyasar payment captured → loyalty points awarded → order status updated
- [ ] V4: driver location update → customer tracking page reflects within 5 seconds
