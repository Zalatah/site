# Product Strategy

## Problem

Saudi restaurant owners spend 2–4 hours manually updating menu prices, adding items, and communicating changes across platforms. Most have no digital menu at all, or a static PDF that's immediately out of date. The SFDA's July 2025 mandate for digital allergen and nutrition labeling has created a compliance deadline most small restaurants are unprepared for.

## Value Proposition

Turn a restaurant's existing PDF, spreadsheet, photo, or website into a live bilingual, SFDA-aware QR menu in under 30 minutes. Keep it updated from WhatsApp. No hardware, no technical staff, no aggregator commission.

## Target Customer

**Primary (V1):** Small-to-medium Saudi restaurants: 1–3 branches, Arabic-first owner, managing the business from a phone. Not using a POS or using Foodics only for cashiering.

**Secondary (V2+):** Chains of 3–10 branches willing to pay for loyalty and ordering.

**Non-target:** Enterprise chains (need full ERP/POS integration), ghost kitchens (different unit economics), delivery-only brands (no dine-in QR value).

## Market Context

*All figures are assumptions unless marked as verified. Treat as directional only.*

- Saudi QSR market: SAR 35B (2024), projected SAR 62B (2033) — *source: industry reports; requires professional verification*
- 70%+ Saudi/Gulf restaurants have adopted some form of QR menu — *assumption*
- SFDA digital menu mandate effective July 1, 2025 — *verified; see SECURITY_AND_COMPLIANCE.md*
- Dominant platforms: Foodics (SAR 1,500–11,000+/month), menu.sa, TableQR, Ordable (SAR 50–200/month)

## Positioning

| Dimension | Our position |
|---|---|
| vs. Foodics | Lighter, cheaper, no hardware, AI-first. Not a POS. |
| vs. menu.sa / TableQR | SFDA compliance built-in, AI onboarding, WhatsApp management, loyalty, ordering roadmap |
| vs. aggregators (Jahez, HungerStation) | Zero commission on direct orders (V3). Restaurants own their customer data. |
| vs. doing nothing | SFDA compliance risk removal; professional bilingual menu in 30 minutes |

## Business Model

**SaaS subscription:** SAR 0 / 60 / 150 / 375 per month (see PRODUCT_ROADMAP_v4.md for tier details)

**AI image credits:** SAR 5 per generation; SAR 50 for 10-pack. Starter tier: 5 free credits/month. Image generation is a cost center converted to a revenue line.

**Payment processing (V3):** Pass-through Moyasar fees (Mada: ~1.5% + SAR 1; Visa/MC: ~2.2% + SAR 1). Platform takes no additional commission.

**WhatsApp API costs:** Passed through at cost + 10–15% platform margin to cover Unifonic markup.

## Competitive Moats (if validation confirms them)

1. AI-assisted onboarding that makes setup genuinely fast, not just claimed fast
2. SFDA compliance as table stakes, not an add-on
3. WhatsApp-native management in a market where WhatsApp is the operating system
4. No aggregator dependency — restaurants keep their margin and customer data

## Go-to-Market

**Phase -1:** Founder-led sales. Direct outreach to 15 restaurants. Offer free pilot with hands-on setup.

**V1:** Referral. Each pilot restaurant is a reference. Offer 1 month free for each referred restaurant that goes live.

**V1.3+:** Self-serve sign-up with freemium conversion. Target local food blogger / influencer partnerships to reach restaurant owners on Instagram/TikTok.

**Not in scope until V1.3:** paid advertising, outbound sales team, agency channel.
