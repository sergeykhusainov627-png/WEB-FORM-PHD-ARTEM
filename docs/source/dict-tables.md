# Справочники НСИ: t-таблицы и поля (реестр)

Источник: таблица от заказчика (скриншот «кое-что собрал»), дополнено ТТ `ТТ_Анализ и выгрузка данных ТЭП.xlsx`.

Формат строки: `<объект> | <t-таблица> | <поле-ключ в t-таблице> | <join к D.поле> | <поле наименования> | примечание`

## Таблицы фактов и служебные

| Объект | t-таблица | Ключ | Примечание |
|---|---|---|---|
| TBL_PHD_FAP_MULT | TBL_FAP_MULT | — | факты: zsiu_indv, zvalue_sng, period, zphd_stat, key_connect |
| TBL_ZIDNFORM | TBL_ZIDNFORM | — | формы ТЭП СНГ (в запросе — CTE Forms_Agg) |
| DIC_TYPE_PERIOD | t2317517 | — | НСИ, тип периода |
| DICT_PHD_LEFT | t1913698 | `KEY` | НСИ, «шапка» записи: 76 колонок-аналитик + KEY (IS_TEMPORARY = 2) |
| DICT_PHD_GROUPS | на запросе | — | Табличный справочник, T_IDLNK |

## Справочники наименований (RDSD_*)

| Объект | t-таблица | Поле-ключ | time_dependent | Примечание |
|---|---|---|---|---|
| RDSD_ACTTYPE | t2320948 | acttype | datefrom, dateto | |
| RDSD_ACTVTS | t2494931 | code_value | — | код вида деятельности |
| RDSD_INDS | t1895280 | code | datefrom, dateto | **date_from содержит invalid_date** |
| RDSD_INFOSYSTEM | t1895288 | code_value | — | |
| RDSD_MATERIAL | t2321329 | material | — | |
| RDSD_OWNERS | t2364976 | key | — | **ключ забирать через связь в RDSD_INDS.owner** |
| RDSD_ZPH_OPLST | t2311610 | code | — | |
| RDSD_PLANT | t2312312 | plant | — | |
| RDSD_POSID | t2337709 | posid | — | |
| RDSD_PROFIT_CTR | t2320954 | profit_ctr | — | |
| RDSD_SOLDTO | t2301822 | code | — | |
| RDSD_UCVOLTLEVL | t2307584 | ucvoltlevl | — | |
| RDSD_VENDOR | t2322857 | vendor | — | наименование — `TXTMD` (по ТТ) |
| RDSD_Z_CL_NAPR | t2307947 | z_cl_napr | — | |
| RDSD_ZAVIATYPE | t2307768 | zaviatype | — | |
| RDSD_ZBUR_AREA | t2311573 | zbur_area | — | |
| RDSD_ZBUR_LU | t2320979 | code | — | |
| RDSD_ZBUR_PLST | t237842 | zbur_plst | — | |
| RDSD_ZCLSVOBOR | t2308461 | zclsvo_b or | — | |
| RDSD_ZEQUI | t2383584 | zequi | datefrom, dateto | |
| RDSD_ZFUNC_LOC | t2355739 | zfunc_loc | datefrom, dateto | |
| RDSD_ZGAZ_TYPE | t2290906 | code | — | |
| RDSD_ZHRGRPMO | t2306331 | zhrgrpmo | — | |
| RDSD_ZOBJEM | t2355657 | zobjem | — | |
| RDSD_ZORGU | t2355561 | zorgu | datefrom, dateto | |
| RDSD_ZPH_TEHK | t2311619 | code | — | |
| RDSD_ZPH_USR0 | t2310122 | zph_usr0 | zbegda, zendda | |
| RDSD_ZPHD_GRSR | t2311629 | zphd_grsr | — | |
| RDSD_ZPHD_SPR | t2335720 | zphd_spr | — | |
| RDSD_ZPHD_SR | t2356315 | zphd_sr | — | |
| RDSD_ZSHIFR | t2311391 | zshifr | — | |
| RDSD_ZSIU_FLD | t2308973 | zsiu_fld | — | |
| RDSD_ZSIU_TY | t2307875 | zsiu_ty | — | |
| RDSD_ZSKV_ST | t2311231 | zskv_st | — | |

## «Короткие» представления (SHORTCUT_*)

| Объект | t-таблица | Поле-ключ | Примечание |
|---|---|---|---|
| SHORTCUT_TO_RDSD_SOLDTO | t2301822 | code | то же представление SOLDTO (потребитель) |
| SHORTCUT_TO_RDSD_SOLDTO_2 | t2301822 | code | ЭСО физ (дальний) |
| SHORTCUT_TO_RDSD_SOLDTO_3 | t2301822 | code | потребитель |
| SHORTCUT_TO_RDSD_SOLDTO_4 | t2301822 | code | ЭСО покуп |
| SHORTCUT_TO_RDSD_SOLDTO_5 | t2301822 | code | сетевая компания |
| SHORTCUT_TO_RDSD_SOLDTO_6 | t2301822 | code | ген. заказчик |
| SHORTCUT_TO_RDSD_SOLDTO_7 | t2301822 | code | ген. подрядчик |
| SHORTCUT_TO_RDSD_SOLDTO_8 | t2301822 | code | ЗПКР СУБП |
| SHORTCUT_TO_RDSD_UCVOLTLEVL | t2307584 | key | уровень напряжения |

## Ещё нужно уточнить у заказчика

1. **Поле наименования** для каждого справочника (`TXTMD` / `NAME` / `SHORT_NAME`) — из ТТ известно для `RDSD_VENDOR` (`TXTMD`), для остальных нужно подтверждение.
2. **time_dependent-справочники** (`RDSD_ACTTYPE`, `RDSD_INDS`, `RDSD_ZEQUI`, `RDSD_ZFUNC_LOC`, `RDSD_ZORGU`, `RDSD_ZPH_USR0`): по какой дате выбирать актуальную запись — по году отчёта (`CALYEAR`), по дате закрытия периода (`ZBUR_KON`) или по `now()`?
3. `RDSD_INDS.date_from` содержит `invalid_date` — как обходить: отбрасывать такие записи (`WHERE date_from IS NOT NULL` / `date_from <> 'invalid_date'`) или подставлять значения по умолчанию?
4. `RDSD_OWNERS` — ключ владельца брать через `RDSD_INDS.owner` (t1895280), своего прямого поля в `DICT_PHD_LEFT` нет?
5. `DICT_PHD_GROUPS` («на запросе», `T_IDLNK`) — нужен ли он в отчёте и как к нему обращаться?
6. Поля с пустой колонкой F в ТТ (Год, МВЗ, Договор): выводить пары «ключ + наименование» (две одинаковые колонки) или только одну?
