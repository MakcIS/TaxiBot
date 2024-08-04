import re
from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from FSM_data.FSM_classes import FSMDriverOnOrder
from keyboards import driver_keyboards
from lexicon.driver_lexicon import LEXICON
from db_logic.logic import get_driver_info, take_order, get_order_info, order_done

#Продумать логику отказа водителем от заказа

router = Router()
router.message.filter(F.chat.id == -1002173740967)
router.callback_query.filter(F.message.chat.id == -1002173740967)


@router.message(CommandStart())
async def process_start_in_driver_chat(message: Message):
    await message.answer(text=LEXICON['/start'])


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])

@router.message(Command(commands='cancel'))
async def process_cancel(message: Message, state: FSMContext):
    await state.clear()

#Хэндлер обрабатывающий согласие водителя на заказ, с добавлением в БД id водителя к заказу 
#И отправляющий сообщение клиенту с данными водителя
@router.callback_query(StateFilter(default_state), F.data == 'conform_order')
async def process_conform_order(callback: CallbackQuery, bot: Bot, state: FSMContext):
    order_id = int(re.findall(r'#(\d+):', callback.message.text)[0])
    client_id = (await get_order_info(order_id))['client_id']
    driver_info = await get_driver_info(callback.from_user.id)
    
    await bot.send_message(chat_id=client_id, text=LEXICON["message_for_client"].format(name=driver_info["name"], 
                                                                                        car=driver_info["car"], 
                                                                                        color=driver_info["color"], 
                                                                                        plate=driver_info["licence_plate"]
                                                                                        )
                          )
    
    await callback.message.edit_text(text=LEXICON['edit_order_text'].format(name=driver_info["name"], 
                                                                            surname=driver_info["surname"], 
                                                                            message_text=callback.message.text), 
                                    parse_mode="HTML",
                                    reply_markup=driver_keyboards.wating_cancel_keyboard)
    
    await take_order(driver_id=callback.from_user.id, order_id=order_id)
    await state.set_state(FSMDriverOnOrder.on_order)
    await state.update_data(order_id=order_id, 
                            client_id=client_id, 
                            message_id=callback.message.message_id,
                            name=driver_info["name"], 
                            surname=driver_info["surname"])
    await callback.answer()

#Хэндлер реагирующий на нажатие кнопки я подъехал, сообщаяя об этом клиенту
@router.callback_query(StateFilter(FSMDriverOnOrder.on_order), F.data == 'car_waiting')
async def car_waiting_process(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    if callback.message.message_id == data['message_id']:
        await bot.send_message(chat_id=data['client_id'], text='Водитель подъехал, можете выходить.')
        await callback.message.edit_reply_markup(reply_markup=driver_keyboards.done_cencel_keyboard)
        await state.set_state(FSMDriverOnOrder.in_progress)
        await callback.answer()
    else:
        await callback.answer(text='Другой водитель выполняет этот заказ.')

#Хэндлер реагирующий на кнопку выполнения заказа
@router.callback_query(StateFilter(FSMDriverOnOrder.in_progress), F.data == 'order_done')
async def order_done_process(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if callback.message.message_id == data['message_id']:
        await callback.message.edit_text(text=LEXICON['order_done'].format(order_id=data['order_id'],
                                                                           name=data['name'],
                                                                           surname=data['surname']))
        await bot.send_message(chat_id=data['client_id'], text='Спасибо, что воспользовались нашим такси. Ждём вас снова!')
        await order_done(data['order_id'])
        await state.clear()
        await callback.answer()
    else:
        await callback.answer(text='Другой водитель выполняет этот заказ.')

@router.callback_query()
async def call(callback: CallbackQuery):
    print('Перехват в хэндлерах для водителей')
    print(callback.json())
    await callback.answer()


@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)