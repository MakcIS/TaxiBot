from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command

from keyboards import keyboards
from lexicon.driver_lexicon import LEXICON

router = Router()
router.message.filter(F.chat.id == -1002173740967)
router.callback_query.filter(F.chat.id == -1002173740967)


@router.message(CommandStart())
async def process_start_in_driver_chat(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])


@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)