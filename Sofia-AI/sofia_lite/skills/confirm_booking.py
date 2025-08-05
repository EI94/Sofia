from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from ..middleware.calendar import book, create_calendar_event, send_reminder
from sofia_lite.metrics import bookings_confirmed
import re

def run(ctx, text):
    """Complete booking process with Google Calendar integration"""
    
    # Extract slot choice from text (1, 2, 3 or slot description)
    selected_slot = extract_slot_choice(text, ctx.slots.get("candidates", []))
    
    if not selected_slot:
        sys = build_intent_specific_prompt(ctx, "CONFIRM")
        user = "Il cliente non ha specificato chiaramente lo slot orario. Chiedi gentilmente di scegliere tra le opzioni disponibili."
        return chat(sys, user)
    
    # Book the appointment
    booking_success = book(ctx.phone, ctx.name, selected_slot)
    
    if not booking_success:
        sys = build_intent_specific_prompt(ctx, "CONFIRM")
        user = "La prenotazione non è riuscita. Chiedi gentilmente di riprovare o di contattare direttamente l'ufficio."
        return chat(sys, user)
    
    # Create Google Calendar event
    try:
        event_url = create_calendar_event(
            ctx.name,
            ctx.phone,
            selected_slot,
            ctx.slots.get("service", "consulenza"),
            ctx.slots.get("channel", "online")
        )
        
        # Schedule reminder (1 day before)
        send_reminder(ctx.phone, ctx.name, selected_slot)
        
        # Update context
        ctx.state = "CONFIRMED"
        ctx.slots["booking_confirmed"] = True
        ctx.slots["calendar_event_url"] = event_url
        
        # Increment bookings confirmed metric
        bookings_confirmed.inc()
        
        sys = build_intent_specific_prompt(ctx, "CONFIRM")
        user = f"La prenotazione è stata confermata per {ctx.name} alle {selected_slot}. Ringrazia il cliente e conferma i dettagli."
        return chat(sys, user)
        
    except Exception as e:
        # Booking succeeded but calendar failed
        ctx.state = "CONFIRMED"
        sys = build_intent_specific_prompt(ctx, "CONFIRM")
        user = f"La prenotazione è stata confermata per {ctx.name} alle {selected_slot}, ma c'è stato un problema con il calendario. Ringrazia comunque il cliente."
        return chat(sys, user)

def extract_slot_choice(text: str, candidates: list) -> str:
    """Extract slot choice from user text"""
    text_lower = text.lower()
    
    # Check for number choice (1, 2, 3)
    for i, candidate in enumerate(candidates, 1):
        if str(i) in text_lower:
            return candidate
    
    # Check for ordinal words (primo, secondo, terzo)
    ordinal_map = {"primo": 0, "secondo": 1, "terzo": 2}
    for ordinal, index in ordinal_map.items():
        if ordinal in text_lower and index < len(candidates):
            return candidates[index]
    
    # Check for partial match in slot description
    for candidate in candidates:
        if any(word in text_lower for word in candidate.lower().split()):
            return candidate
    
    return None 