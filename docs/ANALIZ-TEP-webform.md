# Веб-форма «Анализ ТЭП» (`backup.txt`) — разбор кода

**Предмет:** `C:\Users\Manya\Downloads\backup.txt` — модуль веб-формы на языке **Fore** (Форсайт),
1574 строки, кодировка UTF-8 без BOM, переводы строк CRLF (проверено побайтово).
**Чем пользовался:** индексированная справка `F:\Scheduler Tasks\docs\forsite\` (`INDEX.md`,
`TOPICS.md`, `api-index.txt`, дампы CHM + `online/`), линтер `F:\Scheduler Tasks\tools\fore-lint-check.js`,
онлайн-справка `help.fsight.ru` (для тем, которых нет в локальном дампе), скрипт инвентаризации
`analiz-tep/tools/form-inventory.js` (написан в ходе разбора).

---

## Итог (TL;DR)

* Форма — **экран подбора параметров** регламентного отчёта: комбобоксы справочников и флажки аналитик →
  строка действия → «кнопка Ок» = гиперссылка в ячейке A1 отчёта, показанного в `ReportBoxOk`.
  По выгрузке окружения: сама форма — `WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV` «Анализ значений ТЭП
  (копия для доработок)» (`KE_CLASS_WEBFORM = 1540`), в `ReportBoxOk` показывается процедурный отчёт
  **`PRX_ANALYSIS_TEP_BUTTON_OK` «Кнопка ОК»** (лист «Лист2»), а ссылка открывает `PRX_ANALYSIS_TEP`.
* Механизм **валиден и документирован**: `ITabHyperlink.Action` + `TabHyperlinkActionType.OpenObject`
  + формат `@ID(ПАРАМЕТР=значение;…)` с массивами `[a,b]`.
* **Главный вывод по коду (по исходникам со стенда):** ссылку в итоге формирует
  `COpenHyperlink.Generate` — она заново собирается из типизированного менеджера параметров
  (`SetParamValue*`) и перезаписывает ячейку. Поэтому ручной разбор строки (`UpdateOpenDefHlink`,
  ~120 строк с 5 вложенными подпрограммами) на результат **не влияет** — это мёртвый груз,
  но именно он исполняется первым и потенциально может упасть (дефект 3).
* Остальное — **незаконченный прототип**: 21 пустой обработчик, ~40 контролов без обработчиков,
  отладочный вывод в `TextArea1`, дубли методов, 55 объявленных констант (4 используются),
  48 неиспользуемых полей `p_*`, `getCollectionValues`/`getAttValueByKey`/`UpdateHyperlinkParams` — мёртвые.
* **Остаётся выяснить на стенде:** (1) привязано ли событие `onShow` к `Sub ANALIZ_TEP_FORM_ON_SHOW`
  (иначе код открытия формы не выполняется вовсе); (2) существует ли в `BA_PHD` отчёт `PRX_ANALYSIS_TEP`
  и какие у него параметры (неизвестные имена молча отбрасываются); (3) не падает ли ручной редактор
  на `String.SubString(-1, …)`.
* Исходники всех ранее «ненайденных» классов (`COpenHyperlink`, `CUrlHyperlink`, `CObjectParamManager`,
  `TabExt`, `DimensionExt`, `WebFormsExt`, `AppNs`) получены из выгрузки и разобраны —
  см. `PEFX-EXPORT-FINDINGS.md` и `pefx/*.fore`.

---

## 1. Кратко: что это

Веб-форма (класс `ANALIZ_TEP_FORM_ON_SHOW: WebForm`) — **экран выбора параметров регламентного
отчёта** `PRX_ANALYSIS_TEP` («Анализ ТЭП», стенд/пространство `AppNs.PHD`).

Схема работы:

```
форма (комбобоксы справочников + флажки аналитик)
   → накопление строки действия гиперссылки:  @PRX_ANALYSIS_TEP(ZLIB_INDC=…;PLANT=…;CALYEAR=…;P_FIELD_LIST=…)
   → «кнопка Ок» = ГИПЕРССЫЛКА в ячейке (0,0) отчёта, который показан в WebReportBox (ReportBoxOk)
   → у пользователя отчёт открывается с переданными параметрами
```

Ключевая особенность: **кнопка «Ок» — это не `WebButton`, а ячейка-гиперссылка внутри отчёта**
(`InitializeHlinkOpenObject`, стр. 1520–1545: ячейка `Cell(0,0)` активного листа, стиль
«Roboto 14 / белым по цвету `ButtonCancel.Color`», `TabExt.SetTabHyperlink(..., TabHyperlinkActionType.OpenObject, action, True)`).
Параметры для неё собираются **правкой строки `ITabHyperlink.Action`** (`UpdateOpenDefHlink`, стр. 1400–1518).

По справке сборки WebForms это стыкуется: `WebReportBox.Report` имеет тип **`IPrxReport`** — то есть
компонент `ReportBoxOk` действительно отдаёт живой регламентный отчёт, у которого можно править ячейки
и гиперссылки. Отдельная рекомендация справки для такого сценария: если веб-форма открывается кнопкой
из регламентного отчёта, активный отчёт доступен как статическое `PrxReport.ActiveReport`, и его
рекомендуется сохранить в переменную уровня класса **в `onShow`**.

---

## 2. Состав формы (инвентарь, машинный подсчёт)

| Тип контрола | Кол-во | Примечание |
|---|---:|---|
| `WebDimensionCombo` | 58 | 48 «рабочих», 4 напрямую в гиперссылку, 2 только в `p_*`, 4 без обработчиков (`DimensionCombo1/9/10/11`) |
| `WebCheckBox` | 95 | 58 → `P_FIELD_LIST`, 18 без обработчиков, 19 с пустыми обработчиками (месяцы/кварталы) |
| `WebTabPage` / `WebTabControl` | 18 / 3 | разделы: «Основные данные», «Энергоснабжение», «Геология и бурение», «Кап. строительство», «Экология», «Прочие аналитики» + блок ТЭП (месяцы/кварталы) |
| `WebButton` | 2 | `ButtonCancel`, `ButtonApply` — **обработчиков нажатия в модуле нет** |
| `WebReportBox` | 1 | `ReportBoxOk` — источник отчёта с кнопкой |
| `WebTextArea` | 1 | `TextArea1` — фактически отладочный лог (8 живых обращений) |
| `WebDateTimePicker`, `WebInput`, `WebPanel` | 1+1+1 | `DateTimePicker1`, `I_ZINDTXT1`, `PANEL3` — кода нет / обработчик пуст |
| Поля класса | 54 `p_*: Variant`, `MB`, `hlink`, `_hlink`, `_AnalyzTepHyperlink` | живьём используются 6 `p_*`; `hlink` — мёртвое поле (стр. 197) |
| Модульная переменная | `fieldList: IStringList` (стр. 1–2) | объявлена **вне класса** — не в стиле проекта |

Код: 1157 строк кода, 143 строки `//`-комментариев, 31 строка внутри `{ }`-комментариев,
244 пустых. Обработчиков: 142 `Sub` + 3 `Function` (плюс 5 вложенных процедур внутри `UpdateOpenDefHlink`),
из них **21 пустой**.

---

## 3. Поток выполнения

1. **Открытие формы** — `Sub ANALIZ_TEP_FORM_ON_SHOW` (стр. 392–416):
   `_hlink := InitializeHlinkOpenObject(ReportBoxOk.Report, "  Ок  ", C_ANALYZ_TEP_REP_ID)` —
   создаётся гиперссылка в ячейке A1 листа отчёта; затем `setDefaultDimensionValue` (стр. 341–380).
2. `setDefaultDimensionValue` → `initialization` (стр. 335–339: `MB := MetabaseClass.Active`,
   `fieldList := New StringList.Create`) → `addDefaultFieldsToStringList` (добавляет
   `"CALYEAR,PLANT,ZLIB_INDC"` **одним элементом**) → `TextArea1.Lines.Add(Hyperlink.tst)`.
   *(Вся автоподстановка значений по умолчанию — год 2024, СП «0200», ТЭП `IND00000100`,
   тип `0000000001` — закомментирована; `getUserSP` (стр. 382–390, атрибут `BUS_AREA` пользователя)
   тоже не вызывается.)*
3. **Выбор значения в комбобоксе** `D_*OnSelectionChange` → два действия подряд:
   `UpdateOpenDefHlinkFromSelection(<ПАРАМЕТР>, <отметка>, <атрибут>)` (ручная правка строки
   `_hlink.Action`) и `Hyperlink.SetParamValueFromSelection(...)` + `Hyperlink.Generate`
   (механизм класса `COpenHyperlink`).
4. **Флажок аналитики** `CB_*OnChange` → `fillFieldListByStatusFlag` (стр. 1552–1564):
   `fieldList.Add/Remove(<имя аналитики>)` → `Hyperlink.SetParamValue("P_FIELD_LIST", fieldList.Text(", "))`
   → `Hyperlink.Generate` → `TextArea1.Text := Hyperlink.Action`.
5. **Нажатие «Ок»** (гиперссылка в отчёте) — платформа открывает объект по строке действия
   `@PRX_ANALYSIS_TEP(<параметр>=<значение>;…)`.

### Формат строки действия — подтверждено справкой

`ITabHyperlink.Action` (`TabSheet__Interface.md:10140–10199`) документирует:

* открытие объекта репозитория — `@Dim`;
* **с параметрами** — `@Dim(STRING=a;INT=1;FLOAT=0.01;DATE=09.02.2021 00:00:00)`;
* **множественное значение — в квадратных скобках**: `@Dim(STRING=[q,e];INT=[1,2])`;
* выполнение макроса — `<OBJ3331.MyFunc>` (Fore — только настольное приложение, JS — только веб).

То есть `UpdateArrayToValue` (стр. 1472–1490) собирает `[a,b,c]` **ровно по документированному
синтаксису**, а `TabHyperlinkActionType.OpenObject = 6` (`TabSheet__Enums.md:1698–1731`).

---

## 4. Как устроена сборка параметров (`UpdateOpenDefHlink`, стр. 1400–1518)

Алгоритм: взять `_hlink.Action` → при необходимости дописать `()` → массив превратить в `[a,b]` →
найти параметр (`GetParamIndex`) → если найден: пустое значение → `RemoveParam`, иначе `UpdateParam`;
если не найден → `InsertParam` → записать обратно `_hlink.Action` → вывести строку в `TextArea1`.

Вложенные процедуры (`InsertParam`, `UpdateParam`, `RemoveParam`, `GetParamIndex`, `UpdateArrayToValue`)
— приём легальный: вложенные функции документированы (`Fore-Language__08_Operators.md:71–91`).

Матрица «параметр ← атрибут справочника» (48 обработчиков `D_*`):

| Атрибут `CODE` | Атрибут `ID` | Атрибут = имени параметра | Отдельно |
|---|---|---|---|
| PLANT, SOLD_TO, ZLIB_INDC, ZPHD_USL1, ZDEBITOR, ZPH_ESO2, ZPHD_SK, ZBUR_LU, ZPH_TEHK, ZPH_OPLST, ZPILOT, ZGEN_POD, ZGEN_ZAK, ZOBJEM, ZGAZ_TYPE | ZTYPEIND, PERIOD_TYPE | ZPHD_STAT, VENDOR, ZHRGRPMO, PROFIT_CTR, COSTCENTER, ZPH_USR2, ACTTYPE, ZEQUI, ZCLSVOBOR, MATERIAL, ZFUNC_LOC, ZSIU_FLD, POSID, ZPHD_DOG, UCVOLTLEVL, Z_CL_NAPR, ZSIU_TY, ZDOGLINK, ZBUR_AREA, ZSKV_KUST, Z_SKV_GEO, ZBUR_PLST, ZSKV_ST, ZSHIFR, ZPHD_SR, ZPHD_GRSR, ZAVIATYPE, ZPHD_SPR | **CALYEAR ← `NAME`**, **ZORGUNIT ← `ZORGU`**, **ZUCVOLTTR ← `UCVOLTLEVL`** |

`ZUCVOLTTR ← UCVOLTLEVL` (стр. 810) — **не копипаста**: по выгрузке источник этого комбобокса —
ярлык `SHORTCUT_TO_RDSD_UCVOLTLEVL` «Уровень напряж. Продажи» на справочник `RDSD_UCVOLTLEVL`,
поэтому Id атрибута `UCVOLTLEVL` корректен. Аналогично `ZORGUNIT ← ZORGU` — у справочника `RDSD_ZORGU`
«Орг.единицы» атрибут называется `ZORGU`.

Итого в гиперссылку реально уходят **53 имени**: 48 параметров-справочников + 4 «прямых»
(`ZLIB_INFS`, `ZBUR_BEG`, `ZBUR_END`, `ZPKR_SUBP`) + `P_FIELD_LIST`.

---

## 5. Три семейства обработчиков — и что из них работает

1. **58 комбобоксов.** 48 — «два механизма сразу» (см. дефект 1). 4 — `_AnalyzTepHyperlink.SetParamValue(...)`
   напрямую (дефект 2). 2 (`D_ZPHD_NCH`, `D_ZPHD_KON`, стр. 1368–1378) — только `p_*`, в комментарии
   «Нет связи с параметром» → значения **теряются**. 4 (`DimensionCombo1/9/10/11`) — вообще без обработчиков.
2. **58 флажков аналитик** → `P_FIELD_LIST` (какие аналитики показывать в отчёте). Из них 7 имён
   (`ACT_UNIT`, `ZPHD_COMM`, `ZINDTXT1`, `ZPHD_NOP1`, `ZPHD_IS`, `ZPHD_PHD`, `ZPHD_PRIZ`) не имеют
   своих комбобоксов — только отображение, без выбора значения.
3. **19 флажков периодов** (12 месяцев, 4 квартала, «6 месяцев», «9 месяцев», «Год») — обработчики
   объявлены, но **пусты** (стр. 1127–1220): выбор периода сейчас ни на что не влияет.

---

## 6. Дефекты, риски и мёртвый код

### Функциональные

1. **Два механизма обновления одной гиперссылки — ручной заведомо проигрывает (выяснено по исходнику).**
   Почти каждый `D_*OnSelectionChange` сначала правит строку вручную (`UpdateOpenDefHlinkFromSelection`),
   затем повторно задаёт тот же параметр через `Hyperlink.SetParamValueFromSelection` +
   `Hyperlink.Generate` (пример: стр. 635–637). По исходнику `COpenHyperlink.Generate`
   (`analiz-tep/pefx/pef248.fore:203–215`) **заново собирает действие из менеджера параметров**
   (`LinkBuilder.BuildOpenObjectLink(ObjectDescriptor, GetObjectParamValues)`) и переписывает
   гиперссылку **той же** ячейки `(0,0)` (`C_HYPERLINK_ROW/COLUMN = 0`, `pef251.fore`).
   Следствие: ручная правка `_hlink.Action` затирается следующей же строкой обработчика —
   ~120 строк разбора строки (`UpdateOpenDefHlink` + 5 вложенных подпрограмм) **не влияют на результат**.
   Единственное, что реально попадает в ссылку, — значения, записанные в `CObjectParamManager.Params`
   (`SetParamValue*`), плюс `P_FIELD_LIST` из флажков. Подробнее — `PEFX-EXPORT-FINDINGS.md` §2.1.
2. **`_AnalyzTepHyperlink` может быть `Null`.** Поле создаётся только в геттере свойства `Hyperlink`
   (стр. 324–333), а стр. 755, 1276, 1283, 1319 вызывают `_AnalyzTepHyperlink.SetParamValue(...)`
   напрямую. Не падает лишь потому, что строка `TextArea1.Lines.Add(Hyperlink.tst)` (стр. 378) дёргает
   геттер при открытии формы — то есть работа этих обработчиков зависит от отладочной строки
   (и от того, что `onShow` вообще вызывается, см. дефект 10). Плюс эти 4 параметра
   (`ZLIB_INFS`, `ZBUR_BEG`, `ZBUR_END`, `ZPKR_SUBP`) не сопровождаются `Generate` → попадут в действие
   **только если позже сработает другой обработчик**. По исходнику: `SetParamValue` в отличие от
   `SetParamValueFromSelection` **не проверяет `ParamManager` на `Null`** (`pef248.fore:186–189`) —
   т.е. при невызванном `InitObject` будет исключение, а не тихий пропуск.
3. **`GetParamIndex` при отсутствующем параметре** (стр. 1455–1470): `IndexOf` вернёт `-1`, после чего
   вызывается `hlinkAction.SubString(-1, …)`. Справка `String.SubString(Start; Count = -1)`
   (help.fsight.ru, `foresys/class/string/string.substring.htm`) **отрицательный `Start` не описывает**:
   при .NET-подобной трактовке будет исключение (вставка нового параметра вообще не сработает),
   при трактовке «с конца» — работает случайно. **Проверить на стенде.**
4. **Флажок по умолчанию нельзя снять.** `addDefaultFieldsToStringList` (стр. 1566–1571) добавляет
   `"CALYEAR,PLANT,ZLIB_INDC"` одним элементом, а `IStringList.Remove` удаляет элемент **целиком по значению**
   (`Online-ModCollections.md:910–912`). Снятие `CB_PLANT`/`CB_ZLIB_INDC` не уберёт аналитику из
   `P_FIELD_LIST`, а повторная установка добавит дубль (`CALYEAR,PLANT,ZLIB_INDC, PLANT`).
   *(Список при этом никогда не очищается.)*
5. **Кнопки формы без обработчиков:** `ButtonCancel`, `ButtonApply` (стр. 33, 35) — в модуле нет ни
   `ButtonCancelOnClick`, ни `ButtonApplyOnClick`; при этом `ButtonCancel.Color` используется как цвет
   гиперссылки-кнопки (стр. 466–467, 1532–1533). Справка описывает обработчик кнопки именно как
   `<ИмяКомпонента>OnClick` (пример `Sub Button1OnClick;`), поэтому **нажатия этих кнопок сейчас, скорее
   всего, не делают ничего** (если привязка не задана в дизайнере).
6. **`getCollectionValues`** (стр. 560–604) — цикл `For i := 0 To myArray.Length - 1` по
   **неинициализированному** `myArray` (заполняется `arrValue`, который не используется) → при вызове
   исключение; `getAttValueByKey` (стр. 606–617) — заглушка: тело `If Not IsNull(Attr) Then` пустое,
   возвращается `Null`. Обе функции мёртвые (вызовов нет).
7. **`UpdateHyperlinkParams`** (стр. 489–494) игнорирует свои аргументы: всегда пишет `CALYEAR` из
   `D_CALYEAR.Selection`, имя параметра/атрибута прогоняет через `String.ToUpper`. Сейчас не вызывается
   (только из закомментированных строк 502, 557) — но при «оживлении» тихо подменит параметр.
8. **Нет экранирования значений.** Значения вставляются в строку действия как есть (стр. 1409–1430):
   значение справочника, содержащее `;`, `=` или `)`, сломает разбор действия. Для `CODE`/`ID` безопасно,
   для атрибутов-наименований — риск.
9. **Пустая отметка** → `UpdateArrayToValue` (стр. 1472–1490) на пустом массиве даст `"]"`
   (`String.Remove(str, Length-1)` + `"]"`), т.е. параметр уйдёт «мусором».

### Риски совместимости / именования

10. **Имя класса и имя обработчика `onShow` — главный риск.** `Class ANALIZ_TEP_FORM_ON_SHOW: WebForm`
    (стр. 4), и внутри класса — `Sub ANALIZ_TEP_FORM_ON_SHOW` (стр. 392), т.е. метод назван **как класс**.
    Справка по веб-формам формулирует правило про класс дословно:
    «*Каждой веб-форме соответствует модуль, содержащий описание класса формы. **Название класса должно
    совпадать со значением свойства `name` веб-формы***», а схема именования обработчиков
    `<ИмяКласса|ИмяКомпонента> + <ИмяСобытия>` **выведена из примеров** справки (явной статьи с правилом
    нет): `Sub TESTWebFormOnShow;` для `Class TESTWebForm`, `Sub Button1OnClick;`.
    Значит обработчик `onShow` этой формы по этой схеме должен называться
    `ANALIZ_TEP_FORM_ON_SHOWOnShow`, а не `ANALIZ_TEP_FORM_ON_SHOW`.
    Последствия: если в свойствах/XML формы событие `onShow` привязано к имени `ANALIZ_TEP_FORM_ON_SHOW` —
    всё работает; если нет — **код открытия формы (создание гиперссылки «Ок») не выполняется вообще**.
    Проверяется в дизайнере веб-формы (панель «Свойства/События», событие `onShow`) либо по XML формы
    (блок `COMPONENT.EVENTS`). Заодно сверить: имя класса ↔ `name` формы; в проекте «Планировщик задач»
    принято `<Id объекта>Form` (`SCHEDULERForm`).
    *(В модуле нет обработчика `onCommand` — если форма должна принимать команды `IWebForm.SendCommand`
    (это интерфейс сборки **Metabase**; у самой веб-формы как компонента среды разработки интерфейс
    называется `IWebFormComponent`), его тоже придётся добавить.)*
11. **`fieldList` объявлен на уровне модуля** (стр. 1–2, до `Class`), тогда как справка перечисляет
    контексты объявления переменных «класс, пространство имён, интерфейс» (`Fore-Language__06_SyntRules.md:793–859`).
    Проверить компиляцию на стенде либо перенести поле в класс.
12. **Сравнения с `Null`**: `fieldList = Null` (стр. 338), `CB <> Null` (стр. 1554) — принято `IsNull(...)`
    (на это же указывает линтер проекта).
13. **`TabExt.SetTabHyperlink(..., True/False)`** — семантика выяснена по исходнику (`pef206.fore:123–147`):
    последний аргумент — **`showModal`** (`link.Target := showModal ? TabHyperlinkTarget.Parent : Blank`),
    т.е. `True` = открывать в родительском окне, `False` = в новой вкладке. `COpenHyperlink.Generate`
    передаёт `True`; закомментированный прототип в форме (стр. 473) — `False`. Дополнительно метод
    ставит `Locked = On`, `Enable/Active/SeparateLinkText = On`, выравнивание по центру.

### Мёртвый код и отладка

14. **Дубли-близнецы:** закомментированные `UpdateOpenDefHlink` (стр. 448–452) и `InitializeHlinkOpenObject`
    (стр. 454–479) — другие реализации тех же методов, что живые (стр. 1400, 1520).
15. **`madeLinkForMyselfTst`** (стр. 418–446) — отладочный метод: пишет гиперссылку в ячейку `(0,0)`
    листа «Лист2» и текст `"tst"`; не вызывается (только из закомментированной строки 405).
16. **`TextArea1` как отладочный вывод** (8 живых обращений): `TextArea1.Lines.Add(hlinkAction)` (стр. 1517),
    `TextArea1.Text := Hyperlink.Action` (стр. 1562) — отладка видна пользователю. Сделать его
    «только для чтения» из кода нельзя: у `WebTextArea` свойства `ReadOnly` в API нет (в справке оно
    указано только в списке «Режим дизайнера»), поэтому либо `Enabled := False`, либо убирать вывод.
17. **Неиспользуемое:** 55 констант `C_PARAM_*` объявлены, в живом коде используются 4
    (`ZLIB_INFS`, `ZBUR_BEG`, `ZBUR_END`, `ZPKR_SUBP`) + `C_ANALYZ_TEP_REP_ID`; `C_BUTTON_OK_ID`
    (`PRX_ANALYZ_TEP_BUTTON_OK`) не используется. 54 поля `p_*` — живьём 6. Поле `hlink` (стр. 197) — мёртвое.
    `I_ZINDTXT1OnTextChanged` (стр. 1387) и `TextArea1OnTextChanged` (стр. 836) — пустые.
18. **Вероятные опечатки имён:** `CbNovemberOnChange` (стр. 1177), `CbThirdQuarterOnChange` (стр. 1197) —
    выбиваются из схемы `CB_<ИМЯ>OnChange`.

### Проверка линтером проекта

`node "F:\Scheduler Tasks\tools\fore-lint-check.js" analiz-tep/lint` →
**12 предупреждений** (полный вывод — `analiz-tep/out/lint-result.txt`):

* 10 «незакрытых блоков» — **ложные срабатывания** линтера: закомментированный `{ }`/`//`-код
  (`If … End If;` и `While` внутри комментариев) и однострочные `If … Then … End If;`,
  а также `Property … Get … End Get` (стр. 326);
* 2 реальных по стилю проекта: `fieldList = Null` (стр. 338) и `CB <> Null` (стр. 1554).

---

## 7. Что подтверждено справкой, а что — нет

**Подтверждено локальной справкой (`F:\Scheduler Tasks\docs\forsite\`):**

| Факт | Источник |
|---|---|
| Синтаксис строки действия гиперссылки, в т.ч. массивы `[a,b]` | `TabSheet__Interface.md:10140–10199` |
| `TabHyperlinkActionType.OpenObject = 6` | `TabSheet__Enums.md:1698–1731` |
| Члены `ITabHyperlink` (`Action`, `ActionType`, `Color`, `Enable`, `Underline`, `Text`, …) | `api-index.txt:243` |
| `IPrxReport.ActiveSheet`; `ITabSheet.Cell(Row, Column): ITabRange` | `KeReport__Interface.md:16706`; `api-index.txt:288` |
| `IStringList`: `Add`, `Remove(значение)`, `Clear`, `Text(разделитель)`, `Count` | `Online-ModCollections.md:796–937` |
| Вложенные процедуры/функции в Fore | `Fore-Language__08_Operators.md:71–91` |

**Добрано из онлайн-справки по сборке `WebForms`** (в локальном дампе её нет; полная выжимка —
`analiz-tep/research/webforms-api-digest.md`, все факты со ссылками на страницы):

| Факт | Значение |
|---|---|
| Именование класса формы | «*Название класса должно совпадать со значением свойства `name` веб-формы*» |
| Именование обработчиков | `<ИмяКласса\|ИмяКомпонента> + <ИмяСобытия>`: `Sub TESTWebFormOnShow;`, `Sub Button1OnClick;` |
| События формы | `onShow` (можно `OnShow(Args: ISortedList)`), `onCommand` (`IWebCommandEventArgs`) |
| `WebReportBox.Report` | `Report: IPrxReport;` ✅ совпадает с использованием в коде |
| `WebDimensionCombo.Selection` / `.DimInstance` | `IDimSelection` / `IDimInstance` ✅ |
| `WebTextArea.Lines` / `WebCheckBox.Checked` | `IStringList` / `Boolean` ✅ |
| Общие члены компонентов | `Name` (`IWebComponent`; свойства `ID` у компонентов нет), `Text`, `Visible`, `Enabled`, `Color`, `BorderColor`, `PopupMenu` |
| `WebTextArea.ReadOnly` | только режим дизайнера (в коде недоступно) |
| `WebDateTimePicker.Value` | `DateTime`; событие — `OnValueChanged` |

> Про типы `Report`: у **настольного** `IReportBox.Report` тип `IUiReport`
> (`KeReport__Interface.md:34245`), а у **веб**-компонента `WebReportBox.Report` — `IPrxReport`
> (страница `iwebreportbox.report.htm` онлайн-справки). Поэтому передача `ReportBoxOk.Report`
> в `InitializeHlinkOpenObject(report: IPrxReport; …)` (стр. 1520) для веб-формы типологически
> корректна; в настольном аналоге это было бы несоответствие.

**Не найдено ни в справке, ни на диске — но НАЙДЕНО в выгрузке окружения со стенда**
(`full_env_web_form_06102026.pefx`; полный разбор — `analiz-tep/PEFX-EXPORT-FINDINGS.md`,
исходники — `analiz-tep/pefx/*.fore`):

* **`COpenHyperlink`** → `analiz-tep/pefx/pef248.fore` (модуль `UNIT_OOH_COPENHYPERLINK_COPY1`);
  там же `CUrlHyperlink` (`pef249.fore`), `CObjectParamManager` (`pef250.fore`),
  константы `C_HYPERLINK_ROW/COLUMN = 0` и `C_KEY_ATTR_ID = "KEY"` (`pef251.fore`).
* **`WebFormsExt`** → `pef238.fore` (`GetDimSelectionAttrValue(sel, attrId = "")`: `SelectedCount = 0` → `Null`,
  атрибут не найден → `Null`, иначе `AttributeToVariant` / `ToVariant`).
* **`TabExt`** → `pef206.fore` (`SetTabHyperlink(cell, linkText, actionType, action, showModal = False)`).
* **`DimensionExt`** → `pef208.fore`.
* **`AppNs.PHD`** → `pef153.fore`: `Namespace AppNs … PHD = "BA_PHD"; … End Namespace AppNs;`
  (модуль `UNIT_CONSTANTS_EXT` «Глобальные константы») — т.е. это Id бизнес-приложения «ПХД».
* Сборщик строки действия: `CNavigationLinkBuilder.BuildOpenObjectLink` (`pef243.fore:142–154`) +
  `CAppNavigationLinkBuilder.ComposeParamsLink` (`pef246.fore:6–100`) → `"@" + Id + "(ID=value;…)"`,
  массивы `[a,b]`, `Null`/пустые массивы пропускаются.

Что осталось неизвестным и после выгрузки:

* привязка события `onShow` — у объекта веб-формы в манифесте `<CONTENT/>` (пусто), дерево компонентов и
  события в выгрузку не попали;
* целевой отчёт `PRX_ANALYSIS_TEP` и его параметры (в выгрузке есть только отчёт-кнопка
  `PRX_ANALYSIS_TEP_BUTTON_OK` «Кнопка ОК» — см. §9);
* поведение `IHashtable.Add` при повторном ключе (в справке не оговорено);
* трактовка `String.SubString(-1, …)` на стенде (см. дефект 3) — теперь это не «косметика»:
  ручной редактор исполняется до `Generate`, и если он падает, параметры вообще не установятся.

Прочее, что не покрыто справкой: **`LookupDisplayValue`** (используется в мёртвом `getAttValueByKey`,
стр. 613) — 0 вхождений, задокументированный аналог `IDimAttributeInstance.Value(...)`.
Отдельно: правило «может ли `Sub` называться как его класс» в справке **не сформулировано ни в одну
сторону** (проверены правила областей видимости, ошибка 1844 «Повторное определение идентификатора»
и примеры) — это ещё одна причина проверить модуль компилятором на стенде. Полезно и то, что для
**веб**-форм есть документированный запрет на настольные ресурсы — ошибка компилятора 2602
«Недоступно для использования в веб» (`Fore-Language__11_Compiler_Errors.md:104`).

---

## 8. Важное для дальнейшей работы: документированный способ открыть отчёт с параметрами

Вся конструкция с гиперссылкой в ячейке A1 — не единственный и не самый прямой путь: у веб-формы
есть штатный API. `IWebFormComponent.ShowObject(Object: IMetabaseObjectDescriptor; [Ctx: IWebOpenContext])`
(пример из справки):

```fore
Sub Button1OnClick;
Var
	Mb: IMetabase;
	MDesc: IMetabaseObjectDescriptor;
	Values: IMetabaseObjectParamValues;
	Context: IWebOpenContext;
Begin
	Mb := MetabaseClass.Active;
	MDesc := Mb.ItemById("REPORT");
	Context := New WebOpenContext.Create;   // Настройка контекста открытия объекта
	Context.CurrentTab := False;            // новая вкладка браузера
	Context.Edit := False;                  // на просмотр
	Values := MDesc.Params.CreateEmptyValues;
	Values.FindById("P_START").Value := 2010;
	Values.FindById("P_FINISH").Value := 2020;
	Context.ParamValues := Values;
	Self.ShowObject(MDesc, Context);        // Открытие объекта
End Sub Button1OnClick;
```

Ограничения из справки: метод работает **только из кода веб-формы**; нельзя открывать объекты типов
Модуль/Сборка/Документ/Бизнес-приложение и др.; справочники, использованные при открытии с параметрами,
закрываются только при закрытии сессии.

Это даёт альтернативу ручной сборке строки `@PRX_ANALYSIS_TEP(...)`: параметры задаются типизированно
(`IMetabaseObjectParamValues`), без склейки строк, без зависимости от `COpenHyperlink`/`TabExt`
и без риска сломать строку значениями со `;`/`)`. Решение — за владельцем стенда (у hyperlink-варианта
может быть своя причина: кнопка должна оставаться внутри отчёта).

### Практические выводы (если браться за правку)

1. **Сначала проверить привязку `onShow`** (дефект 10) — если обработчик не вызывается, всё остальное
   не имеет смысла.
2. **Оставить один механизм — `COpenHyperlink`** (`SetParamValue*` + `Generate`), а ручной редактор
   (`UpdateOpenDefHlink`, `UpdateOpenDefHlinkFromSelection` и 5 вложенных подпрограмм) **удалить**:
   по исходнику `Generate` всё равно пересобирает ссылку из менеджера параметров и затирает ручную правку,
   а сам редактор исполняется первым и может упасть (дефект 3). Из каждого обработчика тогда остаётся
   одна строка `Hyperlink.SetParamValueFromSelection(...)`; `Generate` достаточно вызвать один раз
   (например, в конце обработчика).
3. **Убрать прямые обращения к `_AnalyzTepHyperlink`** (стр. 755, 1276, 1283, 1319) — заменить на свойство
   `Hyperlink` и добавить `Generate`; иначе 4 параметра «зависают» и зависят от порядка действий.
4. **`P_FIELD_LIST` хранить отдельными элементами**, а не строкой `"CALYEAR,PLANT,ZLIB_INDC"`, иначе
   флажки по умолчанию не снимаются и появляются дубли (дефект 4).
5. **Навести порядок:** имена параметров — в константы (объявлено 55, используется 4) и сверить их
   с параметрами отчёта; убрать отладочный вывод из `TextArea1`; удалить мёртвый код (дубли методов,
   `getCollectionValues`, `getAttValueByKey`, `madeLinkForMyselfTst`, 48 неиспользуемых `p_*`,
   мёртвое поле `hlink`).
6. **Дозаполнить или удалить заготовки:** 19 пустых обработчиков периодов, 18 флажков без обработчиков,
   кнопки `ButtonCancel`/`ButtonApply`, `DateTimePicker1`.
7. **Рассмотреть `Self.ShowObject`** (выше) как замену хрупкой строковой сборке.
8. **Учесть зависимости при переносе:** по выгрузке форма ссылается на сборки `DimensionExt`, `TabExt`,
   `ExpressExt`, `ASSM_OPEN_OBJECT_HYPERLINK_COPY1` и модули `UNIT_CONSTANTS_EXT` (namespace `AppNs`),
   `UNIT_WEBFORMS_EXT` (`WebFormsExt`) — без этих ссылок модуль не соберётся (ошибка 1337
   «Неизвестный идентификатор»). Сами классы существуют на стенде (исходники — в `pefx/*.fore`),
   так что при необходимости их можно заменить документированным API:
   `TabExt.SetTabHyperlink` → `ITabRange.Style.Hyperlink` + `ActionType`/`Action` (как в `madeLinkForMyselfTst`),
   `DimensionExt.Get*By*` → рецепты `KnowledgeBase__01_Fore.md:1915–1963`. Для веб-формы действует
   и запрет на настольные ресурсы — ошибка 2602 «Недоступно для использования в веб».
9. **Сверить `IUiReport`/`IPrxReport`** там, где код работает с `ReportBoxOk.Report` (для веб-компонента
   тип документирован как `IPrxReport`, для настольного — `IUiReport`).

---

## 9. Открытые вопросы (что нужно уточнить, прежде чем что-то менять)

**Закрыто выгрузкой окружения** (`full_env_web_form_06102026.pefx`, см. `PEFX-EXPORT-FINDINGS.md`):
исходники `COpenHyperlink`/`CUrlHyperlink`/`CObjectParamManager`/`TabExt`/`DimensionExt`/`WebFormsExt`;
значение `AppNs.PHD = "BA_PHD"`; роль `Generate` (пересборка ссылки из менеджера параметров);
смысл последнего аргумента `SetTabHyperlink` (`showModal`); Id объекта веб-формы и отчёта-кнопки.

Осталось уточнить (по приоритету):

1. **Привязка события `onShow`** (см. дефект 10): вызывается ли `Sub ANALIZ_TEP_FORM_ON_SHOW` вообще.
   Проверять в дизайнере формы на стенде — объект **`WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV`**
   «Анализ значений ТЭП (копия для доработок)» (папка `FLD_ANALIZ_TEP` бизнес-приложения `BA_PHD`);
   сверить `name` формы ↔ имя класса и имя обработчика в XML формы (`COMPONENT.EVENTS`).
   В выгрузке дерева компонентов нет (`<CONTENT/>` пуст).
2. **Целевой отчёт `PRX_ANALYSIS_TEP`** и его параметры: сверить 53 отправляемых имени (особенно
   `P_FIELD_LIST`, `P_ANALYTIC_SET`, `ACT_UNIT`, «потерянные» `ZPHD_NCH`/`ZPHD_KON`). В выгрузке есть
   только отчёт-кнопка `PRX_ANALYSIS_TEP_BUTTON_OK` «Кнопка ОК» — проверьте, что `PRX_ANALYSIS_TEP`
   существует в `BA_PHD` (иначе `MbExt.ItemById` в `Generate` упадёт).
3. **Работает ли `UpdateOpenDefHlink` фактически** (см. дефект 3): если `String.SubString(-1, …)` бросает
   исключение, параметры не установятся вообще; признак — пустая строка действия у «Ок» после выбора
   значений (смотреть `TextArea1` / `Hyperlink.tst`).
4. Что должны делать `ButtonCancel` / `ButtonApply` (обработчиков нет вообще) и `DateTimePicker1`.
5. Что должно происходить с периодами (месяцы/кварталы) — сейчас обработчики пусты.
6. Нужны ли значения по умолчанию (закомментированный блок на стр. 346–374) и подстановка СП
   пользователя (`getUserSP`, атрибут `BUS_AREA`).
7. Поведение `IHashtable.Add` при повторной установке параметра (в справке не оговорено).
8. Формат/локализация значений при генерации ссылки (`CultureExt.FormatVariant` → `UI.FormatVariant`) —
   важно для дат и чисел, если в параметры попадут не только коды справочников.

---

## 10. Требования (ТТ) ↔ код: главное

Появилось ТТ `ТТ_Анализ и выгрузка данных ТЭП.xlsx` (5 листов) — полный разбор и таблицы сверки:
**`analiz-tep/TT-vs-CODE.md`** (машинная сверка — `analiz-tep/tt/tt-vs-code2.md`, дампы листов —
`analiz-tep/tt/*.txt`).

Что важно для чтения кода:

* **«СЭ» = Селекционный экран** — так в ТТ называется этот самый экран подбора параметров, поэтому
  комментарий «Параметры СЭ регламентного отчёта с кнопкой» читается буквально.
* **57 полей фильтрации** в 7 разделах — совпадают с разделами/комбобоксами формы (41 поле покрыто
  верно); 4 «даты» в ТТ описаны как **календарь**, а в форме смоделированы комбобоксами
  (`D_ZBUR_BEG`, `D_ZBUR_END`, `D_ZPHD_NCH`, `D_ZPHD_KON`); 2 текстовых поля (`Мероприятие`,
  `Примечание`) — один необработанный `I_ZINDTXT1`.
* **128 пунктов «Поля для вывода»** — это и есть смысл `P_FIELD_LIST`; в форме 58 флажков с рабочими
  обработчиками, 19 периодов (месяцы/кварталы) **с пустыми обработчиками**, а групп «с начала года»
  (19) и «корректировки» (19) нет вовсе; чек-боксы «Выводить коды аналитик» и «Выводить информацию
  по статусам» объявлены, но обработчиков не имеют.
* **Значения по умолчанию** из ТТ (текущий год, СП пользователя, Тип данных «План» `0000000001`,
  набор полей по умолчанию) в коде закомментированы — ровно тот блок в `setDefaultDimensionValue`,
  который разбирался выше; `getUserSP` (атрибут `BUS_AREA`) написан, но не вызывается.
* **Ролевая модель СП** (`PHD_ADMIN`/`PHD_CURATOR_***` — любое значение, остальные — только своё)
  не реализована.
* **Зависимые выборки** (лист «Выбор атрибутов ТЭП»): Вид деятельности, Вид показателя, Формы отчётов,
  ТЭП-источники, Владелец — делаются через `TBL_IDLNK`, `TBL_ZIDNFORM`, `DICT_PHD_GROUPS`,
  `RDSD_INDS`, `RDSD_ACTVTS`, `RDSD_OWNERS`; в коде не реализованы, этих объектов нет и в зависимостях.
* **Сверка идентификаторов:** 12 имён из кода (`CALYEAR`, `PLANT`, `ZTYPEIND`, `PERIOD_TYPE`,
  `ZPH_USR2`, `SOLD_TO`, `ZORGUNIT`, `ZPHD_STAT`, `ZPHD_SPR`, `ZPHD_NOP1`, `ZPHD_PHD`, `ZPHD_PRIZ`)
  не встречаются в колонках идентификаторов ТТ, а часть полей ТТ (`ZPH_EPOK`, `ACTVTS`, `OWNER`,
  `ZF_NUMB`, `ID1`) отсутствует в коде — поскольку неизвестные параметры отбрасываются молча
  (`CObjectParamManager.GetObjectParamValues`), эти расхождения надо проверить на стенде первым делом.

---

## 11. Артефакты разбора (в этой папке)

| Файл | Что это |
|---|---|
| `analiz-tep/ANALIZ-TEP-webform.md` | этот разбор |
| `analiz-tep/TT-vs-CODE.md` | сверка ТТ ↔ код: покрытие полей, пробелы, этапы работ |
| `analiz-tep/PEFX-EXPORT-FINDINGS.md` | разбор выгрузки окружения со стенда: исходники классов, ответы на открытые вопросы, карта объектов |
| `analiz-tep/research/webforms-api-digest.md` | API сборки WebForms по онлайн-справке (со ссылками на страницы) |
| `analiz-tep/research/fore-stand-helpers.md` | поиск на диске определений `COpenHyperlink`/`WebFormsExt` и факты платформы из локальной справки |
| `analiz-tep/pefx/*.fore` | 78 исходных модулей из выгрузки (`pef248.fore` = COpenHyperlink, `pef238.fore` = WebFormsExt, …) |
| `analiz-tep/pefx/INDEX.md`, `analiz-tep/pefx/OBJECTS.md` | карта модулей и полный список объектов выгрузки |
| `analiz-tep/tt/*.txt`, `analiz-tep/tt/tt-vs-code2.md` | дампы листов ТТ и машинная сверка ТТ ↔ код |
| `analiz-tep/tools/pefx-extract.js`, `analiz-tep/tools/pefx-scan.js` | разбор `.pefx` (манифест → карта, CDATA → `*.fore`) |
| `analiz-tep/tools/tt-dump.py`, `analiz-tep/tools/tt-vs-code2.py` | дамп листов ТТ и сверка с кодом |
| `analiz-tep/tools/form-inventory.js` | скрипт инвентаризации: контролы ↔ обработчики, пустые обработчики, константы, поля `p_*`, параметры гиперссылки |
| `analiz-tep/out/form-inventory.txt` | результат инвентаризации (полный) |
| `analiz-tep/out/lint-result.txt` | вывод линтера проекта по копии модуля |
| `analiz-tep/lint/ANALIZ_TEP_FORM_ON_SHOW.fore` | побайтовая копия `backup.txt` (UTF-8, CRLF) для проверок |
