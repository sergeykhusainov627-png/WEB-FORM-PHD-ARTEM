import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
lines = io.open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n')

out, n = [], 0
for l in lines:
    m = re.match(r'^(\s*)If (.+?) Then (.+?); End If;\s*$', l)
    if m:
        ind, cond, act = m.group(1), m.group(2), m.group(3)
        out.append(ind + 'If ' + cond + ' Then')
        out.append(ind + '\t' + act + ';')
        out.append(ind + 'End If;')
        n += 1
    else:
        out.append(l)

t = '\n'.join(out)
io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('раскрыто однострочных If:', n)
print('строк:', len(out), '; SHA-256:', hashlib.sha256(b).hexdigest())
