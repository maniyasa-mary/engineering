# -- Вариант 2 
# -- Располагаем скачанный json в подготовленной папке
# -- Распарсиваем полученный json средствами Python
# -- Запись в БД всего набора строк разом, массовый ввод. 
# -- Используется, если нбх загрузить набор строк разом, например, анкеты от прошедшего опроса,
# -- обычно такие строки по бизнес-логике считаются новыми, обеспечиваются новым суррогатным ключом 
# -- и/или содержат собственный уникальный ключ
# -- В случае необходимости к sql-команде добавляется проверка на существование, например, составного ключа
# -- пишется или хранимая процедура, обновляющая строку или UPSERT

import json
import psycopg2
from psycopg2 import sql

# -- подключение к БД созданным на сервере пользователем
# -- с разрешенными правами
connection = psycopg2.connect(database='funcdrink', user='func', password='func', host='192.168.*.*', port = 5432)

# -- функция преобразовывает переданный объект типа list
# -- в объект типа dict, разворачиваем список из 110 строк 
# -- в список из ответов на каждый вопрос, включая пустые
def converter(item: list):
    anket = {}
    for i in item:
        anket[i[0]] = i[1]
    return anket

# -- функция формирует объект,  подготовленный для подстановки набором значений
# -- содержит 4 элемента 
# -- ID анкеты, Время создания, Текст вопроса, Текст ответа
def to_questions_list(anket):
    result = []
    for anket in ankets:
        for question in anket.items():
            if question[0] == "ID" or question[0] == "Время создания":
                continue
            result.append((anket['ID'], anket['Время создания'], question[0], question[1]))
    return result

with open(r"""D:\путь к файлу\имя файла.json""", 'r', encoding="utf8") as f:
    # -- прочитали файл
    data = json.loads(f.read())
    # -- развернули полученный набор
    ankets = list(map(converter, data))
    # -- формируем набор строк, который будет вставлен разом
    # for anket in ankets:
    all_questions = to_questions_list(ankets)
    # print(all_questions)
    # -- работаем с БД
    with connection.cursor() as cur_to:
        # -- обеспечиваем закрытие курсора после выполнения команды
        connection.autocommit = True
        # -- формируем строку-команду
        insert = sql.SQL('INSERT INTO funcdrink.data.form_land("id_form","date_create","question_text", "answer_text") VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, all_questions))
        )
        # -- исполняем массовый ввод - приземление данных
        cur_to.execute(insert)

# -- как вариант здесь можно вызвать запуск хранимых процедур для обработки внутри БД
# -- в нашем варианте они запускались вручную скриптами после визуальной оценки данных
# -- и формирования бизнес-правил

# -- например
# with connection:
#     with connection.cursor() as date_reload:
#         # date_reload.execute("call data.do_update_address()")
#         # date_reload.execute("call data.do_update_objects()")

# -- закрыли 
connection.close()