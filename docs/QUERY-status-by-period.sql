-- Статусы по периодам для запроса QRY_PHD_MULT_DATA_COPY1 (ветка Main_Data).
-- Куда вставлять: в SELECT ветки Main_Data, сразу после блока значений
-- (после строки "Год. С нач.года"), перед закрывающей скобкой и FROM VIEW_PHD_MULT_LEFT v.
--
-- Логика зеркальна показателю: значение разнесено по периодам через FILTER (WHERE period = N),
-- статус разносится так же. ZPHD_STAT — колонка вьюхи VIEW_PHD_MULT_LEFT (по ней же идёт
-- фильтр AND (ZPHD_STAT IN (:ZPHD_STAT) OR COALESCE(:ZPHD_STAT,'')='')), поэтому берём её как есть.
--
-- Если в одном периоде в группе встречается несколько статусов, MAX вернёт старший по алфавиту.
-- Варианты: MIN(zphd_stat) или STRING_AGG(DISTINCT zphd_stat, ', ').

    MAX(zphd_stat) FILTER (WHERE period = 1       ) AS "Январь. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 2       ) AS "Февраль. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 3       ) AS "Март. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 4       ) AS "Апрель. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 5       ) AS "Май. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 6       ) AS "Июнь. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 7       ) AS "Июль. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 8       ) AS "Август. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 9       ) AS "Сентябрь. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 10      ) AS "Октябрь. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 11      ) AS "Ноябрь. Статус",
    MAX(zphd_stat) FILTER (WHERE period = 12      ) AS "Декабрь. Статус",
    MAX(zphd_stat) FILTER (WHERE period IN (13)   ) AS "I кв.. Статус",
    MAX(zphd_stat) FILTER (WHERE period IN (14)   ) AS "II кв.. Статус",
    MAX(zphd_stat) FILTER (WHERE period IN (16)   ) AS "III кв.. Статус",
    MAX(zphd_stat) FILTER (WHERE period IN (18)   ) AS "IV кв.. Статус",
    MAX(zphd_stat) FILTER (WHERE period IN (19)   ) AS "Год. Статус"

-- Подписи колонок: "<период>. Статус". Если нужен и второй набор (С нач.года), добавьте такой же
-- блок с подписями "<период>. С нач.года. Статус" — значения статусов будут те же.
--
-- Чтобы статусы не показывались без чек-бокса «Выводить информацию по статусам», модуль отчёта
-- может пропускать эти колонки: для этого форме нужно передавать признак (см. docs/WHAT-TO-DEPLOY.md,
-- параметр P_STATUS_FIELDS = 1/0). Пока признак не заведён — колонки выводятся всегда.
