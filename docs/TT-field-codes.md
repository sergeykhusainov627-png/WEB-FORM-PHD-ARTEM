# Откуда берутся коды аналитик (по ТТ)

Источник: ТТ, лист **«Перечень полей отчета»** (`ТТ_Анализ и выгрузка данных ТЭП.xlsx`).
Для каждого поля отчёта в ТТ заданы ДВЕ пары «источник + поле»:

* **наименование** — столбцы C/D: справочники `RDSD_*` (поле `NAME`/`TXTMD`);
* **код** — столбцы F/G: таблица фактов `DICT_PHD_LEFT` (колонка E «да/нет» говорит, есть ли отдельный код).

Запрос `QRY_PHD_MULT_DATA_COPY1` построен на вьюхе `VIEW_PHD_MULT_LEFT`, поэтому поля-коды
из `DICT_PHD_LEFT` в ней доступны напрямую; исключения (СП, вид деятельности, номер договора)
берутся из `TBL_PHD_FAP_MULT`, `RDSD_INDS`, `TBL_IDLNK` — для вида деятельности в запросе уже
есть подзапрос к справочнику (`SELECT t.ACTVTS FROM t1895280 t ... AS "Код вида деятельности"`).

## Поля с отдельным кодом (E = «да») — 41 шт.

| Поле отчёта | Наименование: источник.поле | Код: источник.поле | id аналитики (сверить) |
|---|---|---|---|
| СП | RDSD_PLANT.TXTMD | TBL_PHD_FAP_MULT.SP |  |
| Поставщик | RDSD_VENDOR.TXTMD | DICT_PHD_LEFT.VENDOR |  |
| Заказчик | RDSD_SOLDTO.NAME | DICT_PHD_LEFT.KEY |  |
| Регион | RDSD_ZHRGRPMO.NAME | DICT_PHD_LEFT.ZHRGRPMO |  |
| Вид производства | RDSD_PROFIT_CTR.NAME | DICT_PHD_LEFT.PROFIT_CTR |  |
| Орг.единица | RDSD_ZORGU.NAME | DICT_PHD_LEFT.ZORGU |  |
| Рабочее место исполнителя | RDSD_ZPH_USR0.NAME | DICT_PHD_LEFT.CODE_ZPH_USR0 |  |
| Вид работ | RDSD_ACTTYPE.NAME | DICT_PHD_LEFT.ACTTYPE |  |
| Единица оборудования | RDSD_ZEQUI.NAME | DICT_PHD_LEFT.ZEQUI |  |
| Класс вида оборудования | RDSD_ZCLSVOBOR.NAME | DICT_PHD_LEFT.ZCLSVOBOR |  |
| Материал | RDSD_MATERIAL.NAME | DICT_PHD_LEFT.MATERIAL |  |
| Тех.место | RDSD_ZFUNC_LOC.NAME | DICT_PHD_LEFT.ZFUNC_LOC |  |
| Месторождение | RDSD_ZSIU_FLD.NAME | DICT_PHD_LEFT.ZSIU_FLD |  |
| СПП | RDSD_POSID.NAME | DICT_PHD_LEFT.POSID |  |
| ИАС | RDSD_INFOSYSTEM.NAME | DICT_PHD_LEFT.ZLIB_INFS |  |
| Тип периода | DIC_TYPE_PERIOD.NAME | DICT_PHD_LEFT.PERIOD_TY |  |
| Потребитель | SHORTCUT_TO_RDSD_SOLDTO_3.NAME | DICT_PHD_LEFT.ZPHD_USL1 |  |
| ЭСО физ | SHORTCUT_TO_RDSD_SOLDTO.NAME | DICT_PHD_LEFT.ZDEBITOR |  |
| Эсо физ (даль) | SHORTCUT_TO_RDSD_SOLDTO_2.NAME | DICT_PHD_LEFT.ZPH_ESO2 |  |
| ЭСО покуп | SHORTCUT_TO_RDSD_SOLDTO_4.NAME | DICT_PHD_LEFT.ZPH_EPOK |  |
| Сетевая компания | SHORTCUT_TO_RDSD_SOLDTO_5.NAME | DICT_PHD_LEFT.ZPHD_SK |  |
| Ур.напр. | RDSD_UCVOLTLEVL.NAME | DICT_PHD_LEFT.UCVOLTLEVL |  |
| Ур.напр.продаж | SHORTCUT_TO_RDSD_UCVOLTLEVL.NAME | DICT_PHD_LEFT.ZUCVOLTTR |  |
| Класс напр. | RDSD_Z_CL_NAPR.NAME | DICT_PHD_LEFT.Z_CL_NAPR |  |
| Тип тарифов | RDSD_ZSIU_TY.NAME | DICT_PHD_LEFT.ZSIU_TY |  |
| Участок недр | RDSD_ZBUR_LU.NAME | DICT_PHD_LEFT.ZBUR_LU |  |
| Пощадь бурения | RDSD_ZBUR_AREA.NAME | DICT_PHD_LEFT.ZBUR_AREA |  |
| Куст | DICT_PHD_LEFT.ZKUST | DICT_PHD_LEFT.ZSKV_KUST |  |
| Пласт | RDSD_ZBUR_PLST.ZBUR_PLST | DICT_PHD_LEFT.ZBUR_PLST |  |
| Мероприятие | DICT_PHD_LEFT.ZPHD_COMM | DICT_PHD_LEFT.ZPHD_COMM |  |
| Ген.подрядчик | SHORTCUT_TO_RDSD_SOLDTO_7.NAME | DICT_PHD_LEFT.ZGEN_POD |  |
| Ген.заказчик | SHORTCUT_TO_RDSD_SOLDTO_6.NAME | DICT_PHD_LEFT.ZGEN_ZAK |  |
| Субподрядчик | SHORTCUT_TO_RDSD_SOLDTO_8.NAME | DICT_PHD_LEFT.ZPKR_SUBP |  |
| Объект исследования | RDSD_ZPHD_SR.NAME | DICT_PHD_LEFT.ZPHD_SR |  |
| Группировка сред ЭМ | RDSD_ZPHD_GRSR.NAME | DICT_PHD_LEFT.ZPHD_GRSR |  |
| Вид газа | RDSD_ZGAZ_TYPE.NAME | DICT_PHD_LEFT.ZGAZ_TYPE |  |
| Тип воздушного судна | RDSD_ZAVIATYPE.NAME | DICT_PHD_LEFT.ZAVIATYPE |  |
| ГТМ (Универсальный справочник) | RDSD_ZPHD_SPR.NAME, по ZPHD_NOP1 при ZPHD_SPR = GTM_SKV | DICT_PHD_LEFT.ZPHD_NOP1 при ZPHD_SPR = GTM_SKV |  |
| Вид деятельности | RDSD_ACTVTS.SNAME | RDSD_INDS.ACTVTS |  |
| Вид показателя | DICT_PHD_GROUPS.NAME | TBL_IDLNK.ID1 |  |
| Владелец ТЭП | RDSD_OWNERS.SHORT_NAME | RDSD_INDS.OWNER |  |

## Поля без отдельного кода (E = «нет») — 19 шт.

| Поле отчёта | Источник.поле |
|---|---|
| Год | TBL_PHD_FAP_MULT.YEAR |
| ТЭП | DICT_PHD_LEFT.ZLIB_INDC |
| Наименование ТЭП | RDSD_INDS.SNAME |
| Ед.измерения | DICT_PHD_LEFT.ACT_UNIT |
| МВЗ | DICT_PHD_LEFT.COSTCENTER |
| Договор | DICT_PHD_LEFT.ZPHD_DOG |
| Договор по воде | DICT_PHD_LEFT.ZDOGLINK |
| Скважина (геол.ном) | DICT_PHD_LEFT.Z_SKV_GEO |
| Дата начала бурения | DICT_PHD_LEFT.ZBUR_BEG |
| Дата окончания бурения | DICT_PHD_LEFT.ZBUR_END |
| Пилотный ствол | DICT_PHD_LEFT.ZPILOT |
| Примечание | DICT_PHD_LEFT.ZINDTXT1 |
| Шифр проекта стройки | RDSD_ZSHIFR.NAME |
| Номер объекта ЭМ | RDSD_ZOBJEM.NAME |
| Дата ввода скв. в экспл. | DICT_PHD_LEFT.ZPHD_NCH |
| Дата проведения ГТМ | DICT_PHD_LEFT.ZPHD_KON |
| Формы  отчетов | TBL_ZIDNFORM.ZF_NUMB |
| ТЭП-источник | TBL_ZIDNFORM.ZF_NUMB |
| Наименование ТЭП-источника | RDSD_INDS.SNAME |

## Что уже прописано в модуле формы

`_codeIds` (аналитика → поле-код): `PLANT → SP`, `SOLD_TO → KEY`, `ZPH_USR2 → CODE_ZPH_USR0`,
`PERIOD_TYPE → PERIOD_TY`. Остальные пары нужно подтвердить: ключом должен быть идентификатор
аналитики, который уходит в `ANALYTIC_SET` (нижний регистр), значением — поле-код из колонки G.
