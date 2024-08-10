from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.admin_lexicon import LEXICON


def main_admin_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=LEXICON['swicher'](), callback_data='switcher_for_open')],
                                                     [InlineKeyboardButton(text='Выйти из режима', callback_data='exit_from_mode')]])
    
    return keyboard
