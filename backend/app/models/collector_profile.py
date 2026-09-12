from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class CollectorProfile(Base):
    """
    Location + WhatsApp contact details for a COLLECTOR-role user.

    Used by the Telegram gateway (and any other channel) to find the
    nearest active collector to a citizen's pickup location and hand the
    conversation off to that collector's WhatsApp number.
    """
    __tablename__ = "collector_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    # E.164 format, e.g. +919876543210 (used to build wa.me deep links)
    whatsapp_number = Column(String, nullable=False)
    display_name = Column(String, nullable=True)
    area = Column(String, nullable=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    active = Column(Boolean, default=True, nullable=False)

    user = relationship("User", backref="collector_profile")
