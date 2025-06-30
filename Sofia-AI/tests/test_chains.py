"""
Test per le chains Sofia AI
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.chains.detect_language import detect_language
from app.chains.classify_intent import classify_intent, aclassify_intent
from app.chains.planner import plan


def test_detect_language():
    """Test per rilevamento lingua"""
    # Mock del LLM
    mock_llm = AsyncMock()
    mock_llm.invoke.return_value.content = "it"
    
    result = detect_language("Ciao, come stai?", mock_llm)
    assert result == "it"


@pytest.mark.asyncio
async def test_plan_saluto_nuovo_cliente():
    """Test planner per saluto di nuovo cliente"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value=None)  # Nuovo cliente
        
        result = await plan("it", "saluto", "Ciao", "+393123456789")
        
        assert "Sofia di Studio Immigrato" in result
        assert "pratiche di immigrazione" in result
        assert "— Sofia | Studio Immigrato" in result


@pytest.mark.asyncio
async def test_plan_saluto_cliente_esistente():
    """Test planner per saluto di cliente esistente"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value={"payment_status": "paid"})  # Cliente esistente
        
        result = await plan("it", "saluto", "Ciao", "+393123456789")
        
        assert "già nostro cliente" in result
        assert "— Sofia | Studio Immigrato" in result


@pytest.mark.asyncio
async def test_plan_prenotazione_online_non_pagato():
    """Test prenotazione online senza pagamento"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value={"payment_status": "unpaid"})
        
        result = await plan("it", "prenotazione", "Voglio prenotare online", "+393123456789")
        
        assert "bonifico" in result
        assert "BG20STSA93000031613097" in result
        assert "upload?phone=+393123456789" in result


@pytest.mark.asyncio
async def test_plan_prenotazione_online_pagato():
    """Test prenotazione online con pagamento confermato"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value={"payment_status": "paid"})
        
        result = await plan("it", "prenotazione", "Voglio prenotare online", "+393123456789")
        
        assert "pagamento è confermato" in result
        assert "prenotata" in result


@pytest.mark.asyncio
async def test_plan_servizio_escluso():
    """Test per servizi non offerti"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value=None)
        
        result = await plan("it", "info", "Visto turistico per USA", "+393123456789")
        
        assert "non offriamo questo servizio" in result


@pytest.mark.asyncio
async def test_plan_info_generali():
    """Test per richiesta informazioni generali"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value=None)
        
        result = await plan("it", "info", "Che servizi offrite?", "+393123456789")
        
        assert "Permessi di soggiorno" in result
        assert "consulenza iniziale (60€)" in result
        assert "— Sofia | Studio Immigrato" in result


@pytest.mark.asyncio
async def test_plan_reclamo_cliente_esistente():
    """Test reclamo da cliente esistente"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(return_value={"payment_status": "paid"})
        
        result = await plan("it", "reclamo", "Ho un problema", "+393123456789")
        
        assert "cliente attivo" in result
        assert "priorità" in result


@pytest.mark.asyncio
async def test_plan_error_handling():
    """Test gestione errori nel planner"""
    with patch('app.chains.planner.memory') as mock_memory:
        mock_memory.get_user = AsyncMock(side_effect=Exception("Database error"))
        
        result = await plan("it", "saluto", "Ciao", "+393123456789")
        
        assert "Ti risponderemo a breve" in result
        assert "— Sofia | Studio Immigrato" in result


if __name__ == "__main__":
    # Esegui i test
    pytest.main([__file__, "-v"]) 