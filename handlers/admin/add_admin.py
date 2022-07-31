from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ADMINS_ID, password
from create_bot import dp


@dp.callback_query_handler(text='menu_add_admin', state=None, chat_id=ADMINS_ID)
async def add_pottery_state(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Попроси админа выбрать "Добавить изделие", а затем ввести пароль:', reply=False)
    await callback.message.reply(f'{password}', reply=False)
    await callback.answer()