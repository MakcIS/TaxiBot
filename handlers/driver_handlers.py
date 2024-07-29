from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command

from keyboards import keyboards
from lexicon.driver_lexicon import LEXICON

router = Router()
router.message.filter(F.chat.id == -1002173740967)
router.callback_query.filter(F.message.chat.id == -1002173740967)


@router.message(CommandStart())
async def process_start_in_driver_chat(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])

@router.callback_query(F.data == 'conform_order')
async def process_conform_order(callback: CallbackQuery, bot: Bot):
    await bot.send_message(chat_id=callback.message.external_reply.origin.sender_user.id, text=f'К вам выехал {callback.from_user.first_name}')
    await callback.answer()

@router.callback_query()
async def call(callback: CallbackQuery):
    print('Перехват в хэндлерах для водителей')
    print(callback.json())
    await callback.answer()


@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)