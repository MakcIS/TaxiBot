from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location, ReplyParameters)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_logic import logic
from filters.filters import IsAdmin
from FSM_data.FSM_classes import FSMAdminMode
from db_logic.logic import switcher_taxi_status, get_taxi_status
from lexicon.admin_lexicon import LEXICON
from keyboards import admin_keyboards

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

#Хэндлер на команду старт
@router.message(CommandStart())
async def admin_start_process(message:Message):
    await message.answer(text=LEXICON['start'])
    
#Хэндлер на помощь вне режима Администратора
@router.message(Command(commands='help'), StateFilter(default_state))
async def admin_help_process(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Режим админа', callback_data='admin_mode')]])
    await message.answer(text=LEXICON['help'], 
                         reply_markup=keyboard)

#Хэндлер на вход в режим Администратора    
@router.callback_query(F.data == 'admin_mode')
async def move_to_admin_mode(callback: CallbackQuery, state: FSMContext):
    
    await state.set_state(FSMAdminMode.in_mode)
    await callback.message.edit_text(text=LEXICON['in_mode'], reply_markup=admin_keyboards.main_admin_keyboard())
    await callback.answer()
    
    
#Хэндлер на выход из режима Администратора
@router.callback_query(StateFilter(FSMAdminMode.in_mode), F.data == 'exit_from_mode')
async def exit_from_mode(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.answer(text='Вы вышли из режима Администратора')

#Хэндлер реагирующий на закрытие/открытие такси
@router.callback_query(StateFilter(FSMAdminMode.in_mode), F.data == 'switcher_for_open')
async def switcher_for_open(callback: CallbackQuery, state: FSMContext):
        switcher_taxi_status()
        await callback.message.edit_reply_markup(reply_markup=admin_keyboards.main_admin_keyboard())
        await callback.answer(text=LEXICON['press_switcher_inform']())

#Хэндлер срабатывающий, когда администратор в режиме, хочет совершить инные действия
@router.message(StateFilter(FSMAdminMode.in_mode))
async def message_in_mode(message: Message):
     await message.answer(text=LEXICON['error_in_mode'])

#Хэндлер срабатывающий, когда администратор в режиме, хочет совершить инные действия
@router.callback_query(StateFilter(FSMAdminMode.in_mode))
async def callback_in_mode(callback: CallbackQuery):
     await callback.answer(text=LEXICON['error_in_mode'])