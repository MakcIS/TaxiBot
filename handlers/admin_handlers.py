from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location, ReplyParameters)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSM_data.FSM_classes import FSMOrderTaxiProcess, FSMOrderFoodProcess
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.bot_command_scope_chat import BotCommandScopeChat
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_logic import logic
from filters.filters import IsAdmin

router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

@router.message(CommandStart())
async def admin_start_process(message:Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Режим админа', callback_data='admin_mode')]])
    await message.answer(text='Здравствуйте! Я бот для заказа такси. Так как вы являетесь администратором, вам доступен особый режим.', 
                         reply_markup=keyboard)

@router.message(Command(commands='help'))
async def admin_help_process(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Режим админа', callback_data='admin_mode')]])
    await message.answer(text='Здравствуйте! Я бот для заказа такси. Так как вы являетесь администратором, вам доступен особый режим.', 
                         reply_markup=keyboard)
    
@router.callback_query(F.data == 'admin_mode')
async def move_to_admin_mode(callback: CallbackQuery):
    pass