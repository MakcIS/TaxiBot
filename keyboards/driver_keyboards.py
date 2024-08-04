from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


wating_cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отказаться', callback_data='cancel_order')],
                                                             [InlineKeyboardButton(text='Я подъехал', callback_data='car_waiting')]])

done_cencel_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отказаться', callback_data='cancel_order')],
                                                             [InlineKeyboardButton(text='Вополнен!', callback_data='order_done')]])