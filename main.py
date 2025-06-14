import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import Redis, RedisStorage 
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat

from config_data.settings import get_settings
from handlers import client_handlers, driver_handlers, admin_handlers
from db_logic.logic import admin_list_from_pg_to_redis, taxi_is_close



async def set_main_menu(bot: Bot):
    commands = [BotCommand(command='/start', description='Погнали!'),
                BotCommand(command='/help', description='Помощь'),
                BotCommand(command='/cancel', description='Отменяет текущие заказы')]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)


async def main():
    bot_config = get_settings().tg_bot

    bot = Bot(bot_config.token)
    dp = Dispatcher(storage=RedisStorage(redis=Redis()))

    await admin_list_from_pg_to_redis()
    taxi_is_close()
    dp.startup.register(set_main_menu)
    dp.include_router(admin_handlers.router)
    dp.include_router(driver_handlers.router)
    dp.include_router(client_handlers.router)

    await dp.start_polling(bot)

asyncio.run(main())

