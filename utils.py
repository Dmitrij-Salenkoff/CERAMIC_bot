import re


months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
          'декабря']


def info_to_dict(string: str) -> dict:
    # TODO: add try except
    out = {'phone_number': re.findall('\+?\d \d{3} [\d-]{9}', string)[0].lstrip().rstrip(),
           'price': re.findall('(по \d+)', string)[0][3:].lstrip().rstrip(),
           'time_start': re.findall('\d?\d:\d{2}', string)[0].lstrip().rstrip(),
           'time_end': re.findall('\d?\d:\d{2}', string)[1].lstrip().rstrip(),
           'name': re.findall("\+?\w*[ \+]\d?", string)[0].lstrip().rstrip(),
           'type': re.findall("\w* ", string)[1].lstrip().rstrip()}

    place_month = [(string.find(months[i]), months[i]) for i in range(len(months)) if string.find(months[i]) > 0][0]
    out['date'] = string[place_month[0] - 3:place_month[0] + len(place_month[1])].lstrip().rstrip()

    return out



def reply_template(row, columns, cur):
    columns_pottery_db = [col[0] for col in cur.description]
    reply_arr = dict(zip(columns_pottery_db, row))

    rep = 'Информация о работе:'

    if 'id' in columns:
        rep += f'\nНомер изделия: {reply_arr["id"]}'
    if 'name' in columns:
        rep += f'\nИмя автора: {reply_arr["name"]}'
    if 'type' in columns:
        rep += f'\nТип занятия: {reply_arr["type"]}'
    if 'date' in columns:
        rep += f'\nДата изготовления: {reply_arr["date"]}'

    photo_id = False
    if 'photo_id' in columns:
        if reply_arr['photo_id'] == '-':
            rep += '\n\nФото нет'
        else:
            photo_id = reply_arr['photo_id']

    return rep, photo_id


def find_name_phone(string: str) -> dict:
    dict = {}
    dict['name'] = string.partition('/')[0].lstrip().rstrip()
    dict['phone'] = string.partition('/')[2].lstrip().rstrip()
    return dict

# print(find_name_phone('Sergay/8 985 909 2690'))
# print(find_name_phone('Sergay/89859092690'))
