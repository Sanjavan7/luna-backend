from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    interests: List[str]
    preferred_price_range: str  # "budget", "moderate", "upscale"
    viewing_history: dict = {}  # venue_id -> seconds_viewed
    
class Venue(BaseModel):
    id: str
    name: str
    category: str
    latitude: float
    longitude: float
    price_range: str
    tags: List[str]
    description: str
    
class CompatibilityScore(BaseModel):
    user_id: str
    user_name: str
    score: float
    shared_interests: List[str]
    distance_km: float
    
class VenueRecommendation(BaseModel):
    venue: Venue
    score: float
    reasons: List[str]
    interested_users: List[CompatibilityScore]
    
class BookingRequest(BaseModel):
    venue_id: str
    user_ids: List[str]
    date: str
    time: str
    party_size: int
    
class BookingConfirmation(BaseModel):
    booking_id: str
    status: str
    venue_name: str
    confirmation_code: str
    details: dict