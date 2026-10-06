# patch-webform.py — дописывает в модуль веб-формы СЭ логику «Поля для вывода», режимы
# «Выводить коды аналитик»/«Выводить информацию по статусам», значения по умолчанию и
# ограничение выбора СП по полномочиям (по ТТ «Анализ и выгрузка данных ТЭП»).
#
# Таблица «чек-бокс -> идентификатор поля отчёта» собирается автоматически:
#   * 58 существующих обработчиков (их аргументы уже согласованы с отчётом) — как есть;
#   * новые поля (ТТ «Данные показателя», «Данные расчёта») и периоды — из списков ниже.
#
# Запуск: python tools/patch-webform.py <исходный.fore> <результат.fore>

import io, re, sys

src_path, dst_path = sys.argv[1], sys.argv[2]
src = io.open(src_path, encoding='utf-8').read().replace('\r\n', '\n')   # работаем в LF
orig = src

def sub_once(pattern, repl, text, what):
    new, n = re.subn(pattern, repl, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('НЕ НАЙДЕНО (%s): %s' % (what, pattern[:70]))
    return new

# ---------------------------------------------------------------- 0. сбор таблицы полей
existing = re.findall(r'fillFieldListByStatusFlag\(\s*([A-Za-z_]\w*)\s*,\s*"([^"]+)"\s*\)', src)
existing = [(c, f) for c, f in existing if c != 'CB']          # без строки-определения метода
seen, pairs = set(), []
for c, f in existing:
    if c not in seen:
        seen.add(c)
        pairs.append((c, f))

# Новые поля: контрол -> идентификатор (⚠ — в ТТ идентификатор не указан, принят по имени поля)
NEW_FIELDS = [
    ('CbHigherInd', 'ZPH_HIGHER', 'Вышестоящий ТЭП (⚠ уточнить)'),
    ('CB_ACTIVITY_TYPE', 'ACTVTS', 'Вид деятельности'),
    ('CB_IND_TYPE', 'ID1', 'Вид показателя'),
    ('CB_TEP_FORM_OF_SNG', 'ZF_NUMB', 'Формы отчётов'),
    ('CB_TEP_OWNER', 'OWNER', 'Владелец ТЭП'),
    ('CB_FUNCTION_OF_WOKERS', 'ZPH_FUNC', 'Функция/задача (⚠ уточнить)'),
    ('CB_VOLUME', 'ZPH_VOLUME', 'Объёмный (⚠ уточнить)'),
    ('CB_TRUD', 'ZPH_TRUD', 'Трудоёмкость (⚠ уточнить)'),
    ('CB_COMPARABLE_PRICES', 'ZPH_PRICE_CP', 'В сопоставимых ценах (⚠ уточнить)'),
    ('CB_CURRENT_PRICES', 'ZPH_PRICE_CD', 'В действующих ценах (⚠ уточнить)'),
    ('CB_ACTTYPE2', 'ZPH_ACTTYPE2', 'Вид работ (классификация) (⚠ уточнить)'),
]
# Значения ТЭП: месяцы и периоды (ТТ: TBL_PHD_FAP_MULT.ZSIU_INDV при QUARTER/CALMONTH).
# Имена полей периодов в ТТ не приведены — принят шаблон ZSIU_INDV_<период> (⚠ уточнить).
PERIODS = [
    ('CB_JANUARY', 'ZSIU_INDV_01', 'Январь'), ('CB_FEBRUARY', 'ZSIU_INDV_02', 'Февраль'),
    ('CB_MARCH', 'ZSIU_INDV_03', 'Март'), ('CB_APRIL', 'ZSIU_INDV_04', 'Апрель'),
    ('CB_MAY', 'ZSIU_INDV_05', 'Май'), ('CB_JUNE', 'ZSIU_INDV_06', 'Июнь'),
    ('CB_JULY', 'ZSIU_INDV_07', 'Июль'), ('CB_AUGUST', 'ZSIU_INDV_08', 'Август'),
    ('CB_SEPTEMBER', 'ZSIU_INDV_09', 'Сентябрь'), ('CB_OCTOBER', 'ZSIU_INDV_10', 'Октябрь'),
    ('CB_NOVEMBER', 'ZSIU_INDV_11', 'Ноябрь'), ('CB_DECEMBER', 'ZSIU_INDV_12', 'Декабрь'),
    ('CB_FIRST_QUARTER', 'ZSIU_INDV_Q1', 'I кв.'), ('CB_SECOND_QUARTER', 'ZSIU_INDV_Q2', 'II кв.'),
    ('CB_THIRD_QUARTER', 'ZSIU_INDV_Q3', 'III кв.'), ('CB_FOURTH_QUARTER', 'ZSIU_INDV_Q4', 'IV кв.'),
    ('CB_SIX_MONTH', 'ZSIU_INDV_Q6', '6 мес.'), ('CB_NINE_MONTH', 'ZSIU_INDV_Q9', '9 мес.'),
    ('CB_YEAR', 'ZSIU_INDV_Q0', 'Год'),
]
# Обработчики периодов в модуле названы не по имени контрола — сохраняем их имена как есть
PERIOD_HANDLERS = {'CB_NOVEMBER': 'CbNovember', 'CB_THIRD_QUARTER': 'CbThirdQuarter'}
PERIOD_CTRLS = {c for c, _, _ in PERIODS}
for ctrl, fid, title in PERIODS:
    if (ctrl, fid) not in [(a, b) for a, b, _ in NEW_FIELDS]:
        NEW_FIELDS.append((ctrl, fid, title))

pairs_block = ['\t\t// --- существующие поля (идентификаторы уже согласованы с отчётом) ---']
for c, f in sorted(pairs):
    pairs_block.append('\t\t_fieldIds.Add("%s", "%s");' % (c, f))
pairs_block.append('\t\t')
pairs_block.append('\t\t// --- поля ТТ, для которых обработчиков не было ---')
for c, f, title in NEW_FIELDS:
    pairs_block.append('\t\t_fieldIds.Add("%s", "%s");%s// %s' % (c, f, ' ' * max(1, 34 - len(c) - len(f)), title))
pairs_text = '\n'.join(pairs_block)

# Строки сбора состояний чек-боксов: IWebComponents нельзя объявлять как тип (в отличие от
# IWebComponent) и Self.Components использовать нельзя — перебираем контролы явным списком.
collect_lines = []
for ctrl, _fid in sorted(pairs):
    collect_lines.append('\t\tCollectIfChecked(%s, "%s");' % (ctrl, ctrl))
for ctrl, _fid, _title in NEW_FIELDS:
    if ctrl not in {c for c, _ in pairs}:
        collect_lines.append('\t\tCollectIfChecked(%s, "%s");' % (ctrl, ctrl))
collect_text = '\n'.join(collect_lines)

# ---------------------------------------------------------------- 1. поля класса
src = sub_once(
    r'(\t_hlink: ITabHyperlink;\n)',
    r'''\1	
	// --- «Поля для вывода»: таблицы соответствия «имя чек-бокса -> идентификатор поля отчёта» ---
	_fieldIds: IHashtable;
	_codeIds: IHashtable;
''',
    src, 'поля класса')

# ---------------------------------------------------------------- 2. константы
src = sub_once(
    r'(\tConst C_PARAM_ZPKR_SUBP = "ZPKR_SUBP";\n)',
    r'''\1	// Значения по умолчанию для СЭ (ТТ, лист «Селекционный экран»)
	Const C_DEFAULT_TYPE_IND = "0000000001";
	Const C_ACCESS_SP_GROUP = "PHD_ADMIN";
	Const C_ACCESS_SP_GROUP_PREFIX = "PHD_CURATOR_";
	// Суффикс идентификатора поля статуса для режима «Выводить информацию по статусам»
	Const C_STATUS_FIELD_SUFFIX = "_STAT";
	// Отмечать ли чек-боксы «Поля для вывода» по умолчанию (ТТ: Год, СП, ТЭП, Ед.измерения,
	// I кв., II кв., 6 мес., III кв., 9 мес., IV кв., Год). False — вывод только по выбору пользователя.
	Const C_APPLY_DEFAULT_CHECKED = True;
''',
    src, 'константы')

# ---------------------------------------------------------------- 3. initialization
src = sub_once(
    r'\tSub initialization;\n\tBegin\t\n\t\tMB := MetabaseClass\.Active;\n\t\tIf fieldList = Null Then fieldList := New StringList\.Create; End If;\t\t\n\tEnd Sub initialization;',
    '''\tSub initialization;
\tBegin\t
\t\tMB := MetabaseClass.Active;
\t\tIf IsNull(fieldList) Then fieldList := New StringList.Create; End If;
\t\tInitOutputFieldIds;
\tEnd Sub initialization;''',
    src, 'initialization')

# ---------------------------------------------------------------- 4. getUserSP — без падений
src = sub_once(
    r'\tPrivate Function getUserSP: String;.*?\n\tEnd Function getUserSP;',
    '''\tPrivate Function getUserSP: String;
\tVar
\t\tuserSP: String;
\t\tUser: IMetabaseUser;
\tBegin
\t\t// СП пользователя из основной записи (атрибут BUS_AREA). Ошибки не должны ронять форму.
\t\tuserSP := "";
\t\tTry
\t\t\tUser := MB.LogonSession.User; //Получаем пользователя запустившего отчет
\t\t\tIf Not IsNull(User) Then
\t\t\t\tuserSP := User.Attributes.FindById("BUS_AREA").Value As String; //Получаем значение атрибута "BUS_AREA"
\t\t\tEnd If;
\t\tExcept On E: Exception Do
\t\t\tuserSP := "";
\t\tEnd Try;
\t\tReturn userSP;
\tEnd Function getUserSP;''',
    src, 'getUserSP')

# ---------------------------------------------------------------- 5. setDefaultDimensionValue
src = sub_once(
    r'\tSub setDefaultDimensionValue;.*?\n\tEnd Sub setDefaultDimensionValue;',
    '''\t/// <summary>
\t/// 	Значения по умолчанию СЭ (ТТ, лист «Селекционный экран»): год — текущий, СП — из основной
\t/// 	записи пользователя, тип данных — «План», плюс набор полей вывода по умолчанию.
\t/// </summary>
\tSub setDefaultDimensionValue;
\tBegin
\t\tinitialization;
\t\t// Год: текущий год
\t\tsetComboSelectionByAttribute(D_CALYEAR, C_PARAM_CALYEAR, "NAME", DateTime.Now.Year.ToString);
\t\t// СП: из основной записи пользователя
\t\tsetComboSelectionByAttribute(D_PLANT, C_PARAM_PLANT, "CODE", getUserSP);
\t\t// Тип данных: «План» (ID 0000000001)
\t\tsetComboSelectionByAttribute(D_ZTYPEIND, C_PARAM_ZTYPEIND, "ID", C_DEFAULT_TYPE_IND);
\t\t// Поля вывода, установленные по умолчанию (ТТ, лист «СЭ - поля для вывода»)
\t\tinitOutputDefaults;
\t\tRefreshFieldList;
\tEnd Sub setDefaultDimensionValue;''',
    src, 'setDefaultDimensionValue')

# ---------------------------------------------------------------- 6. обработчик onShow
src = sub_once(
    r'\tSub ANALIZ_TEP_FORM_ON_SHOW;\n\tVar\s*\n\t\topenReportTab: ITabSheet;\n\t\toptionReport: IPrxReport;\n\t\tMObj:IMetabaseObject;\t\t\t\n\tBegin\n\t\t_hlink := InitializeHlinkOpenObject\(ReportBoxOk\.Report, "  Ок  ", C_ANALYZ_TEP_REP_ID\);\n\t\t\n\t\tsetDefaultDimensionValue;',
    '''\tSub ANALIZ_TEP_FORM_ON_SHOW;
\tBegin
\t\t_hlink := InitializeHlinkOpenObject(ReportBoxOk.Report, "  Ок  ", C_ANALYZ_TEP_REP_ID);
\t\t// Создаёт COpenHyperlink и менеджер параметров (геттер свойства Hyperlink)
\t\t_AnalyzTepHyperlink := Hyperlink;
\t\t// Значения по умолчанию, набор полей вывода и генерация ссылки
\t\tsetDefaultDimensionValue;
\t\t// Ограничение выбора СП согласно полномочиям (ТТ, лист «Селекционный экран»)
\t\tapplyPlantAccessRights;''',
    src, 'onShow (начало)')

# ---------------------------------------------------------------- 7. UpdateOpenDefHlinkFromSelection
src = sub_once(
    r'\tSub UpdateOpenDefHlinkFromSelection\(paramId: String; dimSel: IDimSelection; attrId: String = ""\);\n\tVar\n\t\tparamValue: Variant;\n\tBegin\n\t\tparamValue := WebFormsExt\.GetDimSelectionAttrValue\(dimSel, attrId\);\n\t\tUpdateOpenDefHlink\(paramId, paramValue\);\n\tEnd Sub UpdateOpenDefHlinkFromSelection;',
    '''\t/// <summary>
\t/// 	Передаёт значение отметки в гиперссылку. Значение пишется в менеджер параметров
\t/// 	(CObjectParamManager), из которого строку действия собирает COpenHyperlink.Generate.
\t/// 	Ручная сборка строки не нужна: Generate всё равно пересобирает её из менеджера параметров.
\t/// </summary>
\tSub UpdateOpenDefHlinkFromSelection(paramId: String; dimSel: IDimSelection; attrId: String = "");
\tBegin
\t\tIf IsNull(dimSel) Then Return; End If;
\t\tHyperlink.SetParamValueFromSelection(paramId, dimSel, attrId);
\tEnd Sub UpdateOpenDefHlinkFromSelection;''',
    src, 'UpdateOpenDefHlinkFromSelection')

# ---------------------------------------------------------------- 8. удалить ручной редактор строки
src = sub_once(
    r'\tSub UpdateOpenDefHlink\(paramId: String; paramValue: Variant\);.*?\n\tEnd Sub UpdateOpenDefHlink;\n',
    '''\t/// <summary>
\t/// 	Здесь был ручной разбор строки действия (UpdateOpenDefHlink + 5 вложенных подпрограмм).
\t/// 	Он удалён: COpenHyperlink.Generate пересобирает строку из менеджера параметров и затирает
\t/// 	ручную правку, а сам разбор мог падать на String.SubString(-1) при отсутствующем параметре.
\t/// </summary>
''',
    src, 'удаление UpdateOpenDefHlink')

# ---------------------------------------------------------------- 9. поля без чек-бокса
src = sub_once(
    r'\tSub addDefaultFieldsToStringList;\n\tBegin\n\t\tfieldList\.Add\("CALYEAR,PLANT,ZLIB_INDC"\);\n\t\t//fieldList\.Add\("PLANT"\);\n\t\t//fieldList\.Add\("ZLIB_INDC"\);\n\tEnd Sub addDefaultFieldsToStringList;',
    '''\t/// <summary>
\t/// 	Полей, выводимых без чек-бокса, нет: в P_FIELD_LIST попадают ТОЛЬКО отмеченные поля,
\t/// 	поэтому если чек-бокс не отмечен — в отчёте не будет ни значения, ни колонки.
\t/// 	Если когда-нибудь понадобится выводить поле, для которого в форме нет чек-бокса,
\t/// 	добавьте здесь строку вида:  addFieldToList("CALYEAR");   // Год
\t/// </summary>
\tSub addFieldsWithoutCheckBox;
\tBegin
\tEnd Sub addFieldsWithoutCheckBox;''',
    src, 'addDefaultFieldsToStringList')

# ---------------------------------------------------------------- 10. fillFieldListByStatusFlag
src = sub_once(
    r'\tSub fillFieldListByStatusFlag\(CB: IWebCheckBox; fieldName : String\);\n\tBegin\t\n\t\tIf CB <> Null Then\n\t\t\tIf CB\.Checked Then\n\t\t\t\tfieldList\.Add\(fieldName\);\n\t\t\tElse\n\t\t\t\tfieldList\.Remove\(fieldName\);\n\t\t\tEnd If;\n\t\t\tHyperlink\.SetParamValue\("P_FIELD_LIST", fieldList\.Text\(", "\)\);\n\t\t\tHyperlink\.Generate;\n\t\t\tTextArea1\.Text := Hyperlink\.Action;\n\t\tEnd If;\t\t\n\tEnd Sub fillFieldListByStatusFlag;',
    '''\t/// <summary>
\t/// 	Обработчик чек-бокса «Поля для вывода». Идентификатор поля берётся из таблицы
\t/// 	InitOutputFieldIds по имени контрола, поэтому список всегда пересобирается целиком.
\t/// </summary>
\tSub fillFieldListByStatusFlag(CB: IWebCheckBox; fieldName : String);
\tBegin\t
\t\tIf IsNull(CB) Then Return; End If;
\t\tRefreshFieldList;
\tEnd Sub fillFieldListByStatusFlag;''',
    src, 'fillFieldListByStatusFlag')

# ---------------------------------------------------------------- 11. прямые вызовы _AnalyzTepHyperlink
for macro, var in [('ZLIB_INFS', 'p_zlib_infs'), ('ZBUR_BEG', 'p_zbur_beg'), ('ZBUR_END', 'p_zbur_end'), ('ZPKR_SUBP', 'p_zpkr_subp')]:
    old = '_AnalyzTepHyperlink.SetParamValue(C_PARAM_%s, %s);' % (macro, var)
    new = 'Hyperlink.SetParamValue(C_PARAM_%s, %s);\n\t\tHyperlink.Generate;' % (macro, var)
    if old not in src:
        raise SystemExit('НЕ НАЙДЕНО (прямой вызов %s)' % macro)
    src = src.replace(old, new)

# ---------------------------------------------------------------- 12. пустые обработчики периодов
for ctrl, fid, title in PERIODS:
    handler = PERIOD_HANDLERS.get(ctrl, ctrl)
    src = sub_once(
        r'\tSub %sOnChange;\n\tBegin\n\t\t\n\tEnd Sub %sOnChange;' % (handler, handler),
        '''\tSub %sOnChange;
\tBegin
\t\tfillFieldListByStatusFlag(%s, "%s");
\tEnd Sub %sOnChange;''' % (handler, ctrl, fid, handler),
        src, 'период ' + handler)

# ---------------------------------------------------------------- 13. новые обработчики + справка
new_subs = []
for ctrl, fid, title in NEW_FIELDS:
    if ctrl in PERIOD_CTRLS:         # обработчики периодов заполнены в шаге 12 (в т.ч. под их именами)
        continue
    new_subs.append('''\tSub %sOnChange;
\tBegin
\t\tfillFieldListByStatusFlag(%s, "%s");
\tEnd Sub %sOnChange;''' % (ctrl, ctrl, fid, ctrl))

# Дубли обработчиков периодов под каноничными именами: если в дизайнере событие привязано
# к <Контрол>OnChange, сработает именно этот вариант (у CbNovember/CbThirdQuarter имена иные).
for ctrl, fid, title in PERIODS:
    if PERIOD_HANDLERS.get(ctrl, ctrl) != ctrl:
        new_subs.append('''\tSub %sOnChange;
\tBegin
\t\tfillFieldListByStatusFlag(%s, "%s");
\tEnd Sub %sOnChange;''' % (ctrl, ctrl, fid, ctrl))

new_subs.append('''\tSub CB_DISPLAY_CODE_ANALYTOnChange;
\tBegin
\t\tRefreshFieldList;
\tEnd Sub CB_DISPLAY_CODE_ANALYTOnChange;''')
new_subs.append('''\tSub CB_DISPLAY_INFO_BY_STATUSOnChange;
\tBegin
\t\tRefreshFieldList;
\tEnd Sub CB_DISPLAY_INFO_BY_STATUSOnChange;''')

HELPERS = r'''
	// ============================================================================================
	//  «Поля для вывода» — идентификаторы полей отчёта для параметра P_FIELD_LIST
	//
	//  Источник: ТТ «Анализ и выгрузка данных ТЭП», лист «Вывод полей в отчете» (колонка «Поле»).
	//  Идентификаторы, помеченные «уточнить», в ТТ не указаны — приняты по имени поля/контрола;
	//  при расхождении с отчётом PRX_ANALYSIS_TEP правьте ТОЛЬКО этот метод.
	//
	//  Чего пока нет (нужны контролы в дизайнере формы):
	//    * группа «Значения ТЭП с начала года»  — 19 полей, источник TBL_PHD_FAP_MULT.ZVALUE_SNG;
	//    * группа «Значения корректировок ТЭП»   — 19 полей, ZSIU_INDV + ZLIB_INFS=KOROUND;
	//    * «Класс вида оборудования» (ZCLSVOBOR) — есть поле в ТТ, контрола на форме нет;
	//    * не размечены: CB_ANALYTIC_SET, CB_AREA, CB_ESTIMATED_PRICES, CB_MVP_TEP, CbESO3
	//      (в ТТ не найдены — уточнить назначение).
	// ============================================================================================
	Sub InitOutputFieldIds;
	Begin
		If Not IsNull(_fieldIds) Then Return; End If;
		_fieldIds := New Hashtable.Create;
		_codeIds := New Hashtable.Create;
__FIELDS__
		
		// --- Идентификаторы полей-кодов для режима «Выводить коды аналитик»
		// (ТТ, лист «Вывод полей в отчете», колонка «Поле» при «Выводить код = да»).
		// Ключ — основной идентификатор поля; указываются только те, где код отличается от него.
		_codeIds.Add("PLANT", "SP");
		_codeIds.Add("SOLD_TO", "KEY");
		_codeIds.Add("ZPH_USR2", "CODE_ZPH_USR0");
		_codeIds.Add("PERIOD_TYPE", "PERIOD_TY");
	End Sub InitOutputFieldIds;
	
	/// <summary>
	/// 	Пересобирает P_FIELD_LIST по состояниям чек-боксов и генерирует гиперссылку.
	/// 	Единственная точка изменения списка полей: чек-боксы + таблица InitOutputFieldIds.
	/// 	Перебор контролов — явным списком: IWebComponents нельзя объявлять как тип
	/// 	(в отличие от IWebComponent), поэтому Self.Components здесь не используется.
	/// </summary>
	Sub RefreshFieldList;
	Var
		codes: String;
	Begin
		If IsNull(fieldList) Then fieldList := New StringList.Create; End If;
		fieldList.Clear;
		addFieldsWithoutCheckBox;
		
__COLLECT__
		
		// Режим «Выводить информацию по статусам»: к выбранным периодам добавляются поля статусов
		If (Not IsNull(CB_DISPLAY_INFO_BY_STATUS)) And CB_DISPLAY_INFO_BY_STATUS.Checked Then
			addStatusFields;
		End If;
		
		Hyperlink.SetParamValue("P_FIELD_LIST", fieldList.Text(", "));
		
		// Режим «Выводить коды аналитик»: список аналитик, по которым отчёт добавляет коды
		codes := "";
		If (Not IsNull(CB_DISPLAY_CODE_ANALYT)) And CB_DISPLAY_CODE_ANALYT.Checked Then
			codes := codeFieldsText;
		End If;
		setParamOrRemove(C_PARAM_P_ANALYTIC_SET, codes);
		
		Hyperlink.Generate;
		If Not IsNull(TextArea1) Then TextArea1.Text := Hyperlink.Action; End If;
	End Sub RefreshFieldList;
	
	/// <summary>Идентификатор поля отчёта по имени чек-бокса (пусто — контрол не размечен)</summary>
	Function fieldIdByControl(controlName: String): String;
	Var
		value: Variant;
	Begin
		If IsNull(_fieldIds) Or controlName.IsEmpty Then Return ""; End If;
		value := _fieldIds.Item(controlName);
		If IsNull(value) Then Return ""; End If;
		Return value As String;
	End Function fieldIdByControl;
	
	/// <summary>Добавляет поле, если его чек-бокс отмечен (идентификатор берётся из таблицы)</summary>
	Sub CollectIfChecked(cb: IWebCheckBox; controlName: String);
	Begin
		If IsNull(cb) Then Return; End If;
		If Not cb.Checked Then Return; End If;
		addFieldToList(fieldIdByControl(controlName));
	End Sub CollectIfChecked;
	
	/// <summary>Добавляет идентификатор в список полей, если его там ещё нет</summary>
	Sub addFieldToList(fieldId: String);
	Begin
		If IsNull(fieldList) Or fieldId.IsEmpty Then Return; End If;
		If fieldList.IndexOf(fieldId) = -1 Then fieldList.Add(fieldId); End If;
	End Sub addFieldToList;
	
	/// <summary>Поля статусов для выбранных периодов (режим «Выводить информацию по статусам»)</summary>
	Sub addStatusFields;
	Var
		fieldId: String;
		i, count: Integer;
	Begin
		// count фиксируем заранее: добавляемые поля статусов не должны попасть в этот же перебор
		count := fieldList.Count;
		For i := 0 To count - 1 Do
			fieldId := fieldList.Item(i) As String;
			If fieldId.StartsWith("ZSIU_INDV_") Then
				addFieldToList(fieldId + C_STATUS_FIELD_SUFFIX);
			End If;
		End For;
	End Sub addStatusFields;
	
	/// <summary>Список полей-кодов выбранных аналитик (режим «Выводить коды аналитик»)</summary>
	Function codeFieldsText: String;
	Var
		list: IStringList;
		fieldId: String;
		codeId: Variant;
		i, count: Integer;
	Begin
		list := New StringList.Create;
		count := fieldList.Count;
		For i := 0 To count - 1 Do
			fieldId := fieldList.Item(i) As String;
			codeId := _codeIds.Item(fieldId);
			If Not IsNull(codeId) Then
				If list.IndexOf(codeId As String) = -1 Then list.Add(codeId As String); End If;
			End If;
		End For;
		Return list.Text(", ");
	End Function codeFieldsText;
	
	/// <summary>Устанавливает параметр или убирает его из менеджера (пустое значение = убрать)</summary>
	Sub setParamOrRemove(paramId, value: String);
	Var
		params: IHashtable;
	Begin
		If IsNull(Hyperlink.ParameterManager) Then Return; End If;
		params := Hyperlink.ParameterManager.Params;
		If IsNull(params) Then Return; End If;
		If value.IsEmpty Then
			// Пустое значение нельзя писать в параметры: CObjectParamManager присваивает значение как есть
			If params.Contains(paramId) Then params.Remove(paramId); End If;
		Else
			Hyperlink.SetParamValue(paramId, value);
		End If;
	End Sub setParamOrRemove;
	
	/// <summary>Состояния чек-боксов «Поля для вывода» по умолчанию (ТТ, лист «СЭ - поля для вывода»)</summary>
	Sub initOutputDefaults;
	Begin
		If Not C_APPLY_DEFAULT_CHECKED Then Return; End If;
		// Основные данные: СП, ТЭП, Ед.измерения (Год — без чек-бокса, см. C_FIELDS_WITHOUT_CHECKBOX)
		SetCheckBoxIfExists(CB_PLANT, True);
		SetCheckBoxIfExists(CB_ZLIB_INDC, True);
		SetCheckBoxIfExists(CB_ACT_UNIT, True);
		// Значения ТЭП: кварталы, полугодие, 9 месяцев и год
		SetCheckBoxIfExists(CB_FIRST_QUARTER, True);
		SetCheckBoxIfExists(CB_SECOND_QUARTER, True);
		SetCheckBoxIfExists(CB_SIX_MONTH, True);
		SetCheckBoxIfExists(CB_THIRD_QUARTER, True);
		SetCheckBoxIfExists(CB_NINE_MONTH, True);
		SetCheckBoxIfExists(CB_FOURTH_QUARTER, True);
		SetCheckBoxIfExists(CB_YEAR, True);
	End Sub initOutputDefaults;
	
	Sub SetCheckBoxIfExists(CB: IWebCheckBox; checked: Boolean);
	Begin
		If IsNull(CB) Then Return; End If;
		CB.Checked := checked;
	End Sub SetCheckBoxIfExists;
	
	/// <summary>Отметка элемента справочника по значению атрибута (значение — в т.ч. из полномочий)</summary>
	Sub setComboSelectionByAttribute(combo: IWebDimensionCombo; paramId, attrId, value: String);
	Var
		index: Integer;
		sel: IDimSelection;
	Begin
		If IsNull(combo) Or value.IsEmpty Then Return; End If;
		index := DimensionExt.GetElementIndexByAttributeValue(combo.DimInstance, attrId, value);
		If index = -1 Then Return; End If;
		sel := combo.DimInstance.CreateSelection;
		sel.SelectElement(index, False);
		combo.Selection := sel;
		Hyperlink.SetParamValueFromSelection(paramId, combo.Selection, attrId);
	End Sub setComboSelectionByAttribute;
	
	/// <summary>
	/// 	Ограничение на вывод (выбор) СП: PHD_ADMIN и PHD_CURATOR_* выбирают любое СП,
	/// 	остальным подставляется СП из основной записи пользователя и выбор запрещается.
	/// </summary>
	Sub applyPlantAccessRights;
	Var
		spCode: String;
	Begin
		If IsNull(D_PLANT) Then Return; End If;
		If isPlantPrivileged Then Return; End If;
		
		spCode := getUserSP;
		If spCode.IsEmpty Then
			// Полномочий нет и СП не определён — оставляем выбор, иначе форму нельзя заполнить
			Return;
		End If;
		
		setComboSelectionByAttribute(D_PLANT, C_PARAM_PLANT, "CODE", spCode);
		D_PLANT.Enabled := False;
		Hyperlink.Generate;
	End Sub applyPlantAccessRights;
	
	Function isPlantPrivileged: Boolean;
	Var
		user: IMetabaseUser;
		group: ISecuritySubject;
	Begin
		user := MB.LogonSession.User;
		If IsNull(user) Then Return False; End If;
		If user.IsAdmin Then Return True; End If;
		
		For Each group In user.MemberOf Do
			If Not IsNull(group) Then
				If group.Name = C_ACCESS_SP_GROUP Then Return True; End If;
				If group.Name.StartsWith(C_ACCESS_SP_GROUP_PREFIX) Then Return True; End If;
			End If;
		End For;
		
		Return False;
	End Function isPlantPrivileged;
'''.replace('__FIELDS__', pairs_text).replace('__COLLECT__', collect_text)

src = sub_once(r'(\nEnd Class ANALIZ_TEP_FORM_ON_SHOW;)',
               '\n' + '\n'.join(new_subs) + '\n' + HELPERS + r'\1', src, 'вставка обработчиков и справки')

# --- контроль: в живом коде не осталось прямых вызовов _AnalyzTepHyperlink.SetParamValue
live, in_brace = [], False
for l in src.split('\n'):
    t = l.strip()
    if in_brace:
        if '}' in t:
            in_brace = False
        continue
    if t.startswith('//'):
        continue
    if t.startswith('{'):
        if '}' not in t:
            in_brace = True
        continue
    live.append(l)
assert not any('_AnalyzTepHyperlink.SetParamValue' in l for l in live), 'остались прямые вызовы'
# IWebComponents нельзя объявлять как тип (в отличие от IWebComponent), Self.Components — тоже
assert not any('IWebComponents' in l or 'Self.Components' in l for l in live), 'использован IWebComponents/Self.Components'

io.open(dst_path, 'w', encoding='utf-8', newline='').write(src.replace('\n', '\r\n'))
print('готово: %s' % dst_path)
print('строк: %d -> %d; полей в таблице: %d' % (orig.count('\n') + 1, src.count('\n') + 1, len(pairs) + len(NEW_FIELDS)))
