from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ContentType

from config import password, ADMINS_ID
from create_bot import dp
from data_Base.database import sql_add_pottery_client, sql_client_find, sql_add_admin, sql_del_pottery
from utils import find_name_phone
from keyboards.admin_kb import kb_admin


class AddPotteryClient(StatesGroup):
    id = State()


class DelPotteryClient(StatesGroup):
    id = State()


class AddAdmin(StatesGroup):
    name_phone = State()


@dp.callback_query_handler(text='client_add', state=None)
async def client_add_pottery_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Введите номер изделия', reply=False)
    await callback.answer()
    await AddPotteryClient.id.set()


async def client_add_pottery_id(message: types.Message, state: FSMContext):
    if message.text == password:
        await message.reply('Введите имя-фамилию и телефон в формате\n{ФИО} / {телефон}', reply=False)
        await state.finish()
        await AddAdmin.name_phone.set()
    else:
        await sql_add_pottery_client(message)
        await state.finish()


async def admin_add_name_phone(message: types.Message, state:FSMContext):
    d = find_name_phone(message.text)
    await sql_add_admin(message, name=d['name'], phone_number=d['phone'])
    await message.reply('Вы стали админом!', reply=False, reply_markup=kb_admin)
    await state.finish()


@dp.callback_query_handler(text='client_list', state=None)
async def client_find_pottery_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await sql_client_find(callback.message)
    await callback.answer()


@dp.callback_query_handler(text='client_del', state=None)
async def client_del_pottery_menu_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Введите номер изделия', reply=False)
    await callback.answer()
    await DelPotteryClient.id.set()


async def client_del_pottery_id(message: types.Message, state: FSMContext):
    await sql_del_pottery(message)
    await state.finish()


# @dp.callback_query_handler()
# async def find_id(callback: types.CallbackQuery, state: FSMContext):
#     await callback.answer()


def register_handlers_client_menu(dp_in: Dispatcher):
    # dp_in.register_message_handler(menu, commands=['start', 'menu'])
    dp_in.register_message_handler(client_add_pottery_id, state=AddPotteryClient.id, content_types=ContentType.TEXT)
    dp_in.register_message_handler(client_del_pottery_id, state=DelPotteryClient.id, content_types=ContentType.TEXT)
    dp_in.register_message_handler(admin_add_name_phone, state=AddAdmin.name_phone, content_types=ContentType.TEXT)
