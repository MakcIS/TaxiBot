from aiogram import Router, Bot, F
from aiogram.types import (Message, CallbackQuery, BotCommand, Location, ReplyParameters)
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from FSM_data.FSM_classes import FSMOrderTaxiProcess, FSMOrderFoodProcess
from aiogram.types import ReplyKeyboardRemove


from keyboards import keyboards
from lexicon.client_lexicon import LEXICON
from db_logic import logic
from geo_location.geo_location import get_address
from filters.filters import IsClosed

#Добавить обработку геометок и сделать так что бы во время заказа бот не принимал ничего кроме текста и геометок
router = Router()

@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup=keyboards.order_keyboard)


@router.message(Command(commands='help'))
async def process_help(message: Message):
    await message.answer(text=LEXICON['/help'])

#Хэндлер перехватывающий сообщения, когда такси закрыто
@router.message(IsClosed())
async def message_is_closed(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['taxi_closed'])
    await state.clear()
    
#Хэндлер перехватывающий коллбэки, когда такси закрыто
@router.callback_query(IsClosed())
async def callback_is_closed(callback: CallbackQuery, state: FSMContext):
    await callback.answer(text=LEXICON['taxi_closed'])
    await state.clear()

#Хэндлер реагирующий на попытку совершить заказ во время оформления заказа
@router.message(~StateFilter(default_state), F.text.in_(['Заказать такси', 'Продуктовый заказ']))
async def incorrect(message: Message):
    await message.answer(text=LEXICON["incorrect"])

#Хэндлер прерывающий процесс заказа
@router.callback_query(~StateFilter(default_state), F.data == 'cancel_order')
async def cancel_order(callback: CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(text=LEXICON['cancel_order'])
    await callback.answer()

    data = await state.get_data()
    await bot.delete_messages(chat_id=callback.from_user.id, message_ids=[*range(data['start_message_id'], callback.message.message_id + 1)])
    await state.clear()

#Хэндлер инициирующий процедуру заказа такси
@router.message(F.text == 'Заказать такси', StateFilter(default_state))
async def car_order(message: Message, state: FSMContext):
    await message.answer(text='Укажите откуда вас забрать:', reply_markup=keyboards.cancel_order_keyboard)
    await state.set_state(FSMOrderTaxiProcess.from_input)
    await state.update_data(start_message_id=message.message_id)

#Хэндлер просящий ввести адрес назначения, и фиксирующий адрес клиента
@router.message(StateFilter(FSMOrderTaxiProcess.from_input), F.text)
async def from_input_process(message: Message, state: FSMContext):
    await state.update_data(from_place=message.text)
    await message.answer(text='Укажите куда поедите:', reply_markup=keyboards.cancel_back_order_keyboard)
    await state.set_state(FSMOrderTaxiProcess.to_input)

#Хэндлер возвращающий назад к указанию адреса клиента
@router.callback_query(StateFilter(FSMOrderTaxiProcess.to_input), F.data == 'back')
async def back_to_from(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Укажите откуда вас забрать:', reply_markup=keyboards.cancel_order_keyboard)
    await state.set_state(FSMOrderTaxiProcess.from_input)

#Хэндлер фиксирующий адрес назначения и выводящий форму подтверждения заказа
@router.message(StateFilter(FSMOrderTaxiProcess.to_input), F.text)
async def to_input_process(message: Message, state: FSMContext):
    await state.update_data(to_place=message.text)
    data = await state.get_data()
    await message.answer(text=LEXICON['check_order_data'].format(frm=data['from_place'], to=data['to_place']), reply_markup=keyboards.cancel_back_conform_order_keyboard, parse_mode="HTML")
    await state.set_state(FSMOrderTaxiProcess.check_order_data)

#Хэндлер возвращающий к указанию пункта назначения
@router.callback_query(StateFilter(FSMOrderTaxiProcess.check_order_data), F.data == 'back')
async def back_to_from(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Укажите куда поедите:', reply_markup=keyboards.cancel_back_order_keyboard)
    await state.set_state(FSMOrderTaxiProcess.to_input)

#Хэндлер срабатывающий на положительный ответ о заказе, создающий новый заказ в БД и отправляющий сообщение в чат водителей
@router.callback_query(StateFilter(FSMOrderTaxiProcess.check_order_data), F.data == 'conform_order')
async def check_order_process(callback: CallbackQuery, state: FSMContext, bot: Bot):    
    data = await state.get_data()

    order_id = await logic.create_new_order_and_return_order_id(client_id=callback.from_user.id,
                                                          client_address=data['from_place'],
                                                          destination=data['to_place'])
    await bot.send_message(chat_id=-1002173740967, 
                           text=LEXICON['taxi_order_form'].format(order_id, data["from_place"], data["to_place"]), 
                           reply_markup=keyboards.conform_keyboard)
    
    await callback.message.answer(text=LEXICON['conforming_order'].format(order_id=order_id, frm=data['from_place'], to=data['to_place']), parse_mode="HTML")
    await bot.delete_messages(chat_id=callback.from_user.id, message_ids=[*range(data['start_message_id'], callback.message.message_id + 1)])
    await callback.answer()  
    await state.clear()

#Хэндлер инициируюший продуктовый заказ
@router.message(F.text == 'Продуктовый заказ', StateFilter(default_state))
async def shopping_list_proces(message: Message, state: FSMContext):
    await message.answer(text='Отправте список продуктов:', reply_markup=keyboards.cancel_order_keyboard)
    await state.set_state(FSMOrderFoodProcess.shopping_list)

#Хэндлер фиксирующий список покупок и просящий указать адрес доставки
@router.message(StateFilter(FSMOrderFoodProcess.shopping_list))
async def food_place(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(shopping_list=message.text)
    await message.answer(text='Укажите куда доставить заказ:', reply_markup=keyboards.cancel_back_order_keyboard)
    await state.set_state(FSMOrderFoodProcess.to_input)

#Хэндлер возвращающий к списку продуктов
@router.callback_query(StateFilter(FSMOrderFoodProcess.to_input), F.data == 'back')
async def back_to_from(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Отправте список продуктов:', reply_markup=keyboards.cancel_order_keyboard)
    await state.set_state(FSMOrderFoodProcess.shopping_list)

#Хэндлер фиксирующий адрес доставки и формирующий заказ с передачей его в чат водителей 
@router.message(StateFilter(FSMOrderFoodProcess.to_input))
async def conform_food_order(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(to_place=message.text)
    data = await state.get_data()
    await bot.send_message(chat_id=-1002173740967, 
                           text=LEXICON['food_order_form'].format(data["shopping_list"], data["to_place"]), 
                           reply_markup=keyboards.conform_keyboard)
    await message.answer(text=LEXICON['conforming_order'])
    await state.clear()

#Тестовый хэндлер удалить после
@router.message(F.location)
async def cache_location(message: Message):
    print(await get_address(message.location.latitude, message.location.longitude))

#Тестовый хэндлер удалить после
@router.message()
async def out_chat(message: Message):
    await message.send_copy(chat_id=message.chat.id)

@router.callback_query()
async def callback_all(callback: CallbackQuery):
    print('Перехват коллбэка', callback.json(), sep='\n')
    await callback.answer()