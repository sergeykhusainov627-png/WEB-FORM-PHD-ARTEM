import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
lines = io.open(p, encoding='utf-8').read().replace('\r\n', '\n').split('\n')
log = []

# ---------- 1. Замена трёх строк шаблона на плейсхолдер ----------
idx = [k for k, l in enumerate(lines) if re.match(r'^\s*\+ "        \(SELECT t\.ACTVTS', l)]
if idx and ':REF_COLUMNS' not in '\n'.join(lines):
    i = idx[0]
    lines = lines[:i] + ['\t\t+ "        :REF_COLUMNS" + C_CRLF'] + lines[i + 3:]
    log.append('три справочные колонки заменены плейсхолдером :REF_COLUMNS')
t = '\n'.join(lines)

# ---------- 2. Объявление refCols в buildSql ----------
if 'refCols' not in t:
    t = t.replace('\t\tsql, text, tempId, tempText: String;',
                  '\t\tsql, text, tempId, tempText, refCols: String;', 1)
    log.append('объявлена refCols')

# ---------- 3. Логика формирования справочных колонок ----------
anchor = '\t\tsql := String.Replace(sql, ":EXTRA_NAMES", _sqlExtraNames);'
block = '''
		// Справочные колонки — по чек-боксам «Вид деятельности» и «Формы ТЭП СНГ»
		refCols := "";
		If (Not IsNull(CB_ACTIVITY_TYPE)) And CB_ACTIVITY_TYPE.Checked Then
			refCols := refCols + '        (SELECT t.ACTVTS FROM ' + nsiTable(C_NSI_RDSD_INDS) + ' t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Код вида деятельности"",' + C_CRLF;
			refCols := refCols + '        (SELECT t.SNAME FROM ' + nsiTable(C_NSI_RDSD_INDS) + ' t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS ""Наименование вида деятельности"",' + C_CRLF;
		End If;
		If (Not IsNull(CB_TEP_FORM_OF_SNG)) And CB_TEP_FORM_OF_SNG.Checked Then
			refCols := refCols + '        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS ""Формы ТЭП СНГ"",' + C_CRLF;
		End If;
		sql := String.Replace(sql, ":REF_COLUMNS", refCols);'''
if anchor in t and 'refCols := ""' not in t:
    t = t.replace(anchor, anchor + block, 1)
    log.append('добавлено формирование refCols по чек-боксам')

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('правок:', len(log))
for x in log:
    print('  - ' + x)
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())
print('REF_COLUMNS:', t.count(':REF_COLUMNS'), '; refCols:', t.count('refCols'),
      '; CB_ACTIVITY_TYPE:', t.count('CB_ACTIVITY_TYPE'), '; CB_TEP_FORM_OF_SNG:', t.count('CB_TEP_FORM_OF_SNG'))
