# Zalatah Menu → Restaurant SaaS: Full Product Roadmap (v3 — Saudi-Compliant + AI Features)

---

## User's Intent (Restated)

> I want to transform my existing static restaurant menu website into a SaaS platform that restaurants can use to upload and manage their digital menus. I want to plan the full product landscape across four versions so I don't have to recode or re-architect between iterations. V2 will introduce a loyalty card system (stamp-based or points-based). V3 will add online ordering. V4 will add delivery management. For each version I need both the basic (must-have) and advanced (differentiating) feature lists. I also need a cost-efficiency analysis for deployment, keeping in mind this is a one-person company. The platform will be based in Saudi Arabia — it must comply with NCA cybersecurity requirements and PDPL, and must avoid services with known ties to Israel. AI features should be integrated throughout: Arabic input with auto-translation to English, ingredient-to-allergen detection, AI-generated food photos, photo editing and background removal, and AI-written menu descriptions.

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

**AI-specific PDPL note**: Menu item descriptions and images sent to AI APIs (OpenRouter/Mistral/fal.ai) are business content, not personal data — no PDPL consent needed. However, if customers submit photos or text as part of an order or review, that data must stay within KSA or under a documented transfer agreement.

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

This is not optional. Any platform serving Saudi restaurants must make SFDA compliance easy and automatic. **The AI allergen detection feature directly solves this requirement** — restaurants enter ingredients and the AI populates allergen declarations automatically.

**Implementation**: `calories`, `sodium`, `caffeine`, `allergens[]` fields in `menu_items` schema from V1. AI populates these fields; staff reviews and confirms.

---

## Payment Processing Analysis

### Services Evaluated

#### Whop — Not Applicable

Whop is a US-based Merchant of Record platform built for Western digital product sellers (courses, communities, software). It **cannot accept Mada or STC Pay**, is not SAMA-licensed, and has no path to Saudi bank payouts. Effective international transaction rate reaches 6–7% (2.7% + $0.30 base + 1.5% international surcharge + 1% FX + 0.5% billing fee). The only relevant BNPL it offers is Klarna, which does not operate in Saudi Arabia. **Disqualified entirely.**

#### StreamPay.sa — Not Applicable

StreamPay.sa is a Riyadh-based billing layer designed specifically for schools and nurseries collecting tuition installments. It is not a payment gateway — it sits on top of a licensed PSP and does not publish its fees. While it handles recurring billing and ZATCA invoicing, it has no restaurant SaaS use case, no published pricing, and no BNPL capability. **Skip.**

#### MyFatoorah — Relevant for GCC Expansion

Kuwait-founded (2015), operating across 8 GCC countries with one API integration. Supports Mada, Visa/MC, Apple Pay, STC Pay, and 10+ regional payment methods. Supports recurring billing via `RecurringModel` API parameter. No native Tamara or Tabby BNPL integration. No public pricing (requires contact). Developer docs are good but slightly behind Moyasar's quality. No Israeli connections found.

**Strategic value**: If the platform expands to Kuwait, UAE, Bahrain, or Qatar within 12–18 months, MyFatoorah covers all of them with one existing integration. Switching from Moyasar to MyFatoorah later would be a significant re-integration — the right move is to design the payment abstraction layer in V1 so the gateway is swappable.

#### Tamara — BNPL for Large Orders Only

Saudi Arabia's dominant BNPL provider. Saudi-founded, PIF-subsidiary-backed, SAMA full consumer finance license (March 2025). First Saudi fintech unicorn. The most geopolitically safe payment provider possible for this platform.

| Detail | Value |
|---|---|
| Merchant fee | 4–7% |
| Minimum order | ~300 SAR |
| Maximum order | SAR 10,000+ |
| Payment splits | 3 monthly / 4 bi-weekly / 24 months (new) |
| Customer interest | 0% (Shariah-compliant) |
| Settlement | Weekly to merchant |
| Israeli connections | **None** (Saudi/PIF-backed) |

**For food orders (V3)**: Not practical for typical restaurant orders (SAR 50–150). The ~300 SAR minimum disqualifies most meals. However, relevant for catering, large group orders, corporate lunch orders, or subscription meal plans where order values consistently exceed SAR 300.

**For SaaS subscriptions (restaurant billing)**: Not suitable — BNPL is a one-time purchase mechanism, not compatible with recurring monthly billing.

**Gateway integrations**: HyperPay, Checkout.com, Amazon Payment Services, Tap Payments. Moyasar does not natively integrate Tamara.

#### Tabby — Secondary BNPL Option

UAE-dominant with strong Saudi Arabia presence. Founded by Hosam Arab (Arab, ex-Namshi CEO) and Daniil Barkalov (ex-Careem). $3.3B+ valuation (Feb 2025). SAMA-licensed. No Israeli connections found.

| Detail | Value |
|---|---|
| Merchant fee | 4–8% |
| Minimum order | ~100–300 SAR (merchant-configurable) |
| Payment splits | 4 bi-weekly payments |
| Customer interest | 0% (Shariah-compliant) |
| Settlement | Regular |
| Israeli connections | None |
| Gateway integrations | Checkout.com, MoneyHash, direct API |

**For food orders**: Same minimum order problem as Tamara. More viable for UAE customers. Better choice if the platform expands to UAE before BNPL is needed in KSA.

---

### Payment Gateway Decision Matrix

| | **Moyasar** | **MyFatoorah** | Whop | StreamPay.sa |
|---|---|---|---|---|
| HQ | Riyadh, KSA | Kuwait | New York | Riyadh, KSA |
| SAMA licensed | Yes | Yes (effectively) | **No** | Via partner only |
| Mada | Yes (1.5% + 1 SAR) | Yes (~1.5–2.0%) | **No** | Via partner |
| Visa/MC | Yes (2.2% + 1 SAR) | Yes (2.0–2.75%) | 2.7% + $0.30 (USD) | Undisclosed |
| STC Pay | Yes | Yes | **No** | Via partner |
| Apple Pay | Yes | Yes | **No** | Via partner |
| Monthly fee | 0–200 SAR | None | None | Undisclosed |
| Recurring/SaaS | Yes | Yes | Yes | Yes |
| Native BNPL | No | No | Klarna (not KSA) | No |
| Multi-GCC | **No** | **Yes (8 countries)** | 187 countries | No |
| Israeli risk | None | None | None | None |
| Public pricing | Yes | **No** | Yes | **No** |
| Developer docs | Excellent | Good | Excellent | Poor |
| Restaurant SaaS fit | **Primary** | **GCC expansion** | Skip | Skip |

### BNPL Decision Matrix

| | **Tamara** | **Tabby** | Postpay | Spotii/Zip |
|---|---|---|---|---|
| KSA market position | Dominant | Strong | Small | Tier 3 |
| SAMA license | Yes (full) | Yes | Yes | Yes (2023) |
| Merchant fee | 4–7% | 4–8% | Undisclosed | Undisclosed |
| Min order | ~300 SAR | ~100–300 SAR | Undisclosed | Undisclosed |
| Food order fit | Low (min too high) | Low–Medium | Low | Low |
| Large/catering orders | Yes | Yes | Maybe | Maybe |
| SaaS subscriptions | **No** | **No** | No | No |
| Israeli risk | **None (PIF-backed)** | None | None | None |
| Gateway partners | HyperPay, Checkout.com, APS, Tap | Checkout.com, MoneyHash | Direct | Direct |
| Moyasar integration | **Not confirmed** | Not confirmed | Not confirmed | Not confirmed |

### Recommendations

**Phase 1 (Launch):**
Keep **Moyasar** as the sole payment processor for:
- Restaurant SaaS subscription billing
- V3 customer food order checkout (Mada, Visa/MC, Apple Pay, STC Pay)

No BNPL integration at launch — average food order values are below BNPL minimums.

**Phase 2 (GCC Expansion, ~12–18 months post-launch):**
Add **MyFatoorah** as a secondary gateway option that restaurants in Kuwait, UAE, Bahrain, or Qatar can select during onboarding. The payment gateway must be abstracted behind a `PaymentProvider` interface from V1 to allow this swap.

```typescript
// Payment abstraction layer — design this in V1
interface PaymentProvider {
  createSubscription(plan: Plan, org: Organization): Promise<SubscriptionResult>
  chargeOrder(order: Order, customer: Customer): Promise<ChargeResult>
  webhook(payload: unknown): Promise<WebhookEvent>
}

class MoyasarProvider implements PaymentProvider { ... }
class MyFatoorahProvider implements PaymentProvider { ... }  // add in GCC expansion
```

**Phase 3 (Large Order BNPL, V3 Advanced):**
Add **Tamara** as an optional checkout method for orders exceeding SAR 300. Target use case: catering orders, large group orders, corporate meal subscriptions. Implement via HyperPay (which integrates both Moyasar-equivalent methods AND Tamara in one gateway) or integrate Tamara's API directly alongside Moyasar.

**Tamara pricing impact on restaurant economics:**
- Restaurant receives 93–96% of order value (Tamara takes 4–7%)
- Compare: third-party aggregators (Jahez, HungerStation) take 25–30% commission
- Platform's zero-commission positioning holds: Tamara cost is passed to restaurant transparently, still far cheaper than aggregators

---

## Vendor Risk Assessment (Israeli Connections)

The following assessment is based on public information available as of mid-2026.

### Infrastructure & Platform Services

| Vendor | Connection to Israel | KSA Availability | Decision |
|---|---|---|---|
| **Vercel** | CEO posted selfie with PM Netanyahu (Sep 2025); active developer boycott campaigns | Available | **REPLACE** — use Cloudflare Pages |
| **Supabase** | None found | Available | **SAFE TO USE** |
| **Google Cloud / Firebase** | Project Nimbus: $1.2B contract providing cloud + AI to Israeli military | Available | **AVOID** — highest risk |
| **AWS** | Project Nimbus co-contractor | Available | **HIGH RISK** — use Oracle Cloud KSA instead |
| **Stripe** | Israeli entity "Stripe Israel Payments Ltd."; CEO visited Israel Nov 2024 | **NOT AVAILABLE IN KSA** | **CANNOT USE** — use Moyasar |
| **Cloudflare** | R&D center confirmed in Israel; also has Dubai office | Available | **MODERATE RISK** — accept for CDN/DNS only |
| **Resend** | None found | Available | **ACCEPTABLE** |
| **Sentry** | None found | Available | **SAFE** — replace with self-hosted GlitchTip |
| **Umami** | None found (open source, MIT) | Self-hosted | **SAFE — RECOMMENDED** |
| **Twilio** | No R&D office in Israel | Available | **LOW RISK** — replace with Unifonic |
| **Mapbox** | None found | Available | **SAFE — RECOMMENDED** |
| **Oracle Cloud** | None found | Available (KSA DC) | **SAFE — RECOMMENDED** |

### AI Service Providers

| Vendor | Connection to Israel | Notes | Decision |
|---|---|---|---|
| **Mistral AI** | None found (French company, Paris HQ) | EU-based, strong Arabic support | **SAFE — PRIMARY TEXT AI** |
| **Groq** | None found (US startup) | Free tier suitable for allergen detection | **SAFE — FREE TIER TEXT** |
| **OpenRouter** | None found (US routing platform) | Routes to multiple providers — configure to exclude Google models | **SAFE** (avoid routing via Google/AWS) |
| **fal.ai** | None found (US startup, YC-backed) | EU/US data centers; image generation + editing | **SAFE — PRIMARY IMAGE AI** |
| **Replicate** | None found (US startup) | Open-source model hosting | **SAFE — BACKUP IMAGE AI** |
| **Google Gemini** (via OpenRouter) | Project Nimbus | Avoid routing to Google models on OpenRouter | **DO NOT USE** — even indirectly |
| **OpenAI / GPT Image** | None found (US company) | Acceptable if needed; not the cheapest | **ACCEPTABLE — BACKUP ONLY** |

**Key AI vendor rule**: When using OpenRouter, explicitly set `provider.allow` to exclude Google models. Use Mistral direct API or Groq as the default text providers.

### Payment Processing Providers

| Vendor | HQ | Connection to Israel | SAMA Licensed | Decision |
|---|---|---|---|---|
| **Moyasar** | Riyadh, KSA | None found | Yes (fully) | **SAFE — PRIMARY** |
| **MyFatoorah** | Kuwait | None found | GCC-equivalent | **SAFE — GCC EXPANSION** |
| **Tamara** | Riyadh, KSA (PIF-backed) | None found | Full consumer finance license (Mar 2025) | **SAFE — BNPL V3 large orders** |
| **Tabby** | Dubai, UAE | None found | SAMA licensed | **SAFE — BNPL alternative** |
| **Whop** | New York, USA | None found | **Not licensed in KSA** | **SKIP — not KSA-compatible** |
| **Stripe** | Dublin (Israeli entity) | "Stripe Israel Payments Ltd."; CEO visit Nov 2024 | **Not available in KSA** | **DO NOT USE** |

---

## AI Features

AI is integrated into the admin menu-building workflow in V1 and carried through all versions. All AI processing happens server-side (Cloudflare Worker or Next.js API route) — raw menu content never reaches the browser from AI APIs.

### AI Feature 1: Arabic Input → Auto English Translation

**What it does**: Restaurant owner types item name and description in Arabic. A single button click sends the text to the AI and populates the English fields automatically. Owner reviews and saves.

**Technology**: Mistral Ministral 3B (direct API) — smallest model, cheapest per token, handles Arabic-to-English translation accurately.

**Fallback for quality**: If the owner wants richer English prose, route to Groq Llama 3.3 70B (still cheap, better output quality for marketing text).

**Cost per translation** (100 in + 100 out tokens):
| Provider | Cost per translation | Monthly (2,500 ops) |
|---|---|---|
| Mistral Ministral 3B (direct) | **$0.000008** (~0.03 halala) | **$0.02** |
| Groq Llama 3.3 70B | $0.000191 | $0.48 |
| OpenRouter Qwen3 8B | $0.000010 | $0.025 |

**Monthly cost at scale** (50 restaurants × 50 items each = 2,500 translations): **under $0.50 total**.

**UX flow in admin**:
```
[اسم الصنف: كبسة جمال] → [Translate ✨] → [Name: Camel Kabsa]
[الوصف: أرز بسمتي مع لحم جمال...] → [Translate ✨] → [Description: Basmati rice with camel meat...]
```

---

### AI Feature 2: Ingredients → Auto Allergen Detection

**What it does**: Restaurant owner enters a free-text ingredients list (in Arabic or English). AI returns a structured list of allergens per the SFDA-required categories: gluten, dairy, eggs, tree nuts, peanuts, shellfish, fish, sesame, soy, mustard, sulfites.

**Why this matters**: Directly satisfies the **SFDA July 2025 mandate** for allergen declarations. Removes a major friction point for restaurant owners who don't know which allergens apply to their ingredients.

**Technology**: Groq Llama 3.1 8B — free tier, structured JSON output, this task requires minimal reasoning capacity so even a small model performs accurately.

**System prompt approach**:
```
You are a food allergen classifier. Given an ingredients list, return a JSON array of allergens from this fixed list: [gluten, dairy, eggs, tree_nuts, peanuts, shellfish, fish, sesame, soy, mustard, sulfites]. Return ONLY the array, no explanation. Arabic input is acceptable.
```

**Cost per allergen detection** (100 in + 30 out tokens):
| Provider | Cost per detection | Monthly (2,500 ops) |
|---|---|---|
| Groq free tier | **$0.000000** | **$0.00** |
| Mistral Ministral 3B (backup) | $0.000006 | $0.015 |

**Monthly cost at scale**: **$0.00** using Groq free tier (14,400 requests/day limit — more than sufficient). Falls back to Mistral at $0.015/month if Groq rate limit is hit.

**UX flow in admin**:
```
[المكونات: دقيق، بيض، حليب، سمسم، خل] 
→ [Detect Allergens ✨]
→ Allergens detected: ✓ Gluten  ✓ Eggs  ✓ Dairy  ✓ Sesame  ✓ Sulfites
→ [Confirm & Save]
```

---

### AI Feature 3: AI-Written Menu Descriptions

**What it does**: Given item name + ingredients list (both already entered), AI generates a polished 1–2 sentence marketing description in both Arabic and English. Owner reviews, edits if needed, and saves.

**Technology**: Two-tier approach based on plan level:
- **Budget (Starter tier)**: Mistral Ministral 3B — functional descriptions, lowest cost
- **Quality (Pro/Business tier)**: Groq Llama 3.3 70B or Mistral Large — richer Arabic prose, more evocative marketing language

**Cost per description** (150 in + 300 out tokens, bilingual):
| Provider | Cost per description | Monthly (2,500 ops) |
|---|---|---|
| Mistral Ministral 3B (direct) | **$0.000018** | **$0.045** |
| Groq Llama 3.3 70B | $0.000462 | $1.15 |
| Mistral Nemo 12B (mid-quality) | $0.000045 | $0.11 |
| Mistral Large 2 (premium) | $0.000990 | $2.48 |

**Monthly cost at scale**: **$0.05–$2.50** depending on quality tier — negligible even at the premium end.

**UX flow in admin**:
```
[Item: Zalatah Caesar Salad]
[Ingredients: romaine lettuce, parmesan, croutons, caesar dressing, lemon]
→ [Write Description ✨]
→ AR: "سلطة قيصر مميزة بالخس الروماني الطازج وقطع الخبز المحمص..."
   EN: "A classic Caesar salad with crisp romaine, shaved Parmesan, golden croutons..."
→ [Edit | Accept]
```

---

### AI Feature 4: AI Food Photo Generation

**What it does**: If a restaurant has no photo for a menu item, they can generate a placeholder photo using a text prompt. The platform auto-constructs the prompt from the item name and description.

**⚠️ Note**: Banana.dev shut down permanently in March 2024. DALL-E 3 was removed from the OpenAI API in May 2026. Use fal.ai or Replicate with FLUX models instead.

**Technology**:
- **Draft/preview**: FLUX.1 Schnell on Replicate or fal.ai — fast, cheap, good enough to see the concept
- **Final production photo**: fal.ai FLUX Pro v1.1 — photorealistic food photography quality suitable for the public menu

**Auto-prompt template** (built into the platform):
```
Professional food photography of {item_name_en}, {short_description}, 
white marble surface, soft studio lighting, top-down angle, 
restaurant menu style, vibrant colors, sharp focus, no text, no logo
```

**Cost per image**:
| Provider & Model | Cost/Image | Quality | Notes |
|---|---|---|---|
| Replicate FLUX Schnell | **$0.003** | Draft — good concept | Fast, 4 steps |
| fal.ai FLUX Schnell | **$0.003** | Draft | Identical model |
| fal.ai FLUX Pro v1.1 | **$0.040** | Photorealistic | Production quality |
| fal.ai FLUX Pro Ultra | $0.060 | Highest quality | For hero images |
| Fireworks AI FLUX Schnell | **$0.0014** | Draft — cheapest | Ultra-budget option |

**UX flow in admin**:
```
[Item has no photo]
→ [Generate Photo ✨] (uses 1 credit)
→ Preview: [draft image displayed]
→ [Regenerate] | [Upgrade to HD — 10 credits] | [Upload my own photo instead]
```

**Credit system** (to control cost and monetize AI):
- Free tier: 3 AI image generations/month
- Starter: 20 generations/month
- Pro/Business: 100 generations/month
- Additional: restaurant buys credit packs (e.g., 10 credits = SAR 10)

**Monthly cost at scale** (2,500 restaurants × 3 draft images each = 7,500 images):
| Model | Monthly Cost |
|---|---|
| All drafts (FLUX Schnell × 7,500) | **$22.50** |
| 20% upgraded to production (FLUX Pro × 1,500) | **$60.00** |
| **Total** | **~$82.50/month** |

---

### AI Feature 5: Photo Background Removal & Enhancement

**What it does**: Restaurant uploads an existing photo taken on a phone (often against a cluttered background). The platform automatically removes the background and replaces it with a clean white/gradient background suitable for a professional menu.

**Technology**: fal.ai Bria RMBG 2.0 — trained specifically for product/food photography, professional quality, simple single-call API.

**Cost per image**:
| Provider | Model | Cost/Image | Quality |
|---|---|---|---|
| fal.ai | Bria RMBG 2.0 | **$0.018** | Professional, e-commerce grade |
| fal.ai | rembg (OSS) | **~$0.001–0.003** | Good, open-source, slight edge artifacts |
| PhotoRoom API | PhotoRoom | $0.020 | Excellent, food-optimized |
| remove.bg | remove.bg | $0.200 | Best quality but 10x more expensive |
| Clipdrop API | Clipdrop | $0.120–0.180 | High quality, overpriced |

**Recommended**: fal.ai Bria RMBG 2.0 at **$0.018/image** — professional results at 10x cheaper than remove.bg.

**Photo upscaling** (for low-res phone photos, 4x enhancement):
| Provider | Model | Cost/Image | Notes |
|---|---|---|---|
| fal.ai | Real-ESRGAN | **~$0.002** | Compute-second billing (~3s per image) |
| ModelsLab | Real-ESRGAN | **$0.002** flat | Predictable billing |

**UX flow in admin**:
```
[Upload photo from phone]
→ Auto-detect: low resolution detected
→ [Remove Background ✨] | [Enhance & Upscale ✨] | [Both ✨]
→ Before / After preview
→ [Save to menu]
```

**Monthly cost at scale** (500 new photos uploaded per month across all restaurants):
| Task | Volume | Cost/Image | Monthly Cost |
|---|---|---|---|
| Background removal | 500 photos | $0.018 | **$9.00** |
| Upscaling (40% of photos) | 200 photos | $0.002 | **$0.40** |
| **Total photo editing** | | | **~$9.40/month** |

---

### AI Cost Summary

| AI Feature | Recommended Provider | Cost per Operation | Monthly Cost (500 restaurants) |
|---|---|---|---|
| Arabic → English translation | Mistral Ministral 3B | $0.000008 | **$0.02** |
| Allergen detection | Groq Llama 3.1 8B (free) | $0.000000 | **$0.00** |
| Description writing (budget) | Mistral Ministral 3B | $0.000018 | **$0.05** |
| Description writing (quality) | Groq Llama 3.3 70B | $0.000462 | **$1.15** |
| Image generation — draft | Replicate FLUX Schnell | $0.003 | **$22.50** |
| Image generation — production | fal.ai FLUX Pro v1.1 | $0.040 | **$60.00** |
| Background removal | fal.ai Bria RMBG 2.0 | $0.018 | **$9.00** |
| Photo upscaling | fal.ai Real-ESRGAN | ~$0.002 | **$0.40** |
| **Total AI costs** | | | **~$93/month** |

**Key insight**: Text AI (translation, allergen detection, description writing) is effectively free — under $1.25/month for 500 restaurants. The only meaningful AI cost is image generation. This can be fully offset by charging restaurants for an "AI Credits" add-on.

---

## WhatsApp Menu Management (V1 Advanced Feature)

**Goal**: Restaurant owners can add, edit, or remove menu items by sending a WhatsApp message to a dedicated business number — no web dashboard login required. Designed for mobile-first Saudi restaurant operators who spend their day in WhatsApp, not browsers.

### How It Works

Each restaurant is linked to a single Unifonic WhatsApp Business number (the platform's number). When the owner messages it, a Cloudflare Worker receives the webhook, identifies the restaurant from the sender's phone number, and runs a conversational flow powered by Mistral AI.

**Conversation flow (Arabic or English)**:

```
Owner:  "أضف صنف جديد"   (or: "add new item")

Bot:    "تفضل! أرسل اسم الصنف"
Owner:  "كبسة دجاج مشوي"

Bot:    "ما هي الفئة؟ الفئات الحالية: مشويات، مقبلات، مشروبات"
Owner:  "مشويات"

Bot:    "كم السعر؟ (أو أرسل نطاق مثل 45-65)"
Owner:  "55"

Bot:    "أرسل المكونات لاكتشاف المواد المسببة للحساسية تلقائياً، أو اكتب 'تخطى'"
Owner:  "أرز، دجاج، بهارات، لبن"

Bot:    "المواد المسببة للحساسية المكتشفة: حليب ✓
         هل تريد كتابة وصف تسويقي بالذكاء الاصطناعي؟ (نعم/لا)"
Owner:  "نعم"

Bot:    "الوصف: كبسة دجاج مشوي على الفحم مع الأرز العنبر...
         EN: Grilled chicken kabsa with fragrant amber rice...
         
         هل تريد إضافة صورة؟
         1️⃣ أرسل صورة من هاتفك
         2️⃣ توليد صورة بالذكاء الاصطناعي (يستهلك رصيد واحد)
         3️⃣ بدون صورة الآن"
Owner:  [sends photo from phone]

Bot:    "تم استلام الصورة. هل تريد إزالة الخلفية؟ (نعم/لا)"
Owner:  "نعم"

Bot:    "✅ تمت إضافة كبسة دجاج مشوي إلى قائمتك الآن!
         شاهد القائمة: yoursaas.com/[slug]"
```

### Supported Commands (Arabic + English)

| Command | Action |
|---|---|
| `أضف صنف` / `add item` | Start the add-item conversational flow |
| `عدّل صنف [اسم]` / `edit [item name]` | Edit an existing item (price, description, availability) |
| `احذف صنف [اسم]` / `remove [item name]` | Remove item from menu |
| `أوقف صنف [اسم]` / `86 [item name]` | Mark item unavailable (hidden on public menu, not deleted) |
| `فعّل صنف [اسم]` / `enable [item name]` | Re-enable a paused item |
| `القائمة` / `my menu` | Bot replies with a summary of all categories and item counts |
| `الأصناف غير المتوفرة` / `unavailable items` | List all currently paused items |
| `مساعدة` / `help` | Show all available commands |

### Meta / WhatsApp Business API Requirements

This is the infrastructure that must be provisioned per restaurant before any bot message can be sent or received.

#### Architecture: One WABA per Restaurant (Mandatory)

Meta policy prohibits a shared WhatsApp number across multiple business tenants. Each restaurant must have its own **WhatsApp Business Account (WABA)** and its own **registered phone number**. There is no multi-tenant shortcut.

The correct architecture is:

```
Your SaaS Platform (Unifonic BSP Partner Account)
    ├── Restaurant A — WABA-A + Number +966-5x-xxx-xxxx
    ├── Restaurant B — WABA-B + Number +966-5x-xxx-xxxx
    ├── Restaurant C — WABA-C + Number +966-5x-xxx-xxxx
    └── ... one WABA per tenant
```

Unifonic acts as the **Business Solution Provider (BSP)** and manages all WABAs under your platform's partner account. Restaurants connect via **Meta Embedded Signup** — they don't need a developer account.

#### Per-Restaurant Onboarding Steps

| Step | Who Does It | Time |
|---|---|---|
| 1. Create Meta Business Portfolio (once, platform level) | You (once) | 15 min |
| 2. Set up Unifonic BSP partner account | You (once) | 1–2 days |
| 3. Restaurant completes Meta Embedded Signup via your dashboard | Restaurant owner | 5 min |
| 4. Meta Business Verification (CR + legal name match) | Restaurant owner uploads docs | 2–4 business days |
| 5. Phone number registration + display name submission | Auto via Unifonic | Same day after verification |
| 6. Display name approval | Meta | Same day to 24 hours |
| 7. Bot goes live | Automatic | Immediate |

**Critical:** The restaurant's legal name in Meta Business Manager must **exactly match** the Commercial Registration (السجل التجاري) — including Arabic/English, punctuation, and legal suffixes (ش.م.م., LLC). The #1 rejection cause globally.

#### Phone Number Rules

- Each restaurant needs a **dedicated phone number** — mobile, landline, or toll-free all work
- If the restaurant already uses WhatsApp (consumer or Business app) on that number: they must **delete it from WhatsApp first** — this permanently loses chat history
- New numbers provisioned by Unifonic avoid this issue
- Number must receive OTP via SMS or voice call during registration

#### Message Templates

Most WhatsApp bot interactions fall inside the **24-hour service window** (when a customer messages first), which means they are **free Service messages** — no template needed.

Templates are only required for outbound messages initiated by the platform after the 24-hour window closes:

| Message Type | Template Needed? | Category | KSA Cost/Message |
|---|---|---|---|
| Bot replies to customer (inside 24h window) | No | Service | **Free** |
| "Your order is ready" (inside 24h) | No | Service | **Free** |
| Order confirmation (inside 24h) | No | Service | **Free** |
| Order confirmation (outside 24h) | Yes | Utility | $0.0107 |
| Loyalty reward notification (proactive) | Yes | Utility | $0.0107 |
| Promotional campaign | Yes | Marketing | $0.0455 |
| OTP / login code | Yes | Authentication | $0.0107 |

**Template approval:** Submit via Unifonic dashboard → Meta reviews → typically same day for verified businesses. Rejection rate drops below 5% with BSP pre-screening.

#### Meta Pricing (KSA, per-message model effective July 1, 2025)

| Category | KSA Rate/Message |
|---|---|
| Service (customer-initiated, 24h window) | **Free** |
| Utility | $0.0107 |
| Authentication | $0.0107 |
| Marketing | $0.0455 |

Budget estimate per restaurant per month:
- 500 service conversations (inbound bot) → **$0**
- 200 Utility templates (order confirmations, loyalty alerts) → **$2.14**
- 100 Marketing templates (campaigns) → **$4.55**
- **Total Meta API cost: ~$6.69/restaurant/month**

Unifonic applies ~10–30% markup over Meta's rates. Budget **~$8–9/restaurant/month** for WhatsApp at active usage.

#### Bot Compliance Requirements

- **AI chatbot policy (effective Jan 15, 2026):** Meta banned general-purpose AI chatbots. A structured restaurant menu bot (add items, edit prices, 86 dishes) is **fully compliant** — it is task-specific business automation, not open-domain chat.
- **Opt-in:** When a customer scans the restaurant's QR and messages the bot, this is user-initiated — implicit opt-in for service messages. For marketing messages (loyalty campaigns), capture explicit opt-in within the conversation.
- **Human escalation path:** Bot must always offer a path to reach a human (e.g., "رد بـ 'إنسان' للتحدث مع الفريق") — required by Meta's bot policy.
- **Saudi PDPL:** Customer messages processed by the bot are personal data. Store session data on Oracle KSA; retain only as long as necessary; include in deletion workflow.

#### Required Templates to Pre-Approve at Launch

| Template Name | Category | Content |
|---|---|---|
| `order_confirmation` | Utility | "طلبك رقم {{1}} استلمناه وسيكون جاهز خلال {{2}} دقيقة" |
| `order_ready` | Utility | "طلبك جاهز! تفضل بالاستلام" |
| `loyalty_reward_earned` | Utility | "مبروك! حصلت على مكافأتك: {{1}}" |
| `loyalty_stamp_added` | Utility | "تم إضافة طابع جديد. رصيدك: {{1}}/{{2}}" |
| `welcome_first_message` | Utility | First proactive contact after onboarding |
| `promo_campaign` | Marketing | Restaurant-defined; per-campaign |
| `otp_verification` | Authentication | "رمز التحقق: {{1}}. صالح لمدة 5 دقائق" |

### Technical Architecture

```
Customer scans QR → sends WhatsApp message to restaurant's number (via Unifonic)
    │
    ▼
Unifonic Webhook → Cloudflare Worker (whatsapp-bot.ts)
    ├── Identify restaurant by destination number → Supabase lookup (org_id)
    ├── Identify customer by sender phone number → Supabase lookup
    ├── Load conversation session state (whatsapp_sessions table, 30-min TTL)
    ├── Parse intent via Mistral AI (Arabic/English → structured action)
    ├── Execute action:
    │     ├── CRUD on menu_items (via Supabase service role, scoped to org_id)
    │     ├── Allergen detection (Groq API — free tier)
    │     ├── Description generation (Mistral API)
    │     ├── Image processing (fal.ai — background removal or AI generation)
    │     └── Translation if needed (Mistral API)
    └── Reply via Unifonic WhatsApp API (free Service message inside 24h window)
```

### New Database Table

```sql
whatsapp_sessions (
  id UUID PRIMARY KEY,
  organization_id UUID NOT NULL REFERENCES organizations(id),
  phone_number TEXT NOT NULL,       -- sender's WhatsApp number
  state TEXT NOT NULL,              -- 'idle' | 'adding_item' | 'editing_item' | ...
  context JSONB,                    -- partial item data accumulated mid-flow
  last_message_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ            -- sessions expire after 30 min of inactivity
)
```

### AI Cost for WhatsApp Bot

Each WhatsApp interaction chains multiple AI calls. Worst-case (full add-item flow with AI description + allergen detection):

| Step | Provider | Cost |
|---|---|---|
| Intent parsing (1 call × ~100 tokens) | Mistral Ministral 3B | $0.000008 |
| Allergen detection (1 call) | Groq free | $0.000000 |
| Description generation (1 call) | Mistral Ministral 3B | $0.000018 |
| Translation if needed (1 call) | Mistral Ministral 3B | $0.000008 |
| **Total text AI per full item add** | | **$0.000034 (~0.13 halala)** |

Image costs are the same as the dashboard (deducted from AI credits).

**Monthly text AI cost for WhatsApp bot at scale** (500 restaurants × 10 WhatsApp item operations each = 5,000 operations): **~$0.17** — negligible.

### Photo Handling via WhatsApp

- Owner sends a photo directly in WhatsApp → Unifonic webhook delivers the media URL → Cloudflare Worker downloads it → uploads to Supabase Storage (KSA) → triggers background removal on fal.ai → serves optimized WebP from Cloudflare CDN
- The photo never touches the owner's app or browser — entirely server-side pipeline

### Plan Gating

| Tier | WhatsApp Access |
|---|---|
| Free | Not available (upsell hook: "Upgrade to Starter to manage your menu from WhatsApp") |
| Starter | Add/edit/remove items; photo upload; allergen detection |
| Pro | Everything + AI description writing; AI image generation (uses credit balance) |
| Business | Everything + batch item import via WhatsApp (send CSV or multiple items in one message) |

### Why This Is a Strong Differentiator

- No Saudi restaurant SaaS competitor offers WhatsApp-native menu management
- Saudi restaurant operators are mobile-first; most manage their business entirely from WhatsApp
- Zero learning curve — operators already know how to send a WhatsApp message
- Works for staff too (if owner grants their number access) — a staff member can 86 an item from the kitchen without touching a laptop
- The entire AI stack (translation, allergen, description, photo) is accessible from the chat

### AI Vendor Stack (Added to Tech Stack)

| Layer | Choice | Israeli Risk | Notes |
|---|---|---|---|
| Text AI — primary | **Mistral AI direct API** | SAFE (French company) | Cheapest paid; great Arabic support |
| Text AI — free tier | **Groq** (Llama 3.1 8B) | SAFE (US, no Israeli connection) | Free 14.4K requests/day; ideal for allergen detection |
| Text AI — routing | **OpenRouter** (Mistral/Llama models only) | SAFE (exclude Google routing) | Use `:floor` suffix for cheapest provider; block Google |
| Image generation | **fal.ai** (FLUX Schnell + FLUX Pro) | SAFE (US startup) | Single API, both draft and production models |
| Image editing | **fal.ai** (Bria RMBG + ESRGAN) | SAFE | Same API key as image generation |
| Image backup | **Replicate** | SAFE (US startup) | Fallback if fal.ai is down |

---

## Monorepo Architecture

**Answer: Yes — a monorepo is the right call.** The project has multiple deployment targets (Next.js web app, Cloudflare Worker bot, staff PWA, wallet pass service) that share types, Supabase client config, UI components, and AI utilities. Without a monorepo, type changes in the database schema cascade into manual copy-paste across repos.

### Tool Choice: pnpm + Turborepo (not Nx)

Nx adds value at team scale (20+ packages, multiple developers). For a solo developer, the configuration overhead is unjustified. Turborepo is lightweight, works natively with Cloudflare Pages + Workers, and provides cached incremental builds from day one.

**Remote caching** (eliminates redundant CI rebuilds) is self-hosted free on Cloudflare R2/KV — no Vercel account needed.

### Monorepo Structure

```
your-project/
├── apps/
│   ├── web/              # Next.js 15 — admin dashboard + public menu pages + wallet endpoints
│   ├── staff-pwa/        # PWA — restaurant staff stamp issuance app (no App Store)
│   └── bot/              # Cloudflare Worker — WhatsApp webhook handler
├── packages/
│   ├── db/               # Supabase client + all TypeScript types (raw TS, not compiled)
│   ├── ui/               # Shared React components (shadcn/ui base + brand tokens)
│   ├── ai/               # Mistral + Groq + fal.ai client wrappers
│   ├── wallet/           # Apple Wallet (.pkpass) + Google Wallet pass generation
│   └── tsconfig/         # Base TS configs per runtime (next, worker, pwa)
├── turbo.json
├── pnpm-workspace.yaml
└── package.json          # Root: only dev tooling (turbo, typescript, eslint root config)
```

**Critical constraint:** `packages/wallet` uses Node.js `crypto` for Apple's PKCS#7 signing — import only from `apps/web` API routes (Node.js runtime). The Cloudflare Worker (`apps/bot`) cannot import it directly; if the bot needs to trigger a wallet update, it calls a `apps/web` API endpoint.

**TypeScript config per runtime** (in `packages/tsconfig/`):
- `next.json` — JSX support, DOM types, strict mode
- `worker.json` — `lib: ["ES2022"]`, no DOM, `webworker` types
- `pwa.json` — JSX, DOM + Service Worker types

### Independent Per-App Deployments

```bash
turbo build --filter=@app/bot        # builds bot + @pkg/db + @pkg/ai only
turbo build --filter=@app/web...     # builds web + all its dependencies
turbo build --filter=@app/staff-pwa  # builds PWA + @pkg/db + @pkg/ui
```

Each app has its own deploy step in CI — changing the WhatsApp bot never triggers a web rebuild.

---

## Revised Tech Stack (Saudi-Compliant + AI)

### Application Layer

| App | Framework | Deployment | Notes |
|---|---|---|---|
| `apps/web` | **Next.js 15** (App Router) | Cloudflare Pages + `@opennextjs/cloudflare` adapter | Admin dashboard, public menu, API routes, wallet endpoints |
| `apps/staff-pwa` | **Next.js 15** (PWA via `next-pwa`) | Cloudflare Pages (separate project) | Staff stamping app; installable, camera access, offline-capable |
| `apps/bot` | **Cloudflare Worker** (TypeScript) | `wrangler deploy` | WhatsApp webhook handler; AI proxy calls |

### Language & Tooling

| Tool | Choice | Version |
|---|---|---|
| Language | TypeScript | 5.x strict mode |
| Package manager | **pnpm** | v9+ |
| Monorepo | **Turborepo** | v2.x |
| Build (Next.js) | Turbopack | Built into Next.js 15 |
| Linting | ESLint (flat config) + Prettier | Latest |
| Git hooks | Husky + lint-staged | Pre-commit quality gate |
| Secret detection | Gitleaks | Pre-commit |

### Frontend

| Layer | Choice | Why |
|---|---|---|
| UI Framework | **Next.js 15 App Router** | RSC, Server Actions, streaming; eliminates separate API layer for most mutations |
| Component Library | **shadcn/ui** + Tailwind CSS v4 | Copy-paste components; no bundle overhead; full control over style |
| State (client) | **Zustand** | Minimal; only for UI state not covered by RSC (cart, camera, session) |
| Forms | **React Hook Form** + **Zod** | Validation shared between client and server; Zod schemas live in `packages/db` |
| Styling | **Tailwind CSS v4** | JIT, RTL plugin for Arabic layouts |
| RTL support | **tailwindcss-rtl** plugin | Auto-flips margins, padding, flex direction for Arabic |
| QR Scanner (staff PWA) | **@zxing/browser** | Camera QR decoding; no native dependency |
| Maps (V3/V4) | **Mapbox GL JS** | No Israeli ties; 50K tile loads/month free |

### Backend / API

| Layer | Choice | Why |
|---|---|---|
| API pattern | **Next.js Server Actions** (primary) + **Route Handlers** (webhooks/external) | Server Actions for form mutations; Route Handlers for Moyasar/Unifonic/Apple Wallet webhooks |
| Auth | **Supabase Auth** (self-hosted) | Email, magic link, OAuth; JWT claims carry `org_id` for RLS |
| ORM / Query | **Drizzle ORM** | Type-safe; lightweight (~27KB); generates types from schema; works with Supabase Postgres |
| Realtime | **Supabase Realtime** (self-hosted) | WebSocket-based; used for live order updates (V3) and driver tracking (V4) |
| Background jobs | **Cloudflare Workers** (cron triggers) | Nightly loyalty reminders, campaign scheduling, pass update batching |
| File uploads | **tus-node-server** → Supabase Storage | Resumable uploads for large images |

### Data Layer

| Component | Choice | Notes |
|---|---|---|
| Database | **PostgreSQL** (via self-hosted Supabase) | RLS for multi-tenancy; Drizzle for type-safe queries |
| BaaS | **Supabase** self-hosted on Oracle KSA | Postgres + Auth + Storage + Realtime in one Docker Compose |
| Schema migrations | **Drizzle Kit** (`drizzle-kit generate`, `drizzle-kit migrate`) | Or `supabase db push` — pick one and stay consistent |
| Caching | **Cloudflare KV** | Edge-cache public menu JSON (invalidate on menu update); rate-limit counters |
| Queue (future V3/V4) | **Cloudflare Queues** | Order processing; driver dispatch events |

### Infrastructure

| Layer | Choice | Notes |
|---|---|---|
| Compute | **Oracle Cloud KSA** (Riyadh DC) | Always Free: 4 Arm CPU, 24GB RAM, 200GB; hosts Supabase + Umami + GlitchTip |
| Frontend/API hosting | **Cloudflare Pages** | Automatic deploy on git push; preview per branch; $0 |
| Worker hosting | **Cloudflare Workers** | WhatsApp bot + AI proxy + cron jobs |
| CDN | **Cloudflare** | Static assets + menu images; moderate risk accepted |
| Object storage | **Supabase Storage** (KSA) | Menu images; integrated RLS |
| Container runtime | **Docker Compose** + **docker-rollout** | Zero-downtime service restarts on Oracle KSA |

### External Services

| Service | Provider | Israeli Risk | Purpose |
|---|---|---|---|
| Payments | **Moyasar** | SAFE (Saudi-native) | Mada, Visa/MC, Apple Pay, STC Pay; SAMA-licensed |
| SMS / WhatsApp | **Unifonic** | SAFE (Saudi CPaaS) | OTP, notifications, WhatsApp Business API |
| Email | **Resend** | SAFE | Transactional email; 3K/day free |
| Text AI | **Mistral AI** (direct API) | SAFE (French) | Translation, descriptions, campaigns, intent parsing |
| Text AI (free) | **Groq** | SAFE | Allergen detection (free tier, 14.4K req/day) |
| Image AI | **fal.ai** | SAFE | FLUX Schnell/Pro generation + Bria RMBG + ESRGAN |
| Analytics | **Umami** (self-hosted) | SAFE | Traffic analytics on Oracle KSA |
| Error monitoring | **GlitchTip** (self-hosted) | SAFE | Sentry-compatible; Oracle KSA |
| Uptime | **UptimeRobot** (free) | SAFE | 50 monitors, 5-min interval |
| Maps | **Mapbox** | SAFE | Delivery zones (V4); 50K loads/month free |
| Apple Wallet | **Apple PassKit** | SAFE | Loyalty card passes for iOS |
| Google Wallet | **Google Wallet API** | MODERATE (Project Nimbus concern) | Loyalty passes for Android; no viable alternative |
| QR codes | `qrcode` npm package | SAFE | Self-contained; no third-party service |
| WhatsApp (Meta) | via Unifonic BSP | SAFE (routed via Unifonic) | WhatsApp Business API; Unifonic abstracts Meta dependency |

### AI Stack

| Task | Provider | Model | Cost/op |
|---|---|---|---|
| Arabic→English translation | Mistral (direct) | Ministral 3B | $0.000008 |
| Allergen detection | Groq | Llama 3.1 8B | $0 (free) |
| Description writing | Mistral (direct) | Ministral 3B / Nemo 12B | $0.000018–$0.000045 |
| Campaign copy | Mistral (direct) | Nemo 12B | ~$0.000045 |
| WhatsApp intent parsing | Mistral (direct) | Ministral 3B | $0.000008 |
| Image generation (draft) | fal.ai | FLUX Schnell | $0.003 |
| Image generation (HD) | fal.ai | FLUX Pro v1.1 | $0.040 |
| Background removal | fal.ai | Bria RMBG 2.0 | $0.018 |
| Photo upscaling | fal.ai | Real-ESRGAN | ~$0.002 |

**OpenRouter** used optionally as fallback router — configured to **block all Google and AWS-hosted models**.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   CLOUDFLARE NETWORK                        │
│  Pages (apps/web)   Pages (apps/staff-pwa)   Workers        │
│  ├─ Public menu     ├─ Stamp interface        ├─ WhatsApp bot│
│  ├─ Admin dashboard ├─ QR scanner             ├─ AI proxy   │
│  ├─ Order checkout  └─ Reward redemption      └─ Cron jobs  │
│  └─ Wallet endpoints                                         │
└─────────────┬───────────────────────────────────────────────┘
              │ (KSA-only PII; all DB calls)
              ▼
┌─────────────────────────────────────────────────────────────┐
│              ORACLE CLOUD KSA (Riyadh DC)                   │
│  Self-hosted Supabase                                        │
│  ├─ PostgreSQL + Drizzle ORM (RLS multi-tenant)             │
│  ├─ Supabase Auth (JWT with org_id claim)                   │
│  ├─ Supabase Storage (menu images → Cloudflare CDN)         │
│  └─ Supabase Realtime (orders, driver tracking)             │
│  Umami (analytics)    GlitchTip (error tracking)            │
└─────────────────────────────────────────────────────────────┘
              │
    External APIs (business data only — no PII crosses border)
    ├─ Mistral AI (text)          ├─ fal.ai (images)
    ├─ Groq (allergen detection)  ├─ Moyasar (payments)
    ├─ Unifonic (WhatsApp/SMS)    ├─ Resend (email)
    ├─ Apple PassKit (wallet)     └─ Google Wallet API
```

---

## Oracle Cloud KSA — Always Free Tier Details

Oracle's Always Free tier includes resources that never expire:
- 4 Arm-based Ampere A1 CPUs + 24 GB RAM (runs Supabase + GlitchTip + Umami comfortably)
- 200 GB block storage
- 2 x AMD VMs
- 10 GB object storage
- Outbound data: 10 TB/month free

Infrastructure cost at early stage: **SAR 15–50/month** (domain + any overages).

---

## Deployment Cost Analysis (Saudi-Compliant + AI Stack)

### Early Stage (0–50 restaurants, pre-revenue)

| Service | Cost/Month |
|---|---|
| Oracle Cloud KSA (Always Free) | SAR 0 |
| Cloudflare Pages (Free tier) | SAR 0 |
| Umami + GlitchTip (self-hosted) | SAR 0 |
| Resend (Free: 3,000 emails/day) | SAR 0 |
| Groq API (free tier for allergen detection) | SAR 0 |
| Mistral AI (text AI — 50 restaurants × ~50 items) | ~$0.05 (~SAR 0.19) |
| fal.ai (image AI — 50 restaurants × 3 draft images) | ~$0.45 (~SAR 1.69) |
| Unifonic SMS (pay-per-use OTP) | ~SAR 0.25–0.50 per OTP |
| Domain | ~SAR 4/month |
| Moyasar | 2.2% + 1 SAR per transaction |
| **Total fixed** | **~SAR 6/month** |

### Growth Stage (SAR 5,000–15,000 MRR, 50–300 restaurants)

| Service | Cost/Month |
|---|---|
| Oracle Cloud KSA (paid compute) | SAR 150–400 |
| Cloudflare Pro | SAR 75 ($20) |
| Resend Starter | SAR 75 ($20) |
| Unifonic SMS + WhatsApp | SAR 100–300 |
| Backup storage (Oracle Object) | SAR 50–100 |
| Mistral AI (text) | ~$1.50 (~SAR 6) |
| fal.ai (image AI — 300 restaurants) | ~$50–100 (~SAR 190–375) |
| **Total infra + AI** | **SAR 650–1,300/month** |
| Moyasar fees at SAR 10K MRR | ~SAR 225 (2.2%) |
| **Total all-in** | **~SAR 875–1,525/month** |

**AI cost offset strategy**: Charge restaurants for AI credits separately (e.g., 10 image generations = SAR 10, free with Pro/Business plans). At 300 restaurants generating 10 images each/month, credit revenue covers AI costs ~3–4x over.

### Full Scale ($10K+ MRR, 300+ restaurants)

| Service | Cost/Month |
|---|---|
| Oracle Cloud KSA (upgraded compute) | SAR 400–750 |
| Cloudflare Pro | SAR 75 |
| Resend Growth | SAR 190–340 ($50–90) |
| Unifonic (SMS + WhatsApp at volume) | SAR 300–600 |
| Mistral AI (text — 500 restaurants) | ~$5 (~SAR 19) |
| fal.ai (image AI — 500 restaurants, ~$93/month estimate) | ~$93 (~SAR 349) |
| **Total infra + AI** | **SAR 1,330–2,130/month** |

At SAR 37,500 MRR (~SAR 450K ARR), infra is 3.5–5.7% of revenue — sustainable for a solo operator.

---

## Database Schema (Forward-Compatible for All 4 Versions)

```
organizations
  ├── users                  — staff/owners (role: owner|manager|staff|driver)
  ├── ai_credits             — image generation credit balance per org
  ├── subscriptions          — Moyasar billing metadata + plan tier
  │
  ├── menus
  │     └── categories
  │           └── menu_items
  │                 ├── name_ar, name_en, description_ar, description_en
  │                 ├── ingredients_text           (raw input → AI allergen detection)
  │                 ├── allergens[]                (AI-detected, staff-confirmed — SFDA)
  │                 ├── calories, sodium, caffeine (SFDA mandate)
  │                 ├── image_url, image_ai_generated BOOL
  │                 ├── badge TEXT                 (new|bestseller|limited|sold_out)
  │                 └── item_modifiers             (extras, V3)
  │
  ├── banners                — promotional banners displayed at top of menu
  │     ├── content_ar, content_en, image_url
  │     ├── scheduled_start, scheduled_end
  │     └── is_active BOOL
  │
  ├── whatsapp_sessions      — WhatsApp bot conversation state (30-min TTL)
  │
  ├── customers              — end customers (loyalty + orders)
  │     ├── loyalty_cards    — program enrollment per customer per org
  │     │     ├── stamp_count, points_balance, tier
  │     │     └── stamp_events
  │     ├── wallet_passes    — Apple + Google Wallet pass records (V2)
  │     │     └── wallet_devices  — APNs device tokens for Apple push (V2)
  │     └── loyalty_campaigns     — sent campaigns + analytics (V2)
  │
  ├── orders                 (V3 — stubbed in V1 with status column only)
  │     └── order_items
  │
  ├── drivers                (V4 — stubbed in V1)
  └── delivery_zones         (V4 — stubbed in V1)
```

Every table carries `organization_id UUID NOT NULL`. Supabase RLS policies enforce tenant isolation at the database layer.

---

## V1 — Digital Menu SaaS (with AI)

**Goal**: Any restaurant can sign up, build their menu with AI assistance, and share a QR-code-linked digital menu. SFDA-compliant from day one.

### Basic Features (MVP)

| Feature | Description |
|---|---|
| Restaurant onboarding | Sign-up flow: name, logo, slug, contact info, CR number |
| Menu builder | Add/edit/delete categories and items |
| **AI: Arabic → English translation** | One-click translation of name and description from Arabic input |
| **AI: Allergen detection** | Enter ingredients → AI returns SFDA allergen list |
| SFDA compliance fields | Calories, sodium, caffeine, allergens — displayed on public menu |
| Image upload | Upload photos → stored on Oracle KSA → served via Cloudflare CDN |
| QR code generation | Unique QR per restaurant + per table |
| Public menu page | `/[slug]` — bilingual RTL, no login, loads <2s |
| Basic analytics | Page views, QR scans, most-viewed items (Umami) |
| Multi-user access | Owner invites staff (owner / manager / staff roles) |
| Plan & billing | Moyasar subscription tiers |
| Admin dashboard | Manage menu, analytics, QR download |
| Privacy & consent | PDPL-compliant policy; consent banner |

### Migration Tools (V1 Advanced — Onboarding Flow)

**Goal**: A restaurant on any competing platform can migrate their full menu to this platform in under 10 minutes without manually re-entering data. This is positioned as a first-screen feature in the onboarding wizard — shown immediately after account creation.

#### Migration Sources Supported

| Source | Method | Notes |
|---|---|---|
| **Foodics** (فودكس) | CSV export importer | Foodics allows menu export; field mapping is well-defined |
| **menu.sa** | CSV / PDF importer | CSV if available; fallback to PDF extraction |
| **TableQR / Ordable** | CSV importer | Standard CSV format |
| **Any POS (generic)** | Excel / CSV importer with AI field mapping | AI suggests which column maps to name, price, category, etc. |
| **Existing PDF menu** | AI vision extraction | Upload PDF → AI reads and structures all items |
| **Photo of paper menu** | AI vision extraction | Upload phone photo(s) → AI extracts items |
| **WhatsApp photo import** | Via WhatsApp bot | Owner sends photos of menu pages → AI extracts → confirmation flow in chat |
| **Current website (URL)** | AI web crawl + extraction | Owner pastes their restaurant website URL → platform crawls homepage + menu page → extracts menu items, opening hours, social links, phone, address, and logo automatically |

#### Migration Wizard Flow (Web Dashboard)

```
Step 1 — Choose source
  ○ I'm coming from Foodics
  ○ I'm coming from menu.sa / TableQR / Ordable
  ○ I have a CSV or Excel file
  ○ I have a PDF menu
  ○ I have photos of my menu
  ○ I'll paste my restaurant's website URL (we'll crawl it and import everything)
  ○ Start from scratch

Step 2 — Upload / connect
  [drag-and-drop zone or URL input]
  Accepted: .csv, .xlsx, .pdf, .jpg, .png, .webp (up to 20 pages / 20 photos)

Step 3 — AI extraction + preview
  "Analysing your menu..." (Mistral Pixtral or fal.ai OCR for images/PDFs)
  Preview table: detected categories, items, prices, descriptions
  Confidence score per item (high / needs review)
  Inline edit before import

Step 4 — AI enrichment (optional, applies AI features to all imported items)
  ☑ Auto-translate missing English/Arabic
  ☑ Auto-detect allergens from descriptions
  ☑ Auto-write missing descriptions
  ☑ Generate AI photos for items with no image

Step 5 — Confirm & import
  "Importing 7 categories and 34 items..."
  Items with low confidence flagged for manual review post-import
  Full rollback available for 24 hours ("Undo import")
```

#### WhatsApp Migration Flow

For restaurant owners who prefer WhatsApp over the web dashboard:

```
Owner: "استيراد قائمتي" (or: "import my menu")

Bot: "أرسل صور قائمتك، صفحة واحدة في كل رسالة.
     أرسل 'انتهيت' عندما تنتهي."

Owner: [sends 4 photos of menu pages]
Owner: "انتهيت"

Bot: "جاري تحليل 4 صفحات... ✅
     اكتشفت 6 أقسام و 28 صنف.
     
     مثال:
     🍽 كبسة دجاج — 45 ريال
     🥗 سلطة فتوش — 22 ريال
     
     هل تريد مراجعة ومراجعة القائمة على الموقع؟ (نعم/لا)"

Owner: "نعم"

Bot: "تم! افتح لوحة التحكم لمراجعة 28 صنف قبل النشر:
     [رابط القائمة المستوردة]"
```

#### Technical Implementation

**PDF / Image extraction** — Mistral Pixtral (vision model, clean vendor):
```
POST https://api.mistral.ai/v1/chat/completions
model: "pixtral-large-latest"
System: "You are a menu data extractor. Given an image of a restaurant menu,
         return structured JSON: { categories: [{ name_ar, name_en, items: [
         { name_ar, name_en, description_ar, description_en, price, calories? }] }] }"
```
Cost: Pixtral Large ~$3/M input tokens (image tokens); a typical menu page = ~800 tokens → **~$0.002/page**. Full 20-page menu = ~$0.04.

**CSV / Excel import** — parse client-side with `papaparse` (CSV) and `xlsx` (Excel); display column mapping UI; AI suggests mappings via Mistral text call (what column name maps to what field):
```
Cost per import: ~$0.0001 (50 tokens to classify 10-20 column headers)
```

**Website URL crawl** — Cloudflare Worker passes the URL through **Jina AI Reader** (`r.jina.ai`), which renders the page (including JS SPAs) and returns clean Markdown. Two passes: homepage (social links, hours, phone, address, logo) then the menu sub-page if one exists. Combined markdown sent to Mistral for structured extraction. Fallback if site is bot-blocked: prompt owner to upload a screenshot or PDF instead.

**Rollback**: store original import payload in `import_jobs` table for 24 hours; one-click delete all items from that import job.

#### New Database Table

```sql
import_jobs (
  id UUID, organization_id UUID,
  source TEXT,           -- 'foodics_csv' | 'pdf' | 'image' | 'csv' | 'url' | 'whatsapp'
  raw_payload JSONB,     -- original extracted data before any edits
  status TEXT,           -- 'pending' | 'review' | 'imported' | 'rolled_back'
  item_count INT,
  confidence_avg FLOAT,  -- average AI confidence score across items
  imported_at TIMESTAMPTZ,
  expires_at TIMESTAMPTZ -- rollback window: 24h after import
)
```

#### Cost Per Migration

| Source | AI Cost | Time to Complete |
|---|---|---|
| Foodics CSV (34 items) | ~$0.0001 (column mapping only) | <30 seconds |
| PDF menu (5 pages) | ~$0.01 (Pixtral vision) | ~20 seconds |
| Photo of paper menu (8 photos) | ~$0.016 | ~30 seconds |
| WhatsApp photos (4 pages via bot) | ~$0.008 + Unifonic msg cost | ~45 seconds |
| Website URL crawl (2-pass Jina + Mistral) | ~$0.001–$0.04 | ~20 seconds |
| + AI enrichment (translate all + allergens) | ~$0.001 | +10 seconds |

**Migration is effectively free from the platform's cost perspective** — total AI cost per restaurant onboarding is under $0.02. This makes it viable to offer migration as a free feature on all tiers, including Free.

#### Competitive Positioning

No Saudi restaurant SaaS competitor offers AI-powered migration from photos or PDFs. A restaurant on Foodics or menu.sa can fully migrate in under 10 minutes without leaving WhatsApp. This dramatically lowers the switching cost and removes the #1 barrier to adoption ("I'll have to re-enter everything").

---

### Advanced Features (Post-MVP)

| Feature | Description |
|---|---|
| **Promotional banners** | Full-width announcement banners at the top of the public menu page — limited offers, sold-out notices, seasonal greetings, holiday hours; schedule start/end date; supports images and rich text |
| **Opening hours display** | Show today's hours prominently on menu page with open/closed status auto-calculated |
| **Social media links** | Instagram, TikTok, WhatsApp, Snapchat, X — shown in a tappable strip (already in current static site; must carry forward) |
| **Review / rating link** | Direct link to Google Maps or Zomato review page from the menu footer |
| **Menu search** | Customer types to filter menu items by keyword (name or ingredient) |
| **Item badge system** | "New", "Bestseller", "Chef's Choice", "Sold Out", "Limited" badges on items |
| **WhatsApp menu management** | Restaurant owner adds/edits/removes menu items by sending a WhatsApp message — no dashboard login needed |
| **AI: Description writing** | AI writes Arabic + English marketing copy from item name + ingredients |
| **AI: Food photo generation** | Generate professional food photo from item name; draft ($0.003) or HD ($0.04) |
| **AI: Background removal** | Remove phone photo background; replace with clean white/gradient |
| **AI: Photo upscaling** | 4x enhance low-resolution phone photos |
| **AI: Batch processing** | Apply translation, allergen detection, description writing to all items at once |
| Multiple menus | Day-part menus with schedule-based switching |
| Table-specific QR codes | Table-level QR codes with analytics |
| Item availability toggle | 86 items in real time |
| Custom branding | Cover photo, accent color, font |
| Custom domain | `menu.restaurant.com` via Cloudflare for SaaS |
| White-label | Remove platform branding |
| Allergen filtering | Customers filter menu by dietary requirement |
| Item scheduling | Items auto-show/hide by time of day |
| Multi-location | Multiple branches, one account |
| Export | PDF + printable version |
| SFDA audit export | Export nutrition data in SFDA format |
| Embed widget | `<iframe>` for restaurant's own site |
| Public API | Read-only menu data for POS integrations |

### V1 Pricing Model (SAR)

| Tier | SAR/Month | AI Included | Limits |
|---|---|---|---|
| Free | 0 | Translation + allergen only | 1 menu, 20 items, platform branding |
| Starter | 60 | + 20 AI image generations/month | 3 menus, 100 items, no branding |
| Pro | 150 | + 100 AI image generations/month | Unlimited menus/items, custom domain, 3 locations |
| Business | 375 | + 300 AI image generations/month | Everything + white-label, embed, API |
| AI Credit Pack | 37.50 (10 SAR/generation) | Extra 10 image generations | Available on all tiers |

---

## V2 — Loyalty (Stamp & Points with Apple/Google Wallet)

**Goal**: Restaurants run digital stamp/points programs. Customers carry their card in Apple Wallet or Google Wallet — no separate loyalty app, no login screen. Staff use a dedicated PWA to stamp cards. The entire setup is done via the restaurant's web dashboard or WhatsApp.

### Loyalty Architecture Overview

```
SETUP (restaurant):
  Web dashboard  ─OR─  WhatsApp bot
       │
       └─ Define program (stamps needed, reward, branding colors, logo)
          └─ Platform generates Pass Class (Google) + Pass Type config (Apple)

CUSTOMER EXPERIENCE:
  Customer scans QR at table
       └─ Lands on menu page → "Join Loyalty" prompt
          └─ Enters phone number (PDPL consent captured)
             └─ Receives WhatsApp message with:
                ├─ [Add to Apple Wallet] button → .pkpass download
                └─ [Add to Google Wallet] button → JWT URL

STAMPING:
  Staff opens Staff PWA (apps/staff-pwa) on their phone
       └─ Camera scans QR on customer's Wallet pass
          └─ Stamps awarded → Wallet pass updates silently (no customer action needed)
             └─ Lock screen notification: "طابع جديد! رصيدك 6/10 🎉"

REWARD:
  Stamp threshold reached → pass updates to show reward
       └─ Customer shows pass at counter
          └─ Staff taps "Redeem" in PWA → pass resets for next cycle
```

### Staff Stamping App (`apps/staff-pwa`)

A Progressive Web App installed on staff phones — no App Store, no review process.

**Features:**
- Staff log in with their role credentials (Supabase Auth)
- Camera opens to scan QR code from customer's Apple/Google Wallet pass
- Customer loyalty profile loads instantly (name, stamps, history)
- One-tap to award stamp(s) or points
- One-tap to redeem reward (validates and resets counter)
- Works offline for stamp recording; syncs when connection restored
- PIN lock after inactivity (security)
- Manager view: see all stamps awarded today per staff member

**Tech:** Next.js 15 PWA (`next-pwa`) + `@zxing/browser` for camera QR decoding + Supabase Realtime for instant sync with web dashboard.

### Apple Wallet Integration

**One-time platform setup (not per restaurant):**

| Item | Action | Cost |
|---|---|---|
| Apple Developer Program | Enroll at developer.apple.com | $99/year (platform pays once) |
| Pass Type ID | Create `pass.com.yourapp.loyalty` in Developer Portal | Free; instant |
| Signing Certificate | Generate `.p12` from Developer Portal → store in GitHub Secret | Free |
| APNs Auth Key `.p8` | Create in Developer Portal → store in GitHub Secret | Free |
| WWDR Intermediate Cert | Download from Apple | Free |

**`packages/wallet` — Apple pass generation (`passkit-generator` library):**
```typescript
// Stamp card pass structure
{
  passTypeIdentifier: "pass.com.yourapp.loyalty",
  serialNumber: customer.id,
  webServiceURL: "https://yourapp.com/api/wallet/apple",
  authenticationToken: crypto.randomBytes(16).toString('hex'),
  storeCard: {
    primaryFields: [{ key: "stamps", label: "طوابع", value: "5 / 10",
                      changeMessage: "طابع جديد! رصيدك الآن %@" }],
    secondaryFields: [{ key: "name", label: "العضو", value: customer.name }]
  },
  barcode: { format: "PKBarcodeFormatQR", message: customer.id },
  locations: [{ latitude: org.lat, longitude: org.lng,
                relevantText: "أنت بالقرب — أظهر بطاقتك!" }],
  backgroundColor: "rgb(230, 0, 64)",   // NOTE: must be rgb() format; hex silently fails
  foregroundColor: "rgb(255, 255, 255)"
}
```

**4 server endpoints required** (in `apps/web/app/api/wallet/apple/`):
- `POST /v1/devices/{deviceId}/registrations/{passTypeId}/{serialNumber}` — device registers
- `DELETE` same — device unregisters
- `GET /v1/devices/{deviceId}/registrations/{passTypeId}` — list passes needing update
- `GET /v1/passes/{passTypeId}/{serialNumber}` — serve freshly signed `.pkpass`

**Stamp update flow (customer does nothing):**
1. Staff stamps in PWA → DB updates stamp count
2. Server sends silent APNs push to `api.push.apple.com` (HTTP/2, JWT auth with `.p8` key)
3. Apple Wallet calls `GET /v1/passes/...` → server returns freshly signed `.pkpass`
4. Pass updates silently; `changeMessage` triggers lock screen notification

**Per-pass cost from Apple:** $0. Per-push cost: $0.

### Google Wallet Integration

**One-time platform setup:**

| Item | Action | Cost |
|---|---|---|
| Google Pay & Wallet Console | Register at pay.google.com/business/console | Free |
| Google Cloud project + service account | Create in Cloud Console | Free |
| Enable Google Wallet API | 1-click in Cloud Console | Free |
| Demo → Production approval | Submit Business Profile in Console | Free; ~2 business days |

**`packages/wallet` — Google pass generation (`@googleapis/walletobjects`):**

```typescript
// Per restaurant: create one Loyalty Class (template)
// Per customer: create one Loyalty Object (individual pass)

// "Add to Google Wallet" button URL:
const claims = {
  iss: serviceAccountEmail, aud: 'google', typ: 'savetowallet',
  iat: Math.floor(Date.now() / 1000),
  payload: { loyaltyObjects: [{ id: `${issuerId}.${customerId}` }] }
};
const token = jwt.sign(claims, privateKey, { algorithm: 'RS256' });
const addToWalletUrl = `https://pay.google.com/gp/v/save/${token}`;

// Add a stamp (PATCH — only updates specified fields):
await walletClient.loyaltyobject.patch({
  resourceId: `${issuerId}.${customerId}`,
  requestBody: {
    loyaltyPoints: {
      balance: { string: `${newCount} / ${goal}` },
      label: "طوابع"
    }
  }
});
// notifyPreference: "NOTIFY_ON_UPDATE" triggers lock screen notification automatically
```

**Key advantage over Apple:** No APNs infrastructure, no device token storage, no 4-endpoint web service. Just a REST PATCH call. Google handles delivery to the customer's device.

**Per-pass cost from Google:** $0. Per-update cost: $0. Push limit: 3 notifications per pass per 24 hours.

### Basic Features

| Feature | Description |
|---|---|
| Loyalty program setup | Via web dashboard or WhatsApp bot — define stamps needed, reward, branding |
| Digital stamp card | Customer receives card in Apple Wallet or Google Wallet (no app download) |
| Points program | Earn X points per SAR spent; displayed on wallet pass |
| Staff PWA stamping | Staff scan customer's wallet QR → one-tap stamp award |
| Reward redemption | Staff tap "Redeem" in PWA → pass resets; lock screen notification sent |
| Customer registration | Phone number lookup; PDPL-compliant consent captured via WhatsApp |
| Real-time pass updates | Stamps appear on customer's pass within seconds of award — no customer action |
| Location-aware notifications | Customer's phone shows loyalty card on lock screen when near the restaurant |
| WhatsApp notifications | Unifonic WhatsApp message when reward earned (in addition to wallet notification) |

### Advanced Features

| Feature | Description |
|---|---|
| **AI: Auto-create campaigns** | Restaurant owner sends "إنشاء حملة للعملاء الغائبين" or clicks a button in dashboard → AI analyzes customer data, segments the audience, writes bilingual WhatsApp message, schedules send time, and queues the campaign — owner reviews + approves before sending |
| **AI: Personalized reward suggestions** | AI analyzes order patterns to recommend which reward types (free item, discount, tier upgrade) maximize repeat visits for each restaurant's customer profile |
| **AI: Campaign copy writing** | AI generates WhatsApp message copy for any campaign type in Arabic + English |
| Tiered loyalty levels | Bronze / Silver / Gold — wallet pass updates to show tier; earn multipliers unlock |
| Birthday rewards | Auto-trigger proactive WhatsApp + wallet notification on customer birthday |
| Referral program | Customer gets stamps for referring new registered customers |
| Campaign builder | Time-limited bonus events with scheduled start/end; AI writes the copy |
| Customer segmentation | Target inactive (>30 days), top spenders, near-reward customers |
| Gamification | Progress bars on wallet pass; milestone badges via WhatsApp messages |
| Analytics dashboard | Visit frequency, CLV per customer, redemption rates, campaign ROI, pass adoption rate |
| Multi-location loyalty | Stamps/points earned at any branch of the same restaurant; centralized wallet pass |
| WhatsApp CRM | All loyalty communications via Unifonic WhatsApp; no email required |
| CSV export | Customer list with PDPL consent records; timestamps included |

### AI Auto-Campaign Feature (Detail)

**Trigger options:**
- Owner types "إنشاء حملة" in WhatsApp bot or clicks "New Campaign" in dashboard
- System auto-suggests campaign when it detects a drop in visit frequency

**AI pipeline:**
```
1. Input: campaign type (re-engagement / seasonal / milestone / custom)
2. Supabase query: relevant customer segment (e.g., 45 customers who haven't visited in 14+ days)
3. Mistral Nemo 12B: generate campaign message in Arabic + English
4. Preview: owner sees message + segment size + estimated Meta cost
5. Owner approves → Unifonic schedules WhatsApp blast
6. Post-send: analytics tracked (delivery rate, redemption rate)
```

**Example auto-generated campaign:**
```
Segment: 45 customers, last visit >21 days ago
Type: Re-engagement

AR: "نفتقدك في زلطة! 🌿 كحلى مستاء خاص لعودتك — احصل على طابع مزدوج
     في زيارتك القادمة هذا الأسبوع. العرض ينتهي الجمعة."
EN: "We miss you at Zalatah! 🌿 A special welcome-back offer —
     earn double stamps on your next visit this week. Ends Friday."

Estimated Meta cost: 45 × $0.0455 = $2.05
```

### New Database Tables (V2)

```sql
-- Apple Wallet infrastructure
wallet_passes (
  id UUID, organization_id UUID, customer_id UUID,
  platform TEXT,                     -- 'apple' | 'google'
  serial_number TEXT,                -- unique per pass
  auth_token TEXT,                   -- Apple: 16-char random; Google: not needed
  pass_type_id TEXT,                 -- Apple pass type identifier
  google_object_id TEXT,             -- Google: issuerId.customerId
  stamp_count INT DEFAULT 0,
  created_at TIMESTAMPTZ
)

-- Apple APNs device registrations (needed for push updates)
wallet_devices (
  id UUID, device_id TEXT,           -- Apple device library identifier
  push_token TEXT,                   -- APNs push token
  pass_id UUID REFERENCES wallet_passes(id),
  registered_at TIMESTAMPTZ
)

-- Campaign tracking
loyalty_campaigns (
  id UUID, organization_id UUID,
  name_ar TEXT, name_en TEXT,
  message_ar TEXT, message_en TEXT,  -- AI-generated
  segment_query JSONB,               -- customer segment definition
  scheduled_at TIMESTAMPTZ,
  sent_at TIMESTAMPTZ,
  recipient_count INT,
  ai_generated BOOL DEFAULT false,
  status TEXT                        -- 'draft' | 'scheduled' | 'sent'
)
```

### V2 Pricing Addition

| Tier | Loyalty Access |
|---|---|
| Free | Not available — upsell hook: "Preview your loyalty card" blurred |
| Starter | Stamp card only; Apple + Google Wallet; Staff PWA; up to 200 customers |
| Pro | Stamp + points; unlimited customers; tiered levels; manual campaigns |
| Business | Everything + AI auto-campaigns; segmentation; analytics; WhatsApp CRM |
| AI Campaign pack | SAR 10 per campaign (covers AI generation cost; Meta message costs passed through) |

---

## V3 — Online Ordering

**Goal**: Customers order directly through the menu page. Zero commission to aggregators.

### Basic Features

| Feature | Description |
|---|---|
| Add to cart | Items + modifiers to cart while browsing |
| Order type | Dine-in, pickup, or delivery |
| Checkout | Moyasar — Mada, Visa/MC, Apple Pay, STC Pay |
| Order confirmation | WhatsApp (Unifonic) to customer + dashboard alert |
| Order management | Accept/reject, set prep time |
| Order status updates | received → preparing → ready |
| Order history | Via loyalty wallet session |
| Basic analytics | Orders/day, revenue, popular items |
| VAT display | 15% VAT per ZATCA requirements |

### Advanced Features

| Feature | Description |
|---|---|
| KDS | Web-based Kitchen Display System — color-coded tickets |
| Scheduled orders | Order for pickup at specific time |
| Order throttling | Cap simultaneous orders |
| Reorder | One-tap reorder from history |
| Loyalty auto-award | Points/stamps on order completion |
| Discount & promo engine | Coupons, combos, spend-threshold deals |
| Table QR ordering | Scans table QR → tagged to table |
| Third-party aggregator sync | Jahez, HungerStation, Talabat orders in same dashboard |
| ZATCA e-invoicing | Phase 2 Fatoora-compliant e-invoices |
| Revenue analytics | Channel breakdown, item margins, cohort retention |
| **AI: Smart upsell suggestions** | When customer adds item to cart, AI suggests complementary items based on order history and what other customers ordered together |
| **AI: Demand forecasting** | AI analyzes historical order data to predict busy periods and help kitchen staff plan prep |

### ZATCA E-Invoicing Note

VAT-registered restaurants require Phase 2 e-invoicing (Fatoora integration). Build this or partner with a ZATCA-approved vendor. This feature is a key enterprise/chain retention driver.

### V3 Pricing Addition (SAR)

| Model | SAR/Month |
|---|---|
| Ordering module add-on | +100–200 SAR on existing plan (zero commission) |
| OR commission hybrid | Lower monthly + 0.5–1% per order |
| Payment processing | Pass-through Moyasar fees (2.2% + 1 SAR) |

---

## V4 — Delivery Management

**Goal**: Restaurants manage their own drivers, dispatch orders, and give customers live tracking.

### Basic Features

| Feature | Description |
|---|---|
| Delivery zone setup | Draw zones on Mapbox; set fee per zone |
| Driver accounts | `driver` role users |
| Manual dispatch | Assign delivery orders to drivers |
| Driver mobile view | Mobile-optimized PWA for assigned orders |
| Customer tracking page | Real-time tracking link |
| Delivery notifications | WhatsApp/SMS at milestones via Unifonic |
| Delivery fee calculation | Auto by distance or zone |
| Basic analytics | Avg. delivery time, on-time rate |

### Advanced Features

| Feature | Description |
|---|---|
| Auto-dispatch | Assign to nearest available driver |
| Route optimization | Multi-drop routing |
| Driver PWA | Navigation, status updates, messaging |
| Geofencing | Auto status on zone entry/exit |
| Driver incentives | Leaderboard, bonuses |
| Third-party fleet fallback | Aramex API (KSA-native) overflow |
| Dynamic delivery pricing | Surge pricing by demand/distance |
| Proof of delivery | Photo or signature capture |
| Live map dashboard | All drivers on Mapbox live map |
| Delivery analytics | Cost/delivery, zone profitability |
| **AI: ETA prediction** | AI estimates delivery time based on driver location, distance, and historical delivery data for that zone |
| **AI: Zone optimization** | AI analyzes delivery patterns to suggest optimal zone boundaries and fee structures |

### V4 Pricing Addition (SAR)

- Delivery module: +115–225 SAR/month
- Driver seats: Free up to 5 drivers, SAR 20/driver/month after

---

## Saudi Market & Competitive Landscape

### Market Size

- Saudi restaurant management software: **SAR 556M (2024)**, growing rapidly
- 70%+ of Saudi/Gulf restaurants have adopted QR menus (2024)
- **81% of Saudi customers prefer digital menus** (YouGov 2024)
- QSR market projected **SAR 62B by 2033** (from SAR 35B in 2024)

### Competitor Analysis

| Competitor | Category | SAR/Month | AI Features | What They Don't Have |
|---|---|---|---|---|
| **Foodics** (فودكس) | Full POS/RMS | 1,500–11,000+ | Limited | Lightweight tier; AI menu building; deep QR dine-in focus |
| **Qlub** | QR pay-at-table | Not public | None | Full menu management; loyalty; delivery |
| **TableQR** | QR menu only | ~50–200 | None | Loyalty; ordering; delivery; AI |
| **Ordable** | QR ordering | ~50–200 | None | Loyalty; delivery; multi-location; AI |

### Our Positioning

| Dimension | Our Advantage |
|---|---|
| Arabic-first | RTL, Arabic-default, AI translates to English — no bilingual setup friction |
| AI-powered | Only platform with built-in AI translation, allergen detection, description writing, and photo generation |
| SFDA-compliant | Nutrition labeling + AI allergen detection built in from Day 1 |
| PDPL-compliant | Privacy-by-design; builds trust with Saudi restaurant owners |
| All-in-one | Menu + Loyalty + Ordering + Delivery in one platform |
| Affordable | SAR 60–375/month vs Foodics SAR 1,500+ |
| No POS hardware | Software-only; lower barrier to entry |
| Clean vendor stack | No Google, no AWS Project Nimbus, no Stripe, no Vercel |
| WhatsApp-native | Unifonic WhatsApp for notifications (Saudi's #1 messaging channel) |

**Primary target**: Small-to-medium Saudi restaurants (1–3 branches) that want digital presence beyond a QR menu but aren't ready for the complexity/cost of Foodics.

**AI as differentiator**: No local competitor offers AI-assisted menu building. A restaurant owner can sign up, type their menu in Arabic, and have a professional bilingual menu with allergen labels and AI-generated food photos ready in under 30 minutes.

---

## CI/CD Pipeline with Cybersecurity Checks

A complete end-to-end pipeline for a one-person team. Total cost: **$4/month** (GitHub Pro). All security tools are free.

### Source Control

- **Platform:** GitHub (private repo, GitHub Pro at $4/month)
  - NCA ECC does not require source code to reside in KSA — code is not personal data under PDPL
  - GitHub Enterprise self-hosted would be needed only for government contracts
- **Branch strategy:**
  ```
  main        ← protected; never directly pushed to; production source of truth
  feature/*   ← all development work; PRs into main
  fix/*       ← hotfixes
  ```
- **Branch protection on `main`:** Required status checks must pass; block direct push; require linear history
- **Solo developer approval gate:** GitHub Environment (`production`) with a **10-minute wait timer** — creates an explicit abort window and satisfies NCA change-control requirements without a second reviewer
- **Signed commits:** GPG signing enforced on `main` — every commit is cryptographically attributed (NCA ECC audit attribution control)

---

### Workflow 1: `ci.yml` — Every Pull Request (target: under 5 minutes, all jobs parallel)

```yaml
on: [pull_request]

jobs:
  lint-typecheck:
    # next lint --max-warnings 0
    # tsc --noEmit (strict: true)
    # prettier --check
    # ~1 min

  unit-tests:
    # Vitest (not Jest — Next.js 15 is ESM-first; Vitest is native ESM, no config)
    # vitest run --coverage --reporter=junit
    # Fail if coverage drops below threshold
    # ~2 min

  sast:
    # Semgrep CI (free Team tier for ≤10 contributors — full Pro ruleset)
    # semgrep ci --config=auto
    # Covers: Next.js, TypeScript, React, SQL injection, SSRF, XSS, hardcoded secrets
    # Posts inline PR comments on findings
    # ~2 min

  secret-scan:
    # TruffleHog — 700+ detectors, verifies if secrets are live
    # trufflehog git file://. --since-commit HEAD~1 --fail
    # Also: Gitleaks pre-commit hook (blocks secrets locally before CI)
    # ~1 min

  iac-scan:
    # Trivy --scanners config,secret on Docker Compose + Dockerfile
    # ⚠️ SECURITY NOTE: Trivy GitHub Action tags were COMPROMISED in early 2026
    #    ALWAYS pin to full commit SHA, never a version tag:
    #    uses: aquasecurity/trivy-action@<commit-sha>  ← not @v0.x.x
    # Checkov on Docker Compose files (Docker-specific IaC policies)
    # ~1 min

  build-check:
    # next build (verify production build succeeds; no artifacts kept)
    # ~1 min

  lighthouse:
    # Lighthouse CI against Cloudflare Pages preview URL
    # Fail if performance < 80 or accessibility < 90
    # ~2 min
```

**All 6 jobs run in parallel → total under 5 minutes.**

---

### Workflow 2: `deploy.yml` — Merge to Main

```yaml
on:
  push:
    branches: [main]

jobs:
  integration-tests:
    # supabase start (local Docker) → run Vitest integration suite
    # Tests auth, RLS isolation (tenant A cannot read tenant B), migrations
    # ~3 min

  container-scan:
    # Trivy on all service images: supabase/postgres, supabase/gotrue,
    # sentry/glitchtip, ghcr.io/mikecao/umami
    # CRITICAL CVE = fail and block deploy
    # HIGH CVE = warn (does not block)
    # Pin Trivy action to commit SHA (supply chain compromise prevention)
    # ~3 min

  deploy-staging:
    needs: [integration-tests, container-scan]
    # 1. Run: supabase db push --db-url "$STAGING_DB_URL"  (migrations first)
    # 2. Deploy: wrangler pages deploy (Cloudflare Pages staging environment)
    # 3. Deploy self-hosted services: SSH to Oracle KSA staging VM
    #    → docker compose pull && docker rollout <service>  (zero-downtime)
    # ~4 min

  dast-staging:
    needs: [deploy-staging]
    # OWASP ZAP Baseline Scan (passive) against staging preview URL
    # Nuclei (targeted CVE/misconfiguration templates) against staging
    # Upload SARIF report to GitHub Security tab
    # ~5 min

  e2e-tests:
    needs: [deploy-staging]
    # Playwright E2E against staging preview URL
    # Tests: sign up → build menu → QR scan → public menu loads
    # Tests: WhatsApp bot webhook (mock Unifonic webhook)
    # Tests: Moyasar checkout (sandbox)
    # ~5 min

  deploy-production:
    needs: [dast-staging, e2e-tests]
    environment: production          # ← 10-minute wait timer configured here
    # 1. Migrations: supabase db push --db-url "$PRODUCTION_DB_URL"
    # 2. Frontend: wrangler pages deploy (Cloudflare Pages production)
    # 3. Self-hosted: SSH to Oracle KSA production VM
    #    → docker compose pull
    #    → docker rollout supabase-rest supabase-auth supabase-realtime
    #    → docker rollout umami glitchtip
    # 4. Health check: curl /api/health → expect 200 within 60s
    # 5. Smoke test: synthetic order flow
    # ~5 min total (plus 10-min gate)
```

---

### Workflow 3: `nightly.yml` — Runs at 02:00 AST (23:00 UTC) every night

```yaml
on:
  schedule:
    - cron: '0 23 * * *'

jobs:
  container-scan-full:
    # Trivy: pull latest tags of all service images → scan for ALL CVEs
    # High/Critical = open GitHub Issue automatically
    # ~10 min

  zap-full-scan:
    # OWASP ZAP Full Active Scan against staging (not production)
    # Probes for SQLi, XSS, IDOR, CSRF, broken auth
    # Uploads HTML report as GitHub Actions artifact
    # ~25 min

  dependency-audit:
    # npm audit --audit-level=moderate
    # If failures: open GitHub Issue with affected packages
    # ~2 min

  trufflehog-history:
    # TruffleHog --since-commit HEAD~500 (rolling 500-commit history scan)
    # Catches secrets accidentally committed and pushed
    # ~5 min
```

---

### Zero-Downtime Deployment for Self-Hosted Services (Oracle KSA)

Standard `docker compose up -d` causes a brief container restart gap. Use **docker-rollout** for graceful replacement:

```bash
# Install once on Oracle KSA VM:
mkdir -p ~/.docker/cli-plugins
curl https://raw.githubusercontent.com/wowu/docker-rollout/master/docker-rollout \
  -o ~/.docker/cli-plugins/docker-rollout && chmod +x ~/.docker/cli-plugins/docker-rollout

# In CI (SSH step):
docker compose pull supabase-rest
docker rollout supabase-rest   # graceful: new container starts → health check → old stops
```

**Services that support rolling restarts:** PostgREST, GoTrue (Auth), Supabase Realtime, Kong, Umami, GlitchTip.

**PostgreSQL:** Cannot be rolled live. Upgrade PostgreSQL in a maintenance window (typically < 30 seconds downtime). Acceptable for a startup; document as a known SLA exception.

---

### Database Migration Safety

```
Migration order (always):
  1. Apply backward-compatible DB migration first (supabase db push staging)
  2. Deploy new application code (Cloudflare Pages + Workers)
  3. After 100% deployment confirmed — apply any destructive migrations
```

All migrations stored in `supabase/migrations/` with timestamp prefix. Self-hosted Supabase uses direct `supabase db push --db-url` (not `supabase link` — that only works with Supabase Cloud).

---

### Secrets Management

**GitHub Actions Secrets** (sufficient for MVP):
- Encrypted at rest; never exposed in logs; injected as env vars at runtime
- Secrets: `PRODUCTION_DB_URL`, `STAGING_DB_URL`, `ORACLE_KSA_SSH_KEY`, `MISTRAL_API_KEY`, `GROQ_API_KEY`, `FALAI_API_KEY`, `UNIFONIC_API_KEY`, `MOYASAR_SECRET_KEY`, `CLOUDFLARE_API_TOKEN`, `SEMGREP_APP_TOKEN`

**Cloudflare secrets:** Set separately via Wrangler CLI (`wrangler secret put`) for Workers and Cloudflare Pages environment variables — not sourced from GitHub Secrets.

**NCA ECC control:** Use `::add-mask::` GitHub annotation to mask any dynamically generated secret values in logs. Never `echo` secrets in CI steps.

**Upgrade path (at SAR 400K ARR):** Move to **Infisical** (self-hosted on Oracle KSA, free, open source) for secret versioning, rotation, audit logs, and point-in-time recovery.

---

### Post-Deployment Monitoring

| Tool | Purpose | Cost |
|---|---|---|
| **UptimeRobot** (50 monitors, 5-min intervals) | Uptime + SSL expiry alerts | Free |
| **GlitchTip** (self-hosted) | Error tracking + crash reporting | Free (self-hosted) |
| **Umami** (self-hosted) | Real user analytics | Free (self-hosted) |
| **Cloudflare Analytics** | Edge traffic, bot traffic, DDoS | Free |
| **Supabase logs** (self-hosted) | DB query logs, auth events | Free |

Configure UptimeRobot monitors for:
- `yourdomain.com/api/health` (Next.js health endpoint)
- Supabase REST endpoint: `supabase.yourdomain.com/rest/v1/`
- Cloudflare Pages production URL
- WhatsApp webhook endpoint (Cloudflare Worker)

---

### NCA ECC Compliance Mapping for CI/CD

| NCA ECC Control | Requirement | CI/CD Implementation |
|---|---|---|
| 2-5 (App Security) | Security testing before production | Semgrep SAST + Trivy + ZAP must pass before deploy |
| 2-9 (Vulnerability Mgmt) | Continuous scanning | Dependabot (daily) + Trivy nightly + ZAP nightly |
| 2-10 (Pen Testing) | Annual test | Nightly ZAP full scan serves as continuous pen testing; annual external pen test as supplement |
| 2-11 (Audit Logs) | Log all production access | GitHub Actions run history (immutable) + signed commits + Supabase auth logs |
| Change Management | Review before production | PR process with all CI gates required; PR description = formal Change Request |
| Separation of Duties | Code review before deploy | **Compensating control (solo dev):** Automated SAST + DAST + E2E replaces peer review. Document formally as a one-page policy. GitHub's immutable audit log is the audit trail. |
| Secrets in logs | Secrets never in logs/artifacts | GitHub Secrets + `::add-mask::` + TruffleHog/Gitleaks |
| Business Continuity | Daily backups + restore testing | Oracle KSA automated block storage snapshots (daily, 7-day retention) + monthly restore drill |

---

### Total CI/CD Cost

| Tool | Monthly Cost |
|---|---|
| GitHub Pro (required for Environment protection rules on private repo) | $4.00 |
| Semgrep Team (≤10 contributors) | Free |
| Dependabot | Free |
| TruffleHog + Gitleaks | Free |
| Trivy + Checkov | Free |
| OWASP ZAP + Nuclei | Free |
| Playwright | Free |
| Vitest | Free |
| Lighthouse CI | Free |
| Cloudflare Pages (preview deploys + production) | Free |
| UptimeRobot (50 monitors) | Free |
| GitHub Container Registry (public images) | Free |
| GitHub Actions minutes (~1,860 min/month; Pro includes 3,000) | Included |
| **Total** | **$4/month** |

If nightly scans push past 3,000 minutes: move the nightly Trivy and ZAP jobs to a **self-hosted runner** on the Oracle KSA VM (free, GitHub cancelled planned charges for self-hosted runners in December 2025).

---

## Implementation Phases (Technical Execution Order)

### Phase 0 — Foundation (Before V1 Launch)

**Infrastructure & DevOps:**
1. Initialize **pnpm + Turborepo monorepo** with the 3-app / 5-package structure; push to GitHub private repo
2. Set up GitHub Pro ($4/month); configure branch protection on `main`; enable GPG signed commits
3. Create GitHub Actions workflows: `ci.yml`, `deploy.yml`, `nightly.yml` (security pipeline runs from Day 1)
4. Provision Oracle Cloud KSA instance (Always Free Arm VM); install self-hosted Supabase via Docker Compose
5. Install docker-rollout on Oracle KSA VM (zero-downtime container restarts)
6. Deploy Umami + GlitchTip on Oracle KSA VM (same instance, separate Docker Compose services)
7. Configure UptimeRobot monitors (health endpoint + Supabase REST endpoint)
8. Configure Cloudflare Pages for deployment; wildcard subdomain for `[slug].yourdomain.com`
9. Store all secrets in GitHub Actions Secrets; configure Cloudflare Worker secrets via Wrangler CLI
10. Set up GitHub Environment `production` with 10-minute wait timer

**Schema & Product:**
11. Design full forward-compatible database schema (V2–V4 stub tables, SFDA fields, AI fields, `whatsapp_sessions` table)
12. Migrate Zalatah static site as the first tenant under the new system
13. Implement multi-tenant routing: `/[slug]/menu`, `/[slug]/admin`, `/[slug]/order`
14. Set up Moyasar account; implement subscription billing
15. Integrate Unifonic for OTP verification (Saudi phone numbers)

**WhatsApp / Meta (one-time platform setup):**
16. Create Meta Business Portfolio (business.facebook.com) for the platform
17. Set up Unifonic BSP partner account; integrate Embedded Signup flow into restaurant onboarding UI
18. Pre-approve the 7 launch templates (order_confirmation, order_ready, loyalty_reward_earned, loyalty_stamp_added, welcome_first_message, promo_campaign, otp_verification)
19. Test full WABA provisioning flow end-to-end with Zalatah as the first tenant

**Compliance:**
20. Write PDPL-compliant privacy policy + data processing agreements (Mistral AI, Groq, fal.ai, Unifonic, Cloudflare, Resend)
21. Write Incident Response Plan + compensating control policy document (solo developer separation-of-duties)

### Phase 1 — V1 (Menu SaaS + AI + Migration)

22. Restaurant onboarding + Moyasar subscription checkout
23. Admin dashboard: menu builder with SFDA fields + banner management + item badges
24. **Migration wizard**: CSV/Excel importer (`papaparse` + `xlsx`) + AI column mapping (Mistral)
25. **Migration wizard**: PDF + image extractor (Mistral Pixtral vision) + confidence review UI
26. **Migration wizard**: WhatsApp photo import flow (Unifonic → bot → Pixtral → confirmation)
27. **Migration wizard**: `import_jobs` table + 24-hour rollback
28. **AI integration**: Mistral proxy in Cloudflare Worker (translation + descriptions + column mapping + vision extraction)
29. **AI integration**: Groq proxy in Cloudflare Worker (allergen detection — free tier)
30. **AI integration**: fal.ai proxy in Cloudflare Worker (image generation + background removal)
31. **WhatsApp bot**: Unifonic webhook → Cloudflare Worker (intent parsing, session state, CRUD + migration photo flow)
32. Public menu page at `/[slug]` — port existing HTML/CSS/JS to React components; add banner strip + search + item badges
33. QR code generation + download (PNG + SVG)
34. Analytics: Umami event tagging + AI usage tracking
35. AI credit system: track usage per org, enforce plan limits
36. Onboarding email sequence via Resend

### Phase 2 — V2 (Loyalty + Wallet + Staff PWA)

37. **One-time Apple setup**: enroll Apple Developer Program ($99); create Pass Type ID + Signing Certificate + APNs key; store all in GitHub Secrets
38. **One-time Google setup**: register Google Pay & Wallet Console; create service account; request production approval (~2 business days)
39. Build `packages/wallet`: Apple `.pkpass` generator (`passkit-generator`) + Google Wallet JWT/PATCH helpers (`@googleapis/walletobjects`)
40. Build `apps/staff-pwa`: Next.js 15 PWA with camera QR scanner (`@zxing/browser`), stamp interface, reward redemption
41. Activate loyalty_cards + stamp_events + wallet_passes + wallet_devices tables
42. Customer registration with PDPL consent + "Add to Wallet" flow (Apple/Google)
43. Implement 4 Apple Wallet server endpoints + APNs push on stamp award
44. Implement Google Wallet PATCH on stamp award (simpler — no device endpoints needed)
45. Campaign builder + AI copywriting (Mistral Nemo 12B) + Unifonic WhatsApp send
46. AI auto-campaign pipeline: segment query → AI copy → owner preview → schedule → send

### Phase 3 — V3 (Ordering)

47. Cart + checkout flow with Moyasar Payment Intents
48. Real-time order notifications (Supabase Realtime + Unifonic WhatsApp)
49. Order management dashboard + KDS web app
50. Loyalty auto-award on order completion
51. AI upsell suggestions (Mistral API on cart page)
52. ZATCA e-invoice generation (or partner integration)

### Phase 4 — V4 (Delivery)

53. Delivery zone map UI (Mapbox)
54. Driver PWA (Progressive Web App)
55. Dispatch dashboard + Supabase Realtime for live driver tracking
56. Aramex API integration for third-party courier overflow
57. AI ETA prediction model (Mistral or lightweight custom model)

---

## Key Architectural Principles

1. **KSA data residency by default** — all customer PII stays on Oracle Cloud KSA
2. **AI calls are server-side only** — all AI API calls go through Cloudflare Workers; API keys never exposed to browser; only business content (item names, descriptions) sent to AI — never PII
3. **RLS is the security layer** — Supabase RLS enforces tenant isolation at the DB layer
4. **PDPL consent is captured explicitly** — consent recorded with timestamp and scope; deletable
5. **SFDA fields mandatory from Day 1** — allergen detection AI populates; staff confirms
6. **Stub before you need it** — V2–V4 tables exist as stubs in V1 migrations
7. **Feature flags per plan** — gate features via `plan_features` lookup table; includes AI credit limits
8. **WhatsApp over email** — Unifonic WhatsApp is primary notification channel
9. **Moyasar is the only payment processor** — never introduce Stripe (unavailable in KSA)
10. **AI costs are monetized** — AI image credits are a revenue line, not just a cost center
11. **No Google models** — never route AI requests through Google (Gemini, PaLM, Vertex) — use Mistral (French) and Groq instead

---

## Compliance Action Checklist

### Before Launch

**Legal & Privacy:**
- [ ] Draft and publish Arabic + English Privacy Policy (PDPL-compliant)
- [ ] Implement explicit consent capture on customer registration and WhatsApp bot opt-in
- [ ] Sign Data Processing Agreements (DPA) with Resend, Unifonic, Cloudflare, Mistral AI, Groq, fal.ai
- [ ] Document all cross-border data flows on National Data Governance Platform (AI calls are business data, not PII — document accordingly)
- [ ] Write Incident Response Plan (IR plan) with 72-hour SDAIA breach notification procedure
- [ ] Write compensating control policy (automated CI/CD checks replace peer code review — solo developer)

**Security Controls:**
- [ ] Enable TLS 1.2+ on all endpoints (Cloudflare handles frontend; Supabase Kong handles API)
- [ ] Implement AES-256 encryption at rest (Oracle KSA block storage + Supabase)
- [ ] Set up centralized security logging (GlitchTip + Supabase audit logs) retained ≥12 months
- [ ] Configure MFA requirement for all admin accounts
- [ ] Configure OpenRouter to block Google/AWS-hosted model routing
- [ ] Enable GitHub Secret Scanning alerts (free on public repos; GitHub Advanced Security adds private)
- [ ] Enable Gitleaks pre-commit hook on local development machine
- [ ] Pin all GitHub Actions third-party actions to full commit SHA (not version tags — supply chain risk)

**CI/CD:**
- [ ] `ci.yml` passing: lint, typecheck, Vitest, Semgrep SAST, TruffleHog, IaC scan, build, Lighthouse all green
- [ ] `deploy.yml` passing: integration tests, container scan, staging deploy, ZAP baseline, E2E, production deploy with 10-min gate
- [ ] `nightly.yml` scheduled and firing: Trivy full, ZAP full scan, dependency audit, TruffleHog history
- [ ] UptimeRobot monitors configured for production health endpoint, Supabase, and WhatsApp webhook

**WhatsApp / Meta:**
- [ ] Meta Business Portfolio created and verified for platform
- [ ] Unifonic BSP partner account active and Embedded Signup integrated into onboarding
- [ ] All 7 launch message templates pre-approved by Meta
- [ ] End-to-end WABA provisioning tested with Zalatah as first tenant
- [ ] Human escalation path implemented in bot ("رد بـ 'إنسان' للتحدث مع الفريق")

**Wallet (V2):**
- [ ] Apple Developer Program enrolled ($99/year); Pass Type ID `pass.com.yourapp.loyalty` created
- [ ] Apple Signing Certificate (.p12) + APNs Auth Key (.p8) + WWDR cert stored in GitHub Secrets
- [ ] Google Pay & Wallet Console registered; service account JSON stored in GitHub Secrets
- [ ] Google Wallet API production approval received (~2 business days after Business Profile submitted)
- [ ] End-to-end test: customer registers → receives WhatsApp link → adds to Apple Wallet → staff scans QR in Staff PWA → stamp awarded → pass updates silently on customer phone
- [ ] Staff PWA installable on Android and iOS (manifest.json + service worker configured correctly)
- [ ] Apple Wallet `changeMessage` triggers lock screen notification on stamp award
- [ ] Google Wallet `notifyPreference: NOTIFY_ON_UPDATE` triggers lock screen notification

**Monorepo:**
- [ ] `turbo run build` completes without errors across all apps and packages
- [ ] Turborepo remote cache configured on Cloudflare R2/KV; CI hit rate >80% after first week
- [ ] Each app deploys independently via `--filter` without triggering unrelated rebuilds
- [ ] Shared types in `packages/db` catch breaking schema changes at compile time across all apps

### At SAR 400K ARR (~100–150 restaurants)
- [ ] Begin ISO 27001 certification process
- [ ] Conduct first annual penetration test
- [ ] Implement formal vendor risk assessment process (include AI vendors)

---

## Verification Checklist (Per Version)

### V1
- [ ] Migration (CSV): upload Foodics CSV → items imported with correct categories, prices, names in <30 seconds
- [ ] Migration (PDF): upload 5-page PDF → Pixtral extracts >90% of items correctly → low-confidence items flagged
- [ ] Migration (WhatsApp): send 4 menu photos to bot → items extracted → web review link returned in <60 seconds
- [ ] Migration (rollback): undo import within 24h removes all imported items cleanly with no orphaned records
- [ ] New tenant signs up → types menu in Arabic → translation + allergen detection runs → public menu live with QR code, end-to-end in <30 minutes
- [ ] RLS test: authenticated as tenant A, attempt to read tenant B's data — expect 0 rows
- [ ] WhatsApp bot: owner sends "أضف صنف" → full add-item flow completes → item live on public menu, end-to-end via WhatsApp only
- [ ] WhatsApp bot: "86 [item name]" → item hidden on public menu within 5 seconds
- [ ] WhatsApp bot: photo sent via WhatsApp → background removed → uploaded to CDN → confirmed in reply within 30 seconds
- [ ] WhatsApp session expires after 30 min of inactivity; new message restarts cleanly
- [ ] AI translation: Arabic text in → English text out in <2 seconds
- [ ] AI allergen: "دقيق، بيض، حليب، سمسم" → `[gluten, eggs, dairy, sesame]` returned correctly
- [ ] AI image generation: prompt sent → FLUX Schnell draft returned in <10 seconds → fal.ai FLUX Pro HD in <30 seconds
- [ ] Background removal: photo upload → clean white background in <15 seconds
- [ ] Moyasar checkout: subscription upgrade reflected in feature access within 60 seconds
- [ ] Public menu loads in <2s on 3G (Lighthouse score >90)
- [ ] PDPL: customer deletion request removes all PII within 30 minutes
- [ ] SFDA: calories/allergens visible on public menu; SFDA audit export works

### V2
- [ ] Stamp awarded → customer wallet updates in real time (Supabase Realtime)
- [ ] AI campaign copy: campaign type entered → WhatsApp message generated in Arabic + English in <3 seconds

### V3
- [ ] Order placed → WhatsApp notification sent → KDS ticket appears in <3 seconds
- [ ] Moyasar payment captured → loyalty points awarded → order status updated
- [ ] AI upsell: item added to cart → complementary suggestion shown within 500ms (cached AI response)

### V4
- [ ] Driver location update → customer tracking page reflects within 5 seconds
- [ ] AI ETA prediction within ±3 minutes of actual delivery time (measure after 100+ deliveries)
