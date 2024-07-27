import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.filters import CommandStart

from config_data.settings import get_settings
from handlers import client_handlers, driver_handlers

async def set_main_menu(bot: Bot):
    commands = [BotCommand(command='/start', description='Погнали!'),
                BotCommand(command='/help', description='Помощь')]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands)


async def main():
    settings = get_settings()

    bot = Bot(settings.token)
    dp = Dispatcher()


    dp.startup.register(set_main_menu)
    dp.include_router(driver_handlers.router)
    dp.include_router(client_handlers.router)

    await dp.start_polling(bot)

asyncio.run(main())

