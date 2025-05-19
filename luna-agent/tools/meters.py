from pymodbus.client import AsyncModbusTcpClient

# Modbus registers for Huawei SUN2000
REG_PV_AC = 32016       # Photovoltaic AC power
REG_LOAD = 37113        # Load power (EMMA)
REG_GRID = 37101        # Grid import/export

async def read_register(ip, register, unit=0):
    """
    Reads a Modbus register
    """
    async with AsyncModbusTcpClient(host=ip, port=502, unit_id=unit) as client:
        result = await client.read_holding_registers(register-1, 1)
        return result.registers[0]

async def get_pv_kw(ip, unit=0):
    """
    Reads the photovoltaic production power in kW
    """
    value = await read_register(ip, REG_PV_AC, unit)
    return value / 1000  # Convert from W to kW

async def get_load_kw(ip, unit=0):
    """
    Reads the facility load power in kW
    """
    value = await read_register(ip, REG_LOAD, unit)
    return value / 1000  # Convert from W to kW

async def get_grid_kw(ip, unit=0):
    """
    Reads the power exchange with the grid in kW
    Positive = import, Negative = export
    """
    value = await read_register(ip, REG_GRID, unit)
    return value / 1000  # Convert from W to kW 