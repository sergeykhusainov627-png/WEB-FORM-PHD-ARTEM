/*
   Запрос-генератор значений для параметров EXTRA_FIELDS и EXTRA_NAMES.
   Подключается как источник справочника в редакторе параметров (как сейчас сделано для ANALYTIC_SET).

   Колонки результата:
     SORT      - порядок (период, затем тип данных, затем вид колонки) — по нему сортируется справочник
     PERIOD    - подпись периода
     DATA_TYPE - наименование типа данных из DICT_DATA_TYPE (таблица t117604)
     KIND      - вид колонки: значение / статус / значение с нач.года / статус с нач.года
     EXPR      - ЗНАЧЕНИЕ для параметра EXTRA_FIELDS (готовый фрагмент SELECT с псевдонимом)
     NAME      - ЗНАЧЕНИЕ для параметра EXTRA_NAMES (тот же псевдоним в кавычках)

   Типы данных берутся целиком из справочника DICT_DATA_TYPE (таблица t117604), периоды — из списка ниже.
   Число строк = 17 периодов x K типов x 4 вида колонок.
*/
WITH P(ord, caption, cond) AS (VALUES
        (1, 'Январь', 'period = 1'),
        (2, 'Февраль', 'period = 2'),
        (3, 'Март', 'period = 3'),
        (4, 'Апрель', 'period = 4'),
        (5, 'Май', 'period = 5'),
        (6, 'Июнь', 'period = 6'),
        (7, 'Июль', 'period = 7'),
        (8, 'Август', 'period = 8'),
        (9, 'Сентябрь', 'period = 9'),
        (10, 'Октябрь', 'period = 10'),
        (11, 'Ноябрь', 'period = 11'),
        (12, 'Декабрь', 'period = 12'),
        (13, 'I кв.', 'period IN (13)'),
        (14, 'II кв.', 'period IN (14)'),
        (16, 'III кв.', 'period IN (16)'),
        (18, 'IV кв.', 'period IN (18)'),
        (19, 'Год', 'period IN (19)')
),
T(ord, id, name) AS (
    SELECT ord, id, name FROM t117604
),
K(ord, suffix, agg, measure) AS (VALUES
        (1, '', 'SUM', 'zsiu_indv'),
        (2, '. Статус', 'MAX', 'zphd_stat'),
        (3, '. С нач.года', 'SUM', 'zvalue_sng'),
        (4, '. С нач.года. Статус', 'MAX', 'zphd_stat')
)
SELECT
    p.ord * 100 + t.ord * 10 + k.ord                       AS "SORT",
    p.caption                                              AS "PERIOD",
    t.name                                                 AS "DATA_TYPE",
    CASE k.ord WHEN 1 THEN 'значение' WHEN 2 THEN 'статус'
               WHEN 3 THEN 'значение с нач.года' ELSE 'статус с нач.года' END AS "KIND",
    k.agg || '(' || k.measure || ') FILTER (WHERE ' || p.cond ||
        ' AND ztypeind = ''' || t.id || ''') AS "' || p.caption || k.suffix || ' (' || t.name || ')"' AS "EXPR",
    '"' || p.caption || k.suffix || ' (' || t.name || ')"'   AS "NAME"
FROM P p
CROSS JOIN T t
CROSS JOIN K k
ORDER BY p.ord, t.ord, k.ord;
