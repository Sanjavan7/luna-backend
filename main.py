from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Venue, VenueRecommendation, CompatibilityScore, BookingRequest, BookingConfirmation
from recommendation import recommend_venues, recommend_people
from agent import BookingAgent
from mock_data import USERS, VENUES

# Initialize FastAPI app
app = FastAPI(
    title="Luna Backend API",
    description="Recommendation engine and booking agent for social venue discovery",
    version="1.0.0"
)

# Initialize booking agent
booking_agent = BookingAgent()

@app.get("/")
def root():
    """Welcome endpoint with API information"""
    return {
        "message": "🌙 Luna Backend API - Social Venue Discovery Platform",
        "version": "1.0.0",
        "description": "Intelligent Social Venue Discovery",
        "endpoints": {
            "users": "GET /users - List all users",
            "venues": "GET /venues - List all venues",
            "venue_recommendations": "GET /recommendations/venues/{user_id}",
            "people_recommendations": "GET /recommendations/people/{user_id}",
            "create_booking": "POST /bookings/create",
            "docs": "GET /docs - Interactive API documentation"
        },
        "features": [
            "Multi-factor venue recommendation algorithm",
            "User compatibility scoring",
            "Automated booking agent with external API simulation",
            "Spatial analysis and interest matching"
        ]
    }

@app.get("/users", response_model=List[User])
def get_users():
    """
    Get all users in the system.
    
    Returns user profiles including location, interests, and viewing history.
    """
    return USERS

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str):
    """Get a specific user by ID"""
    user = next((u for u in USERS if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user

@app.get("/venues", response_model=List[Venue])
def get_venues():
    """
    Get all venues in the system.
    
    Returns venue details including location, category, and tags.
    """
    return VENUES

@app.get("/venues/{venue_id}", response_model=Venue)
def get_venue(venue_id: str):
    """Get a specific venue by ID"""
    venue = next((v for v in VENUES if v.id == venue_id), None)
    if not venue:
        raise HTTPException(status_code=404, detail=f"Venue {venue_id} not found")
    return venue

@app.get("/recommendations/venues/{user_id}", response_model=List[VenueRecommendation])
def get_venue_recommendations(user_id: str, top_n: int = 5):
    """
    Get personalized venue recommendations for a user.
    
    **Algorithm Overview:**
    Multi-factor scoring system (0-100 scale) considering:
    - Distance from user location (25% weight)
    - Interest matching with venue tags (35% weight)
    - Price range compatibility (15% weight)
    - Viewing history - implicit interest (25% weight)
    
    **Social Layer:**
    For each recommended venue, identifies compatible users who are also interested.
    Compatibility is based on shared interests, proximity, and price preferences.
    
    **Parameters:**
    - user_id: The user to generate recommendations for
    - top_n: Number of recommendations to return (default: 5, max: 20)
    
    **Returns:**
    List of venue recommendations with scores, reasons, and compatible users.
    """
    if top_n > 20:
        top_n = 20
    
    user = next((u for u in USERS if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    recommendations = recommend_venues(user, VENUES, USERS, top_n)
    return recommendations

@app.get("/recommendations/people/{user_id}", response_model=List[CompatibilityScore])
def get_people_recommendations(user_id: str, top_n: int = 10):
    """
    Get compatible people recommendations for a user.
    
    **Compatibility Algorithm:**
    Weighted scoring system (0-100 scale):
    - Shared interests (40% weight)
    - Geographic proximity (30% weight)
    - Price range preferences (30% weight)
    
    **Use Case:**
    Helps users discover compatible people to meet at venues.
    Powers the "who else wants to go here?" feature.
    
    **Parameters:**
    - user_id: The user to find matches for
    - top_n: Number of recommendations to return (default: 10)
    
    **Returns:**
    List of compatible users with scores, shared interests, and distance.
    """
    user = next((u for u in USERS if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    recommendations = recommend_people(user, USERS, top_n)
    return recommendations

@app.post("/bookings/create", response_model=BookingConfirmation)
async def create_booking(request: BookingRequest):
    """
    Create an automated booking for a group at a venue.
    
    **Booking Agent Features:**
    - Generates unique confirmation codes
    - Simulates integration with external booking platforms (OpenTable, Resy, etc.)
    - Handles payment processing (via Stripe simulation)
    - Sends notifications to all participants (email, SMS, push)
    - Manages group bookings with special handling
    
    **Request Body:**
    - venue_id: The venue to book
    - user_ids: List of users in the group
    - date: Booking date (YYYY-MM-DD)
    - time: Booking time (HH:MM)
    - party_size: Number of people
    
    **Returns:**
    Booking confirmation with unique ID, confirmation code, and full details.
    
    **Production Integration:**
    In production, this would:
    1. Call external booking APIs (OpenTable, Resy, Eventbrite)
    2. Process payments via Stripe
    3. Send real notifications via Twilio/SendGrid
    4. Store in database with transaction logging
    """
    # Validate venue exists
    venue = next((v for v in VENUES if v.id == request.venue_id), None)
    if not venue:
        raise HTTPException(status_code=404, detail=f"Venue {request.venue_id} not found")
    
    # Verify all users exist
    for user_id in request.user_ids:
        if not any(u.id == user_id for u in USERS):
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    # Validate party size matches users
    if request.party_size != len(request.user_ids):
        raise HTTPException(
            status_code=400, 
            detail=f"Party size ({request.party_size}) doesn't match number of users ({len(request.user_ids)})"
        )
    
    # Create booking via agent
    confirmation = await booking_agent.create_booking(request, venue)
    return confirmation

@app.get("/health")
def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "luna-backend",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Add datetime import at the top if needed
from datetime import datetime