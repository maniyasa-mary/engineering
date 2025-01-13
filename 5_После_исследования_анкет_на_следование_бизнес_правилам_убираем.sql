-- 1 вариант
-- удаляем данные по анкетам, признанным несущественными для нашего исследования 
-- DELETE 
-- SELECT *
-- FROM data.form_data
-- WHERE id_form IN (1929215075, 1929186296)

-- 2 вариант 
-- создаем view в схеме data
-- в котором учтем "удаленные" анкеты
-- в этом случае все данные у нас сохраняются
CREATE VIEW data.v_form_data AS

SELECT * 
FROM data.form_data
WHERE id_form NOT IN (1929215075, 1929186296)
