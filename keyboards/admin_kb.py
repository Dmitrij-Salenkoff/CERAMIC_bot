from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


kb_admin_reply = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('/menu')],
        [KeyboardButton('/cancel')]
    ], one_time_keyboard=True, resize_keyboard=True)


kb_admin = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(text='Добавить изделие', callback_data='add_pottery')
b2 = InlineKeyboardButton(text='Отправить изделие', callback_data='complete_pottery')
b3 = InlineKeyboardButton(text='Найти изделие', callback_data='find_pottery')
b5 = InlineKeyboardButton(text='Список админов', callback_data='menu_admins_list')
b6 = InlineKeyboardButton(text='Добавить админа', callback_data='menu_add_admin')
kb_admin.row(b1).row(b3, b2).row(b5, b6)

kb_admin_save = InlineKeyboardMarkup()
s1 = InlineKeyboardButton(text='Сохранить изделие', callback_data='save_pottery')
s2 = InlineKeyboardButton(text='Не сохранять изделие', callback_data='reset_pottery')
kb_admin_save.row(s1, s2)

