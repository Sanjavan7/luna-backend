import numpy as np
from typing import List, Tuple
from models import User, Venue, CompatibilityScore, VenueRecommendation
import math

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers using Haversine formula"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def calculate_user_compatibility(user1: User, user2: User) -> CompatibilityScore:
    """
    Calculate compatibility score between two users.
    
    Algorithm uses weighted scoring:
    - Shared interests: 40% weight
    - Distance proximity: 30% weight  
    - Price range compatibility: 30% weight
    """
    
    # 1. Shared interests (40% weight)
    shared_interests = list(set(user1.interests) & set(user2.interests))
    interest_score = len(shared_interests) / max(len(user1.interests), len(user2.interests))
    
    # 2. Distance proximity (30% weight)
    distance = calculate_distance(user1.latitude, user1.longitude, user2.latitude, user2.longitude)
    distance_score = max(0, 1 - (distance / 5))  # Max 5km range
    
    # 3. Price range compatibility (30% weight)
    price_ranges = {"budget": 1, "moderate": 2, "upscale": 3}
    price_diff = abs(price_ranges[user1.preferred_price_range] - price_ranges[user2.preferred_price_range])
    price_score = max(0, 1 - (price_diff / 2))
    
    # Combined score (0-100 scale)
    final_score = (0.4 * interest_score + 0.3 * distance_score + 0.3 * price_score) * 100
    
    return CompatibilityScore(
        user_id=user2.id,
        user_name=user2.name,
        score=round(final_score, 2),
        shared_interests=shared_interests,
        distance_km=round(distance, 2)
    )

def recommend_venues(user: User, all_venues: List[Venue], all_users: List[User], top_n: int = 5) -> List[VenueRecommendation]:
    """
    Generate personalized venue recommendations for a user.
    
    Multi-factor scoring algorithm (0-100 scale):
    - Distance from user: 25% weight
    - Interest matching: 35% weight
    - Price range fit: 15% weight
    - Viewing history: 25% weight
    
    Also identifies compatible users interested in each venue.
    """
    
    recommendations = []
    
    for venue in all_venues:
        score = 0
        reasons = []
        
        # 1. Distance score (25% weight)
        distance = calculate_distance(user.latitude, user.longitude, venue.latitude, venue.longitude)
        distance_score = max(0, 1 - (distance / 3))  # Max 3km preferred
        score += 25 * distance_score
        if distance < 1:
            reasons.append(f"Only {distance:.1f}km away")
        
        # 2. Interest match (35% weight)
        matching_tags = set(user.interests) & set(venue.tags)
        interest_score = len(matching_tags) / len(user.interests) if user.interests else 0
        score += 35 * interest_score
        if matching_tags:
            reasons.append(f"Matches your interests: {', '.join(matching_tags)}")
        
        # 3. Price range match (15% weight)
        if venue.price_range == user.preferred_price_range:
            score += 15
            reasons.append(f"Fits your {venue.price_range} budget")
        
        # 4. Viewing history (25% weight) - implicit interest signal
        if venue.id in user.viewing_history:
            view_time = user.viewing_history[venue.id]
            view_score = min(1, view_time / 60)  # 60 seconds = max score
            score += 25 * view_score
            reasons.append(f"You spent {view_time}s viewing this")
        
        # Find compatible users interested in this venue
        interested_users = []
        for other_user in all_users:
            if other_user.id != user.id:
                # Check if they have interest in this venue
                user_venue_interest = 0
                
                # Factor 1: Viewing history
                if venue.id in other_user.viewing_history:
                    user_venue_interest += other_user.viewing_history[venue.id] / 60
                
                # Factor 2: Interest overlap with venue
                other_matching = set(other_user.interests) & set(venue.tags)
                user_venue_interest += len(other_matching) / len(venue.tags)
                
                # If user shows interest in this venue
                if user_venue_interest > 0.3:  # Interest threshold
                    compatibility = calculate_user_compatibility(user, other_user)
                    if compatibility.score > 40:  # Compatibility threshold
                        interested_users.append(compatibility)
        
        # Sort by compatibility score
        interested_users.sort(key=lambda x: x.score, reverse=True)
        
        if interested_users:
            top_matches = interested_users[:3]
            reasons.append(f"{len(top_matches)} compatible friends interested")
        
        recommendations.append(VenueRecommendation(
            venue=venue,
            score=round(score, 2),
            reasons=reasons,
            interested_users=interested_users[:5]  # Top 5 most compatible
        ))
    
    # Sort by score and return top N
    recommendations.sort(key=lambda x: x.score, reverse=True)
    return recommendations[:top_n]

def recommend_people(user: User, all_users: List[User], top_n: int = 10) -> List[CompatibilityScore]:
    """
    Find most compatible people for a user to meet.
    
    Uses the same compatibility algorithm as venue matching.
    """
    
    compatibilities = []
    for other_user in all_users:
        if other_user.id != user.id:
            compatibility = calculate_user_compatibility(user, other_user)
            compatibilities.append(compatibility)
    
    # Sort by compatibility score (highest first)
    compatibilities.sort(key=lambda x: x.score, reverse=True)
    return compatibilities[:top_n]