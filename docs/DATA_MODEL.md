# Data Model

## Rules

- All prices and monetary values stored as **integers in halalas** (1 SAR = 100 halalas). Never store SAR as a float.
- Every tenant-scoped table carries `organization_id UUID NOT NULL` with a foreign key and an RLS policy.
- Audit-sensitive mutations (price changes, allergen changes, publish/unpublish) write a row to `audit_events`.
- AI-generated content writes a row to `ai_audit_events` before being applied.
- Do not create V2–V4 tables in V1 migrations. They are documented below for reference only.

---

## V1 Schema

```sql
-- ============================================================
-- ORGANIZATIONS
-- ============================================================
CREATE TABLE organizations (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug         TEXT UNIQUE NOT NULL CHECK (slug ~ '^[a-z0-9-]{3,50}$'),
  name_ar      TEXT NOT NULL,
  name_en      TEXT,
  logo_url     TEXT,
  cover_url    TEXT,
  phone        TEXT,
  address_ar   TEXT,
  address_en   TEXT,
  vat_number   TEXT,
  cr_number    TEXT,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- MEMBERSHIPS (V1: one row per org, role = 'owner')
-- ============================================================
CREATE TABLE organization_memberships (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role            TEXT NOT NULL CHECK (role IN ('owner', 'manager', 'staff')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (organization_id, user_id)
);

-- ============================================================
-- OPENING HOURS
-- ============================================================
CREATE TABLE opening_hours (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  day_of_week     INT  NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0 = Sunday
  open_time       TIME,
  close_time      TIME,
  is_closed       BOOLEAN NOT NULL DEFAULT false,
  UNIQUE (organization_id, day_of_week)
);

-- ============================================================
-- SOCIAL LINKS
-- ============================================================
CREATE TABLE social_links (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE UNIQUE,
  instagram       TEXT,
  tiktok          TEXT,
  snapchat        TEXT,
  whatsapp        TEXT,
  x               TEXT,
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- MENUS
-- ============================================================
CREATE TABLE menus (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name_ar         TEXT NOT NULL,
  name_en         TEXT,
  is_published    BOOLEAN NOT NULL DEFAULT false,
  published_at    TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- BANNERS (one active banner per menu)
-- ============================================================
CREATE TABLE banners (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  menu_id         UUID NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
  content_ar      TEXT,
  content_en      TEXT,
  image_url       TEXT,
  is_active       BOOLEAN NOT NULL DEFAULT false,
  scheduled_start TIMESTAMPTZ,
  scheduled_end   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- CATEGORIES
-- ============================================================
CREATE TABLE menu_categories (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id), -- denormalized for RLS
  menu_id         UUID NOT NULL REFERENCES menus(id) ON DELETE CASCADE,
  name_ar         TEXT NOT NULL,
  name_en         TEXT,
  sort_order      INT NOT NULL DEFAULT 0,
  is_visible      BOOLEAN NOT NULL DEFAULT true,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- MENU ITEMS
-- ============================================================
CREATE TABLE menu_items (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id      UUID NOT NULL REFERENCES organizations(id), -- denormalized for RLS
  category_id          UUID NOT NULL REFERENCES menu_categories(id) ON DELETE CASCADE,
  name_ar              TEXT NOT NULL,
  name_en              TEXT,
  description_ar       TEXT,
  description_en       TEXT,
  price_halalas        INT  NOT NULL CHECK (price_halalas >= 0),
  calories             INT,
  sodium_mg            INT,
  caffeine_mg          INT,
  allergens            TEXT[] NOT NULL DEFAULT '{}',
  allergens_confirmed  BOOLEAN NOT NULL DEFAULT false,
  ingredients_text     TEXT,   -- raw input used for allergen detection
  image_url            TEXT,
  image_source         TEXT CHECK (image_source IN ('upload', 'ai_generated', 'imported')),
  badge                TEXT CHECK (badge IN ('new', 'bestseller', 'limited', 'sold_out')),
  is_available         BOOLEAN NOT NULL DEFAULT true,
  sort_order           INT NOT NULL DEFAULT 0,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- MEDIA ASSETS
-- ============================================================
CREATE TABLE media_assets (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  storage_path    TEXT NOT NULL,
  original_name   TEXT,
  mime_type       TEXT,
  size_bytes      INT,
  source          TEXT NOT NULL CHECK (source IN ('upload', 'ai_generated', 'imported', 'crawled')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- IMPORT JOBS
-- ============================================================
CREATE TABLE import_jobs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  source          TEXT NOT NULL CHECK (source IN ('csv', 'xlsx', 'pdf', 'image', 'url', 'whatsapp')),
  status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'processing', 'review', 'imported', 'rolled_back', 'failed')),
  raw_payload     JSONB,
  item_count      INT,
  confidence_avg  FLOAT,
  error_message   TEXT,
  imported_at     TIMESTAMPTZ,
  expires_at      TIMESTAMPTZ, -- 24-hour rollback window
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- AI AUDIT EVENTS (append-only)
-- ============================================================
CREATE TABLE ai_audit_events (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  user_id         UUID REFERENCES auth.users(id),
  feature         TEXT NOT NULL, -- 'translation' | 'allergen_detection' | 'description' | 'csv_mapping' | 'extraction'
  provider        TEXT NOT NULL, -- 'mistral' | 'groq'
  model           TEXT NOT NULL,
  prompt_version  TEXT NOT NULL, -- semver slug, e.g. 'allergen-v1.0'
  input_hash      TEXT NOT NULL, -- SHA-256 of input; never store raw input here
  output_summary  JSONB NOT NULL,
  approved_by     UUID REFERENCES auth.users(id),
  approved_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- CONSENT RECORDS
-- ============================================================
CREATE TABLE consent_records (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id),
  user_id         UUID REFERENCES auth.users(id),
  consent_type    TEXT NOT NULL, -- 'pdpl_data_processing' | 'marketing' | 'ai_processing'
  consented       BOOLEAN NOT NULL,
  ip_address      TEXT,
  user_agent      TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ============================================================
-- AUDIT EVENTS (immutable; never update or delete rows)
-- ============================================================
CREATE TABLE audit_events (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID REFERENCES organizations(id),
  user_id         UUID REFERENCES auth.users(id),
  action          TEXT NOT NULL, -- 'menu_item.price_changed' | 'menu_item.allergen_confirmed' | etc.
  entity_type     TEXT NOT NULL,
  entity_id       UUID,
  before_snapshot JSONB,
  after_snapshot  JSONB,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

## RLS Policies (pattern — apply to every tenant-scoped table)

```sql
-- Enable RLS
ALTER TABLE menu_items ENABLE ROW LEVEL SECURITY;

-- Authenticated org members can read their own org's data
CREATE POLICY "members read own org" ON menu_items
  FOR SELECT TO authenticated
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_memberships WHERE user_id = auth.uid()
    )
  );

-- Authenticated owners/managers can write
CREATE POLICY "owners write own org" ON menu_items
  FOR ALL TO authenticated
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_memberships
      WHERE user_id = auth.uid() AND role IN ('owner', 'manager')
    )
  );

-- Public (anon) access to published menu items — scoped by org in application layer
-- (Next.js server component resolves slug → org_id and passes it explicitly)
CREATE POLICY "public reads available items" ON menu_items
  FOR SELECT TO anon
  USING (is_available = true);
```

**Note on public RLS:** The `anon` policy permits reading any org's available items. The application layer is responsible for filtering by `organization_id`. A public menu Server Component always calls `.eq('organization_id', resolvedOrgId)` — never returns all items unfiltered.

---

## V1.3 Tables (Billing & Multi-user — document only; create in V1.3 migration)

```
subscriptions        — plan tier, Moyasar subscription ID, status, billing dates
subscription_plans   — plan definitions (tier name, price_halalas, feature flags)
webhook_events       — Moyasar webhook payloads (idempotent processing)
idempotency_keys     — prevent duplicate payment processing
```

---

## V2 Tables (Loyalty — document only; create in V2 migration)

```
loyalty_programs     — program config per org (stamps needed, reward description)
loyalty_cards        — one card per customer per org
loyalty_events       — immutable ledger: stamp earned, stamp redeemed, reward issued
wallet_passes        — Apple + Google pass records
wallet_devices       — APNs device tokens for silent Apple Wallet push
campaigns            — AI-generated or manual campaigns
campaign_recipients  — send log per customer
```

---

## V3 Tables (Ordering — document only; create in V3 migration)

```
orders               — order header (type: dine_in | pickup | delivery)
order_items          — line items with price_halalas snapshot at time of order
order_status_events  — immutable status history
payments             — Moyasar charge records with tax_halalas, refund_halalas snapshots
restaurant_locations — for multi-branch pickup/delivery
```

---

## V4 Tables (Delivery — document only; create in V4 migration)

```
drivers              — driver accounts
delivery_zones       — zone polygons (Mapbox GeoJSON)
delivery_events      — driver location events (append-only)
```
