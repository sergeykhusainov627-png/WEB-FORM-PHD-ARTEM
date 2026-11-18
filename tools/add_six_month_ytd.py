import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')

if 'addYtdPeriodIfChecked(B_SIX_MONTH_YEAR_TO_DATE' not in t:
    m = re.search(r'\n(\t\taddYtdPeriodIfChecked\(CB_SECOND_QUARTER_YEAR_TO_DATE, 14[^\n]*)\n', t)
    if m:
        t = t[:m.end()] + '\t\taddYtdPeriodIfChecked(B_SIX_MONTH_YEAR_TO_DATE, 15, "period IN (15)", "6 мес.");\n' + t[m.end():]
        print('добавлен вызов для B_SIX_MONTH_YEAR_TO_DATE (15)')
    else:
        print('ВНИМАНИЕ: место вставки (CB_SECOND_QUARTER_YEAR_TO_DATE) не найдено')
else:
    print('уже есть')

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())
print('вызовов YTD:', len(re.findall(r"\n\t\taddYtdPeriodIfChecked\(", t)))
print('вызовов CORR:', len(re.findall(r"\n\t\taddCorrPeriodIfChecked\(", t)))
