from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from db_logic import logic

class IsAdmin(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery):
        admins = logic.get_admins_list_from_redis()
        return update.from_user.id in admins
    
class IsClosed(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery):
        if logic.get_taxi_status() != "open":
            return True
         