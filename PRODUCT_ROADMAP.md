# Zalatah Menu → Restaurant SaaS: Full Product Roadmap

---

## User's Intent (Restated)

> I want to transform my existing static restaurant menu website into a SaaS platform that restaurants can use to upload and manage their digital menus. I want to plan the full product landscape across four versions so I don't have to recode or re-architect between iterations. V2 will introduce a loyalty card system (stamp-based or points-based). V3 will add online ordering. V4 will add delivery management. For each version I need both the basic (must-have) and advanced (differentiating) feature lists. I also need a cost-efficiency analysis for deployment, keeping in mind this is a one-person company.

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

This is an ideal starting point: the client-side rendering logic and data schema (`category → products[]`) maps directly onto a multi-tenant SaaS data model.

---

## Architecture Decision: Build for All 4 Versions from Day One

The database schema, auth layer, and API surface must be designed in V1 to accommodate V2–V4 without destructive migrations. This means:

- **Tenant isolation** via `organization_id` on every table from V1
- **User roles** seeded in V1: `owner`, `manager`, `staff`, `customer`
- **Orders table** created as a stub in V1 (even if unused until V3)
- **Loyalty profile** FK relationship stubbed in V1 customer table
- **Delivery zones table** stubbed in V1 (populated in V4)

---

## Recommended Tech Stack (One-Man Company, Cost-Optimized)

### Core Services

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 15 (App Router) + Tailwind CSS | SSR/SSG/ISR in one, edge-ready, Vercel native |
| Backend/API | Next.js API Routes + Supabase Edge Functions | Serverless, no separate server to manage |
| Database | Supabase (PostgreSQL) | RLS for multi-tenancy, auth included, storage included |
| Auth | Supabase Auth | Email, OAuth, magic link — zero config |
| File Storage | Supabase Storage (menu images) + Cloudflare R2 (high-frequency assets) | R2 has $0 egress fees — critical for menu images served to end customers |
| Payments | Stripe (subscriptions) + Stripe Connect (future marketplace) | Wire in Connect from V1 even if unused until needed |
| Email | Resend | Developer-friendly, generous free tier (3K emails/day) |
| Analytics | Keep Umami (self-hosted) | Already in place |
| Monitoring | Sentry free tier | Error tracking with zero cost early on |
| Deployment | Vercel (frontend/API) | Native Next.js, global CDN, zero DevOps |
| QR Codes | `qrcode` npm package (server-side generation) | No third-party dependency |

### Multi-Tenancy Pattern

Every database table carries `organization_id UUID NOT NULL`. Supabase Row Level Security (RLS) policies enforce isolation at the database layer:

```sql
-- Applied on every tenant-scoped table
CREATE POLICY "org_isolation" ON menu_items
  FOR ALL USING (organization_id = auth.jwt() -> 'org_id');
```

Restaurants are `organizations`. Each organization has a `slug` used as a subdomain or path prefix (e.g., `zalatah.yoursaas.com` or `yoursaas.com/zalatah`).

### Custom Domain Strategy

- **Phase 1**: Path-based routing (`yoursaas.com/[slug]`) — zero infrastructure cost
- **Phase 2**: Subdomain routing (`[slug].yoursaas.com`) — Vercel wildcard domain, $0 extra
- **Phase 3** (advanced): True custom domains (`menu.zalatah.com`) — Vercel domain API or Cloudflare for SaaS (~$0.10/domain/month)

---

## Deployment Cost Analysis

### Early Stage (0–50 restaurants, pre-revenue)

| Service | Cost/Month |
|---|---|
| Vercel Hobby | $0 |
| Supabase Free | $0 |
| Cloudflare R2 | $0 (10GB free) |
| Resend | $0 (3K/day free) |
| Stripe | 2.9% + $0.30 per transaction |
| Domain | ~$1/month ($12/year) |
| **Total** | **~$1/month** |

### Growth Stage ($1K–$5K MRR, 50–300 restaurants)

| Service | Cost/Month |
|---|---|
| Vercel Pro | $20 |
| Supabase Pro | $25 (100K MAU, 8GB DB, 100GB storage) |
| Cloudflare R2 | ~$5–15 (1TB included) |
| Resend | $20 |
| Sentry | $0–26 |
| **Total infra** | **~$70–90/month** |
| Stripe fees at $3K MRR | ~$90 |
| **Total all-in** | **~$160–180/month** |

### Scale Stage ($10K+ MRR, 300+ restaurants)

| Service | Cost/Month |
|---|---|
| Vercel Pro | $20 |
| Supabase Pro + Compute upgrade | $75–125 |
| Cloudflare R2 | $15–40 |
| Resend Growth | $50–90 |
| Monitoring | $30–50 |
| **Total infra** | **~$190–300/month** |

**Key insight**: At $10K MRR, infra is ~2–3% of revenue. The stack scales without re-architecture up to thousands of tenants.

### Why NOT Firebase / AWS

- **Firebase**: 4–5× more expensive than Supabase at scale; NoSQL is a poor fit for relational restaurant data (orders → items → modifiers → loyalty → customers)
- **AWS Amplify**: ~$3,180/month at 100K MAU vs ~$630 on Supabase. Massive operational overhead for a solo founder
- **Railway/Render/Fly.io**: Good for containers but add operational complexity. Avoid until you need something Supabase Edge Functions can't handle

---

## Database Schema (Forward-Compatible for All 4 Versions)

```
organizations          — tenant root (restaurant account)
  ├── users            — staff/owners (auth.users FK)
  ├── menus            — one or more menus per org (lunch/dinner/etc.)
  │     └── categories
  │           └── menu_items
  │                 └── item_modifiers     (extras/add-ons, V3)
  ├── customers        — end customers (loyalty + orders link here)
  │     ├── loyalty_cards  (V2)
  │     └── stamp_events   (V2)
  ├── orders           (V3 — stubbed in V1)
  │     └── order_items
  ├── drivers          (V4 — stubbed in V1)
  ├── delivery_zones   (V4 — stubbed in V1)
  └── subscriptions    — Stripe billing per org
```

---

## V1 — Digital Menu SaaS

**Goal**: Any restaurant can sign up, build their menu, and share a QR-code-linked digital menu with customers.

### Basic Features (MVP — ship these first)

| Feature | Description |
|---|---|
| Restaurant onboarding | Sign-up flow: name, logo, slug, contact info |
| Menu builder | Add/edit/delete categories and items (name, description, price, image, calories) |
| Image upload | Upload product photos → stored in Supabase Storage/R2, auto-resized server-side |
| QR code generation | Unique QR per restaurant (and optionally per table) linking to public menu URL |
| Public menu page | Customer-facing page at `/[slug]` — responsive, fast, no login required |
| Bilingual support | Arabic + English content fields per item (carry over existing schema) |
| Basic analytics | Page views, QR scans, most-viewed items (via Umami events) |
| Multi-user access | Owner can invite staff with role-based access |
| Plan & billing | Stripe subscription: Free tier + paid plans |
| Admin dashboard | Restaurant owner dashboard: manage menu, view analytics, download QR code |

### Advanced Features (Differentiators — ship after MVP)

| Feature | Description |
|---|---|
| Multiple menus | Separate menus per day-part (breakfast, lunch, dinner) with schedule-based switching |
| Table-specific QR codes | Each table gets a unique QR; analytics track table-level engagement |
| Item availability toggle | Mark items 86'd (out of stock) — hidden on public menu instantly |
| Custom branding | Upload cover photo, customize accent color, font choice |
| Custom domain | Point `menu.restaurant.com` to the public menu (Vercel domain API) |
| White-label | Remove "Powered by" branding (premium tier) |
| Allergen & dietary tags | Tag items as vegan, gluten-free, spicy, etc. — customer-side filtering |
| Item scheduling | Items auto-show/hide based on time of day |
| Nutritional info | Calorie count, macro display per item |
| Export | PDF menu export, printable version |
| Multi-location | One account, multiple branches — each with own menu + QR codes |
| Embed widget | `<iframe>` snippet restaurants can embed on their own website |
| Public API | Read-only API for menu data (future POS integrations) |

### V1 Pricing Model

| Tier | Price | Limits |
|---|---|---|
| Free | $0 | 1 menu, 20 items, platform branding, basic analytics |
| Starter | $15/month | 3 menus, 100 items, no branding, QR customization |
| Pro | $39/month | Unlimited menus/items, custom domain, multi-location (3), advanced analytics |
| Business | $99/month | Everything + white-label, embed widget, public API, priority support |

---

## V2 — Loyalty Card (Stamp & Points)

**Goal**: Restaurants can run digital stamp cards and/or points programs. Customers access their card via the menu page — no separate app required.

### Basic Features

| Feature | Description |
|---|---|
| Digital stamp card | Define stamp goal (e.g., "10 stamps = 1 free item") |
| Points program | Earn X points per SAR spent; redeem for rewards |
| Customer wallet | Customer sees card/points balance from the public menu page (phone-number lookup) |
| Manual stamp/points award | Staff award stamps via a simple interface (tap to stamp) |
| Reward catalogue | Define what stamps/points unlock (free item, discount, custom reward) |
| Reward redemption | Staff validate and mark rewards as redeemed |
| Customer registration | Lightweight sign-up (phone or email) — no app download required |
| Basic notifications | Notify customers when they earn a reward (email or SMS) |

### Advanced Features

| Feature | Description |
|---|---|
| Tiered loyalty levels | Bronze / Silver / Gold — unlock multipliers and perks |
| Birthday rewards | Auto-trigger reward on customer birthday |
| Referral program | Customer gets stamps for referring new customers |
| Campaign builder | Time-limited bonus events ("double stamps this weekend") |
| Customer segmentation | Target inactive customers, top spenders, etc. |
| Gamification | Progress bars, badges, mini-challenges |
| Analytics dashboard | Visit frequency, CLV per customer, redemption rates, campaign ROI |
| Physical-to-digital bridge | Scan a printed QR at table to access card (same URL as menu) |
| Loyalty widget on menu | Customer sees their stamp card inline while browsing menu |
| Multi-location loyalty | Stamps/points earned at any branch of the same restaurant |
| CSV export | Export customer list for external CRM use |

### V2 Pricing Addition

- Starter: Loyalty locked (upsell hook)
- Pro: Stamp cards only, up to 500 customers
- Business: Full loyalty suite, unlimited customers, campaigns, segmentation

---

## V3 — Online Ordering

**Goal**: Customers can place orders directly through the menu page. Restaurants receive and manage orders in a dashboard. Zero commission to third parties.

### Basic Features

| Feature | Description |
|---|---|
| Add to cart | Customer adds items + modifiers/extras to cart while browsing menu |
| Order type selection | Dine-in (table number), pickup, or delivery (if enabled) |
| Checkout flow | Customer info, order review, payment |
| Payment processing | Stripe Payment Intents — card, Apple Pay, Google Pay |
| Order confirmation | SMS/email to customer; notification to restaurant dashboard |
| Restaurant order dashboard | Incoming orders with accept/reject, prep time setting |
| Order status updates | Customer sees status: received → preparing → ready |
| Order history | Customer can view past orders |
| Basic order analytics | Orders/day, popular items, peak times, revenue |
| Modifier/extras support | Upsell add-ons per item (already in JSON schema) |

### Advanced Features

| Feature | Description |
|---|---|
| Kitchen Display System (KDS) | Web-based KDS — color-coded tickets by urgency, multi-station routing |
| Scheduled orders | Customer places order for pickup at specific time |
| Order throttling | Limit simultaneous orders to prevent kitchen overload |
| Reorder | One-tap reorder from order history |
| Loyalty integration | Auto-award points/stamps on order completion |
| Discount & promo engine | Coupon codes, combo deals, spend-threshold discounts |
| Table QR ordering | Customer scans table QR, order auto-tagged by table number |
| Split bill | Multiple customers at same table order independently |
| Staff ordering portal | Staff can place orders on behalf of customers |
| Third-party aggregator sync | Receive orders from Jahez, HungerStation, Talabat in same dashboard |
| POS webhook | Push completed orders to external POS via webhook |
| Revenue analytics | Channel breakdown, item margins, order frequency, cohort retention |

### V3 Pricing Addition

| Model | Description |
|---|---|
| Flat subscription | +$25–50/month on existing plan — zero commission (competitive differentiator vs. Jahez 25–30%) |
| OR commission hybrid | Lower monthly fee + 0.5–1% per order (lowers barrier to entry) |
| Payment processing | Pass-through Stripe fees (2.9% + $0.30) to the restaurant |

---

## V4 — Delivery Management

**Goal**: Restaurants that offer delivery can manage their own drivers, dispatch orders, and give customers live tracking — all within the platform.

### Basic Features

| Feature | Description |
|---|---|
| Delivery zone setup | Draw delivery radius/zones on a map; set fee per zone |
| Driver accounts | Invite delivery drivers as users with `driver` role |
| Order dispatch | Assign delivery orders to available drivers (manual) |
| Driver mobile view | Drivers see their assigned orders on a mobile-optimized screen |
| Customer tracking page | Customer gets a link to track their order/driver in real time |
| Delivery status updates | Automatic SMS/email at key milestones (picked up, on the way, delivered) |
| Delivery fee calculation | Auto-calculate fee based on distance or zone |
| Basic delivery analytics | Average delivery time, on-time rate, driver performance |

### Advanced Features

| Feature | Description |
|---|---|
| Auto-dispatch | Automatically assign order to nearest available driver |
| Route optimization | Multi-drop routing for drivers with multiple orders |
| Driver app (PWA) | Progressive Web App for drivers: navigation, status updates, in-app comms |
| Geofencing triggers | Auto-update status when driver enters/exits restaurant or delivery zone |
| Driver incentives | Performance bonuses, leaderboard gamification |
| Third-party fleet fallback | Integrate Aramex/Stuart courier API when in-house drivers unavailable |
| Dynamic delivery pricing | Surge pricing based on demand, time, or distance |
| Proof of delivery | Driver captures photo or customer signature on delivery |
| Live map dashboard | Restaurant sees all drivers on a live map |
| Hybrid dispatch | Mix in-house drivers with third-party couriers in one view |
| Delivery analytics | Cost per delivery, zone profitability, driver utilization rates |

### V4 Pricing Addition

- Delivery module: +$30–60/month on existing plan
- Driver seats: Free up to 5 drivers, $5/driver/month after

---

## Implementation Phases (Technical Execution Order)

### Phase 0 — Foundation (Before V1 Launch)

1. Initialize Next.js 15 project (TypeScript + Tailwind CSS)
2. Set up Supabase: Auth, RLS policies, Storage buckets
3. Design full forward-compatible database schema (including V2–V4 stub tables)
4. Set up Stripe with subscription products; wire Stripe Connect for future use
5. Implement multi-tenant routing: `/[slug]/menu`, `/[slug]/admin`, `/[slug]/order`
6. Migrate existing Zalatah static site as the first tenant
7. Set up Cloudflare R2 for image storage + Next.js image optimization pipeline
8. Deploy to Vercel with wildcard subdomain

### Phase 1 — V1 (Menu SaaS)

9. Restaurant onboarding + Stripe subscription checkout
10. Admin dashboard: menu builder (CRUD categories/items/images)
11. Public menu page at `/[slug]` (port existing HTML/CSS/JS to React)
12. QR code generation + download
13. Analytics via Umami event tagging
14. Onboarding email sequence via Resend

### Phase 2 — V2 (Loyalty)

15. Activate loyalty schema (loyalty_cards, stamp_events tables)
16. Customer registration (phone/email, no app)
17. Staff stamp/award interface
18. Customer wallet embedded in menu page
19. Campaign builder + notification system

### Phase 3 — V3 (Ordering)

20. Cart and checkout flow
21. Stripe Payment Intents integration
22. Order management dashboard + real-time notifications
23. KDS web app
24. Loyalty auto-award on order completion

### Phase 4 — V4 (Delivery)

25. Delivery zone map UI
26. Driver account system
27. Dispatch dashboard + driver PWA
28. Real-time tracking (Supabase Realtime)
29. Third-party courier API integration

---

## Key Architectural Principles

1. **Never hardcode tenant data** — every query scoped by `organization_id`
2. **RLS is the security layer** — application logic is a backup, not the primary guard
3. **Stub before you need it** — create tables and FKs for V2–V4 in V1 migrations
4. **Feature flags per plan** — gate features via a `plan_features` lookup table, not code conditionals
5. **Public menu is read-only and anonymous** — Supabase anon key + RLS for safe public reads
6. **Stripe is source of truth for billing** — never derive plan from your DB; check `stripe_subscription_status`
7. **Images are always CDN-served** — never serve from Next.js directly; Cloudflare R2 + Supabase CDN

---

## Competitive Positioning

| Competitor | Price | Gap We Exploit |
|---|---|---|
| Menubly | $9.99/mo | No loyalty, no ordering, English-first |
| UpMenu | $49–299/mo | Too expensive for SMB restaurants in MENA |
| Loyalzoo | $35–60/mo | Loyalty only, no menu |
| ChowNow | $149/mo + setup | US-only, no Arabic, no loyalty |
| **This SaaS** | $15–99/mo | Arabic-first, all-in-one, MENA market focus |

The Arabic-first, MENA-focused, all-in-one positioning (menu + loyalty + ordering + delivery) at SMB pricing is the white space.

---

## Verification Checklist (Per Version)

- [ ] New tenant can sign up, build a menu, and share a working QR-code URL end-to-end
- [ ] RLS test: authenticated as tenant A, attempt to read tenant B's data — expect 0 rows
- [ ] Stripe webhook: subscription upgrade/downgrade reflects in feature access within 60 seconds
- [ ] Public menu page loads in <2s on 3G (Lighthouse performance score >90)
- [ ] Image upload: file → resized WebP → CDN URL → rendered on menu within 10 seconds
- [ ] V2: stamp awarded → customer wallet updates in real time (Supabase Realtime)
- [ ] V3: order placed → restaurant dashboard notification → KDS ticket appears within 3 seconds
- [ ] V4: driver location update → customer tracking page reflects within 5 seconds
