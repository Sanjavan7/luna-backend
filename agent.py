from models import BookingRequest, BookingConfirmation, Venue
from typing import List
import random
import string
from datetime import datetime

class BookingAgent:
    """
    Automated booking agent that handles reservations and purchases.
    
    In a production system, this would integrate with:
    - OpenTable API for restaurant reservations
    - Resy API for upscale dining
    - Eventbrite API for event tickets
    - Stripe API for payment processing
    
    Currently simulates these integrations with mock responses.
    """
    
    def __init__(self):
        self.booking_counter = 1000
    
    def generate_confirmation_code(self) -> str:
        """Generate a random confirmation code (8 characters)"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    async def create_booking(self, request: BookingRequest, venue: Venue) -> BookingConfirmation:
        """
        Create a booking for a group at a venue.
        
        Process:
        1. Generate unique booking ID
        2. Create confirmation code
        3. Simulate API calls to external booking services
        4. Process payment (simulated)
        5. Send notifications to all users
        6. Return confirmation details
        """
        
        self.booking_counter += 1
        booking_id = f"LUNA-{self.booking_counter}"
        confirmation_code = self.generate_confirmation_code()
        
        # Simulate API call delay and processing
        # In production: await external_booking_api.reserve(...)
        # Examples:
        # - await opentable_api.create_reservation(venue_id, date, time, party_size)
        # - await stripe_api.create_payment_intent(amount, users)
        # - await twilio_api.send_sms(user_phones, confirmation_details)
        
        booking_details = {
            "booking_id": booking_id,
            "venue_id": request.venue_id,
            "venue_name": venue.name,
            "venue_category": venue.category,
            "venue_address": f"{venue.latitude}, {venue.longitude}",
            "date": request.date,
            "time": request.time,
            "party_size": request.party_size,
            "user_ids": request.user_ids,
            "confirmation_code": confirmation_code,
            "status": "confirmed",
            "booked_at": datetime.now().isoformat(),
            "estimated_wait": "0 minutes",
            "special_requests": "Luna group booking - social meetup",
            
            # Simulated external integrations
            "external_booking_systems": {
                "opentable_id": f"OT-{random.randint(100000, 999999)}",
                "resy_id": f"RESY-{random.randint(100000, 999999)}",
                "payment_intent_id": f"pi_{self.generate_confirmation_code().lower()}",
                "payment_status": "succeeded"
            },
            
            # Simulated notifications sent
            "notifications_sent": {
                "email": True,
                "push_notification": True,
                "sms": True,
                "in_app": True
            },
            
            # Additional details
            "cancellation_policy": "Free cancellation up to 2 hours before",
            "estimated_cost_per_person": self._estimate_cost(venue.price_range),
            "group_discount_applied": len(request.user_ids) >= 4
        }
        
        return BookingConfirmation(
            booking_id=booking_id,
            status="confirmed",
            venue_name=venue.name,
            confirmation_code=confirmation_code,
            details=booking_details
        )
    
    def _estimate_cost(self, price_range: str) -> str:
        """Estimate cost per person based on price range"""
        estimates = {
            "budget": "$10-20",
            "moderate": "$25-50",
            "upscale": "$60-150"
        }
        return estimates.get(price_range, "$30-60")
    
    async def cancel_booking(self, booking_id: str) -> dict:
        """
        Cancel an existing booking.
        
        In production, would:
        - Call external APIs to cancel reservation
        - Process refund via payment processor
        - Notify all participants
        """
        return {
            "booking_id": booking_id,
            "status": "cancelled",
            "refund_status": "processed",
            "refund_amount": "Full refund issued",
            "cancelled_at": datetime.now().isoformat(),
            "cancellation_reason": "User requested",
            "notifications_sent": True
        }
    
    async def modify_booking(self, booking_id: str, modifications: dict) -> dict:
        """
        Modify an existing booking (time, party size, etc.)
        
        In production, would update via external APIs.
        """
        return {
            "booking_id": booking_id,
            "status": "modified",
            "changes": modifications,
            "modified_at": datetime.now().isoformat(),
            "new_confirmation_code": self.generate_confirmation_code(),
            "notifications_sent": True
        }
    
    async def get_booking_status(self, booking_id: str) -> dict:
        """Check status of a booking"""
        return {
            "booking_id": booking_id,
            "status": "confirmed",
            "checked_at": datetime.now().isoformat()
        }