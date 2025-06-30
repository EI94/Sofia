from app.tools.moderation import is_abusive
import pytest, asyncio

@pytest.mark.asyncio
async def test_abuse():
    bad = "Sei uno stupido pezzo di ****!"
    good = "Ciao, vorrei info."
    assert await is_abusive(bad) is True
    assert await is_abusive(good) is False 