# check-webform.py — структурная проверка модуля веб-формы после патча.
# Запуск: python tools/check-webform.py <модуль.fore>
import io, re, sys

path = sys.argv[1]
text = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
lines = text.split('\n')

# --- разметка: живой код / комментарий / внутри { } ---
live = [True] * len(lines)
in_brace = False
for i, l in enumerate(lines):
    t = l.strip()
    if in_brace:
        live[i] = False
        if '}' in t:
            in_brace = False
        continue
    if t.startswith('//'):
        live[i] = False
        continue
    if t.startswith('{'):
        live[i] = False
        if '}' not in t:
            in_brace = True
        continue

problems, notes = [], []
MOD = r'(?:(?:Private|Public|Protected|Friend|Shared)\s+)*'

# --- 1. объявленные контролы ---
controls, decl_end = {}, False
for i, l in enumerate(lines):
    if not live[i]:
        continue
    if re.match(r'^\t(Sub|Function|Property|Const)\b', l):
        decl_end = True
    if not decl_end:
        m = re.match(r'^\t([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*;', l)
        if m:
            controls[m.group(1)] = m.group(2)

# --- 2. парность Sub/Function ---
stack, counts = [], {}
for i, l in enumerate(lines, 1):
    if not live[i - 1]:
        continue
    m = re.match(r'^\t' + MOD + r'(Sub|Function)\s+([A-Za-z_]\w*)', l)
    if m:
        stack.append((m.group(1), m.group(2), i))
        counts[m.group(2)] = counts.get(m.group(2), 0) + 1
    m = re.match(r'^\tEnd\s+(Sub|Function)\s+([A-Za-z_]\w*)\s*;', l)
    if m:
        if not stack:
            problems.append('стр.%d: End %s %s без начала' % (i, m.group(1), m.group(2)))
            continue
        kind, name, start = stack.pop()
        if kind != m.group(1) or name != m.group(2):
            problems.append('стр.%d: End %s %s не закрывает %s %s (стр.%d)' % (i, m.group(1), m.group(2), kind, name, start))
for kind, name, start in stack:
    problems.append('стр.%d: %s %s не закрыт' % (start, kind, name))
for name, n in counts.items():
    if n > 1:
        problems.append('дублирующееся имя подпрограммы: %s (x%d)' % (name, n))

# --- 3. вложенные подпрограммы ---
for i, l in enumerate(lines, 1):
    if live[i - 1] and re.match(r'^\t\t' + MOD + r'(Sub|Function)\s', l):
        problems.append('стр.%d: осталась вложенная подпрограмма: %s' % (i, l.strip()))

# --- 4. вызовы fillFieldListByStatusFlag ---
code = '\n'.join(l for l in lines if not l.strip().startswith('//'))
calls = re.findall(r'fillFieldListByStatusFlag\(\s*([A-Za-z_]\w*)\s*,', code)
calls = [c for c in calls if c not in ('CB',)]        # строка-определение метода
for cb in sorted(set(calls)):
    if cb not in controls:
        problems.append('fillFieldListByStatusFlag(%s): контрол не объявлен' % cb)
    elif controls[cb] != 'WebCheckBox':
        problems.append('fillFieldListByStatusFlag(%s): тип %s, а не WebCheckBox' % (cb, controls[cb]))

# --- 5. таблицы соответствия ---
field_keys = re.findall(r'_fieldIds\.Add\("([^"]+)"', text)
code_keys = re.findall(r'_codeIds\.Add\("([^"]+)"', text)
for k in sorted(set(field_keys + code_keys)):
    if k not in controls:
        problems.append('таблица соответствия: контрол %s не объявлен' % k)
    elif controls[k] != 'WebCheckBox':
        problems.append('таблица соответствия: %s имеет тип %s' % (k, controls[k]))
for k in code_keys:
    if k not in field_keys:
        problems.append('_codeIds: %s отсутствует в _fieldIds' % k)
dupes = [k for k in set(field_keys) if field_keys.count(k) > 1]
for k in dupes:
    problems.append('_fieldIds: дубль ключа %s' % k)

# --- 6. покрытие чек-боксов идентификаторами ---
checkboxes = [c for c, t in controls.items() if t == 'WebCheckBox']
mapped = set(field_keys)
service = {'CB_DISPLAY_CODE_ANALYT', 'CB_DISPLAY_INFO_BY_STATUS'}
unmapped = [c for c in sorted(checkboxes) if c not in mapped and c not in service]
notes.append('чек-боксов: %d; размечено идентификаторами: %d; служебных: %d; не размечено: %d'
             % (len(checkboxes), len(mapped - service), len(service), len(unmapped)))
for c in unmapped:
    notes.append('  без идентификатора (уточнить назначение): ' + c)

# --- 7. обработчики onChange ---
no_handler = [c for c in sorted(checkboxes) if ('Sub %sOnChange;' % c) not in text]
notes.append('чек-боксов без обработчика <Контрол>OnChange: %d' % len(no_handler))
for c in no_handler:
    notes.append('  ' + c)

# --- 8. баланс блоков ---
opens = {k: 0 for k in ('Begin', 'If', 'For', 'While', 'Try', 'Select', 'Property')}
closes = {k: 0 for k in ('End', 'End If', 'End For', 'End While', 'End Try', 'End Select', 'End Property')}
for i, l in enumerate(lines):
    if not live[i]:
        continue
    core = l.strip().split('//')[0]
    if re.match(r'^Begin\b', core):
        opens['Begin'] += 1
    if re.match(r'^End\s*;', core):
        closes['End'] += 1
    for kw in ('If', 'For', 'While', 'Try', 'Select', 'Property'):
        if re.match(r'^%s\b' % kw, core):
            opens[kw] += 1
        if re.search(r'\bEnd\s+%s\b' % kw, core):
            closes['End ' + kw] += 1
notes.append('блоки: Begin %d; End; %d; If %d/End If %d; For %d/End For %d; While %d/End While %d; Try %d/End Try %d; Select %d/End Select %d; Property %d/End Property %d'
             % (opens['Begin'], closes['End'], opens['If'], closes['End If'], opens['For'], closes['End For'],
                opens['While'], closes['End While'], opens['Try'], closes['End Try'],
                opens['Select'], closes['End Select'], opens['Property'], closes['End Property']))

print('файл: %s (%d строк, контролов %d)' % (path, len(lines), len(controls)))
if problems:
    print('--- ОШИБКИ ---')
    for p in problems:
        print('  ' + p)
else:
    print('--- структурных ошибок нет ---')
print('--- справка ---')
for n in notes:
    print('  ' + n)
sys.exit(1 if problems else 0)
