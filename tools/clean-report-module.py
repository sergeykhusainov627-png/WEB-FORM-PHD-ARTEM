# clean-report-module.py — чистка модуля сборки ASM_ANALYSIS_TEP (MAIN, mod_main_analys_tep).
# Удаляется только мёртвый код: закомментированные прототипы, пустые процедуры, неиспользуемые
# переменные и присваивания «в никуда». Логика (hideColumns / replaceTableTitles / genReport)
# не меняется.
#
# Запуск:
#   python tools/clean-report-module.py <исходник.txt> <результат.fore> [--report]
import io, re, sys

src_path = sys.argv[1]
dst_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else None
show_report = '--report' in sys.argv or dst_path is None

lines = io.open(src_path, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
removed = []            # (номер строки в исходнике, что удалено, причина)
drop = set()


def mark(idx, text, why):
    drop.add(idx)
    removed.append((idx + 1, text.rstrip(), why))


# 1. Закомментированные блоки (в т.ч. прототипы tst / getHyperlink / fillStringListByParams)
for i, l in enumerate(lines):
    if l.lstrip().startswith('//'):
        mark(i, l, 'закомментированный код')

# 2. Пустые процедуры addQuerry и MAIN
def drop_empty_sub(name):
    start = None
    for i, l in enumerate(lines):
        if i in drop:
            continue
        if re.match(r'^\s*Sub %s;\s*$' % name, l):
            start = i
        elif start is not None and re.match(r'^\s*End Sub %s;\s*$' % name, l):
            # тело процедуры без строки Begin, без объявлений Var и без уже удалённых строк
            body = [x for j, x in enumerate(lines[start + 1:i])
                    if (start + 1 + j) not in drop
                    and x.strip() not in ('', 'Begin', 'Var')]
            if not body:
                for k in range(start, i + 1):
                    mark(k, lines[k], 'пустая процедура %s' % name)
            return
    return


drop_empty_sub('addQuerry')
drop_empty_sub('MAIN')

# 3. Неиспользуемая переменная curRep (только присваивалась) и присваивания «в никуда»
for i, l in enumerate(lines):
    if i in drop:
        continue
    if re.match(r'^\s*curRep\s*:\s*IPrxReport;\s*$', l):
        mark(i, l, 'неиспользуемая переменная curRep')
    if re.match(r'^\s*curRep\s*:=\s*Report;\s*$', l):
        mark(i, l, 'присваивание неиспользуемой переменной curRep')
    if re.match(r'^\s*MB\s*:=\s*MetabaseClass\.Active;\s*$', l):
        # в OnBeforeOpenReport результат нигде не используется; в readDataToJsonArrFromQuery нужен
        ctx = '\n'.join(lines[max(0, i - 30):i])
        if 'OnBeforeOpenReport' in ctx and 'readDataToJsonArrFromQuery' not in ctx:
            mark(i, l, 'присваивание MB, результат не используется')
    if re.match(r'^\s*TableIsland\s*:=\s*TableIsland;\s*$', l):
        mark(i, l, 'присваивание параметра самому себе')
    if re.match(r'^\s*arrayLenght\s*:=\s*.*$', l):
        mark(i, l, 'промежуточная переменная arrayLenght')
    if re.match(r'^\s*fieldArrayFromParam\s*:=\s*New String\[arrayLenght\];\s*$', l):
        mark(i, l, 'массив сразу перезаписывается следующей строкой')
    if re.match(r'^\s*arrayLenght\s*:\s*Integer;\s*$', l):
        mark(i, l, 'объявление неиспользуемой arrayLenght')
    if re.match(r'^\s*mb\s*:\s*IMetabase;\s*$', l):
        mark(i, l, 'неиспользуемая локальная переменная mb')

out = [l for i, l in enumerate(lines) if i not in drop]
# убрать возможные двойные пустые строки, оставшиеся после удаления
cleaned = []
for l in out:
    if l.strip() == '' and cleaned and cleaned[-1].strip() == '':
        continue
    cleaned.append(l)
text = '\n'.join(cleaned).strip('\n') + '\n'

print('удалено строк: %d (было %d, стало %d)' % (len(removed), len(lines), len(cleaned)))
if show_report:
    for ln, txt, why in sorted(removed):
        print('  стр.%-4d %-28s | %s' % (ln, why, (txt[:70] + '…') if len(txt) > 70 else txt))

# проверка парности Sub/Function
pairs, opens = 0, 0
for l in cleaned:
    if re.match(r'^\s*(Sub|Function)\s+\w+', l):
        opens += 1
    if re.match(r'^\s*End\s+(Sub|Function)\s+\w+', l):
        pairs += 1
print('процедур: %d, завершений: %d %s' % (opens, pairs, 'OK' if opens == pairs else 'ОШИБКА'))

if dst_path:
    io.open(dst_path, 'w', encoding='utf-8', newline='').write(text.replace('\n', '\r\n'))
    print('записано: %s' % dst_path)
