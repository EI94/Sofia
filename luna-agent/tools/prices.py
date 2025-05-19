from mercati_energetici import MercatiElettrici
import datetime
import pandas as pd

async def get_pun_now() -> float:
    """
    Gets the current PUN price in €/kWh
    """
    async with MercatiElettrici() as me:
        today = datetime.date.today()
        df: pd.DataFrame = await me.get_pun_index(today)
        ora_attuale = datetime.datetime.now().hour
        # Convert from €/MWh to €/kWh
        return float(df.iloc[ora_attuale]['pun €/MWh']) / 1000 