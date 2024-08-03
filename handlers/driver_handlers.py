import re
from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command

from keyboards import keyboards
from lexicon.driver_lexicon import LEXICON
from db_logic.logic import get_driver_info, add_id_in_redis, get_order_info

router = Router()
router.message.filter(F.chat.id == -1002173740967)
router.callback_query.filter(F.message.chat.id == -1002173740967)


@router.message(CommandStart())
async def process_start_in_driver_chat(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])

#Хэндлер обрабатывающий согласие водителя на заказ(дописать добавление в БД  ИД водителя)
@router.callback_query(F.data == 'conform_order')
async def process_conform_order(callback: CallbackQuery, bot: Bot):
    order_id = int(re.findall(r'#(\d+):', callback.message.text)[0])
    client_id = (await get_order_info(order_id))['client_id']
    driver_info = await get_driver_info(callback.from_user.id)
    
    await bot.send_message(chat_id=client_id, text=f'К вам выехал: {driver_info["name"]}\nАвтомобиль: {driver_info["car"]}\nЦвет: {driver_info["color"]}\nНомер: *{driver_info["licence_plate"]}**')

    await callback.answer()

@router.callback_query()
async def call(callback: CallbackQuery):
    print('Перехват в хэндлерах для водителей')
    print(callback.json())
    await callback.answer()


@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)