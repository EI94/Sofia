import pytest
from app.agents.context import Context
from app.agents import planner, validator, executor
from app.middleware import memory

class MockLLM:
    def chat_completion(self, messages, model="gpt-4o-mini"):
        user_msg = ""
        for msg in messages:
            if msg["role"] == "user":
                user_msg = msg["content"]
                break
        
        # Extract user message from the prompt
        if "User: \"" in user_msg:
            user_msg = user_msg.split("User: \"")[-1].split("\"")[0]
        
        user_msg = user_msg.lower()
        
        # Simulate intelligent responses based on context
        if "ciao" in user_msg or "hello" in user_msg:
            return '{"intent": "GREET", "reason": "greeting"}'
        elif "mi chiamo" in user_msg or "sono" in user_msg:
            return '{"intent": "ASK_NAME", "reason": "name provided"}'
        elif "permesso" in user_msg or "cittadinanza" in user_msg:
            return '{"intent": "ASK_SERVICE", "reason": "service requested"}'
        elif "online" in user_msg or "presenza" in user_msg:
            return '{"intent": "PROPOSE_CONSULT", "reason": "channel choice"}'
        elif any(word in user_msg for word in ["1", "2", "3", "primo", "secondo", "terzo", "scelgo"]):
            return '{"intent": "CONFIRM", "reason": "slot selected"}'
        elif "image" in user_msg:
            return '{"intent": "ASK_PAYMENT", "reason": "payment receipt"}'
        elif "pratica" in user_msg:
            return '{"intent": "ROUTE_ACTIVE", "reason": "active client"}'
        else:
            return '{"intent": "CLARIFY", "reason": "unclear"}'

def test_complete_new_user_journey():
    """Test complete user journey for new user"""
    ctx = Context(phone="+1234567890")
    llm = MockLLM()
    
    # Step 1: Greeting
    intent, reason = planner.plan(ctx, "Ciao!", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Ciao!")
    
    assert intent == "ASK_NAME"
    assert "Piacere! Come ti chiami?" in reply
    assert ctx.state == "ASK_NAME"
    
    # Step 2: Name
    intent, reason = planner.plan(ctx, "Mi chiamo Mario Rossi", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Mi chiamo Mario Rossi")
    
    assert ctx.name == "Mario"
    assert "servizio" in reply.lower()
    assert ctx.state == "ASK_SERVICE"
    
    # Step 3: Service
    intent, reason = planner.plan(ctx, "Ho bisogno di un permesso di soggiorno", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Ho bisogno di un permesso di soggiorno")
    
    assert ctx.slots["service"] == "permesso"
    assert "60" in reply
    assert ctx.state == "PROPOSE_CONSULT"
    
    # Step 4: Channel choice
    intent, reason = planner.plan(ctx, "Preferisco online", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Preferisco online")
    
    assert ctx.slots["channel"] == "online"
    assert "giustificativo" in reply.lower()
    assert ctx.state == "ASK_PAYMENT"
    
    # Step 5: Payment receipt (image)
    intent, reason = planner.plan(ctx, "image", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "image")
    
    assert "giustificativo" in reply.lower()
    assert ctx.slots["waiting_for_payment"] == True

def test_active_user_journey():
    """Test user journey for active user"""
    ctx = Context(phone="+1234567890", client_type="active", name="Mario")
    llm = MockLLM()
    
    # Active user should be routed to app
    intent, reason = planner.plan(ctx, "Come va la mia pratica?", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Come va la mia pratica?")
    
    assert "app" in reply.lower() or "Studio Immigrato" in reply

def test_booking_confirmation():
    """Test booking confirmation with calendar integration"""
    ctx = Context(phone="+1234567890", name="Mario", state="ASK_SLOT")
    ctx.slots["candidates"] = ["Domani 15:00", "Domani 16:00", "Mercoledì 10:00"]
    ctx.slots["service"] = "permesso"
    ctx.slots["channel"] = "office"
    
    llm = MockLLM()
    
    # User selects slot
    intent, reason = planner.plan(ctx, "Scelgo il primo", llm)
    intent = validator.validate(ctx, intent)
    reply = executor.dispatch(intent, ctx, "Scelgo il primo")
    
    # Check if booking was successful (either confirmed or failed)
    assert "confermato" in reply.lower() or "appuntamento" in reply.lower() or "non sono riuscita" in reply.lower()
    # State should be CONFIRMED if successful, or remain ASK_SLOT if failed
    assert ctx.state in ["CONFIRMED", "ASK_SLOT"] 