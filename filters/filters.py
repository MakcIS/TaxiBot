from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from db_logic import logic

class IsAdmin(BaseFilter):
    async def __call__(self, update: Message | CallbackQuery):
        admins = await logic.get_admins_list()
        return update.from_user.id in admins
         