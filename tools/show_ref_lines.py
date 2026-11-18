import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
lines = io.open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n')

# найдём три строки шаблона со справочными колонками
idx = [k for k, l in enumerate(lines) if re.match(r'^\s*\+ "        \(SELECT t\.ACTVTS', l)]
print('строки справочных колонок:', [(k + 1) for k in idx])
if idx:
    for k in range(idx[0], idx[0] + 3):
        print('RAW %d: %s' % (k + 1, lines[k]))
