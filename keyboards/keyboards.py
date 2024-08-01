from datetime import date
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


conform_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Принять', callback_data='conform_order'), InlineKeyboardButton(text='Отклонить', callback_data='cencel_order')]])
order_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Заказать такси'), KeyboardButton(text='Продуктовый заказ')]], resize_keyboard=True, one_time_keyboard=True)
cancel_back_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back'), InlineKeyboardButton(text='Отмена', callback_data='cancel_order')]])
cancel_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отмена', callback_data = 'cancel_order')]])
cancel_back_conform_order_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                            [InlineKeyboardButton(text='Назад', callback_data='back'), InlineKeyboardButton(text='Отмена', callback_data='cancel_order')], 
                                                                            [InlineKeyboardButton(text='Подтвердить', callback_data='conform_order')]])