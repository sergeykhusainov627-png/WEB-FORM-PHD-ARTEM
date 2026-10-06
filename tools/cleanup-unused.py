# cleanup-unused.py — убирает из модуля Fore неиспользуемые объявления (переменные и константы),
# по которым компилятор Форсайта выдаёт предупреждения «Переменная/Константа ... не используется».
#
# Запуск:
#   python tools/cleanup-unused.py <модуль.fore> --report            # только показать
#   python tools/cleanup-unused.py <модуль.fore> <результат.fore>    # записать очищенный файл
#
# Учитываются оба стиля объявлений:
#   Var                                   Const
#       a, b: Integer;                        C_X = "X";
#       c: String;
# Закомментированный код (// и { }) при подсчёте использований не учитывается: переменная,
# оставшаяся только в комментариях, считается неиспользуемой.

import io, re, sys

src_path = sys.argv[1]
report_only = '--report' in sys.argv
dst_path = None if report_only else sys.argv[2]

text = io.open(src_path, encoding='utf-8').read().replace('\r\n', '\n')
lines = text.split('\n')

# --- живой код / комментарии ---
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

MOD = r'(?:(?:Private|Public|Protected|Friend|Shared)\s+)*'
DECL_VAR = re.compile(r'^([A-Za-z_]\w*(?:\s*,\s*[A-Za-z_]\w*)*)\s*:\s*(.+?);\s*(//.*)?$')
DECL_CONST = re.compile(r'^([A-Za-z_]\w*)\s*=\s*(.+?);\s*(//.*)?$')

# --- границы подпрограмм ---
methods, stack = [], []
for i, l in enumerate(lines):
    if not live[i]:
        continue
    m = re.match(r'^\t' + MOD + r'(Sub|Function)\s+([A-Za-z_]\w*)', l)
    if m:
        stack.append((m.group(2), i))
    m = re.match(r'^\tEnd\s+(Sub|Function)\s+([A-Za-z_]\w*)\s*;', l)
    if m and stack:
        name, start = stack.pop()
        methods.append((name, start, i))

drop = set()
removed = []

def process_decl(i, mode, body_text, where_):
    """Проверяет объявление; возвращает True, если строку надо удалить."""
    t = lines[i].strip()
    rx = DECL_CONST if mode == 'const' else DECL_VAR
    m = rx.match(t)
    if not m:
        return False
    names = [x.strip() for x in m.group(1).split(',')]
    kind = 'константа' if mode == 'const' else 'переменная'
    keep = [n for n in names if re.search(r'\b' + re.escape(n) + r'\b', body_text)]
    for n in names:
        if n not in keep:
            removed.append((i + 1, n, kind, where_))
    if not keep:
        drop.add(i)
        return True
    if len(keep) != len(names):
        indent = re.match(r'^(\t+)', lines[i]).group(1)
        if mode == 'const':
            lines[i] = '%s%s = %s;' % (indent, ', '.join(keep), m.group(2))
        else:
            lines[i] = '%s%s: %s;' % (indent, ', '.join(keep), m.group(2))
    return False

# --- 1. объявления внутри подпрограмм ---
for name, start, end in methods:
    # секция объявлений: от заголовка до Begin
    begin = None
    for i in range(start + 1, end):
        if lines[i].strip() == 'Begin':
            begin = i
            break
    if begin is None:
        continue
    section = [i for i in range(start + 1, begin)]
    body_text = '\n'.join(lines[i] for i in range(begin, end) if live[i])
    mode, blocks = None, {}          # blocks: индекс заголовка Const/Var -> список объявлений
    header = None
    for i in section:
        t = lines[i].strip()
        if not live[i] or t == '':
            continue
        if t == 'Var':
            mode, header = 'var', i
            blocks[i] = []
            continue
        if t == 'Const':
            mode, header = 'const', i
            blocks[i] = []
            continue
        if mode is not None:
            blocks[header].append(i)
            process_decl(i, mode, body_text, name)
    # если в блоке не осталось объявлений — убираем и заголовок
    for h, decls in blocks.items():
        if h in drop:
            continue
        if all(d in drop for d in decls):
            drop.add(h)

# --- 2. константы уровня класса (вне подпрограмм) ---
method_lines = set()
for _n, s, e in methods:
    method_lines.update(range(s, e + 1))
live_text_all = '\n'.join(l for i, l in enumerate(lines) if live[i])
cls_mode, cls_header, cls_block = None, None, []
for i, l in enumerate(lines):
    if i in method_lines or not live[i]:
        continue
    t = l.strip()
    if t == 'Const':
        cls_mode, cls_header, cls_block = 'const', i, []
        continue
    if t == 'Var' or t.startswith('Property') or t.startswith('Class') or t.startswith('End Class'):
        cls_mode, cls_header = None, None
        continue
    m = None
    if cls_mode == 'const':
        m = DECL_CONST.match(t)
    else:
        m = re.match(r'^Const\s+([A-Za-z_]\w*)\s*=\s*(.+?);\s*(//.*)?$', t)
    if m:
        name = m.group(1)
        uses = len(re.findall(r'\b' + re.escape(name) + r'\b', live_text_all))
        if uses <= 1:                      # только само объявление
            drop.add(i)
            if cls_mode == 'const':
                cls_block.append(i)
            removed.append((i + 1, name, 'константа (уровень класса)', '—'))

print('подпрограмм: %d; удаляется объявлений: %d' % (len(methods), len(removed)))
for ln, n, kind, where in sorted(removed):
    print('  стр.%-5d %-24s %-26s %s' % (ln, n, kind, where))

if report_only:
    sys.exit(0)

out = [l for i, l in enumerate(lines) if i not in drop]
io.open(dst_path, 'w', encoding='utf-8', newline='').write('\n'.join(out).replace('\n', '\r\n'))
print('записано: %s (%d строк, было %d)' % (dst_path, len(out), len(lines)))
