# Wrapper for OCR
from ..tools.ocr import extract_text_from_image

def process_image(image_data):
    """Process image with OCR"""
    try:
        return extract_text_from_image(image_data)
    except Exception:
        return None 