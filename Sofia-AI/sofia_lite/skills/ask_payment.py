from sofia_lite.agents.prompt_builder import build_system_prompt
from sofia_lite.middleware.llm import chat
from ..middleware.ocr import process_payment_image
import asyncio

def run(ctx, user_msg):
    """Handle payment request with OCR for receipt validation"""
    
    # Check if user sent an image (payment receipt)
    if ctx.slots.get("waiting_for_payment") and "image" in user_msg.lower():
        # Process payment receipt with OCR
        try:
            # TODO: Extract image URL from Twilio webhook
            image_url = ctx.slots.get("payment_image_url")
            if image_url:
                # Run OCR asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                payment_result = loop.run_until_complete(
                    process_payment_image(image_url, ctx.phone)
                )
                loop.close()
                
                if payment_result.get("is_valid_payment"):
                    ctx.state = "CONFIRMED"
                    ctx.slots["payment_confirmed"] = True
                    sys = build_system_prompt(ctx)
                    user = "Il pagamento è stato confermato. Conferma la prenotazione e ringrazia il cliente."
                    return chat(sys, user)
                else:
                    sys = build_system_prompt(ctx)
                    user = "Il pagamento non è valido. Chiedi gentilmente di inviare una ricevuta valida."
                    return chat(sys, user)
            else:
                sys = build_system_prompt(ctx)
                user = "Il cliente deve inviare una ricevuta di pagamento. Chiedi gentilmente di inviare la ricevuta."
                return chat(sys, user)
        except Exception as e:
            sys = build_system_prompt(ctx)
            user = "C'è stato un errore nel processare il pagamento. Chiedi gentilmente di riprovare."
            return chat(sys, user)
    
    # First time asking for payment
    ctx.slots["waiting_for_payment"] = True
    sys = build_system_prompt(ctx)
    user = "Il cliente ha scelto la consulenza. Spiega il costo di 60€ e chiedi come vuole procedere con il pagamento (bonifico bancario o PayPal)."
    return chat(sys, user) 