from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS_ID
from create_bot import dp
from data_Base.database import sql_find_id, sql_complete_pottery, sql_check_client_id


class ChangePottery(StatesGroup):
    id = State()
    accept = State()


@dp.callback_query_handler(text='complete_pottery', state=None)
async def change_stage(callback: types.CallbackQuery, state: FSMContext):
    await ChangePottery.id.set()
    await callback.message.reply('Введите номер изделия:', reply=False)
    await callback.answer()


async def change_id(message: types.Message, state: FSMContext):
    change = await sql_find_id(message)

    if await sql_check_client_id(message):
        if not change:
            await message.reply('Такого изделия нет', reply=False)
            await state.finish()
        else:
            await ChangePottery.accept.set()
            await message.reply('Отправить автору напоминание о готовности?', reply=False,
                                reply_markup=InlineKeyboardMarkup().add(
                                    InlineKeyboardButton(text='Да',
                                                         callback_data='complete_yes'),
                                    InlineKeyboardButton(text='Нет',
                                                         callback_data='complete_no'))
                                )
            async with state.proxy() as data:
                data['id'] = message.text
    else:
        await message.reply('Пользователей, подписавшихся на обновления, нет', reply=False)
        await state.finish()


@dp.callback_query_handler(text='complete_yes', state=ChangePottery.accept)
async def complete_yes(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await sql_complete_pottery(state, data=data)
    await state.finish()
    await callback.answer()


def register_handlers_admin_change(dp_in: Dispatcher):
    dp_in.register_message_handler(change_id, state=ChangePottery.id)

    dp_in.register_message_handler(change_stage, state=ChangePottery.accept)
