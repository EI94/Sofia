# OCR middleware wrapper
from ..tools.ocr import process_payment_image
import logging

logger = logging.getLogger(__name__)

async def process_payment_receipt(image_url: str, user_phone: str):
    """Process payment receipt with OCR validation"""
    try:
        result = await process_payment_image(image_url, user_phone)
        logger.info(f"OCR result for {user_phone}: {result.get('is_valid_payment', False)}")
        return result
    except Exception as e:
        logger.error(f"OCR processing error for {user_phone}: {e}")
        return {
            "is_payment": False,
            "is_valid_payment": False,
            "error": str(e)
        } 