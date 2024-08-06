import redis
import asyncpg
from config_data import settings
from datetime import datetime

#Функция возвращающяя коннект с Редисом
def create_redis_connect() -> redis.Redis:
    return redis.Redis()

#Функция возвращающяя коннект с Постгрес
async def _create_postgres_connect():
    db_config = settings.get_settings().db_config
    return await asyncpg.connect(database=db_config.database,
                                    user=db_config.user,
                                    password=db_config.password,
                                    port=db_config.port)

#Функция возвращающяя данные на водителя по telegram_id
async def get_driver_info(tg_id: int) -> dict:
    conn = await _create_postgres_connect()
    
    result = await conn.fetchrow('SELECT * FROM taxi_bot_scheme.drivers WHERE telegram_id = $1;', tg_id)

    await conn.close()
    return dict(result.items())

#Функция создающяя новую запись заказа в БД и возвращающяя id заказа
async def create_new_order_and_return_order_id(client_id: int, client_address: str, destination: str) -> int:
    conn = await _create_postgres_connect()
    start_time = datetime.now()

    await conn.execute('''INSERT INTO taxi_bot_scheme.orders (client_id, client_address, destination, start_time, status) 
                           VALUES ($1, $2, $3, $4, 'waiting driver');''', 
                           client_id, client_address, destination, start_time)

    order_id = await conn.fetchrow('''SELECT id 
                                       FROM taxi_bot_scheme.orders 
                                       WHERE client_id=$1 AND start_time=$2 AND status='waiting driver';''',
                                       client_id, start_time)
    await conn.close()
    return order_id['id']

#Функция возвращающяя информацию о заказе
async def get_order_info(order_id: int):
    conn = await _create_postgres_connect()

    result = await conn.fetchrow('SELECT * FROM taxi_bot_scheme.orders WHERE id = $1;', order_id)

    await conn.close()
    return dict(result.items())

#Функция добавляющяя id водителя к заказу в БД
async def take_order(driver_id: int, order_id: int) -> None:
    conn = await _create_postgres_connect()

    await conn.execute('''UPDATE taxi_bot_scheme.orders
                           SET driver_id=$1, status='in progress'
                           WHERE id=$2;''', driver_id, order_id)
    await conn.close()

#Функция закрывающяя заказ
async def order_done(order_id: int) -> None:
    conn = await _create_postgres_connect()

    await conn.execute('''UPDATE taxi_bot_scheme.orders
                           SET finish_time=$2, status='complete'
                           WHERE id=$1;''', order_id, datetime.now())
    await conn.close()

#Функция возвращающяя список администраторов
async def get_admins_list() -> list:
    conn = await _create_postgres_connect()

    result = await conn.fetch('''SELECT telegram_id
                                 FROM taxi_bot_scheme.admins_list;''')
    
    return [value for record in result for value in record.values()]







def add_id_in_redis(id: str|int):
    conn = create_redis_connect()
    conn.set(id, 2)

def id_in_redis(id: str|int):
    conn = create_redis_connect()
    return conn.get(id)
