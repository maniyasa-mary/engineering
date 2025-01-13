# -- Вариант 1 
# -- Располагаем скачанный json в подготовленной папке
# -- Распарсиваем полученный json средствами Python
# -- Запись в БД по 1 строке. 
# -- Используется в случае небольших обновлений, автоматически прилетающих изменений и проч
# -- В случае изменений к sql-команде добавляется проверка на существование такого ключа
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

with open(r"""D:\путь к файлу\имя файла.json""", 'r', encoding="utf8") as f:
    # -- прочитали файл
    data = json.loads(f.read())
    # -- преобразовали полученный набор
    ankets = list(map(converter, data))
    # -- идем по строкам, пропуская строки-заголовки анкеты
    # -- у нас есть к ним доступ с верхнего цикла >>--for anket in ankets--<<
    for anket in ankets:
        for question in anket.items():
            if question[0] == "ID" or question[0] == "Время создания":
                continue
            # print("|".join([anket['ID'], question[0], question[1]]))
            
            # -- формируем строку-INSERT для передачи исполняемой текстовой команды в БД
            # -- подставляем вместо {} набор из элементов разобранной строки-ответа  
            # -- anket['ID'] - идентификатор анкеты
            # -- question[0], question[1] - текстовый массив [Вопрос, ответ]
            with connection.cursor() as cur_to:
                connection.autocommit = True
                insert = sql.SQL('INSERT INTO funcdrinc.data.form_land("id_form","question_text", "answer_text") VALUES ({})').format(
                    sql.SQL(',').join([sql.Literal(anket['ID']), sql.Literal(question[0]), sql.Literal(question[1])])
                )
                # -- запуск команды на исполнение
                cur_to.execute(insert)
# -- закрыли 
connection.close()
