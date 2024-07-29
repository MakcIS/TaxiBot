from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


conform_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Принять', callback_data='conform_order'), InlineKeyboardButton(text='Отклонить', callback_data='cencel_order')]])
order_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Заказать такси'), KeyboardButton(text='Продуктовый заказ')]], resize_keyboard=True, one_time_keyboard=True)