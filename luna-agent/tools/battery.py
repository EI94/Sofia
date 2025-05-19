from pymodbus.client import AsyncModbusTcpClient

# Modbus registers for LUNA 2000 battery
REG_SOC = 47040  # State of Charge (0-100%)
REG_MODE = 47006  # Operating mode
REG_POWER = 47011  # Power in Watts

# Safety limits
MAX_KW = 2

async def get_soc(ip, unit=0):
    """
    Reads the battery state of charge
    Returns: int (0-100)
    """
    async with AsyncModbusTcpClient(host=ip, port=502, unit_id=unit) as client:
        result = await client.read_holding_registers(REG_SOC-1, 1)
        return result.registers[0]

async def set_battery(ip, unit, mode, power_kw=0):
    """
    Sets the battery mode and power
    Args:
        mode: 0=standby, 1=charge, 2=discharge
        power_kw: power in kW (-2 to +2)
    """
    if abs(power_kw) > MAX_KW:
        raise ValueError(f"Power exceeds safety limits (±{MAX_KW} kW)")
    
    async with AsyncModbusTcpClient(host=ip, port=502, unit_id=unit) as client:
        # Set the mode
        await client.write_registers(REG_MODE-1, [mode])
        
        # If in charge or discharge mode, set the power
        if mode in (1, 2):
            # Convert kW to Watts
            power_watts = int(power_kw * 1000)
            await client.write_registers(REG_POWER-1, [power_watts])

async def safe_set(ip, unit, mode, power_kw=0):
    """
    Sets the battery with additional safety checks
    Args:
        mode: 0=standby, 1=charge, 2=discharge
        power_kw: power in kW (max 2)
    """
    # Check power limits
    if abs(power_kw) > MAX_KW:
        raise ValueError(f"Power exceeds {MAX_KW} kW")
    
    # Check state of charge
    soc = await get_soc(ip, unit)
    
    # Safety checks
    if mode == 2 and soc < 25:  # dangerous discharge
        raise ValueError("Low SoC (< 25%). Discharge not allowed")
    elif mode == 1 and soc > 95:  # dangerous charge
        raise ValueError("High SoC (> 95%). Charge not allowed")
    
    # Execute command if all checks pass
    await set_battery(ip, unit, mode, power_kw) 