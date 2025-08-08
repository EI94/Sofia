from pathlib import Path

from .context import Context

_PARAFILE = Path(__file__).parent.parent / "config" / "parahelp_v3.txt"
_TEMPLATE = _PARAFILE.read_text(encoding="utf-8")


def build_system_prompt(ctx: Context) -> str:
    """Return full ParaHelp system-prompt in the correct language."""
    return f"{_TEMPLATE}\nCURRENT_LANG: {ctx.lang}"
