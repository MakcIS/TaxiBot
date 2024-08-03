import redis
import asyncpg
from config_data import settings
from datetime import datetime

#Функция возвращающяя коннект с Редисом
def create_redis_connect() -> redis.Redis:
    return redis.Redis()

#Функция возвращающяя коннект с Постгрес
async def create_postgres_connect():
    db_config = settings.get_settings().db_config
    return await asyncpg.connect(database=db_config.database,
                                    user=db_config.user,
                                    password=db_config.password,
                                    port=db_config.port)

#Функция возвращающяя данные на водителя по telegram_id
async def get_driver_info(tg_id: int) -> dict:
    conn = await create_postgres_connect()
    
    result = await conn.fetchrow(f'SELECT * FROM taxi_bot_scheme.drivers WHERE telegram_id = {tg_id};')

    await conn.close()
    return dict(result.items())

#Функция создающяя новую запись заказа в БД и возвращающяя id заказа
async def create_new_order_and_return_order_id(client_id: int, client_address: str, destination: str) -> int:
    conn = await create_postgres_connect()
    start_time = datetime.now()

    await conn.execute(f'''INSERT INTO taxi_bot_scheme.orders (client_id, client_address, destination, start_time, status) 
                           VALUES ({client_id}, '{client_address}', '{destination}', '{start_time}', 'waiting driver');''')

    order_id = await conn.fetchrow(f'''SELECT id 
                                       FROM taxi_bot_scheme.orders 
                                       WHERE client_id={client_id} AND start_time='{start_time}' AND status='waiting driver';''')
    await conn.close()
    return order_id['id']

#Функция возвращающяя информацию о заказе
async def get_order_info(order_id: int):
    conn = await create_postgres_connect()

    result = await conn.fetchrow(f'SELECT * FROM taxi_bot_scheme.orders WHERE id = {order_id};')

    await conn.close()
    return dict(result.items())

#Функция добавляющяя id водителя к заказу в БД
async def take_order(driver_id: int, client_id: int):
    conn = await create_postgres_connect()

    await conn.execute(f'''UPDATE taxi_bot_scheme.orders
                           SET driver_id={driver_id}, client_id=0, client_address='', destination='', start_time='', finish_time='', status=''
                           WHERE id=0;''')

def add_id_in_redis(id: str|int):
    conn = create_redis_connect()
    conn.set(id, 2)

def id_in_redis(id: str|int):
    conn = create_redis_connect()
    return conn.get(id)
