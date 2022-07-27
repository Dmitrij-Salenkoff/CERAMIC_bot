import sqlite3 as sq

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter, Filter

from config import ADMINS_ID
from create_bot import bot
from utils import reply_template


class IsAdmin(BoundFilter):
    key = "admin_check"

    def __init__(self, admin_check):
        self.admin_check = admin_check

    async def check(self, message: types.Message) -> bool:
        # return len(cur.execute('SELECT * FROM admins WHERE id_tg=(?)', message.chat.id).fetchall()) > 0
        return True


# class IsAdmin(Filter):
#     key = "is_admin"
#
#     async def check(self, message: types.Message):
#         check = len(cur.execute('SELECT * FROM admins WHERE id_tg=(?)', (message.chat.id,)).fetchall()) > 0
#         print(check)
#         return check


def sql_start():
    global base, cur
    base = sq.connect('data_base.db')
    cur = base.cursor()
    if base:
        print('Database connected \n OK!')
    base.execute(' CREATE TABLE IF NOT EXISTS pottery ('
                 ' id_com INTEGER PRIMARY KEY AUTOINCREMENT,'
                 ' id TEXT NOT NULL,'
                 ' descr TEXT'
                 ')'
                 )

    base.execute(' CREATE TABLE IF NOT EXISTS admins ('
                 ' id_com INTEGER PRIMARY KEY AUTOINCREMENT,'
                 ' id_tg INTEGER NOT NULL,'
                 ' name TEXT,'
                 ' phone_number TEXT)'
                 )

    base.execute(' CREATE TABLE IF NOT EXISTS clients_pottery ('
                 ' id_com INTEGER PRIMARY KEY AUTOINCREMENT,'
                 ' client_id_tg TEXT,'
                 ' id TEXT NOT NULL)'
                 )

    cur.execute('REPLACE INTO admins(id_com, id_tg, name, phone_number) VALUES (?, ?, ?, ?)',
                tuple([1, ADMINS_ID[0], 'Дима Саленков', '8 985 909 2690']))

    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO pottery(id, descr) '
                    'VALUES (?, ?)',
                    (data['id'], data['descr']))
        base.commit()


async def sql_find_id(message: types.Message) -> bool:
    if len(cur.execute(f'SELECT * FROM pottery WHERE id = (?)', (message.text,)).fetchall()) > 0:
        for ret in cur.execute(f'SELECT * FROM pottery WHERE id = (?)', (message.text,)).fetchall():
            await message.reply('Изделие найдено!', reply=False)
            return True
    else:
        await message.reply('Таких изделий нет', reply=False)
        return False

    # await message.reply(f'Выберите, что хотите сделать:', reply_markup=keyboards.kb_admin, reply=False)


async def sql_complete_pottery(state: FSMContext, data: dict):
    for ret in cur.execute('SELECT *'
                           'FROM clients_pottery '
                           'INNER JOIN pottery '
                           'ON clients_pottery.id=pottery.id '
                           'WHERE clients_pottery.id = (?)', (data['id'],)).fetchall():
        rep, photo_id = reply_template(ret, columns=['id', 'photo'], cur=cur)

        await bot.send_message(ret[1], 'Ваше изделие готово!\n\n' + rep)
        if photo_id:
            await bot.send_photo(ret[1], photo_id)
    base.commit()


async def sql_check_client_id(message: types.Message):
    if len(cur.execute('SELECT * FROM clients_pottery WHERE id = (?)', (message.text,)).fetchall()) > 0:
        return True
    else:
        return False


async def sql_add_admin(message: types.Message, name='-', phone_number='-'):
    cur.execute(f'INSERT INTO admins(id_tg, name, phone_number) VALUES (?, ?, ?)',
                tuple([message.chat.id, name, phone_number]))
    base.commit()


async def sql_add_pottery_client(message: types.Message):
    if len(cur.execute('SELECT * FROM pottery WHERE id=(?)', (message.text,)).fetchall()) == 0:
        await message.reply('У нас нет таких изделий((', reply=False)

    elif len(cur.execute('SELECT * FROM clients_pottery WHERE id=(?) AND client_id_tg=(?)',
                         (message.text, message.chat.id)).fetchall()) > 0:
        await message.reply('Изделие уже в списке ваших изделий', reply=False)

    else:
        cur.execute(f'INSERT INTO clients_pottery(client_id_tg, id) VALUES (?, ?)',
                    tuple([message.chat.id, message.text]))
        base.commit()
        await message.reply('Изделие успешно добавлено в ваш список изделий!', reply=False)


async def sql_del_pottery(message: types.Message):
    # TODO: add check if rows haven`t found
    cur.execute('DELETE FROM clients_pottery WHERE id = (?) AND client_id_tg = (?)',
                (message.text, message.chat.id))
    await message.reply('Ваше изделие удалено из списка изделий!', reply=False)
    base.commit()


async def sql_client_find(message: types.Message):
    if len(cur.execute('SELECT *'
                       'FROM clients_pottery '
                       'INNER JOIN pottery '
                       'ON clients_pottery.id=pottery.id '
                       'WHERE client_id_tg = (?)',
                       (str(message.chat.id),)).fetchall()) == 0:
        await message.reply('У вас пустой список изделий(', reply=False)
    else:
        for ret in cur.execute('SELECT *'
                               'FROM clients_pottery '
                               'INNER JOIN pottery '
                               'ON clients_pottery.id=pottery.id '
                               'WHERE client_id_tg = (?)',
                               (str(message.chat.id),)).fetchall():
            rep, photo_id = reply_template(ret, columns=['id', 'name', 'photo', 'type', 'date'], cur=cur)
            if photo_id:
                await message.reply_photo(photo_id, reply=False)
            await message.reply(rep, reply=False)


async def sql_find_admins():
    if len(cur.execute('SELECT * FROM admins').fetchall()) > 0:
        rep = 'Админы: '
        for ret in cur.execute('SELECT * FROM admins').fetchall():
            rep += f'\nИмя: {ret[2]}, телефон: {ret[3]}'
    else:
        rep = ''
    return rep
