# check-webform.py — структурная проверка модуля веб-формы после патча.
# Запуск: python tools/check-webform.py <модуль.fore> [<эталон.fore>]
#   со вторым аргументом дополнительно проверяется, что состав КОМПОНЕНТОВ не изменился
#   относительно эталона (правило проекта: правки только в логике, новые компоненты не создаются).
import io, re, sys

path = sys.argv[1]
baseline = sys.argv[2] if len(sys.argv) > 2 else None
text = io.open(path, encoding='utf-8').read().replace('\r\n', '\n')
lines = text.split('\n')

def declarations(src_text):
    out, ended = [], False
    for l in src_text.split('\n'):
        if re.match(r'^\t(Sub|Function|Property)\b', l):
            ended = True
        if not ended:
            m = re.match(r'^\t([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*;', l)
            if m:
                out.append((m.group(1), m.group(2)))
    return out

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

# --- 3. запрещённые конструкции платформы ---
for i, l in enumerate(lines, 1):
    if not live[i - 1]:
        continue
    if 'IWebComponents' in l:
        problems.append('стр.%d: IWebComponents нельзя объявлять как тип (в отличие от IWebComponent)' % i)
    if 'Self.Components' in l:
        problems.append('стр.%d: Self.Components использовать нельзя — перебирайте контролы явным списком' % i)

# --- 3а. вложенные подпрограммы ---
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
field_pairs = re.findall(r'_fieldIds\.Add\("([^"]+)",\s*"([^"]+)"\)', text)
field_keys = [k for k, _ in field_pairs]              # имена контролов
field_ids = set(v for _, v in field_pairs)            # идентификаторы полей отчёта
code_pairs = re.findall(r'_codeIds\.Add\("([^"]+)",\s*"([^"]+)"\)', text)
for k in sorted(set(field_keys)):
    if k not in controls:
        problems.append('таблица соответствия: контрол %s не объявлен' % k)
    elif controls[k] != 'WebCheckBox':
        problems.append('таблица соответствия: %s имеет тип %s' % (k, controls[k]))
for k, v in code_pairs:
    if k not in field_ids:
        problems.append('_codeIds: ключ %s отсутствует среди значений _fieldIds' % k)
dupes = [k for k in set(field_keys) if field_keys.count(k) > 1]
for k in dupes:
    problems.append('_fieldIds: дубль ключа %s' % k)

# --- 5а. сбор состояний чек-боксов ---
collect = re.findall(r'CollectIfChecked\(\s*([A-Za-z_]\w*)\s*,\s*"([^"]+)"\s*\)', code)
collect = [(c, n) for c, n in collect if c != 'cb']   # без строки-определения метода
for ctrl, name in collect:
    if ctrl != name:
        problems.append('CollectIfChecked(%s, "%s"): имя контрола и ключ таблицы должны совпадать' % (ctrl, name))
    if ctrl not in controls:
        problems.append('CollectIfChecked(%s): контрол не объявлен' % ctrl)
    elif ctrl not in field_keys:
        problems.append('CollectIfChecked(%s): контрол отсутствует в _fieldIds' % ctrl)
not_collected = sorted(c for c in field_keys if c not in [c for c, _ in collect])
for c in not_collected:
    problems.append('чек-бокс %s размечен, но не собирается в RefreshFieldList' % c)

# --- 5б. поля без чек-бокса: добавлять безусловно можно только те, у которых контрола нет ---
NO_CB_FIELDS = {'CALYEAR'}          # «Год» — чек-бокса CB_CALYEAR в форме нет
body, in_sub = [], False
for i, l in enumerate(lines, 1):
    if not live[i - 1]:
        continue
    if re.match(r'^\tSub addFieldsWithoutCheckBox;', l):
        in_sub = True
        continue
    if in_sub and re.match(r'^\tEnd Sub addFieldsWithoutCheckBox;', l):
        in_sub = False
        continue
    if in_sub:
        body.append((i, l))
if not body:
    problems.append('не найден метод addFieldsWithoutCheckBox — безусловные поля не отслеживаются')
for i, l in body:
    for f in re.findall(r'addFieldToList\("([^"]+)"\)', l):
        if f not in NO_CB_FIELDS:
            problems.append('стр.%d: поле %s добавляется в P_FIELD_LIST безусловно, хотя у него есть чек-бокс' % (i, f))
for i, l in enumerate(lines, 1):
    if not live[i - 1] or re.match(r'^\t*(Sub|End Sub|//)', l.strip()):
        continue
    if 'addFieldToList("' in l and not any(i == j for j, _ in body):
        problems.append('стр.%d: литеральное добавление поля вне addFieldsWithoutCheckBox — вывод должен зависеть от чек-бокса' % i)

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

# --- 8. состав компонентов относительно эталона ---
if baseline:
    base_text = io.open(baseline, encoding='utf-8').read().replace('\r\n', '\n')
    base_decls = dict(declarations(base_text))
    cur_decls = dict(declarations(text))
    new_items = [(k, v) for k, v in cur_decls.items() if k not in base_decls]
    lost = [(k, v) for k, v in base_decls.items() if k not in cur_decls]
    retyped = [(k, base_decls[k], v) for k, v in cur_decls.items() if k in base_decls and base_decls[k] != v]
    for k, v in new_items:
        if v.startswith('Web'):
            problems.append('относительно эталона добавлен КОМПОНЕНТ: %s: %s' % (k, v))
        else:
            notes.append('добавлено невизуальное поле: %s: %s' % (k, v))
    for k, v in lost:
        problems.append('относительно эталона потеряно объявление: %s: %s' % (k, v))
    for k, a, b in retyped:
        problems.append('относительно эталона изменён тип: %s: %s -> %s' % (k, a, b))
    notes.append('компонентов (Web*) в эталоне: %d, в проверяемом файле: %d'
                 % (sum(1 for v in base_decls.values() if v.startswith('Web')),
                    sum(1 for v in cur_decls.values() if v.startswith('Web'))))

# --- 9. баланс блоков ---
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
