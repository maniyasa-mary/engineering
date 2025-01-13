
-- перенос данных в "чистую" таблицу 
-- раскомментарить перед запуском
-- INSERT INTO data.form_data (id_fl, id_form, date_create, question_group, question_unit, question, question_answer, answer_text)

SELECT 
-- для связи с land-таблицей, физический FK не делаем, 
-- нет необходимости быстрой связки
fl."id",-- id анкеты
fl.id_form,-- дата создания анкеты
fl.date_create,
-- выделение блока вопросов, выборка части строки до первого пробела и части до точки
NULLIF(split_part(split_part(fl.question_text, ' ', 1), '.', 1), '')::int4 AS question_group,
-- выделение номера вопроса внутри блока, выборка части строки до первого пробела и части после точки
NULLIF(split_part(split_part(fl.question_text, ' ', 1), '.', 2), '')::int4 AS question_unit,-- выборка текста вопроса - часть после первого пробела до символа /
split_part(REPLACE(fl.question_text, split_part(fl.question_text, ' ', 1), ''), ' /', 1) AS question,
-- выборка варианта ответа на вопрос - часть после первого пробела после символа /
split_part(REPLACE(fl.question_text, split_part(fl.question_text, ' ', 1), ''), ' /', 2) AS question_answer,
-- убираем ответы, содержащие один символ как неинформационные (выявленные визуально)
CASE WHEN length(NULLIF(fl.answer_text, '')) < 2 THEN NULL ELSE NULLIF(fl.answer_text, '') END AS answer_text

FROM data."form_land" fl

