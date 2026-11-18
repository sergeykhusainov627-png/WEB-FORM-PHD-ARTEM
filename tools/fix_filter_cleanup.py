import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')

# Ищем строку очистки пустых фильтров: If Not String.Contains(tempText, "IN ('')") Then
m = re.search(r"\n(\t+If Not String\.Contains\(tempText, \"IN \(' '\)\"\) Then)".replace("' '", "''"), t)
if not m:
    # запасной вариант: любой вариант кавычек
    m = re.search(r'\n(\t+If Not String\.Contains\(tempText, "IN \(\.\{2\}\)"\) Then)', t)
print('найдено:', bool(m))
if m:
    ind = re.match(r'^(\s*)', m.group(1)).group(1)
    new = ind + 'If (Not String.Contains(tempText, "IN (\'\')")) Or String.Contains(tempText, "WHERE") Then'
    t = t[:m.start(1)] + new + t[m.end(1):]
    print('очистка: строки с WHERE сохраняются')

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())
for i, l in enumerate(t.split('\n'), 1):
    if 'tempText' in l:
        print('%4d | %s' % (i, l.strip()[:120]))
