import io, re, hashlib

p = r'C:\Users\Manya\Documents\deepseek-harness\default-workspace\web-form-phd-artem\Fore\WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV.fore'
t = io.open(p, encoding='utf-8').read().replace('\r\n', '\n')
log = []

# ===================== 1. Поля модуля =====================
anchor = 'extraCaptions: StringList;'
extra_vars = '''	extraCaptions: StringList;
	extraYtdPeriods: StringList;
	extraYtdConds: StringList;
	extraYtdCaptions: StringList;
	extraCorrPeriods: StringList;
	extraCorrConds: StringList;
	extraCorrCaptions: StringList;'''
if 'extraYtdPeriods' not in t:
    t = t.replace(anchor, extra_vars, 1)
    log.append('добавлены поля extraYtd*/extraCorr*')

# ===================== 2. Новые процедуры сбора периодов =====================
periods = [
    (1, 'CB_JANUARY', 'Январь'), (2, 'CB_FEBRUARY', 'Февраль'), (3, 'CB_MARCH', 'Март'),
    (4, 'CB_APRIL', 'Апрель'), (5, 'CB_MAY', 'Май'), (6, 'CB_JUNE', 'Июнь'),
    (7, 'CB_JULY', 'Июль'), (8, 'CB_AUGUST', 'Август'), (9, 'CB_SEPTEMBER', 'Сентябрь'),
    (10, 'CB_OCTOBER', 'Октябрь'), (11, 'CB_NOVEMBER', 'Ноябрь'), (12, 'CB_DECEMBER', 'Декабрь'),
    (13, 'CB_FIRST_QUARTER', 'I кв.'), (14, 'CB_SECOND_QUARTER', 'II кв.'), (15, 'CB_SIX_MONTH', '6 мес.'),
    (16, 'CB_THIRD_QUARTER', 'III кв.'), (17, 'CB_NINE_MONTH', '9 мес.'), (18, 'CB_FOURTH_QUARTER', 'IV кв.'),
    (19, 'CB_YEAR', 'Год'),
]

procs = '''
	/// <summary>Период «с начала года» (CB_*_YEAR_TO_DATE): считается по ZVALUE_SNG</summary>
	Sub addYtdPeriodIfChecked(cb: IWebCheckBox; periodNum: Integer; cond: String; caption: String);
	Begin
		If IsNull(cb) Then Return; End If;
		If Not cb.Checked Then Return; End If;
		extraYtdPeriods.Add(periodNum.ToString);
		extraYtdConds.Add(cond);
		extraYtdCaptions.Add(caption);
	End Sub addYtdPeriodIfChecked;

	/// <summary>Период «корректировки» (CB_*_CORR): ZSIU_INDV с фильтром ZLIB_INFS = 'KOROUND'</summary>
	Sub addCorrPeriodIfChecked(cb: IWebCheckBox; periodNum: Integer; cond: String; caption: String);
	Begin
		If IsNull(cb) Then Return; End If;
		If Not cb.Checked Then Return; End If;
		extraCorrPeriods.Add(periodNum.ToString);
		extraCorrConds.Add(cond);
		extraCorrCaptions.Add(caption);
	End Sub addCorrPeriodIfChecked;
'''
if 'addYtdPeriodIfChecked' not in t:
    m = re.search(r'\n\tEnd Sub addPeriodIfChecked;', t)
    t = t[:m.end()] + '\n' + procs + t[m.end():]
    log.append('добавлены addYtdPeriodIfChecked / addCorrPeriodIfChecked')

# ===================== 3. buildExtraFields: инициализация, очистка, вызовы =====================
old_init = '''		If IsNull(extraPeriods) Then
			extraPeriods := New StringList.Create;
		End If;
		extraPeriods.Clear;
		extraConds.Clear;
		extraCaptions.Clear;'''
new_init = '''		If IsNull(extraPeriods) Then
			extraPeriods := New StringList.Create;
		End If;
		If IsNull(extraYtdConds) Then
			extraYtdConds := New StringList.Create;
		End If;
		If IsNull(extraYtdCaptions) Then
			extraYtdCaptions := New StringList.Create;
		End If;
		If IsNull(extraYtdPeriods) Then
			extraYtdPeriods := New StringList.Create;
		End If;
		If IsNull(extraCorrConds) Then
			extraCorrConds := New StringList.Create;
		End If;
		If IsNull(extraCorrCaptions) Then
			extraCorrCaptions := New StringList.Create;
		End If;
		If IsNull(extraCorrPeriods) Then
			extraCorrPeriods := New StringList.Create;
		End If;
		extraPeriods.Clear;
		extraConds.Clear;
		extraCaptions.Clear;
		extraYtdPeriods.Clear;
		extraYtdConds.Clear;
		extraYtdCaptions.Clear;
		extraCorrPeriods.Clear;
		extraCorrConds.Clear;
		extraCorrCaptions.Clear;'''
if old_init in t:
    t = t.replace(old_init, new_init, 1)
    log.append('buildExtraFields: инициализация/очистка YTD и CORR')

calls = []
calls.append('\n\t\t// --- 1a. Периоды «с начала года» (CB_*_YEAR_TO_DATE) — ZVALUE_SNG')
for num, cb, cap in periods:
    if cb == 'CB_SIX_MONTH':
        continue  # чекбокса CB_SIX_MONTH_YEAR_TO_DATE на форме нет
    cond = 'period = %d' % num if num <= 12 else 'period IN (%d)' % num
    calls.append('\t\taddYtdPeriodIfChecked(%s_YEAR_TO_DATE, %d, "%s", "%s");' % (cb, num, cond, cap))
calls.append('\n\t\t// --- 1b. Периоды «корректировки» (CB_*_CORR) — ZSIU_INDV, ZLIB_INFS = KOROUND')
for num, cb, cap in periods:
    cond = 'period = %d' % num if num <= 12 else 'period IN (%d)' % num
    calls.append('\t\taddCorrPeriodIfChecked(%s_CORR, %d, "%s", "%s");' % (cb, num, cond, cap))
block = '\n'.join(calls) + '\n'

anchor2 = '\t\t// --- 2. Поля вывода по данным D_ZTYPEIND'
if anchor2 in t and 'addYtdPeriodIfChecked(CB_JANUARY_YEAR_TO_DATE' not in t:
    t = t.replace(anchor2, block + anchor2, 1)
    log.append('buildExtraFields: вызовы для YTD (%d) и CORR (%d)' % (
        sum(1 for c in calls if 'addYtdPeriodIfChecked' in c), sum(1 for c in calls if 'addCorrPeriodIfChecked' in c)))

# ===================== 4. addExtraColumn: доп. фильтр =====================
old_col = re.search(r'\n\tSub addExtraColumn\([^\n]*\n\tBegin\n\t\texprs\.Add\([^\n]*\n\t\tnames\.Add\([^\n]*\n\tEnd Sub addExtraColumn;', t)
new_col = '''
	Sub addExtraColumn(exprs: StringList; names: StringList; agg: String; cond: String; typeId: String; alias: String; name: String; extraFilter: String);
	Var
		filterCond: String;
	Begin
		filterCond := cond + " AND ztypeind = '" + typeId + "'";
		If Not extraFilter.IsEmpty Then
			filterCond := filterCond + " AND " + extraFilter;
		End If;
		exprs.Add(agg + " FILTER (WHERE " + filterCond + ") AS """ + alias + """");
		names.Add("""" + name + """");
	End Sub addExtraColumn;'''
if old_col:
    t = t[:old_col.start()] + new_col + t[old_col.end():]
    log.append('addExtraColumn: параметр extraFilter')

# ===================== 5. addExtraForType: три блока =====================
old_ftype = re.search(r'\n\tSub addExtraForType\([^\n]*\n[\s\S]*?\n\tEnd Sub addExtraForType;', t)
periods_regular = None
new_ftype = '''
	Sub addExtraForType(exprs: StringList; names: StringList; typeId: String; typeName: String; hasStatus: Boolean);
	Var
		i: Integer;
		caption: String;
	Begin
		// 1) за период: ZSIU_INDV
		For i := 0 To extraCaptions.Count - 1 Do
			caption := extraCaptions.Item(i) As String;
			addExtraColumn(exprs, names, "SUM(zsiu_indv)", extraConds.Item(i) As String, typeId,
				caption + " (" + typeName + ")", caption + " (" + typeName + ")", "");
			If hasStatus Then
				addExtraColumn(exprs, names, "MAX(zphd_stat)", extraConds.Item(i) As String, typeId,
					caption + ". Статус (" + typeName + ")", caption + ". Статус (" + typeName + ")", "");
			End If;
		End For;
		// 2) с начала года: ZVALUE_SNG
		For i := 0 To extraYtdCaptions.Count - 1 Do
			caption := extraYtdCaptions.Item(i) As String;
			addExtraColumn(exprs, names, "SUM(zvalue_sng)", extraYtdConds.Item(i) As String, typeId,
				caption + ". С нач.года (" + typeName + ")", caption + ". С нач.года (" + typeName + ")", "");
			If hasStatus Then
				addExtraColumn(exprs, names, "MAX(zphd_stat)", extraYtdConds.Item(i) As String, typeId,
					caption + ". С нач.года. Статус (" + typeName + ")", caption + ". С нач.года. Статус (" + typeName + ")", "");
			End If;
		End For;
		// 3) корректировки: ZSIU_INDV с ZLIB_INFS = 'KOROUND'
		For i := 0 To extraCorrCaptions.Count - 1 Do
			caption := extraCorrCaptions.Item(i) As String;
			addExtraColumn(exprs, names, "SUM(zsiu_indv)", extraCorrConds.Item(i) As String, typeId,
				caption + " (Коррект.) (" + typeName + ")", caption + " (Коррект.) (" + typeName + ")", "zlib_infs = 'KOROUND'");
			If hasStatus Then
				addExtraColumn(exprs, names, "MAX(zphd_stat)", extraCorrConds.Item(i) As String, typeId,
					caption + ". Статус (Коррект.) (" + typeName + ")", caption + ". Статус (Коррект.) (" + typeName + ")", "zlib_infs = 'KOROUND'");
			End If;
		End For;
	End Sub addExtraForType;'''
if old_ftype:
    t = t[:old_ftype.start()] + new_ftype + t[old_ftype.end():]
    log.append('addExtraForType: три блока (период / с нач.года / корректировки)')

# ===================== 6. Пере-вызовы addExtraColumn вне addExtraForType (если есть) =====================
# проверяем, что все вызовы addExtraColumn имеют 8 аргументов
bad = [l for l in t.split('\n') if 'addExtraColumn(' in l and not re.match(r'^\s*Sub addExtraColumn', l)]
print('вызовов addExtraColumn:', len(bad))

io.open(p, 'w', encoding='utf-8', newline='').write(t.replace('\n', '\r\n'))
b = io.open(p, 'rb').read()
print('правок:', len(log))
for x in log:
    print('  - ' + x)
print('строк:', t.count('\n') + 1, '; SHA-256:', hashlib.sha256(b).hexdigest())
