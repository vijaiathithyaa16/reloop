"""
Finds the nearest active collector to a citizen's pickup coordinates.

Uses the Haversine great-circle distance formula over `collector_profiles`.
This is fine at city-scale (tens/hundreds of collectors). If the collector
base grows much larger, swap this for a PostGIS query (ST_DWithin /
ST_Distance with a spatial index) so the database does the geo lookup
instead of Python.
"""
import logging
from math import radians, sin, cos, sqrt, atan2
from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.models.collector_profile import CollectorProfile

logger = logging.getLogger(__name__)

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return EARTH_RADIUS_KM * 2 * atan2(sqrt(a), sqrt(1 - a))


class CollectorMatchingService:
    @staticmethod
    def find_nearest_collector(
        db: Session, latitude: float, longitude: float
    ) -> Optional[Tuple[CollectorProfile, float]]:
        """
        Returns (CollectorProfile, distance_km) for the closest active
        collector, or None if no collector profiles are on file.

        Never raises — any lookup failure is logged and treated as "no
        collector found" so the citizen-facing conversation always
        degrades gracefully instead of breaking the pickup flow.
        """
        try:
            profiles = (
                db.query(CollectorProfile)
                .filter(CollectorProfile.active.is_(True))
                .all()
            )
        except Exception as e:
            logger.error(f"Error querying collector profiles: {e}")
            return None

        if not profiles:
            return None

        try:
            nearest = min(
                profiles,
                key=lambda p: haversine_km(latitude, longitude, p.latitude, p.longitude),
            )
            distance = haversine_km(latitude, longitude, nearest.latitude, nearest.longitude)
            return nearest, round(distance, 2)
        except Exception as e:
            logger.error(f"Error computing nearest collector: {e}")
            return None


collector_matching_service = CollectorMatchingService()
