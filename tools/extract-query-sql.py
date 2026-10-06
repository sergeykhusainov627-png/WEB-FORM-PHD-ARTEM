# extract-query-sql.py — достаёт текст SQL запроса из выгрузки Форсайт.
# В pefN.xml текст запроса лежит в <![CDATA[ ... ]]> в виде base64 от UTF-16LE.
# Запуск: python tools/extract-query-sql.py <pefN.xml> <куда.sql|папка>
import base64, io, os, re, sys

src, dst = sys.argv[1], sys.argv[2]
text = io.open(src, encoding='utf-8').read()
blocks = re.findall(r'<!\[CDATA\[(.*?)\]\]>', text, re.S)
if not blocks:
    raise SystemExit('CDATA с текстом запроса не найдено')
if os.path.isdir(dst) or dst.endswith(('/', '\\')):
    os.makedirs(dst, exist_ok=True)
    names = [os.path.join(dst, '%s_%d.sql' % (os.path.splitext(os.path.basename(src))[0], i + 1))
             for i in range(len(blocks))]
else:
    names = [dst]
for name, block in zip(names, blocks):
    sql = base64.b64decode(block).decode('utf-16-le')
    io.open(name, 'w', encoding='utf-8', newline='').write(sql)
    print('%s <- %d символов SQL' % (name, len(sql)))
