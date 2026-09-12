"""
Seeds a few demo COLLECTOR users + their CollectorProfile (WhatsApp number
+ location) so the Telegram bot's nearest-collector WhatsApp handoff has
data to match against.

Edit SAMPLE_COLLECTORS with your real collectors' phone numbers before a
real deployment (whatsapp_number must be E.164 format), then run:

    python -m app.db.seed_collectors
"""
import uuid

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.collector_profile import CollectorProfile

# Replace with real collector data before going live.
SAMPLE_COLLECTORS = [
    {"email": "collector.central@reloop.org", "name": "GreenCycle Collectors", "whatsapp_number": "+919876500001", "area": "Chennai Central", "latitude": 13.0827, "longitude": 80.2707},
    {"email": "collector.south@reloop.org", "name": "EcoTech Recyclers", "whatsapp_number": "+919876500002", "area": "Chennai South", "latitude": 12.9716, "longitude": 80.2200},
    {"email": "collector.west@reloop.org", "name": "ReCycle Hub", "whatsapp_number": "+919876500003", "area": "Chennai West", "latitude": 13.0500, "longitude": 80.1700},
]


def seed_demo_collectors():
    db = SessionLocal()
    try:
        added = 0
        for c in SAMPLE_COLLECTORS:
            user = db.query(User).filter(User.email == c["email"]).first()
            if not user:
                user = User(
                    email=c["email"],
                    password_hash=get_password_hash(uuid.uuid4().hex),
                    role=UserRole.COLLECTOR,
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            profile = db.query(CollectorProfile).filter(CollectorProfile.user_id == user.id).first()
            if not profile:
                db.add(CollectorProfile(
                    user_id=user.id,
                    whatsapp_number=c["whatsapp_number"],
                    display_name=c["name"],
                    area=c["area"],
                    latitude=c["latitude"],
                    longitude=c["longitude"],
                    active=True,
                ))
                added += 1

        db.commit()
        print(f"Seeded {added} new collector profile(s). {len(SAMPLE_COLLECTORS) - added} already existed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_collectors()
