from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType

from config import ADMINS_ID
from create_bot import dp
from data_Base.database import sql_add_command
from keyboards import admin_kb as adkb
from utils import info_to_dict


class AddPottery(StatesGroup):
    id = State()
    photo = State()
    info = State()
    save = State()


@dp.callback_query_handler(text='add_pottery', state=None)
async def add_pottery_state(callback: types.CallbackQuery, state: FSMContext):
    await AddPottery.id.set()
    await callback.message.reply('Введи номер изделия', reply=False)
    await callback.answer()


@dp.callback_query_handler(text='add_pottery', state="*")
async def add_pottery_state(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()


async def add_id(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text

    await AddPottery.photo.set()
    await message.reply('Отправьте фотографию или пропустить /skip', reply=False)


async def add_skip_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = '-'
    await AddPottery.info.set()
    await message.reply('Отправьте данные из гугл-календаря', reply=False)


async def add_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await AddPottery.info.set()
    await message.reply('Отправьте данные из гугл-календаря', reply=False)


async def add_info(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['descr'] = message.text
        data.update(data)

    reply = f'Информация о работе: \n\n' \
            f'Номер изделия: {data["id"]} \n' \
            f'Строчка из гугла: {data["descr"]}'

    if data['photo'] == '-':
        await message.reply(reply + f'\nФото нет', reply=False, reply_markup=adkb.kb_admin_save)
    else:
        await message.reply_photo(data['photo'], reply=False)
        await message.reply(reply, reply=False, reply_markup=adkb.kb_admin_save)
    await AddPottery.save.set()


@dp.callback_query_handler(text='save_pottery', state=AddPottery.save)
async def add_save(callback: types.CallbackQuery, state: FSMContext):
    await sql_add_command(state)
    await callback.message.reply('Изделие добавлено!', reply=False)
    await callback.message.reply('Выберите, что хотите сделать:', reply_markup=adkb.kb_admin, reply=False)
    await callback.answer()
    await state.finish()


@dp.callback_query_handler(text='reset_pottery', state=AddPottery.save)
async def add_reset(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply('Изделие удалено!', reply=False)
    await callback.message.reply('Выберите, что хотите сделать:', reply_markup=adkb.kb_admin, reply=False)
    await callback.answer()
    await state.finish()


def register_handlers_admin_add_pottery(dp_in: Dispatcher):
    dp_in.register_message_handler(add_id, regexp=r"\d", state=AddPottery.id)

    dp_in.register_message_handler(add_skip_photo, commands=['skip'], state=AddPottery.photo)
    dp_in.register_message_handler(add_photo, state=AddPottery.photo, content_types=ContentType.PHOTO)

    dp_in.register_message_handler(add_info, state=AddPottery.info, content_types=ContentType.TEXT)
