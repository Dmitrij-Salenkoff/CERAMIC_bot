from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import dp
from data_Base.database import sql_find_admins
from keyboards import admin_kb as adkb


@dp.message_handler(commands=['start', 'menu'], state=None)
async def menu(message: types.Message):
    if await sql_find_admins():
        await message.reply('Добрый день!', reply_markup=adkb.kb_admin_reply, reply=False)
        await message.reply(f'Выберите, что хотите сделать:', reply_markup=adkb.kb_admin, reply=False)
    else:
        await message.reply('Добрый день!\nВас приветсвует бот керамической мастерской VolnaCeramics!', reply=False)
        await message.reply(f'Выберите, что вы хотите сделать:',
                            reply=False,
                            reply_markup=InlineKeyboardMarkup().add(
                                InlineKeyboardButton(text='Список работ',
                                                     callback_data='client_list'),
                                InlineKeyboardButton(text='Добавить работу',
                                                     callback_data='client_add'),
                                InlineKeyboardButton(text='Удалить работу',
                                                     callback_data='client_del')
                            ))

