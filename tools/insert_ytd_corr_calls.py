import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')

periods = [
    (1, 'CB_JANUARY', 'Январь'), (2, 'CB_FEBRUARY', 'Февраль'), (3, 'CB_MARCH', 'Март'),
    (4, 'CB_APRIL', 'Апрель'), (5, 'CB_MAY', 'Май'), (6, 'CB_JUNE', 'Июнь'),
    (7, 'CB_JULY', 'Июль'), (8, 'CB_AUGUST', 'Август'), (9, 'CB_SEPTEMBER', 'Сентябрь'),
    (10, 'CB_OCTOBER', 'Октябрь'), (11, 'CB_NOVEMBER', 'Ноябрь'), (12, 'CB_DECEMBER', 'Декабрь'),
    (13, 'CB_FIRST_QUARTER', 'I кв.'), (14, 'CB_SECOND_QUARTER', 'II кв.'), (15, 'CB_SIX_MONTH', '6 мес.'),
    (16, 'CB_THIRD_QUARTER', 'III кв.'), (17, 'CB_NINE_MONTH', '9 мес.'), (18, 'CB_FOURTH_QUARTER', 'IV кв.'),
    (19, 'CB_YEAR', 'Год'),
]

lines = []
lines.append('')
lines.append('\t\t// --- 1a. Периоды «с начала года» (CB_*_YEAR_TO_DATE) — считаются по ZVALUE_SNG')
for num, cb, cap in periods:
    if cb == 'CB_SIX_MONTH':
        continue  # на форме нет CB_SIX_MONTH_YEAR_TO_DATE
    cond = 'period = %d' % num if num <= 12 else 'period IN (%d)' % num
    lines.append('\t\taddYtdPeriodIfChecked(%s_YEAR_TO_DATE, %d, "%s", "%s");' % (cb, num, cond, cap))
lines.append('')
lines.append('\t\t// --- 1b. Периоды «корректировки» (CB_*_CORR) — ZSIU_INDV, ZLIB_INFS = KOROUND')
for num, cb, cap in periods:
    cond = 'period = %d' % num if num <= 12 else 'period IN (%d)' % num
    lines.append('\t\taddCorrPeriodIfChecked(%s_CORR, %d, "%s", "%s");' % (cb, num, cond, cap))
block = '\n'.join(lines) + '\n'

# вставляем после последнего вызова addPeriodIfChecked(CB_YEAR, ...)
m = re.search(r'\n(\t\taddPeriodIfChecked\(CB_YEAR, 19[^\n]*)\n', t)
if m and 'addYtdPeriodIfChecked(CB_JANUARY_YEAR_TO_DATE' not in t:
    t = t[:m.end()] + block + t[m.end():]
    print('вставлены вызовы YTD (%d) и CORR (%d)' % (
        sum(1 for l in lines if 'addYtdPeriodIfChecked' in l),
        sum(1 for l in lines if 'addCorrPeriodIfChecked' in l)))
else:
    print('ВНИМАНИЕ: место вставки не найдено или уже вставлено')

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())

# контроль
print('вызовов addYtdPeriodIfChecked:', len(re.findall(r'\n\t\taddYtdPeriodIfChecked', t)))
print('вызовов addCorrPeriodIfChecked:', len(re.findall(r'\n\t\taddCorrPeriodIfChecked', t)))
print('KOROUND в модуле:', t.count('KOROUND'))
print('zvalue_sng в модуле:', t.count('zvalue_sng'))
