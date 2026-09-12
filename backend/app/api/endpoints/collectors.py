from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.deps import get_current_user
from app.models.user import User, UserRole
from app.models.collector_profile import CollectorProfile
from app.schemas.collector import CollectorProfileUpdate, CollectorProfileResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/me/profile", response_model=CollectorProfileResponse)
def upsert_my_collector_profile(
    payload: CollectorProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lets a logged-in COLLECTOR set/update their WhatsApp contact number and
    live location. This is what the Telegram (and any other) chatbot uses
    to find the nearest active collector and hand a citizen off to them
    on WhatsApp at the end of a pickup request.
    """
    if current_user.role != UserRole.COLLECTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only collectors have a collector profile")

    if not (-90 <= payload.latitude <= 90) or not (-180 <= payload.longitude <= 180):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid GPS coordinates")

    profile = db.query(CollectorProfile).filter(CollectorProfile.user_id == current_user.id).first()
    if profile:
        profile.whatsapp_number = payload.whatsapp_number
        profile.latitude = payload.latitude
        profile.longitude = payload.longitude
        profile.display_name = payload.display_name
        profile.area = payload.area
        profile.active = payload.active
    else:
        profile = CollectorProfile(
            user_id=current_user.id,
            whatsapp_number=payload.whatsapp_number,
            latitude=payload.latitude,
            longitude=payload.longitude,
            display_name=payload.display_name,
            area=payload.area,
            active=payload.active,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile


@router.get("/me/profile", response_model=CollectorProfileResponse)
def get_my_collector_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.COLLECTOR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only collectors have a collector profile")

    profile = db.query(CollectorProfile).filter(CollectorProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No collector profile set yet")
    return profile
