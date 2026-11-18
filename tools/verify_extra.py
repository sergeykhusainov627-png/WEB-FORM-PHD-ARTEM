import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')
lines = t.split('\n')

# показать addExtraForType (единственное число)
idx = [k for k, l in enumerate(lines) if re.match(r'^\s*Sub addExtraForType\(', l)]
print('addExtraForType найдено:', [(k + 1) for k in idx])
if idx:
    i = idx[0]
    j = next(k for k in range(i, len(lines)) if re.match(r'^\s*End Sub addExtraForType;', lines[k]))
    for k in range(i, j + 1):
        print('%4d | %s' % (k + 1, lines[k].rstrip()[:125]))

print()
print('=== контроль ===')
for k in ('KOROUND', 'extraYtdCaptions', 'extraCorrCaptions', 'addYtdPeriodIfChecked', 'addCorrPeriodIfChecked',
          'zvalue_sng', 'zsiu_indv'):
    print('  %-24s %d' % (k, t.count(k)))
print('  строк:', len(lines), '; SHA-256:', hashlib.sha256(io.open(p, 'rb').read()).hexdigest())
