# Telegram Chatbot (with WhatsApp Collector Handoff)

ReLoop's citizen-facing chatbot now runs on **Telegram** instead of the
WhatsApp Cloud API. The conversation flow, AI photo verification, and pickup
creation are unchanged — only the messaging channel and one thing that's
new: **at the end of the conversation, the citizen is handed off to the
nearest active collector's WhatsApp**, so the actual pickup coordination
happens on WhatsApp without needing Meta Business verification.

## How it works

1. Citizen opens `https://t.me/YourReLoopBot` (or scans a QR code encoding
   that link) and taps **Start**.
2. `POST /api/v1/integrations/telegram/webhook` receives the update and
   hands it to `UnifiedGatewayService` (`app/services/gateway_service.py`)
   — the same stateful conversation engine used for WhatsApp, keyed by
   `telegram:<chat_id>`.
3. The bot asks for language → description → photo (AI e-waste
   verification) → GPS location → confirmation, exactly like before.
4. On confirmation, the pickup is created via `pickup_service`, then
   `CollectorMatchingService` (`app/services/collector_matching_service.py`)
   finds the nearest **active** `CollectorProfile` using the Haversine
   formula, auto-assigns the pickup to that collector, and replies with an
   inline **"Chat on WhatsApp"** button — a `wa.me` deep link pre-filled
   with the pickup ID, items, and a Google Maps link to the location.

## Setup

1. **Create the bot**: message [@BotFather](https://t.me/BotFather) on
   Telegram, run `/newbot`, and copy the token it gives you.
2. **Configure environment** (`backend/.env`):
   ```
   TELEGRAM_ENABLED=true
   TELEGRAM_BOT_TOKEN=<token from BotFather>
   ```
3. **Run the migration** to create the `collector_profiles` table:
   ```bash
   cd backend
   alembic upgrade head
   ```
4. **Give collectors a WhatsApp number + location.** Either:
   - Have each collector call `PUT /api/v1/collectors/me/profile` while
     logged in (`{"whatsapp_number": "+91...", "latitude": ..., "longitude": ...}`), or
   - For a demo, seed sample collectors:
     ```bash
     python -m app.db.seed_collectors
     ```
5. **Point Telegram at your webhook** (needs a public HTTPS URL —
   ngrok, or your real deployment):
   ```bash
   curl "https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<your-domain>/api/v1/integrations/telegram/webhook"
   ```
6. Open Telegram, message your bot, and walk through the flow. On
   confirmation you should see the nearest collector's name/distance and a
   WhatsApp button.

## Files touched

| File | Purpose |
|---|---|
| `app/models/collector_profile.py` | `CollectorProfile` model (whatsapp_number, lat/lng, active) |
| `app/services/collector_matching_service.py` | Haversine nearest-collector lookup |
| `app/services/gateway_service.py` | Confirmation step now matches + builds the `wa.me` handoff button |
| `app/services/telegram_service.py` | Renders `url` buttons (WhatsApp link) vs `callback_data` buttons |
| `app/api/endpoints/collectors.py` | `GET`/`PUT /api/v1/collectors/me/profile` |
| `alembic/versions/..._create_collector_profiles_table.py` | Migration |
| `app/db/seed_collectors.py` | Demo collector data |
| ~~`app/services/whatsapp_service.py`, `app/api/endpoints/whatsapp.py`~~ | Removed — WhatsApp is no longer a chatbot channel |

## Notes

- The nearest-collector lookup never raises — if no collector profiles
  exist yet, the citizen still gets their pickup confirmation, just
  without a WhatsApp button, and a note that the team will reach out.
- The old WhatsApp Cloud API conversational bot (`app/services/whatsapp_service.py`,
  `/api/v1/integrations/whatsapp/webhook`) has been fully removed — Telegram is
  now the only citizen-facing chatbot channel. WhatsApp is only used for the
  final `wa.me` handoff link to the nearest collector.
- At real scale, replace the Haversine scan with a PostGIS `ST_DWithin` /
  `ST_Distance` query so the database — not Python — does the geo lookup.
