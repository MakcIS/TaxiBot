from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSM_data.FSM_classes import FSMOrderTaxiProcess
from aiogram.types import ReplyKeyboardRemove


from keyboards import keyboards
from lexicon.client_lexicon import LEXICON

router = Router()

@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup=keyboards.order_keyboard)


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])
    

@router.message(F.text == 'Заказать такси', StateFilter(default_state))
async def car_order(message: Message, state: FSMContext):
    await message.answer(text='Укажите откуда вас забрать:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMOrderTaxiProcess.from_input)

@router.message(StateFilter(FSMOrderTaxiProcess.from_input))
async def from_input_process(message: Message, state: FSMContext):
    await state.update_data(from_place=message.text)
    await message.answer(text='Укажите куда поедите:')
    await state.set_state(FSMOrderTaxiProcess.to_input)


@router.message(StateFilter(FSMOrderTaxiProcess.to_input))
async def to_input_poress(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(to_place=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=-1002173740967, text=f'Заказ:\n\nЗабрать:{data["from_place"]}\nЕдем до:{data["to_place"]}', reply_markup=keyboards.conform_keyboard)
    await message.answer(text='Ваш заказ принят. Скоро будет назначен водитель.', reply_markup=keyboards.order_keyboard)
    await state.clear()


@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)

@router.callback_query()
async def callback_all(callback: CallbackQuery):
    print('Перехват коллбэка', callback.json(), sep='\n')
    await callback.answer()