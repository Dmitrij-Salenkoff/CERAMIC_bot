from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS_ID
from create_bot import dp
from data_Base.database import sql_find_admins
from keyboards import admin_kb as adkb


class FSMcontex:
    pass


@dp.message_handler(commands=['start', 'menu'], state="*")
async def menu(message: types.Message, state: FSMcontex):
    await state.finish()
    if message.chat.id in ADMINS_ID:
        await message.reply('Добрый день!', reply_markup=adkb.kb_admin_reply, reply=False)
        await message.reply(f'Выберите, что хотите сделать:', reply_markup=adkb.kb_admin, reply=False)
    else:
        await message.reply('Добрый день!\nВас приветсвует бот керамической мастерской VolnaCeramics!', reply=False)
        await message.reply(f'Выберите, что вы хотите сделать:',
                            reply=False,
                            reply_markup=InlineKeyboardMarkup().add(
                                InlineKeyboardButton(text='Добавить работу',
                                                     callback_data='client_add')
                            ))
