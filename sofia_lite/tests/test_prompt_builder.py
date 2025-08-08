from sofia_lite.agents.context import Context
from sofia_lite.agents.prompt_builder import build_system_prompt


def test_prompt_contains_lang():
    ctx = Context(phone="debug", lang="fr")
    prompt = build_system_prompt(ctx)
    assert "CURRENT_LANG: fr" in prompt
    assert 'You are **"Sofia"**' in prompt  # sanity check


def test_prompt_contains_parahelp_template():
    ctx = Context(phone="debug", lang="it")
    prompt = build_system_prompt(ctx)

    # Verify key sections of ParaHelp Template v3 are present
    assert "[ P ]  PURPOSE" in prompt
    assert "[ A ]  AUDIENCE" in prompt
    assert "[ R ]  ROLE & RULES" in prompt
    assert "[ A ]  ACTION FLOW" in prompt
    assert "[ H ]  HESITATIONS" in prompt
    assert "[ E ]  EXCLUSIONS" in prompt
    assert "[ S ]  AVAILABLE SERVICES" in prompt
    assert "[ L ]  LANGUAGE & LOCAL FORMATTING" in prompt
    assert "[ P ]  PERSONA" in prompt


def test_prompt_language_consistency():
    # Test different languages
    for lang in ["it", "en", "fr", "es", "ar", "hi", "ur", "bn", "wo"]:
        ctx = Context(phone="debug", lang=lang)
        prompt = build_system_prompt(ctx)
        assert f"CURRENT_LANG: {lang}" in prompt


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
