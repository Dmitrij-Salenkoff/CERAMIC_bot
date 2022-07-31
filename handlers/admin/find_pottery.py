from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import ADMINS_ID
from data_Base.database import sql_find_id
from keyboards import admin_kb as adkb
from telegram_bot import dp


class FindPottery(StatesGroup):
    id = State()


@dp.callback_query_handler(text='find_pottery', state=None, chat_id=ADMINS_ID)
async def find_id(callback: types.CallbackQuery, state: FSMContext):
    await FindPottery.id.set()
    await callback.message.reply('Введите номер изделия', reply=False)
    await callback.answer()


async def find_info(message: types.Message, state: FSMContext):
    await state.finish()
    await sql_find_id(message, photo=True)


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Выберите, что хотите сделать:', reply_markup=adkb.kb_admin, reply=False)


@dp.callback_query_handler(text=['find_pottery', 'save_pottery', 'reset_pottery'], state="*", chat_id=ADMINS_ID)
async def find_id(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()


def register_handlers_admin_find(dp_in: Dispatcher):
    # dp_in.register_message_handler(cancel, commands=['cancel'], state='*')

    dp_in.register_message_handler(find_info, regexp=r"\d+", state=FindPottery.id, chat_id=ADMINS_ID)
