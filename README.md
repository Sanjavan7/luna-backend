# luna-backend
# Luna Backend - AI-Powered Social Venue Discovery

> **Track 2: Backend Development**  
> Recommendation Engine & Automated Booking Agent

## Overview

This backend system powers Luna's social venue discovery platform through intelligent recommendations and automated booking agents. The system helps users discover venues and compatible people to meet, then seamlessly books reservations once users agree to attend.

## Architecture

### System Design
```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Server                         │
│                    (main.py - REST API)                     │
└───────────────┬─────────────────────┬───────────────────────┘
                │                     │
    ┌───────────▼──────────┐  ┌───────▼────────────────┐
    │  Recommendation      │  │   Booking Agent        │
    │  Engine              │  │   (agent.py)           │
    │  (recommendation.py) │  │                        │
    └───────────┬──────────┘  └───────┬────────────────┘
                │                     │
    ┌───────────▼──────────┐  ┌───────▼────────────────┐
    │  Multi-Factor        │  │  Automated             │
    │  Scoring Algorithm   │  │  Reservations          │
    │  - Distance (25%)    │  │  - OpenTable (mock)    │
    │  - Interests (35%)   │  │  - Resy (mock)         │
    │  - Price (15%)       │  │  - Stripe (mock)       │
    │  - History (25%)     │  │  - Notifications       │
    └──────────────────────┘  └────────────────────────┘
                │
    ┌───────────▼──────────┐
    │   Data Models        │
    │   (models.py)        │
    │   - User             │
    │   - Venue            │
    │   - Compatibility    │
    │   - Booking          │
    └──────────────────────┘
```

## Features Implemented

### 1. Venue Recommendation Engine

**Multi-factor scoring algorithm** (0-100 scale):

| Factor | Weight | Description |
|--------|--------|-------------|
| Distance | 25% | Haversine formula, prefers venues <3km |
| Interest Match | 35% | Tag overlap with user interests |
| Price Range | 15% | Exact match bonus for budget alignment |
| Viewing History | 25% | Implicit interest signal (time spent) |

**Social Layer**: For each venue, identifies compatible users who are also interested based on:
- Shared interests (40% weight)
- Geographic proximity (30% weight)
- Price preference alignment (30% weight)

**API Endpoint**: `GET /recommendations/venues/{user_id}`

**Example Response**:
```json
{
  "venue": {
    "name": "Indie Corner Gallery",
    "score": 81.51
  },
  "reasons": [
    "Only 0.1km away",
    "Matches your interests: art, indie",
    "You spent 60s viewing this"
  ],
  "interested_users": [
    {
      "user_name": "Taylor Park",
      "score": 88.74,
      "shared_interests": ["coffee", "art", "indie"]
    }
  ]
}
```

### 2. User Compatibility Scoring

**Weighted compatibility algorithm** (0-100 scale):

- **Shared Interests** (40%): Jaccard similarity of interest sets
- **Proximity** (30%): Distance-based scoring (<5km preferred)
- **Price Preferences** (30%): Budget alignment scoring

**API Endpoint**: `GET /recommendations/people/{user_id}`

### 3. Automated Booking Agent

**Capabilities**:
- Generates unique confirmation codes
- Simulates external API integration (OpenTable, Resy, Eventbrite)
- Mock payment processing (Stripe)
- Notification orchestration (email, SMS, push)
- Group booking handling with special features

**Agent Workflow**:
```
User Agreement → Booking Request → Agent Processing → External APIs (mock)
     ↓              ↓                    ↓                    ↓
  Venue ID    Validation       Generate IDs         Confirmation
  Users       Check Users      Payment Intent       Notifications
  Date/Time   Check Venue      Reservation IDs      Return Details
```

**API Endpoint**: `POST /bookings/create`

**Example Booking**:
```json
{
  "venue_id": "venue1",
  "user_ids": ["user1", "user2"],
  "date": "2025-11-25",
  "time": "19:00",
  "party_size": 2
}
```

## Tech Stack

- **Framework**: FastAPI (Python 3.13)
- **Algorithm Libraries**: NumPy, scikit-learn
- **Data Validation**: Pydantic
- **Server**: Uvicorn (ASGI)
- **API Documentation**: OpenAPI 3.1 (auto-generated)

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/luna-backend.git
cd luna-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Server
```bash
python -m uvicorn main:app --reload
```

Server runs at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/docs**

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API welcome and info |
| `/users` | GET | List all users |
| `/venues` | GET | List all venues |
| `/recommendations/venues/{user_id}` | GET | Get venue recommendations |
| `/recommendations/people/{user_id}` | GET | Get people recommendations |
| `/bookings/create` | POST | Create automated booking |
| `/health` | GET | Health check |

## Testing the API

### Using Interactive Docs (Recommended)

1. Open http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Example Test Cases

**Test 1: Get venue recommendations for user1**
```bash
curl http://localhost:8000/recommendations/venues/user1?top_n=5
```

**Test 2: Create a booking**
```bash
curl -X POST http://localhost:8000/bookings/create \
  -H "Content-Type: application/json" \
  -d '{
    "venue_id": "venue1",
    "user_ids": ["user1", "user2"],
    "date": "2025-11-25",
    "time": "19:00",
    "party_size": 2
  }'
```

## Design Decisions

### Why Multi-Factor Scoring Over ML Models?

**Chosen Approach**: Weighted scoring with transparent factors

**Reasoning**:
- **Explainable**: Each recommendation comes with clear reasons
- **Tunable**: Weights can be adjusted based on user feedback
- **Fast**: No training required, instant results
- **Debuggable**: Easy to trace why a venue was recommended
- **Scalable**: O(n) complexity for n venues

**Alternative Considered**: Deep learning embeddings
- Requires large training dataset
- Black box recommendations
- Higher computational cost
- Harder to debug

### Why Mock External APIs?

**Purpose**: Demonstrates production-ready architecture

- Shows understanding of integration patterns
- Focuses on core algorithm development
- Allows rapid prototyping without API keys
- Production-ready structure for real integrations

### Data Model Design

**Pydantic Models**:
- Type safety and validation
- Auto-generated API documentation
- Easy serialization/deserialization
- Clear contracts for frontend integration

## Production Roadmap

### With More Time, I Would Add:

**1. Real Machine Learning**
- User embedding models (Word2Vec-style for interests)
- Collaborative filtering for venue preferences
- Time-series analysis for trending venues
- A/B testing framework for algorithm improvements

**2. Real Integrations**
- OpenTable API for restaurant reservations
- Resy API for upscale dining
- Eventbrite API for event tickets
- Stripe API for payment processing
- Twilio for SMS notifications
- SendGrid for email

**3. Data Layer**
- PostgreSQL database with proper schema
- Redis caching for hot recommendations
- Elasticsearch for venue search
- Real-time location updates via WebSockets

**4. Advanced Features**
- Group preference aggregation (find venues multiple users like)
- Time-based availability checking
- Dynamic pricing awareness
- Social graph analysis (friends-of-friends)
- Historical attendance patterns
- Weather-aware recommendations

**5. Infrastructure**
- Docker containerization
- Kubernetes deployment
- CI/CD pipeline
- Monitoring and logging (Datadog, Sentry)
- Load balancing
- Rate limiting

## Use of AI Tools

- **Claude AI**: Architecture consultation, algorithm design review, code structure guidance
- **No automated code generation**: All core logic written and understood from scratch
- **Learning focused**: Used AI as a technical advisor, not a code writer

## Algorithm Performance

**Tested with**:
- 5 mock users
- 6 mock venues
- Various interest combinations

**Results**:
- Average response time: <50ms
- Accurate compatibility scoring
- Relevant venue recommendations
- Proper social layer matching

## Notes

### Assumptions Made:
- Users have fixed locations (in production, would use real-time location)
- Viewing history is pre-populated (in production, tracked in real-time)
- All venues are in NYC area (simplified for demo)

### Edge Cases Handled:
- User not found → 404 error
- Venue not found → 404 error
- Party size mismatch → 400 error
- No compatible users → Returns empty list
- No matching venues → Returns all venues sorted by distance

## Author

**Sanjavan**  
Luna Backend Technical Interview - Track 2 (Backend)
Submission Date: November 23, 2025

## Submission

- **Demo Video**: [YouTube link - ]
---

Built for Luna Social!