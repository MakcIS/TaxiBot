import asyncpg
from config_data.settings import get_settings
from datetime import datetime

db_config = get_settings().db_config

async def get_driver_info(tg_id: int) -> dict:
    conn = await asyncpg.connect(database=db_config.database,
                                    user=db_config.user,
                                    password=db_config.password,
                                    port=db_config.port)
    
    result = await conn.fetchrow(f'SELECT * FROM taxi_bot_scheme.drivers WHERE telegram_id = {tg_id};')

    await conn.close()
    return dict(result.items())


async def create_new_order(client_id: int, client_address: str, destination: str) -> None:
    conn = await asyncpg.connect(database=db_config.database,
                                    user=db_config.user,
                                    password=db_config.password,
                                    port=db_config.port)
    
    await conn.execute(f'''INSERT INTO taxi_bot_scheme.orders (client_id, client_address, destination, start_time, status) 
                           VALUES ({client_id}, '{client_address}', '{destination}', '{datetime.now()}', 'waiting to driver');''')
    await conn.close()
