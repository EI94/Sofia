"""
Sofia Lite - Mock OCR Middleware
"""

import logging

logger = logging.getLogger(__name__)


def process_payment_image(image_data: bytes) -> dict:
    """Mock OCR processing for payment receipts"""
    logger.info("Mock OCR processing payment image")
    return {
        "amount": "60.00",
        "currency": "EUR",
        "date": "2025-08-01",
        "confidence": 0.95,
    }


def extract_text_from_image(image_data: bytes) -> str:
    """Mock text extraction from image"""
    logger.info("Mock text extraction from image")
    return "Mock extracted text from image"


def validate_payment_receipt(image_data: bytes) -> bool:
    """Mock payment receipt validation"""
    logger.info("Mock payment receipt validation")
    return True
