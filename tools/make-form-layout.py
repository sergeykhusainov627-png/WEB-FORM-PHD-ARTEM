# make-form-layout.py — собирает макет представления веб-формы
# WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV по модулю формы и ТЗ (ТТ_Анализ и выгрузка данных ТЭП.xlsx).
#
# В выгрузке окружения (.pefx) визуальной части формы нет — только модуль, поэтому макет
# восстанавливается из: (1) объявлений и обработчиков модуля, (2) листов ТТ «Разделы СЭ - Условия
# выборки» и «СЭ - поля для вывода», (3) скриншотов формы. Всё, что не подтверждено, помечается.
#
# Запуск: python tools/make-form-layout.py > docs/form-layout.html
import io, re, sys

MODULE = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'

src = io.open(MODULE, encoding='utf-8').read().replace('\r\n', '\n')

declared = {}                                     # имя -> тип
for m in re.finditer(r'^\t([A-Za-z_]\w*)\s*:\s*(Web\w+)\s*;', src, re.M):
    declared[m.group(1)] = m.group(2)

handlers = set()                                  # контролы, у которых есть обработчик <Имя>On<Событие>
for m in re.finditer(r'^\t+Sub\s+([A-Za-z_]\w*)On[A-Za-z0-9_]*\s*;', src, re.M):
    handlers.add(m.group(1))

field_ids = {m.group(1): m.group(2) for m in re.finditer(r'_fieldIds\.Add\("([^"]+)",\s*"([^"]+)"\)', src)
             if not m.group(0).strip().startswith('//')}
wired_cb = set(field_ids)

# combo -> параметр(ы), которые оно пишет
combo_param = {}
for m in re.finditer(r'^\tSub (D_\w+)OnSelectionChange;\n\tBegin\n(.*?)\n\tEnd Sub \1;', src, re.M | re.S):
    name, body = m.group(1), m.group(2)
    ps = re.findall(r'SetParamSafe\(\s*"([^"]+)"', body)
    ps += re.findall(r'SetParamValueFromSelection\(\s*"([^"]+)"', body)
    ps += re.findall(r'UpdateOpenDefHlinkFromSelection\(\s*"([^"]+)"', body)
    combo_param[name] = sorted(set(ps))

# ---------------------------------------------------------------- содержимое макета
# (раздел, подпись по ТТ, контрол в модуле, справочник по ТТ, примечание)
CONDITIONS = [
    ('Основные данные', [
        ('Справочник статусов', 'D_ZPHD_STAT', 'RDSD_ZPHD_STAT', ''),
        ('Поставщик', 'D_VENDOR', 'RDSD_VENDOR', ''),
        ('Заказчик', 'D_SOLD_TO', 'RDSD_SOLDTO', ''),
        ('Регион', 'D_ZHRGRPMO', 'RDSD_ZHRGRPMO', ''),
        ('Вид производства', 'D_PROFIT_CTR', 'RDSD_PROFIT_CTR', ''),
        ('МВЗ', 'D_COSTCENTER', 'RDSD_COSTCENTER', ''),
        ('Орг.единица', 'D_ZORGUNIT', 'RDSD_ZORGU', ''),
        ('Рабочее место исполнителя', 'D_ZPH_USR2', 'RDSD_ZPH_USR0', ''),
        ('Вид работ', 'D_ACTTYPE', 'RDSD_ACTTYPE', ''),
        ('Единица оборудования', 'D_ZEQUI', 'RDSD_ZEQUI', ''),
        ('Класс вида оборудования', 'D_ZCLSVOBOR', 'RDSD_ZCLSVOBOR', ''),
        ('Материал', 'D_MATERIAL', 'RDSD_MATERIAL', ''),
        ('Тех.место', 'D_ZFUNC_LOC', 'RDSD_ZFUNC_LOC', ''),
        ('Месторождение', 'D_ZSIU_FLD', 'RDSD_ZSIU_FLD', ''),
        ('СПП', 'D_POSID', 'RDSD_POSID', ''),
        ('ИАС', 'D_ZLIB_INFS', 'RDSD_INFOSYSTEM', ''),
        ('Тип периода', 'D_PERIOD_TYPE', 'DIC_TYPE_PERIOD', ''),
    ]),
    ('Энергоснабжение', [
        ('Договор Энерго', 'D_ZPHD_DOG', 'RDSD_ZPHD_DOG', 'в ТТ «надо сделать справочник ZPHD_DOG» — справочник в выгрузке есть'),
        ('Потребитель', 'D_ZPHD_USL1', 'SHORTCUT_TO_RDSD_SOLDTO_3', ''),
        ('ЭСО физ', 'D_ZDEBITOR', 'SHORTCUT_TO_RDSD_SOLDTO', ''),
        ('Эсо физ (даль)', 'D_ZPH_ESO2', 'SHORTCUT_TO_RDSD_SOLDTO_2', ''),
        ('ЭСО покуп', '—', 'SHORTCUT_TO_RDSD_SOLDTO_4', 'контрола нет; параметра ZPH_EPOK нет и в запросе'),
        ('Сетевая компания', 'D_ZPHD_SK', 'SHORTCUT_TO_RDSD_SOLDTO_5', ''),
        ('Ур.напр.', 'D_UCVOLTLEVL', 'RDSD_UCVOLTLEVL', ''),
        ('Ур.напр.продаж', 'D_ZUCVOLTTR', 'SHORTCUT_TO_RDSD_UCVOLTLEVL', ''),
        ('Класс напр.', 'D_Z_CL_NAPR', 'RDSD_Z_CL_NAPR', ''),
        ('Тип тарифов', 'D_ZSIU_TY', 'RDSD_ZSIU_TY', ''),
        ('Договор по воде', 'D_ZDOGLINK', 'RDSD_ZDOGLINK', ''),
    ]),
    ('Геология и бурение', [
        ('Участок недр', 'D_ZBUR_LU', 'RDSD_ZBUR_LU', ''),
        ('Площадь бурения', 'D_ZBUR_AREA', 'RDSD_ZBUR_AREA', ''),
        ('Куст', 'D_ZSKV_KUST', 'RDSD_ZSKV_KUST', ''),
        ('Скважина (геол.ном)', 'D_Z_SKV_GEO', 'RDSD_Z_SKV_GEO', ''),
        ('Пласт', 'D_ZBUR_PLST', 'RDSD_ZBUR_PLST', ''),
        ('Технология отбора керна', 'D_ZPH_TEHK', 'RDSD_ZPH_TEHK', ''),
        ('Струк. особенности пласта', 'D_ZPH_OPLST', 'RDSD_PH_OPLST', 'справочник по ТТ — RDSD_PH_OPLST'),
        ('Мероприятие', '—', 'текстовое, ручной ввод', 'контрола нет: нужен WebInput + OnTextChanged (параметр ZPHD_COMM)'),
        ('Дата начала бурения', 'D_ZBUR_BEG', 'календарь', 'в форме — комбо (не календарь); параметр ZBUR_BEG пишется'),
        ('Дата окончания бурения', 'D_ZBUR_END', 'календарь', 'в форме — комбо; параметр ZBUR_END пишется'),
        ('Пилотный ствол', 'D_ZPILOT', 'RDSD_ZPILOT', ''),
        ('Состояние скважины', 'D_ZSKV_ST', 'RDSD_ZSKV_ST', ''),
        ('Примечание', 'I_ZINDTXT1', 'текстовое, ручной ввод', 'WebInput; параметр ZINDTXT1 (подключён)'),
    ]),
    ('Кап.строительство', [
        ('Ген.подрядчик', 'D_ZGEN_POD', 'SHORTCUT_TO_RDSD_SOLDTO_7', ''),
        ('Ген.заказчик', 'D_ZGEN_ZAK', 'SHORTCUT_TO_RDSD_SOLDTO_6', ''),
        ('Субподрядчик', 'D_ZPKR_SUBP', 'SHORTCUT_TO_RDSD_SOLDTO_8', ''),
        ('Шифр проекта стройки', 'D_ZSHIFR', 'RDSD_ZSHIFR', ''),
    ]),
    ('Экология', [
        ('Номер объекта ЭМ', 'D_ZOBJEM', 'RDSD_ZOBJEM', ''),
        ('Объект исследования', 'D_ZPHD_SR', 'RDSD_ZPHD_SR', ''),
        ('Группировка сред ЭМ', 'D_ZPHD_GRSR', 'RDSD_ZPHD_GRSR', ''),
    ]),
    ('Прочие аналитики', [
        ('Вид газа', 'D_ZGAZ_TYPE', 'RDSD_ZGAZ_TYPE', ''),
        ('Тип воздушного судна', 'D_ZAVIATYPE', 'RDSD_ZAVIATYPE', ''),
        ('Дата ввода скв. в экспл.', 'D_ZPHD_NCH', 'календарь', 'в форме — комбо; параметр ZPHD_NCH подключён'),
        ('Дата проведения ГТМ', 'D_ZPHD_KON', 'календарь', 'в форме — комбо; параметр ZPHD_KON подключён'),
        ('ГТМ', 'D_ZPHD_SPR', 'RDSD_ZPHD_SPR', ''),
    ]),
    ('Данные показателя', [
        ('Вид деятельности', '—', 'DIC_ZSIUT_ACTVTS', 'контрола-фильтра нет (есть только чек-бокс вывода CB_ACTIVITY_TYPE); параметра ACTVTS нет и в запросе'),
        ('Вид показателя', '—', 'RDSD_GROUPS', 'контрола-фильтра нет (чек-бокс вывода CB_IND_TYPE)'),
        ('Формы отчетов', '—', 'PFORM', 'контрола-фильтра нет (чек-бокс вывода CB_TEP_FORM_OF_SNG)'),
        ('Выводить ТЭП-источники (чек-бокс)', '—', 'без справочника', 'контрола нет — уточнить, какой чек-бокс ему соответствует'),
    ]),
]

# «Поля для вывода»: (раздел, [(подпись по ТТ, контрол, идентификатор поля, примечание)])
OUTPUT = [
    ('Основные данные', [
        ('Год', '—', 'CALYEAR', 'чек-бокса нет; «Год» уходит в список всегда'),
        ('СП', 'CB_PLANT', 'PLANT', ''),
        ('ТЭП', 'CB_ZLIB_INDC', 'ZLIB_INDC', ''),
        ('Ед.измерения', 'CB_ACT_UNIT', 'ACT_UNIT', ''),
        ('Поставщик', 'CB_VENDOR', 'VENDOR', ''),
        ('Заказчик', 'CB_SOLD_TO', 'SOLD_TO', ''),
        ('Регион', 'CB_ZHRGRPMO', 'ZHRGRPMO', ''),
        ('Вид производства', 'CB_PROFIT_CTR', 'PROFIT_CTR', ''),
        ('МВЗ', 'CB_COSTCENTER', 'COSTCENTER', ''),
        ('Орг.единица', 'CB_ZORGUNIT', 'ZORGUNIT', ''),
        ('Рабочее место исполнителя', 'CB_ZPH_USR2', 'ZPH_USR2', ''),
        ('Вид работ', 'CB_ACTTYPE', 'ACTTYPE', ''),
        ('Единица оборудования', 'CB_ZEQUI', 'ZEQUI', ''),
        ('Класс вида оборудования', 'CB_ZCLSVOBOR', 'ZCLSVOBOR', ''),
        ('Материал', 'CB_MATERIAL', 'MATERIAL', ''),
        ('Тех.место', 'CB_ZFUNC_LOC', 'ZFUNC_LOC', ''),
        ('Месторождение', 'CB_ZSIU_FLD', 'ZSIU_FLD', ''),
        ('СПП-элемент', 'CB_POSID', 'POSID', ''),
        ('Инфосистема', 'CB_ZLIB_INFS', 'ZLIB_INFS', ''),
        ('Тип периода', 'CB_PERIOD_TYPE', 'PERIOD_TYPE', ''),
        ('Вышестоящий ТЭП', 'CbHigherInd', 'ZPH_HIGHER', 'контрол объявлен, обработчика нет (уточнить идентификатор)'),
    ]),
    ('Значения ТЭП', [
        ('Январь…Декабрь (12)', 'CB_JANUARY … CB_DECEMBER', 'ZSIU_INDV_01…12', '12 чек-боксов; в запросе таких аналитик нет — подставлять в ANALYTIC_SET нельзя'),
        ('I кв. / II кв. / 6 мес. / III кв. / 9 мес. / IV кв. / Год', 'CB_FIRST_QUARTER, CB_SECOND_QUARTER, CB_SIX_MONTH, CB_THIRD_QUARTER, CB_NINE_MONTH, CB_FOURTH_QUARTER, CB_YEAR', 'ZSIU_INDV_Q1…Q9', 'отмечены по умолчанию; III кв. — контрол не подтверждён'),
    ]),
    ('Значения ТЭП с начала года', [
        ('Январь…Год «С нач.года» (19)', '—', 'ZVALUE_SNG и др.', 'контролов нет; колонки в запросе считаются, но в списке полей отчёта их нет'),
    ]),
    ('Значения корректировок ТЭП', [
        ('Январь…Год «Коррект.» (19)', '—', 'ZSIU_INDV при ZLIB_INFS = KOROUND', 'контролов нет'),
    ]),
    ('Энергоснабжение', [
        ('Договор', 'CB_ZPHD_DOG', 'ZPHD_DOG', ''), ('Потребитель', 'CB_ZPHD_USL1', 'ZPHD_USL1', ''),
        ('ЭСО физ', 'CB_ZDEBITOR', 'ZDEBITOR', ''), ('Эсо физ (даль)', 'CB_ZPH_ESO2', 'ZPH_ESO2', ''),
        ('ЭСО покуп', '—', 'ZPH_EPOK', 'контрола нет (аналитика zph_epok в запросе есть)'),
        ('Сетевая компания', 'CB_ZPHD_SK', 'ZPHD_SK', ''), ('Ур.напр.', 'CB_UCVOLTLEVL', 'UCVOLTLEVL', ''),
        ('Ур.напр.продаж', 'CB_ZUCVOLTTR', 'ZUCVOLTTR', ''), ('Класс напр.', 'CB_Z_CL_NAPR', 'Z_CL_NAPR', ''),
        ('Тип тарифов', 'CB_ZSIU_TY', 'ZSIU_TY', ''), ('Договор по воде', 'CB_ZDOGLINK', 'ZDOGLINK', ''),
    ]),
    ('Геология и бурение', [
        ('Лицензионный участок', 'CB_ZBUR_LU', 'ZBUR_LU', 'подпись по экрану (в ТТ «Участок недр»)'),
        ('Площадь бурения', 'CB_ZBUR_AREA', 'ZBUR_AREA', ''),
        ('Куст', 'CB_ZSKV_KUST', 'ZSKV_KUST', 'в ТТ поле ZKUST, в форме — ZSKV_KUST: уточнить'),
        ('Скважина', 'CB_Z_SKV_GEO', 'Z_SKV_GEO', 'подпись по экрану'),
        ('Пласт', 'CB_ZBUR_PLST', 'ZBUR_PLST', ''),
        ('Технология отбора керна', 'CB_ZPH_TEHK', 'ZPH_TEHK', ''),
        ('Структурные особенности пласта', 'CB_ZPH_OPLST', 'ZPH_OPLST', ''),
        ('Мероприятия', 'CB_ZPHD_COMM', 'ZPHD_COMM', 'чек-бокс есть; поля ввода значения — нет'),
        ('Дата начала бурения', 'CB_ZBUR_BEG', 'ZBUR_BEG', ''),
        ('Дата окончания бурения', 'CB_ZBUR_END', 'ZBUR_END', ''),
        ('Пилотный ствол', 'CB_ZPILOT', 'ZPILOT', ''),
        ('Состояние скважины', 'CB_ZSKV_ST', 'ZSKV_ST', ''),
        ('Примечание', 'CB_ZINDTXT1', 'ZINDTXT1', ''),
    ]),
    ('Кап.строительство', [
        ('Ген.подрядчик', 'CB_ZGEN_POD', 'ZGEN_POD', ''), ('Ген.заказчик', 'CB_ZGEN_ZAK', 'ZGEN_ZAK', ''),
        ('Субподрядчик', 'CB_ZPKR_SUBP', 'ZPKR_SUBP', ''), ('Шифр проекта стройки', 'CB_ZSHIFR', 'ZSHIFR', ''),
    ]),
    ('Экология', [
        ('Объект ЭМ', 'CB_ZOBJEM', 'ZOBJEM', 'подпись по экрану (в ТТ «Номер объекта ЭМ»)'),
        ('Объект исследования', 'CB_ZPHD_SR', 'ZPHD_SR', ''),
        ('Группировка сред ЭМ', 'CB_ZPHD_GRSR', 'ZPHD_GRSR', ''),
    ]),
    ('Прочие аналитики', [
        ('Вид газа', 'CB_ZGAZ_TYPE', 'ZGAZ_TYPE', ''),
        ('Тип воздушного судна', 'CB_ZAVIATYPE', 'ZAVIATYPE', ''),
        ('Дата начала', 'CB_ZPHD_NCH', 'ZPHD_NCH', ''),
        ('Дата окончания', 'CB_ZPHD_KON', 'ZPHD_KON', ''),
        ('Универсальный справочник', 'CB_AREA или CbESO3', '?', 'по экрану; какой из двух контролов — уточнить'),
        ('Операция', 'CB_AREA или CbESO3', '?', 'по экрану; какой из двух контролов — уточнить'),
    ]),
    ('Данные показателя', [
        ('Вид деятельности', 'CB_ACTIVITY_TYPE', 'ACTVTS', 'контрол объявлен, обработчика нет'),
        ('Владелец ТЭП', 'CB_TEP_OWNER', 'OWNER', 'контрол объявлен, обработчика нет'),
        ('МВП ТЭП', 'CB_MVP_TEP', '?', 'подпись по экрану; идентификатор уточнить'),
        ('Функция/задача персонала', 'CB_FUNCTION_OF_WOKERS', 'ZPH_FUNC', 'уточнить идентификатор'),
        ('Вид показателя', 'CB_IND_TYPE', 'ID1', 'контрол объявлен, обработчика нет'),
        ('Формы ТЭП СНГ', 'CB_TEP_FORM_OF_SNG', 'ZF_NUMB', 'контрол объявлен, обработчика нет'),
        ('Объемный', 'CB_VOLUME', 'ZPH_VOLUME', 'уточнить идентификатор'),
        ('Трудоемкость', 'CB_TRUD', 'ZPH_TRUD', 'уточнить идентификатор'),
        ('В сопоставимых ценах', 'CB_COMPARABLE_PRICES', 'ZPH_PRICE_CP', 'уточнить идентификатор'),
        ('В действующих ценах', 'CB_CURRENT_PRICES', 'ZPH_PRICE_CD', 'уточнить идентификатор'),
        ('В сметных ценах', 'CB_ESTIMATED_PRICES', '?', 'подпись по экрану; идентификатор уточнить'),
        ('Вид работ (классификация)', 'CB_ACTTYPE2', 'ZPH_ACTTYPE2', 'уточнить идентификатор'),
        ('Код набора аналитик', 'CB_ANALYTIC_SET', '?', 'подпись по экрану; вероятно, список кодов аналитик'),
    ]),
    ('Данные расчета', [
        ('Признак уровня', 'CB_ZPHD_PRIZ или CB_ZPHD_PHD', 'ZPHD_PRIZ / ZPHD_PHD', 'на экране 3 строки, а подходящих контролов 4 — уточнить'),
        ('Исключение из приказа', 'CB_ZPHD_PHD или CB_ZPHD_IS', 'ZPHD_PHD / ZPHD_IS', 'уточнить'),
        ('Источник данных', 'CB_ZPHD_NOP1 или …', 'ZPHD_NOP1', 'уточнить'),
    ]),
]


WHERE = {
    'CB_DISPLAY_CODE_ANALYT': 'верхняя часть формы, чек-бокс «Выводить коды аналитик» (виден на скриншоте)',
    'CB_DISPLAY_INFO_BY_STATUS': 'верхняя часть формы, чек-бокс «Выводить информацию по статусам» (виден на скриншоте)',
    'CB_NOVEMBER': '«Поля для вывода» → «Значения ТЭП» (в модуле обработчик CbNovemberOnChange)',
    'CB_THIRD_QUARTER': '«Поля для вывода» → «Значения ТЭП» (обработчик CbThirdQuarterOnChange)',
    'CbHigherInd': '«Поля для вывода» → «Основные данные», «Вышестоящий ТЭП»',
    'CB_ACTIVITY_TYPE': '«Поля для вывода» → «Данные показателя», «Вид деятельности»',
    'CB_IND_TYPE': '«Поля для вывода» → «Данные показателя», «Вид показателя»',
    'CB_TEP_FORM_OF_SNG': '«Поля для вывода» → «Данные показателя», «Формы отчетов»',
    'CB_TEP_OWNER': '«Поля для вывода» → «Данные показателя», «Владелец ТЭП»',
    'CB_FUNCTION_OF_WOKERS': '«Поля для вывода» → «Данные показателя», «Функция/задача»',
    'CB_VOLUME': '«Поля для вывода» → «Данные показателя», «Объемный»',
    'CB_TRUD': '«Поля для вывода» → «Данные показателя», «Трудоемкость»',
    'CB_COMPARABLE_PRICES': '«Поля для вывода» → «Данные показателя», «В сопоставимых ценах»',
    'CB_CURRENT_PRICES': '«Поля для вывода» → «Данные показателя», «В действующих ценах»',
    'CB_ACTTYPE2': '«Поля для вывода» → «Данные показателя», «Вид работ (классификация)»',
    'CB_ANALYTIC_SET': 'назначение в ТТ не найдено',
    'CB_AREA': 'назначение в ТТ не найдено',
    'CB_ESTIMATED_PRICES': 'назначение в ТТ не найдено',
    'CB_MVP_TEP': 'назначение в ТТ не найдено',
    'CbESO3': 'назначение в ТТ не найдено',
}

missing_rows = []


def status(control):
    """Статус контрола по данным модуля."""
    if control == '—' or control.startswith('?'):
        return 'missing', 'контрола нет'
    names = [x.strip() for x in control.replace('…', ' ').split(',')]
    names = [n for n in names if n and n != '—']
    res = []
    for n in names:
        if n in declared:
            if n in handlers:
                res.append(('ok', n))
            else:
                res.append(('declared', n))
        else:
            res.append(('missing', n))
    if any(x[0] == 'missing' for x in res):
        return 'missing', 'не объявлен в модуле'
    if all(x[0] == 'ok' for x in res):
        return 'ok', 'подключён'
    return 'declared', 'объявлен, обработчика нет'


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def render_conditions():
    out = []
    for section, fields in CONDITIONS:
        rows = []
        for caption, control, dic, note in fields:
            st, st_text = status(control)
            if st == 'missing':
                missing_rows.append(('Условия выборки → ' + section, caption, control, note or dic))
            param = ''
            if control in combo_param:
                ps = combo_param[control]
                param = ', '.join(ps) if ps else 'НЕ ПИШЕТ ПАРАМЕТР'
            rows.append(
                '<tr class="%s"><td>%s</td><td class="ctl">%s</td><td class="ctl">%s</td>'
                '<td class="ctl">%s</td><td class="st">%s</td><td class="note">%s</td></tr>'
                % (st, esc(caption), esc(control), esc(param or '—'), esc(dic), esc(st_text), esc(note)))
        out.append('<h3>%s <span class="cnt">%d полей</span></h3>' % (esc(section), len(fields)))
        out.append('<table class="grid"><thead><tr><th>Поле на экране (ТТ)</th><th>Контрол в модуле</th>'
                   '<th>Параметр</th><th>Справочник (ТТ)</th><th>Состояние</th><th>Примечание</th></tr></thead><tbody>')
        out.extend(rows)
        out.append('</tbody></table>')
    return '\n'.join(out)


def render_output():
    out = []
    for section, fields in OUTPUT:
        rows = []
        for caption, control, fid, note in fields:
            st, st_text = status(control)
            if st == 'missing':
                missing_rows.append(('Поля для вывода → ' + section, caption, control, note or fid))
            rows.append(
                '<tr class="%s"><td>%s</td><td class="ctl">%s</td><td class="ctl">%s</td>'
                '<td class="st">%s</td><td class="note">%s</td></tr>'
                % (st, esc(caption), esc(control), esc(fid), esc(st_text), esc(note)))
        out.append('<h3>%s <span class="cnt">%d полей</span></h3>' % (esc(section), len(fields)))
        out.append('<table class="grid"><thead><tr><th>Поле на экране (ТТ)</th><th>Чек-бокс в модуле</th>'
                   '<th>Идентификатор поля</th><th>Состояние</th><th>Примечание</th></tr></thead><tbody>')
        out.extend(rows)
        out.append('</tbody></table>')
    return '\n'.join(out)


combos = sorted(n for n, t in declared.items() if t == 'WebDimensionCombo')
cbs = sorted(n for n, t in declared.items() if t == 'WebCheckBox')
unused_cb = [c for c in cbs if c not in handlers]
pairs = ''
for m in re.finditer(r'Hyperlink\.SetParamValueFromSelection\(\s*"([^"]+)"', src):
    pairs += m.group(1) + ' '

HTML = '''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<title>Макет веб-формы «Анализ значений ТЭП (копия для доработок)»</title>
<style>
 body {{ font-family: Segoe UI, Arial, sans-serif; margin: 0; padding: 24px; background:#f5f7fb; color:#1b2430; }}
 h1 {{ font-size: 20px; margin: 0 0 4px; }} h2 {{ font-size: 16px; margin: 28px 0 8px; }}
 h3 {{ font-size: 14px; margin: 18px 0 6px; }} .cnt {{ color:#7b8794; font-weight:400; font-size:12px; }}
 .sub {{ color:#5b6875; font-size: 13px; margin-bottom: 16px; }}
 .frame {{ background:#dff1fb; border:1px solid #9dc7e0; border-radius:6px; padding:14px; max-width:1180px; }}
 .top {{ display:flex; gap:24px; }} .col {{ flex:1; }}
 .field {{ display:flex; align-items:center; gap:8px; margin:6px 0; }}
 .lbl {{ width:190px; color:#3b4a5a; font-size:13px; }}
 .combo {{ flex:1; background:#fff; border:1px solid #c7d3de; border-radius:4px; height:26px; line-height:26px;
           padding:0 8px; color:#9aa7b4; font-size:13px; position:relative; }}
 .combo:after {{ content:"▾"; position:absolute; right:8px; color:#7b8794; }}
 .chk {{ display:flex; align-items:center; gap:8px; margin:6px 0; font-size:13px; color:#3b4a5a; }}
 .box {{ width:14px; height:14px; border:1px solid #7b8794; border-radius:3px; background:#fff; display:inline-block; }}
 .btn {{ display:inline-block; background:#3f8fd4; color:#fff; border-radius:4px; padding:8px 26px; font-size:13px; margin:4px 0; }}
 .btn.sec {{ background:#4f9fe0; }}
 .tabs {{ display:flex; gap:2px; margin:14px 0 0; }}
 .tab {{ padding:8px 18px; background:#cfe6f5; border:1px solid #9dc7e0; border-bottom:none; border-radius:6px 6px 0 0; font-size:13px; }}
 .tab.on {{ background:#fff; font-weight:600; }}
 .tabs2 {{ display:flex; gap:2px; margin:0 0 10px; }}
 .tab2 {{ padding:7px 16px; background:#e8f2fa; border:1px solid #b8d4e8; border-radius:4px 4px 0 0; font-size:13px; }}
 .tab2.on {{ background:#fff; border-bottom-color:#fff; font-weight:600; }}
 .scope {{ background:#fff; border:1px solid #9dc7e0; border-radius:0 6px 6px 6px; padding:14px; }}
 table.grid {{ border-collapse:collapse; width:100%; background:#fff; font-size:12.5px; }}
 table.grid th, table.grid td {{ border:1px solid #dde5ee; padding:5px 8px; text-align:left; vertical-align:top; }}
 table.grid th {{ background:#eef4fa; font-weight:600; }}
 td.ctl {{ font-family: Consolas, monospace; color:#1d4e79; }}
 tr.ok td.st {{ color:#1c7d3f; }} tr.declared td.st {{ color:#a8720b; }}
 tr.missing td.st {{ color:#b3261e; }} tr.missing td.ctl {{ color:#b3261e; }}
 td.note {{ color:#5b6875; }}
 .legend span {{ display:inline-block; margin-right:14px; font-size:12.5px; }}
 .k {{ font-family:Consolas, monospace; background:#eef2f7; padding:1px 5px; border-radius:3px; }}
 .warn {{ background:#fff6e5; border:1px solid #f0d29b; border-radius:6px; padding:10px 14px; font-size:13px; margin:10px 0; }}
</style></head><body>
<h1>Макет веб-формы «Анализ значений ТЭП (копия для доработок)»</h1>
<div class="sub">Модуль <span class="k">BA_PHD.WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV</span>.
Макет собран из модуля формы (объявления контролов и обработчики) и ТЗ
(листы «Разделы СЭ - Условия выборки», «СЭ - поля для вывода») — визуальной части формы в выгрузке
окружения нет. Скриншоты формы использованы для подписей и расположения.</div>

<div class="legend">
 <span>🟢 <b>подключён</b> — есть обработчик, значение уходит в отчёт</span>
 <span>🟡 <b>объявлен, обработчика нет</b> — контрол в модуле есть, но в исходном модуле не использовался
 (ссылки в коде выключены, чтобы не ломать дизайнер)</span>
 <span>🔴 <b>контрола нет</b> — по ТЗ нужен, в модуле не объявлен</span>
</div>

<h2>1. Верхняя часть формы (по скриншотам)</h2>
<div class="frame">
 <div class="top">
  <div class="col">
   <div class="field"><span class="lbl">Год <span class="k">D_CALYEAR</span></span><span class="combo"></span></div>
   <div class="field"><span class="lbl">СП <span class="k">D_PLANT</span></span><span class="combo"></span></div>
   <div class="field"><span class="lbl">ТЭП <span class="k">D_ZLIB_INDC</span></span><span class="combo"></span></div>
   <div class="field"><span class="lbl">Тип данных <span class="k">D_ZTYPEIND</span></span><span class="combo"></span></div>
   <div class="chk"><span class="box"></span> Выводить коды аналитик <span class="k">CB_DISPLAY_CODE_ANALYT</span></div>
   <div class="chk"><span class="box"></span> Выводить информацию по статусам <span class="k">CB_DISPLAY_INFO_BY_STATUS</span></div>
  </div>
  <div class="col">
   <div class="field"><span class="lbl">Календарь <span class="k">DateTimePicker1</span></span><span class="combo" style="max-width:280px"></span></div>
   <div class="field"><span class="lbl">Журнал <span class="k">TextArea1</span></span>
     <span class="combo" style="height:74px;max-width:280px;color:#7b8794">TextArea1 (вывод ссылки и ошибок)</span></div>
   <div style="text-align:right"><span class="btn">Применить <span class="k">ButtonApply</span></span><br>
     <span class="btn sec">Отменить <span class="k">ButtonCancel</span></span></div>
  </div>
 </div>
 <div class="tabs"><span class="tab on">Условия выборки</span><span class="tab">Поля для вывода</span></div>
 <div class="scope">
  <div class="tabs2"><span class="tab2 on">Основные данные</span><span class="tab2">Энергоснабжение</span>
   <span class="tab2">Геология и бурение</span><span class="tab2">Кап.строительство</span>
   <span class="tab2">Экология</span><span class="tab2">Прочие аналитики</span>
   <span class="tab2">Данные показателя</span><span class="tab2">Данные расчета</span></div>
  <div style="color:#5b6875;font-size:12.5px">Поля раздела — см. таблицы ниже. Вкладки:
   <span class="k">TabControl</span> (режимы «Условия выборки»/«Поля для вывода»),
   <span class="k">TabControl1</span>, <span class="k">TabControl2</span> (разделы),
   страницы <span class="k">TabPage1…TabPage18</span> — соответствие страниц разделам задаётся
   в дизайнере; в выгрузке подписей вкладок нет, поэтому прошу подтвердить.</div>
 </div>
</div>

<div class="warn"><b>Проверьте, пожалуйста, три вещи:</b>
 1) соответствие «контрол ↔ поле на экране» (столбцы 1–2 таблиц);
 2) какие из жёлтых контролов реально есть на форме (ссылки на них я включу после подтверждения);
 3) красные строки — чего на форме нет и что нужно создать.</div>

<h2>2. Режим «Условия выборки»: поля разделов</h2>
{conditions}

<h2>3. Режим «Поля для вывода»: чек-боксы</h2>
{output}

<h2>4. Сводка по модулю</h2>
<table class="grid"><tbody>
<tr><th>Контролов объявлено</th><td>{declared_total} (в т.ч. 95 чек-боксов, {combo_n} комбо, 18 страниц вкладок,
 3 вкладки, 2 кнопки, 1 поле ввода, 1 календарь, 1 журнал, 1 панель, 1 область отчёта)</td></tr>
<tr><th>Чек-боксов подключено к списку полей</th><td>{wired_n} (пишут идентификатор поля в <span class="k">P_FIELD_LIST</span>)</td></tr>
<tr><th>Чек-боксов без обработчика</th><td>{unused_n}: <span class="k">{unused_list}</span></td></tr>
<tr><th>Комбо, пишущих параметры</th><td>{combo_wired} из {combo_n}</td></tr>
</tbody></table>

<h2>5. Контролы, объявленные в модуле, но не использованные в исходном коде</h2>
<div class="sub">Ссылки на них в коде держу выключенными. Если компонент есть на форме — достаточно навесить
событие <span class="k">OnChange</span>, и он подключится сам. Прошу отметить, какие реально есть на форме.</div>
<table class="grid"><thead><tr><th>Контрол</th><th>Тип</th><th>Где ожидается</th><th>Состояние</th></tr></thead><tbody>
{unused_rows}
</tbody></table>

<h2>6. Чего на форме нет (по ТЗ нужно создать)</h2>
<table class="grid"><thead><tr><th>Раздел / режим</th><th>Поле по ТЗ</th><th>Контрол</th><th>Что нужно</th></tr></thead><tbody>
{missing_rows_html}
</tbody></table>

<h2>7. Что я понял про связь с отчётом</h2>
<ul style="font-size:13px;line-height:1.6">
 <li>Список выбранных полей уходит <b>массивом</b> в нижнем регистре в параметры
     <span class="k">P_FIELD_LIST</span> и <span class="k">ANALYTIC_SET</span>; запрос подставляет его
     прямо в SELECT/GROUP BY — так и получается «чек-бокс → столбец», а невыбранное суммируется.</li>
 <li>Остальные параметры — фильтры (по одному на комбо) и <span class="k">CALYEAR</span> (Год уходит всегда).</li>
 <li>В отчёте <span class="k">PRX_ANALYSIS_TEP</span> осталось сопоставить
     <span class="k">ANALYTIC_SET</span> ← <span class="k">P_FIELD_LIST</span>, а также
     <span class="k">ZTYPEIND</span> и <span class="k">ZGEN_POD</span>.</li>
</ul>
</body></html>
'''

html = HTML.format(
    conditions=render_conditions(),
    output=render_output(),
    declared_total=len(declared),
    combo_n=len(combos),
    wired_n=len(wired_cb),
    unused_n=len(unused_cb),
    unused_list=', '.join(unused_cb),
    combo_wired=sum(1 for c in combos if combo_param.get(c)),
    unused_rows='\n'.join(
        '<tr class="declared"><td class="ctl">%s</td><td>%s</td><td class="note">%s</td>'
        '<td class="st">объявлен, обработчика нет</td></tr>'
        % (esc(c), declared[c], esc(WHERE.get(c, '—'))) for c in unused_cb),
    missing_rows_html='\n'.join(
        '<tr class="missing"><td>%s</td><td>%s</td><td class="ctl">%s</td><td class="note">%s</td></tr>'
        % (esc(a), esc(b), esc(c), esc(d)) for a, b, c, d in missing_rows),
)
io.open(sys.argv[1] if len(sys.argv) > 1 else 'docs/form-layout.html', 'w', encoding='utf-8', newline='\n').write(html)
print('готово: %d байт' % len(html))
