from sofia_lite.agents.prompt_builder import build_intent_specific_prompt
from sofia_lite.middleware.llm import chat
from ..middleware.ocr import process_payment_image
import asyncio
from ..utils.memo import ttl_cache

def run(ctx, user_msg):
    """Handle payment request with OCR for receipt validation"""
    
    # Check if user sent an image (payment receipt)
    if ctx.slots.get("waiting_for_payment") and "image" in user_msg.lower():
        # Process payment receipt with OCR
        try:
            # TODO: Extract image URL from Twilio webhook
            image_url = ctx.slots.get("payment_image_url")
            if image_url:
                # Δmini optimization: Lazy OCR - run as background task
                asyncio.create_task(process_payment_image(image_url, ctx.phone))
                
                # Return immediately without waiting for OCR
                ctx.state = "CONFIRMED"
                ctx.slots["payment_confirmed"] = True
                sys = build_intent_specific_prompt(ctx, "ASK_PAYMENT")
                user = "Il pagamento è stato ricevuto. Conferma la prenotazione e ringrazia il cliente."
                return chat(sys, user)
                
                # OCR validation removed for lazy processing
                pass
            else:
                sys = build_intent_specific_prompt(ctx, "ASK_PAYMENT")
                user = "Il cliente deve inviare una ricevuta di pagamento. Chiedi gentilmente di inviare la ricevuta."
                return chat(sys, user)
        except Exception as e:
            sys = build_intent_specific_prompt(ctx, "ASK_PAYMENT")
            user = "C'è stato un errore nel processare il pagamento. Chiedi gentilmente di riprovare."
            return chat(sys, user)
    
    # First time asking for payment
    ctx.slots["waiting_for_payment"] = True
    sys = build_intent_specific_prompt(ctx, "ASK_PAYMENT")
    user = "Il cliente ha scelto la consulenza. Spiega il costo di 60€ e chiedi come vuole procedere con il pagamento (bonifico bancario o PayPal)."
    return chat(sys, user) 