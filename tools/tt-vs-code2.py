# tt-vs-code2.py — сверка ТТ (xlsx) с кодом веб-формы через идентификаторы полей
# и через зависимости формы из выгрузки окружения (.pefx).
# Запуск: python analiz-tep/tools/tt-vs-code2.py "<ТТ.xlsx>" "<модуль.fore>" "<content.xml выгрузки>" "<папка вывода>"
import sys, os, re
from openpyxl import load_workbook

tt, fore, content, outdir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(outdir, exist_ok=True)
wb = load_workbook(tt, data_only=True)
n = lambda v: ('' if v is None else str(v)).strip()
ID = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')

# ---------- ТТ ----------
ws_f = wb['Разделы СЭ - Условия выборки']
filters, sect = [], ''
for r in range(4, ws_f.max_row + 1):
    a, b, c, d = (n(ws_f.cell(r, i).value) for i in (1, 2, 3, 4))
    if a == 'Раздел':
        sect = b
    elif c:
        filters.append((sect, c, d))

ws_o = wb['СЭ - поля для вывода']
outputs, osect = [], ''
for r in range(4, ws_o.max_row + 1):
    a, b, c = (n(ws_o.cell(r, i).value) for i in (1, 2, 3))
    if a and not b:
        osect = a.rstrip(':')
    elif b:
        outputs.append((osect, b, c))

ws_r = wb['Вывод полей в отчете']
report_rows = []
for r in range(5, ws_r.max_row + 1):
    v = [n(ws_r.cell(r, i).value) for i in range(1, 8)]
    if v[0]:
        report_rows.append(v)

# имя поля ТТ -> идентификаторы (источник и код)
name2ids = {}
for v in report_rows:
    ids = []
    for x in (v[3], v[6]):
        if ID.match(x or ''):
            ids.append(x)
    name2ids.setdefault(v[0].upper().replace(' ', ''), set()).update(ids)

# ---------- код ----------
src = open(fore, encoding='utf-8').read()
cb_fields = re.findall(r'fillFieldListByStatusFlag\(\s*([A-Za-z_]\w*)\s*,\s*"([^"]+)"\s*\)', src)
params = re.findall(r'UpdateOpenDefHlinkFromSelection\(\s*"([^"]+)"\s*,\s*([A-Za-z_]\w*)\.Selection\s*,\s*"([^"]+)"', src)
code_names = {f.upper() for _, f in cb_fields} | {p.upper() for p, _, _ in params}

# ---------- зависимости формы из выгрузки ----------
c = open(content, encoding='utf-8').read()
def obj_by_key(key):
    m = re.search(r'<OBJECT\s+KEY="%s"\s+([^>]*)>' % key, c)
    if not m:
        return None
    a = dict(re.findall(r'([A-Za-z_]+)="([^"]*)"', m.group(1)))
    return a
form_node = re.search(r'FILE_NAME_TAG="pef309"[\s\S]{0,4000}?<DO>([\s\S]*?)</DO>', c)
dep_keys = re.findall(r'K="(\d+)"', form_node.group(1)) if form_node else []
deps = []
for k in dep_keys:
    o = obj_by_key(k)
    if o:
        deps.append((o.get('ID', ''), o.get('NAME', ''), o.get('CLASS', '')))
dep_ids = {i.upper() for i, _, _ in deps}

out = []
def p(s=''):
    out.append(s)
p('# Сверка ТТ ↔ код (по идентификаторам и зависимостям формы)')
p()
p('Зависимостей формы в выгрузке: %d (справочников: %d).' % (len(deps), sum(1 for d in deps if d[2] == '3076')))
p()

p('## A. «Условия выборки»: справочник ТТ ↔ зависимости формы')
p()
p('| Раздел | Поле | Справочник ТТ | Есть в зависимостях формы |')
p('|---|---|---|---|')
miss_a = []
for sect, name, dic in filters:
    key = dic.upper().strip()
    ok = key in dep_ids
    if not ok:
        miss_a.append((sect, name, dic))
    p('| %s | %s | `%s` | %s |' % (sect, name, dic, 'да' if ok else '**нет**'))
p()
p('Справочников/полей ТТ, которых нет среди зависимостей формы (%d):' % len(miss_a))
for s, nm, d in miss_a:
    p('- %s → %s (`%s`)' % (s, nm, d))
p()
p('Зависимости формы (справочники), которых нет в «Условиях выборки» ТТ:')
tt_dics = {d.upper().strip() for _, _, d in filters}
for i, nm, cl in sorted(deps):
    if cl == '3076' and i.upper() not in tt_dics:
        p('- `%s` «%s»' % (i, nm))
p()

p('## B. «Поля для вывода»: идентификаторы ТТ ↔ имена в коде (P_FIELD_LIST/параметры)')
p()
p('| Раздел | Поле ТТ | Идентификатор(ы) ТТ | В коде |')
p('|---|---|---|---|')
miss_b, covered = [], 0
for sect, name, dflt in outputs:
    ids = name2ids.get(name.upper().replace(' ', ''), set())
    hit = sorted(i for i in ids if i.upper() in code_names)
    if hit:
        covered += 1
    else:
        miss_b.append((sect, name, sorted(ids), dflt))
    p('| %s | %s | %s | %s |' % (sect, name, ', '.join('`%s`' % i for i in sorted(ids)) or '—',
                                 ', '.join('`%s`' % i for i in hit) or ('**нет**' if ids else '_нет id в ТТ_')))
p()
p('Покрыто идентификаторами кода: %d из %d.' % (covered, len(outputs)))
p()
p('## C. Имена в коде, которых нет в идентификаторах ТТ')
p()
all_tt_ids = set()
for s in name2ids.values():
    all_tt_ids |= {x.upper() for x in s}
for f in sorted(code_names):
    if f not in all_tt_ids:
        cbs = [cb for cb, fl in cb_fields if fl.upper() == f]
        pms = [pp for pp, _, _ in params if pp.upper() == f]
        p('- `%s` (флажки: %s; параметры: %s)' % (f, ', '.join(cbs) or '—', ', '.join(pms) or '—'))
p()

p('## D. Разделы/поля «Условий выборки», отсутствующие в коде как параметры гиперссылки')
p()
p('Параметры формы (53): ' + ', '.join('`%s`' % x for x in sorted({pp for pp, _, _ in params})))
p()
p('## E. Верхний уровень СЭ (лист «Селекционный экран»)')
p()
ws_s = wb['Селекционный экран']
for r in range(5, ws_s.max_row + 1):
    vals = [n(ws_s.cell(r, i).value) for i in (16, 17, 18)]
    if vals[0]:
        p('- **%s** — %s (%s)' % (vals[0], vals[1], vals[2]))
p()
for r in range(21, ws_s.max_row + 1):
    v = n(ws_s.cell(r, 2).value)
    if v:
        p('  %s' % v)

open(os.path.join(outdir, 'tt-vs-code2.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('готово: %s (%d строк)' % (os.path.join(outdir, 'tt-vs-code2.md'), len(out)))
