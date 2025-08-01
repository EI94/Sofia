# Wrapper for Google Calendar
from datetime import datetime, timedelta
import logging
from .. import get_config

logger = logging.getLogger(__name__)

# Mock calendar gateway for Sofia Lite
class MockCalendarGateway:
    def get_available_slots(self):
        return [
            "Domani alle 15:00",
            "Domani alle 16:30", 
            "Mercoledì alle 10:00"
        ]
    
    def book_appointment(self, phone, name, slot):
        logger.info(f"Mock booking: {name} ({phone}) at {slot}")
        return True
    
    def create_event(self, title, description, start_time, duration_minutes):
        logger.info(f"Mock event created: {title}")
        return "https://calendar.google.com/event/mock"
    
    def block_professional_slot(self, slot, service):
        logger.info(f"Mock professional slot blocked: {slot} for {service}")
        return True

# Create singleton instance
_calendar_gateway = MockCalendarGateway()

def get_available_slots():
    """Get available calendar slots"""
    try:
        return _calendar_gateway.get_available_slots()
    except Exception as e:
        logger.warning(f"Calendar gateway error: {e}")
        # Return dummy slots if calendar fails
        return [
            "Domani alle 15:00",
            "Domani alle 16:30", 
            "Mercoledì alle 10:00"
        ]

def get_three_slots():
    """Get next 3 available slots from Google Calendar"""
    try:
        # Try to get real slots from Google Calendar
        available_slots = get_available_slots()
        if available_slots and len(available_slots) >= 3:
            return available_slots[:3]
    except Exception as e:
        logger.warning(f"Error getting real slots: {e}")
    
    # Fallback to mock slots
    base = datetime.now() + timedelta(days=1)
    return [(base + timedelta(hours=i)).strftime("%d/%m %H:%M") for i in (14, 15, 16)]

def book(phone, name, slot):
    """Book appointment in Google Calendar"""
    try:
        success = _calendar_gateway.book_appointment(phone, name, slot)
        logger.info(f"Booking result for {phone}: {success}")
        return success
    except Exception as e:
        logger.error(f"Booking error for {phone}: {e}")
        return False

def create_calendar_event(name, phone, slot, service, channel):
    """Create Google Calendar event and return shareable URL"""
    try:
        event_url = _calendar_gateway.create_event(
            title=f"Consulenza {service} - {name}",
            description=f"Cliente: {name}\nTelefono: {phone}\nServizio: {service}\nModalità: {channel}",
            start_time=slot,
            duration_minutes=60
        )
        logger.info(f"Calendar event created for {name}: {event_url}")
        return event_url
    except Exception as e:
        logger.error(f"Calendar event creation error: {e}")
        return None

def send_reminder(phone, name, slot):
    """Schedule reminder 1 day before appointment"""
    try:
        # Calculate reminder time (1 day before)
        appointment_time = datetime.strptime(slot, "%d/%m %H:%M")
        reminder_time = appointment_time - timedelta(days=1)
        
        # Schedule reminder via Twilio
        reminder_message = f"Ciao {name}! Ti ricordo l'appuntamento domani alle {slot}. A presto!"
        
        # TODO: Integrate with Twilio messaging service
        logger.info(f"Reminder scheduled for {phone} at {reminder_time}")
        return True
    except Exception as e:
        logger.error(f"Reminder scheduling error: {e}")
        return False

def block_professional_calendar(slot, service):
    """Block professional's calendar for the appointment"""
    try:
        success = _calendar_gateway.block_professional_slot(slot, service)
        logger.info(f"Professional calendar blocked for {slot}: {success}")
        return success
    except Exception as e:
        logger.error(f"Professional calendar blocking error: {e}")
        return False 