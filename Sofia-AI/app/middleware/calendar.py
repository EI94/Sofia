# Wrapper for Google Calendar
from ..gateways.calendar import GoogleCalendarGateway
from datetime import datetime, timedelta

# Create singleton instance
_calendar_gateway = GoogleCalendarGateway()

def get_available_slots():
    """Get available calendar slots"""
    try:
        return _calendar_gateway.get_available_slots()
    except Exception:
        # Return dummy slots if calendar fails
        return [
            "Domani alle 15:00",
            "Domani alle 16:30", 
            "Mercoledì alle 10:00"
        ]

def get_three_slots():
    # mock per ora
    base=datetime.now()+timedelta(days=1)
    return [(base+timedelta(hours=i)).strftime("%d/%m %H:%M") for i in (14,15,16)]

def book(phone,name,slot):
    # TODO: integrazione reale google
    return True 