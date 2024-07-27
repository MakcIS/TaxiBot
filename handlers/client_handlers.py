from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command


from keyboards import keyboards
from lexicon.client_lexicon import LEXICON

router = Router()

@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup=keyboards.order_keyboard)


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])
    

@router.message(F.text == 'Заказать такси')
async def car_order(message: Message, bot: Bot):
    await bot.send_message(chat_id='-1002173740967', text=f'Заказ такси от {message.from_user.first_name}:\n{message.text}', reply_markup= keyboards.conform_keyboard)

@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)

@router.callback_query()
async def callback_all(callback: CallbackQuery):
    print('Перехват коллбэка', callback.json(), sep='\n')
    await callback.answer()