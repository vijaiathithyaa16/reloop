from typing import Optional
from pydantic import BaseModel, Field


class CollectorProfileUpdate(BaseModel):
    whatsapp_number: str = Field(..., description="E.164 format, e.g. +919876543210")
    latitude: float
    longitude: float
    display_name: Optional[str] = None
    area: Optional[str] = None
    active: bool = True


class CollectorProfileResponse(BaseModel):
    id: int
    user_id: int
    whatsapp_number: str
    display_name: Optional[str] = None
    area: Optional[str] = None
    latitude: float
    longitude: float
    active: bool

    class Config:
        from_attributes = True
