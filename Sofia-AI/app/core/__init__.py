"""
Core module for Sofia AI
Contains the ParaHelp template system
"""

from .prompts import (
    get_optimized_prompt,
    validate_prompt_size,
    get_fallback_prompt,
    get_template_by_action,
    format_prompt_with_context,
    PARAHELP_SYSTEM_TEMPLATE,
    PAYMENT_INSTRUCTIONS_TEMPLATE,
    APPOINTMENT_CONFIRMATION_TEMPLATE
)

__all__ = [
    "get_optimized_prompt",
    "validate_prompt_size", 
    "get_fallback_prompt",
    "get_template_by_action",
    "format_prompt_with_context",
    "PARAHELP_SYSTEM_TEMPLATE",
    "PAYMENT_INSTRUCTIONS_TEMPLATE",
    "APPOINTMENT_CONFIRMATION_TEMPLATE"
] 