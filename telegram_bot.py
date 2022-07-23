from aiogram.utils import executor

from create_bot import dp
from data_Base import database
from data_Base.database import IsAdmin
from handlers import client
from handlers.admin import add_pottery, complete_pottery, find_pottery, menu, admins_list, add_admin


async def on_startup(_):
    print('Бот запущен')
    database.sql_start()


if __name__ == '__main__':
    find_pottery.register_handlers_admin_find(dp)
    add_pottery.register_handlers_admin_add_pottery(dp)
    complete_pottery.register_handlers_admin_change(dp)
    # menu.register_handlers_admin_menu(dp)

    client.register_handlers_client_menu(dp)

    dp.filters_factory.bind(IsAdmin)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
