import io, difflib

a_path = r'C:\Users\Manya\Downloads\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.txt'
b_path = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'

a = io.open(a_path, encoding='utf-8-sig', errors='replace').read().replace('\r\n', '\n').split('\n')
b = io.open(b_path, encoding='utf-8').read().replace('\r\n', '\n').split('\n')

print('стенд: %d строк; репозиторий: %d строк' % (len(a), len(b)))
sm = difflib.SequenceMatcher(None, a, b)
ops = [op for op in sm.get_opcodes() if op[0] != 'equal']
print('различий (блоков):', len(ops))
dele = add = 0
for tag, i1, i2, j1, j2 in ops:
    if tag == 'delete':
        dele += i2 - i1
    elif tag == 'insert':
        add += j2 - j1
    elif tag == 'replace':
        dele += i2 - i1
        add += j2 - j1
print('только на стенде:', dele, '; только в репозитории:', add)
print()
print('=== блоки различий (первые 30) ===')
for tag, i1, i2, j1, j2 in ops[:30]:
    print('--- %s stand[%d:%d] repo[%d:%d]' % (tag, i1 + 1, i2, j1 + 1, j2))
    for l in a[i1:min(i2, i1 + 3)]:
        print('  C: ' + l.strip()[:100])
    for l in b[j1:min(j2, j1 + 3)]:
        print('  R: ' + l.strip()[:100])
