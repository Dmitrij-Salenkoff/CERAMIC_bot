from aiogram import types
from aiogram.dispatcher import FSMContext

from config import ADMINS_ID
from create_bot import dp
from data_Base.database import sql_find_admins


@dp.callback_query_handler(text='menu_admins_list', state=None, chat_id=ADMINS_ID)
async def find_id(callback: types.CallbackQuery, state: FSMContext):
    print('I am here')
    rep = await sql_find_admins()
    await callback.message.reply(rep, reply=False)
    await callback.answer()