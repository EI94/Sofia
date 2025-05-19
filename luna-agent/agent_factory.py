from agents import Agent, function_tool
from tools.prices import get_pun_now
from tools.meters import get_pv_kw, get_load_kw, get_grid_kw
from tools.battery import get_soc, safe_set

def make_intelligent_luna(ip="192.168.200.1", unit=0):
    """
    Creates an intelligent agent for LUNA 2000 battery control
    with economic optimization based on prices and production
    """
    # --- TOOLS for data reading ---------------------------------
    @function_tool
    async def read_soc() -> int:
        """Reads the battery state of charge (0-100%)"""
        return await get_soc(ip, unit)

    @function_tool
    async def price_now() -> float:
        """Gets the current energy price in €/kWh"""
        return await get_pun_now()

    @function_tool
    async def pv_kw() -> float:
        """Reads the photovoltaic production power in kW"""
        return await get_pv_kw(ip, unit)

    @function_tool
    async def load_kw() -> float:
        """Reads the facility load power in kW"""
        return await get_load_kw(ip, unit)

    @function_tool
    async def grid_kw() -> float:
        """Reads the power exchange with the grid in kW
        Positive = import, Negative = export"""
        return await get_grid_kw(ip, unit)

    # --- TOOLS for battery control ---------------------
    @function_tool
    async def force_charge(kw: float = 1.0):
        """
        Forces battery charging at the specified power
        Args:
            kw: power in kW (max 2)
        """
        await safe_set(ip, unit, 1, kw)
        return f"Batteria in carica a {kw} kW"

    @function_tool
    async def force_discharge(kw: float = 1.0):
        """
        Forces battery discharging at the specified power
        Args:
            kw: power in kW (max 2)
        """
        await safe_set(ip, unit, 2, kw)
        return f"Batteria in scarica a {kw} kW"

    @function_tool
    async def set_standby():
        """Sets the battery to standby mode (neither charging nor discharging)"""
        await safe_set(ip, unit, 0, 0)
        return "Batteria in standby"

    # --- AGENT creation -------------------------------------
    return Agent(
        name="Smart LUNA Controller",
        instructions="""
Sei il controllore intelligente di una batteria LUNA 2000 da 5 kWh.

Obiettivi prioritari (in ordine di importanza):
1. Mantieni lo stato di carica (SoC) tra 25% e 85%.
2. Se il prezzo attuale > 0,25 €/kWh E SoC > 40% → scarica fino a 2 kW.
3. Se il prezzo attuale < 0,12 €/kWh O produzione in surplus > 0,5 kW → carica fino a 2 kW.
4. Mantieni almeno il 20% di riserva SoC dopo le 18:00.

Se l'utente chiama esplicitamente force_charge / force_discharge, obbedisci A MENO CHE 
non violi i limiti di SoC o potenza. Se non puoi eseguire il comando, spiega chiaramente perché.

Ad ogni "tick" periodico, leggi i dati attuali, prendi una decisione ottimale
e comunica brevemente la tua logica e azione.

Rispondi sempre con frasi brevi e comprensibili in italiano.
""",
        tools=[
            read_soc, price_now, pv_kw, load_kw, grid_kw,
            force_charge, force_discharge, set_standby
        ],
    ) 