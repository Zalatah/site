# V1 Pilot Scope

This is the definitive contract for V1. Features not listed here are excluded. If a feature isn't here, it doesn't ship in V1, regardless of what other documents say.

## In Scope

### Organization Profile
- [ ] Name in Arabic and English
- [ ] Logo image upload
- [ ] Cover/hero image upload
- [ ] Phone number
- [ ] Address in Arabic and English
- [ ] Opening hours (per day of week)
- [ ] Social media links: Instagram, TikTok, Snapchat, WhatsApp, X
- [ ] VAT registration number (displayed on menu if present)
- [ ] CR (commercial registration) number (stored, not displayed)

### Menu Builder
- [ ] Create / edit / delete categories (name AR + EN, sort order, visibility toggle)
- [ ] Create / edit / delete items per category
- [ ] Item fields: name AR, name EN, description AR, description EN, price (SAR), image, availability toggle, sort order, badge (new / bestseller / limited / sold out)
- [ ] SFDA fields: calories (kcal), sodium (mg), caffeine (mg), allergens (array)
- [ ] Allergens are AI-suggested and must be confirmed by the owner before publishing (field `allergens_confirmed BOOLEAN`)
- [ ] Item images: upload from device; stored in Supabase Storage; served via Cloudflare CDN
- [ ] One active promotional banner per menu (text + optional image, AR + EN)

### AI Features (V1)
- [ ] Arabic → English translation for item name and description (Mistral Ministral 3B)
- [ ] Translation result shown in a review UI; owner edits if needed; explicitly saves
- [ ] Ingredient input → allergen suggestion (Groq Llama 3.1 8B free tier; Mistral fallback on rate limit)
- [ ] Allergen suggestions shown with "confirm" button; not applied until confirmed
- [ ] All AI calls logged to `ai_audit_events` (provider, model, prompt version, input hash, output, approval state)

### Import (V1 — CSV only)
- [ ] Upload CSV or Excel file
- [ ] Column mapping UI with AI-suggested field assignments (Mistral)
- [ ] Preview table before import
- [ ] Import stored in `import_jobs` with 24-hour rollback

### Public Menu
- [ ] Public page at `/{slug}` (no auth required)
- [ ] Mobile-first, RTL Arabic default with language toggle (AR / EN)
- [ ] Displays: banner, categories, items with SFDA fields, social links, opening hours with today's open/closed status
- [ ] QR code generation: downloads as PNG and SVG
- [ ] Page load < 2 seconds on a 4G connection (Lighthouse performance ≥ 80)

### Authentication & Accounts
- [ ] Email + password signup / login (Supabase Auth)
- [ ] Email verification required before menu is published
- [ ] One owner per restaurant in V1 (single `organization_memberships` row with role = 'owner')
- [ ] Password reset via email

### Compliance
- [ ] PDPL consent captured on signup (consent type: `pdpl_data_processing`)
- [ ] Privacy policy and terms of service pages (Arabic + English)
- [ ] SFDA fields visible on public menu

## Explicitly Excluded from V1

The following are documented here to prevent scope creep in AI-generated code:

- Billing, subscriptions, Moyasar integration
- Multi-user access, staff roles, manager invitations
- WhatsApp bot or webhook handling
- PDF, image, or URL-based import
- AI image generation, background removal, photo upscaling
- Apple Wallet, Google Wallet, loyalty programs
- Online ordering, cart, checkout
- Analytics dashboards beyond Umami page views
- Custom domains
- White-label / brand removal
- Embed widget
- Public API
- Multi-location / multi-branch
- Table-specific QR codes
- Advanced item modifiers (extras, options)
- Website scraping migration
- Automated campaigns

## Acceptance Tests

Each test must pass before V1 is considered shipped:

| # | Test | Pass Criterion |
|---|---|---|
| 1 | Signup → menu live | New account → create 3 categories, 5 items → publish → QR scan opens public menu | End to end in < 30 minutes |
| 2 | Arabic-only input | Enter name and description in Arabic only → click translate → EN fields populated → owner saves | Translation must not auto-save without confirmation |
| 3 | Allergen flow | Enter ingredient list → click detect → allergens listed → confirm → item saved | Allergens must not appear on public menu until `allergens_confirmed = true` |
| 4 | CSV import | Upload sample Foodics CSV → map columns → preview → import → items appear in menu | Rollback available for 24 hours |
| 5 | Public menu access | Unauthenticated user visits `/{slug}` | No 401; correct items displayed; SFDA fields shown |
| 6 | Tenant isolation | Org A user cannot read or write Org B data via any API route or Supabase client call | RLS test in CI must cover this explicitly |
| 7 | SFDA display | Item with allergens confirmed → public menu shows allergen badges | Items with `allergens_confirmed = false` show "allergen information pending" |
| 8 | Opening hours | Configure hours → public menu shows "Open now" or "Closed" based on current time in AST | Correct at boundary times |
| 9 | Performance | Lighthouse run on public menu page | Performance ≥ 80, Accessibility ≥ 90 |
| 10 | Audit trail | Any price or allergen change by owner | Row written to `audit_events` with before/after snapshot |

## V1 KPIs

Measured weekly across pilot restaurants:

| KPI | Target | Measurement |
|---|---|---|
| Median time from signup to live QR | ≤ 30 minutes | Founder observation during pilot onboarding |
| Founder support time | ≤ 2 hours/week total across all pilots | Time log |
| Weekly QR scans per restaurant | ≥ 50 | Umami analytics |
| SFDA field completeness | ≥ 80% of items have allergens confirmed | Database query |
| Item accuracy | Zero reported incorrect prices on live menu | Pilot restaurant feedback |

## Definition of Done (per feature)

A feature is done when:
1. Acceptance test passes in staging
2. RLS integration test covers the data it touches
3. No TypeScript errors (`tsc --noEmit` clean)
4. No new Semgrep findings
5. `audit_events` records all mutations
6. AI-generated content has a corresponding `ai_audit_events` row
