# Vendor Register

All vendors used by or planned for this platform. Claims marked by status:
- **Verified** — checked against public primary source, date recorded
- **Assumption** — believed to be true, not independently confirmed
- **Requires professional review** — legal, regulatory, or financial claim needing expert verification

Review schedule: quarterly for pricing; annually for compliance and Israeli risk assessment.

| Field | Meaning |
|---|---|
| Status | Current phase this vendor is used in |
| Israeli risk | Based on public information as of review date; not a definitive legal finding |
| Last reviewed | Date of last verification |
| Next review | Scheduled next check |

---

## Infrastructure

### Supabase
| Field | Value |
|---|---|
| Role | Database, Auth, Storage, Realtime |
| Phase | V0+ |
| Hosting | Cloud (EU) for V1; self-hosted Oracle KSA from V2 (PDPL trigger) |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Pricing | Free tier: 500MB DB, 1GB storage, 2 projects. Pro: $25/month — *Verified: supabase.com/pricing, 2026-06* |
| PDPL note | EU region (not KSA); acceptable for pre-revenue pilot; migration required at enterprise/PDPL trigger |
| Next review | 2026-09 |

### Cloudflare (Pages + Workers + CDN)
| Field | Value |
|---|---|
| Role | Frontend hosting, CDN, WhatsApp webhook Worker (V1.2+), edge caching |
| Phase | V0+ |
| Israeli risk | R&D center in Israel confirmed — *Verified: public reporting; accepted risk* |
| Decision | Accepted for CDN, Pages, and application Workers. No PII processed at edge. |
| Pricing | Pages: free. Workers: 100K req/day free; $5/month for 10M req — *Verified: cloudflare.com/plans, 2026-06* |
| Next review | 2026-09 |

### Oracle Cloud KSA
| Field | Value |
|---|---|
| Role | Self-hosted Supabase VM (V2+ when PDPL trigger fires) |
| Phase | V2+ |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Critical caveat | Always Free capacity is not guaranteed. Oracle has reclaimed Always Free resources with limited notice. Treat as best-effort, not SLA. Have a paid fallback ready. |
| Paid fallback | Oracle Cloud paid ARM VM (~$30-60/month) or Hetzner Cloud AX41 in Riyadh (if available) |
| Next review | 2026-09 |

### GitHub (Pro)
| Field | Value |
|---|---|
| Role | Source control, CI/CD, GitHub Actions, secret storage |
| Phase | V0+ |
| Israeli risk | None found — *Assumption* |
| Pricing | $4/month (Pro, required for Environment protection rules on private repos) — *Verified: github.com/pricing, 2026-06* |
| Next review | 2026-09 |

---

## AI Services

### Mistral AI
| Field | Value |
|---|---|
| Role | Primary text AI: translation, allergen detection fallback, descriptions, CSV mapping, extraction |
| Phase | V1+ |
| Israeli risk | None found. French company, Paris HQ — *Assumption; last reviewed 2026-06* |
| Pricing | Ministral 3B: $0.04/M input + $0.10/M output — *Assumption: verify at api.mistral.ai/pricing before launch* |
| Next review | 2026-09 |

### Groq
| Field | Value |
|---|---|
| Role | Allergen detection (free tier); falls back to Mistral on rate limit |
| Phase | V1+ |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Pricing | Free tier: 14,400 requests/day for Llama 3.1 8B — *Assumption: verify at console.groq.com before launch; free tiers change without notice* |
| Critical caveat | Never hard-depend on a free tier in production. Fallback to Mistral is mandatory. |
| Next review | 2026-09 |

### fal.ai
| Field | Value |
|---|---|
| Role | Image generation (FLUX Schnell/Pro), background removal (Bria RMBG), upscaling (Real-ESRGAN) — added in V1.3 |
| Phase | V1.3+ |
| Israeli risk | None found. US startup, YC-backed — *Assumption; last reviewed 2026-06* |
| Pricing | FLUX Schnell: ~$0.003/image; FLUX Pro v1.1: ~$0.040/image; Bria RMBG: ~$0.018/image — *Assumption: verify at fal.ai before launch* |
| Next review | 2026-09 |

---

## Communications

### Unifonic
| Field | Value |
|---|---|
| Role | WhatsApp Business API (BSP), OTP/SMS |
| Phase | V1 (SMS OTP); V1.2 (WhatsApp bot) |
| Israeli risk | None found. Saudi-founded CPaaS — *Assumption; last reviewed 2026-06* |
| Pricing | WhatsApp: Meta rates + 10–30% Unifonic markup. KSA rates: Service messages free; Utility $0.0107/msg; Marketing $0.0455/msg — *Assumption: confirm with Unifonic account team before V1.2* |
| Meta policy | One WABA per restaurant is mandatory. Shared number across tenants is prohibited by Meta. |
| Verified | Meta Business Platform policies, 2026-06 |
| Next review | 2026-09 |

### Resend
| Field | Value |
|---|---|
| Role | Transactional email (verify, password reset, onboarding) |
| Phase | V1+ |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Pricing | Free: 3,000 emails/day — *Verified: resend.com/pricing, 2026-06* |
| Next review | 2026-09 |

---

## Payment Processing

### Moyasar
| Field | Value |
|---|---|
| Role | Primary payment gateway: SaaS subscription billing (V1.3), customer order checkout (V3) |
| Phase | V1.3+ |
| HQ | Riyadh, KSA |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| SAMA licensed | Yes — *Verified: sama.gov.sa licensed entities list, requires date confirmation* |
| Pricing | Mada: ~1.5% + SAR 1 per transaction; Visa/MC: ~2.2% + SAR 1 — *Assumption: verify with Moyasar account team; pricing varies by volume* |
| Methods | Mada, Visa/MC, Apple Pay, STC Pay |
| Recurring billing | Supported |
| Next review | 2026-09 |

### MyFatoorah
| Field | Value |
|---|---|
| Role | GCC expansion gateway (Kuwait, UAE, Bahrain, Qatar) — not used until GCC expansion |
| Phase | Post-V3 GCC expansion |
| HQ | Kuwait |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Pricing | 2.0–2.75% — *Assumption: no public pricing; requires direct contact* |
| Note | No abstraction layer built until this gateway is actually being integrated |
| Next review | 2026-12 |

### Tamara
| Field | Value |
|---|---|
| Role | BNPL for orders ≥ SAR 300 (catering, large group, corporate) — V3 advanced |
| Phase | V3 advanced |
| HQ | Riyadh, KSA |
| Israeli risk | None found. PIF-backed (Saudi Public Investment Fund) — *Verified: public reporting 2025-06* |
| SAMA licensed | Full consumer finance license, March 2025 — *Verified: sama.gov.sa, 2025-03* |
| Pricing | 4–7% merchant fee — *Assumption: varies by merchant category and volume; requires contract* |
| Minimum order | ~SAR 300 — *Assumption: verify with Tamara before integration* |
| Note | Not suitable for typical food orders (SAR 50–150). Not suitable for recurring SaaS billing. |
| Next review | 2026-12 |

### Tabby
| Field | Value |
|---|---|
| Role | BNPL alternative (UAE-dominant); consider for GCC expansion if Tamara not available there |
| Phase | V3 advanced / GCC |
| HQ | Dubai, UAE |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| SAMA licensed | Yes — *Assumption; requires verification* |
| Pricing | 4–8% merchant fee — *Assumption* |
| Next review | 2026-12 |

---

## Wallet & Maps

### Apple PassKit / Wallet
| Field | Value |
|---|---|
| Role | iOS loyalty card passes (V2) |
| Phase | V2+ |
| Israeli risk | None found — *Assumption* |
| Cost | $99/year Apple Developer Program (platform pays once, not per restaurant) |
| Note | rgb() color format mandatory — hex silently fails in PassKit |
| Next review | 2026-12 |

### Google Wallet API
| Field | Value |
|---|---|
| Role | Android loyalty card passes (V2) |
| Phase | V2+ |
| Israeli risk | Google Cloud is a Project Nimbus contractor — *Verified: public reporting*. **Accepted risk** with documented rationale: pass objects are device-local display; no customer PII is processed server-side by Google; no viable Android wallet alternative exists |
| Cost | Free |
| Next review | 2026-12 |

### Mapbox
| Field | Value |
|---|---|
| Role | Delivery zone drawing and driver tracking (V4) |
| Phase | V4+ |
| Israeli risk | None found — *Assumption; last reviewed 2026-06* |
| Pricing | 50,000 tile loads/month free — *Assumption: verify at mapbox.com/pricing before V4* |
| Next review | 2026-12 |

---

## Monitoring & Observability

| Vendor | Role | Phase | Israeli risk | Cost |
|---|---|---|---|---|
| UptimeRobot | Uptime monitoring (50 monitors) | V0+ | None found | Free — *Verified 2026-06* |
| Sentry | Error monitoring (pre-VM) | V0 | None found | Free tier — *Assumption* |
| GlitchTip | Error monitoring (self-hosted, post-VM) | V2+ | None found (open source) | Free self-hosted |
| Umami | Web analytics (self-hosted) | V2+ | None found (MIT open source) | Free self-hosted |
