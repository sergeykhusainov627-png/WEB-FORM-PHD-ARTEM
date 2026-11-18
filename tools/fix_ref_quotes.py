import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')

fixes = [
    # (что искать, на что заменить)
    ("""			refCols := refCols + '        (SELECT t.ACTVTS FROM ' + nsiTable(C_NSI_RDSD_INDS) + ' t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Код вида деятельности"",' + C_CRLF;""",
     """			refCols := refCols + "        (SELECT t.ACTVTS FROM " + nsiTable(C_NSI_RDSD_INDS) + " t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Код вида деятельности""," + C_CRLF;"""),
    ("""			refCols := refCols + '        (SELECT t.SNAME FROM ' + nsiTable(C_NSI_RDSD_INDS) + ' t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Наименование вида деятельности"",' + C_CRLF;""",
     """			refCols := refCols + "        (SELECT t.SNAME FROM " + nsiTable(C_NSI_RDSD_INDS) + " t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Наименование вида деятельности""," + C_CRLF;"""),
    ("""			refCols := refCols + '        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS ""Формы ТЭП СНГ"",' + C_CRLF;""",
     """			refCols := refCols + "        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS ""Формы ТЭП СНГ""," + C_CRLF;"""),
]
n = 0
for old, new in fixes:
    if old in t:
        t = t.replace(old, new, 1)
        n += 1

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('исправлено строк на двойные кавычки:', n)
print('одиночные кавычки в блоке refCols:', len(re.findall(r"refCols := refCols \+ '", t)))
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())
