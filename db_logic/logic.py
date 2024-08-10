import redis
import asyncpg
from config_data import settings
from datetime import datetime

class PGConnect():
    def __init__(self) -> None:
        self.config = settings.get_settings().db_config

    async def __aenter__(self):
        self.connect = await asyncpg.connect(database=self.config.database,
                                            user=self.config.user,
                                            password=self.config.password,
                                            port=self.config.port)
        return self.connect
        
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.connect.close()



#Функция возвращающяя коннект с Редисом
def create_redis_connect() -> redis.Redis:
    return redis.Redis(charset='utf-8', decode_responses=True)


#Функция возвращающяя данные на водителя по telegram_id
async def get_driver_info(tg_id: int) -> dict:
    async with PGConnect() as conn:

        result = await conn.fetchrow('SELECT * FROM taxi_bot_scheme.drivers WHERE telegram_id = $1;', tg_id)

        return dict(result.items())

#Функция создающяя новую запись заказа в БД и возвращающяя id заказа
async def create_new_order_and_return_order_id(client_id: int, client_address: str, destination: str) -> int:
    async with PGConnect() as conn:
        start_time = datetime.now()

        await conn.execute('''INSERT INTO taxi_bot_scheme.orders (client_id, client_address, destination, start_time, status) 
                            VALUES ($1, $2, $3, $4, 'waiting driver');''', 
                            client_id, client_address, destination, start_time)

        order_id = await conn.fetchrow('''SELECT id 
                                        FROM taxi_bot_scheme.orders 
                                        WHERE client_id=$1 AND start_time=$2 AND status='waiting driver';''',
                                        client_id, start_time)
        return order_id['id']

#Функция возвращающяя информацию о заказе
async def get_order_info(order_id: int):
    async with PGConnect() as conn:

        result = await conn.fetchrow('SELECT * FROM taxi_bot_scheme.orders WHERE id = $1;', order_id)

        return dict(result.items())

#Функция добавляющяя id водителя к заказу в БД
async def take_order(driver_id: int, order_id: int) -> None:
    async with PGConnect() as conn:

        await conn.execute('''UPDATE taxi_bot_scheme.orders
                            SET driver_id=$1, status='in progress'
                            WHERE id=$2;''', driver_id, order_id)

#Функция закрывающяя заказ
async def order_done(order_id: int) -> None:
    async with PGConnect() as conn:

        await conn.execute('''UPDATE taxi_bot_scheme.orders
                            SET finish_time=$2, status='complete'
                            WHERE id=$1;''', order_id, datetime.now())


#Функция возвращающяя список администраторов из Постгресс
async def get_admins_list_from_pg() -> list:
    async with PGConnect() as conn:

        result = await conn.fetch('''SELECT telegram_id
                                 FROM taxi_bot_scheme.admins_list;''')
    
        return [value for record in result for value in record.values()]
    
#Функция возвращающая итератор администраторов из Редис    
def get_admins_list_from_redis():
    r_connect = create_redis_connect()
    return map(int, r_connect.smembers('admins_list'))


#Функция берущая список администраторов из Постгресс и добаляющяя его в множество в Редис 
async def admin_list_from_pg_to_redis():
        r_connect = create_redis_connect()
        admins_list = await get_admins_list_from_pg()
        if admins_list:
            r_connect.sadd('admins_list', *admins_list)
        else:
            pass #Место для логгирования

#Создаёт в Редисе ключ отвечающий за состояние открыто\закрыто
def taxi_is_close():
    r_connect = create_redis_connect()
    r_connect.set('taxi_status', 'close')

#Возвращает статус такси
def get_taxi_status() -> str:
    r_connect = create_redis_connect()
    return r_connect.get('taxi_status')

#Переключает состояние такси открыто/закрыто
def switcher_taxi_status():
    r_connect = create_redis_connect()
    status = r_connect.get('taxi_status')
        
    if status == 'open':
        r_connect.set('taxi_status', 'close')
    elif status == 'close':
        r_connect.set('taxi_status', 'open')

