from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location, ReplyParameters)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSM_data.FSM_classes import FSMOrderTaxiProcess, FSMOrderFoodProcess
from aiogram.types import ReplyKeyboardRemove

from db_logic import logic


router = Router(__name__)
router.message.filter()
router.callback_query.filter()

@router.message(CommandStart())
async def admin_start_process(message:Message, bot:Bot):
    bot.set_my_commands