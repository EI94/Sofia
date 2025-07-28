from ..policy.language_support import T
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
                    return T("payment_confirmed", ctx.lang)
                else:
                    return T("payment_invalid", ctx.lang)
            else:
                return T("ask_payment_receipt", ctx.lang)
        except Exception as e:
            return T("payment_error", ctx.lang)
    
    # First time asking for payment
    ctx.slots["waiting_for_payment"] = True
    return T("ask_payment", ctx.lang) 