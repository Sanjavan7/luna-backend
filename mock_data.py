from models import User, Venue

# Mock Users - representing different types of Luna users
USERS = [
    User(
        id="user1",
        name="Alex Chen",
        latitude=40.7580,
        longitude=-73.9855,
        interests=["coffee", "art", "music", "indie"],
        preferred_price_range="moderate",
        viewing_history={"venue1": 45, "venue3": 30, "venue5": 60}
    ),
    User(
        id="user2",
        name="Sam Rivera",
        latitude=40.7589,
        longitude=-73.9851,
        interests=["coffee", "books", "quiet", "study"],
        preferred_price_range="budget",
        viewing_history={"venue1": 120, "venue2": 90}
    ),
    User(
        id="user3",
        name="Jordan Kim",
        latitude=40.7520,
        longitude=-73.9900,
        interests=["music", "cocktails", "nightlife", "dancing"],
        preferred_price_range="upscale",
        viewing_history={"venue4": 80, "venue6": 55}
    ),
    User(
        id="user4",
        name="Taylor Park",
        latitude=40.7595,
        longitude=-73.9840,
        interests=["art", "coffee", "photography", "indie"],
        preferred_price_range="moderate",
        viewing_history={"venue1": 35, "venue5": 90}
    ),
    User(
        id="user5",
        name="Morgan Lee",
        latitude=40.7560,
        longitude=-73.9870,
        interests=["food", "wine", "culture", "art"],
        preferred_price_range="upscale",
        viewing_history={"venue3": 65, "venue5": 40}
    ),
]

# Mock Venues - different types of places in NYC
VENUES = [
    Venue(
        id="venue1",
        name="Brew & Pages Cafe",
        category="cafe",
        latitude=40.7585,
        longitude=-73.9850,
        price_range="moderate",
        tags=["coffee", "books", "wifi", "quiet", "art"],
        description="Cozy cafe with art gallery and book exchange"
    ),
    Venue(
        id="venue2",
        name="Study Spot Coffee",
        category="cafe",
        latitude=40.7575,
        longitude=-73.9845,
        price_range="budget",
        tags=["coffee", "study", "wifi", "quiet"],
        description="Student-friendly cafe with long hours"
    ),
    Venue(
        id="venue3",
        name="The Velvet Room",
        category="bar",
        latitude=40.7530,
        longitude=-73.9910,
        price_range="upscale",
        tags=["cocktails", "music", "nightlife", "lounge"],
        description="Upscale cocktail lounge with live jazz"
    ),
    Venue(
        id="venue4",
        name="Electric Pulse",
        category="club",
        latitude=40.7510,
        longitude=-73.9920,
        price_range="upscale",
        tags=["dancing", "nightlife", "music", "DJ"],
        description="High-energy nightclub with top DJs"
    ),
    Venue(
        id="venue5",
        name="Indie Corner Gallery",
        category="gallery",
        latitude=40.7590,
        longitude=-73.9860,
        price_range="moderate",
        tags=["art", "indie", "photography", "events"],
        description="Independent art gallery with monthly exhibitions"
    ),
    Venue(
        id="venue6",
        name="Midnight Groove",
        category="club",
        latitude=40.7515,
        longitude=-73.9905,
        price_range="upscale",
        tags=["dancing", "music", "nightlife", "cocktails"],
        description="Trendy club with mixed music and VIP sections"
    ),
]