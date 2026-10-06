# Выгрузка окружения `full_env_web_form_06102026` — что в ней найдено

**Источник:** `C:\Users\Manya\Downloads\full_env_web_form_06102026.pefx` (ZIP: сигнатура `50 4B 03 04`) +
распакованная папка `full_env_web_form_06102026\` (`content.xml` + `pefN.xml`/`pefN.mod`).
**Паспорт выгрузки:** Форсайт «Релиз 10.8.2190.0 LTS x64», создана 06.10.2026, автор `KHUSAINOV_SI`,
рабочая станция `SGC\SNG-CUDI-VPN-02`. Объектов в манифесте — **309**.
**Разбор:** `analiz-tep/tools/pefx-extract.js`, `analiz-tep/tools/pefx-scan.js`;
извлечённые исходники — `analiz-tep/pefx/*.fore` (78 модулей), карта — `analiz-tep/pefx/INDEX.md`,
список объектов — `analiz-tep/pefx/OBJECTS.md`.

---

## 1. Главное: исходники всех «ненайденных» классов здесь есть

В прошлом разборе четыре класса были помечены «нет ни в справке, ни на диске». Теперь они найдены
с полным текстом:

| Что искали | Файл в выгрузке | Объект/модуль на стенде |
|---|---|---|
| `COpenHyperlink` (253 стр.) | `analiz-tep/pefx/pef248.fore` | модуль `UNIT_OOH_COPENHYPERLINK_COPY1` «COpenHyperlink» |
| `CUrlHyperlink` (40 стр.) | `analiz-tep/pefx/pef249.fore` | модуль `UNIT_OOH_CURLHYPERLINK_COPY1` |
| `CObjectParamManager` (100 стр.) | `analiz-tep/pefx/pef250.fore` | модуль `UNIT_OOH_COBJECTPARAMMANAGER_COPY1` |
| константы `C_HYPERLINK_ROW/COLUMN = 0`, `C_KEY_ATTR_ID = "KEY"` | `analiz-tep/pefx/pef251.fore` | модуль `UNIT_OOH_CONSTANTS_COPY1` «Константы» |
| `CAppNavigationLinkBuilder` (102 стр.) | `analiz-tep/pefx/pef246.fore` | модуль расширения |
| `CNavigationLinkBuilder`, `INavigationLinkBuilder`, `NavigationObjectType`, `NavigationParams` | `analiz-tep/pefx/pef243.fore` | модуль расширения |
| `TabExt` + `SetTabHyperlink` (149 стр.) | `analiz-tep/pefx/pef206.fore` | сборка `ASSM_TAB_EXT` «TabExt» |
| `DimensionExt` (244 стр.) | `analiz-tep/pefx/pef208.fore` | сборка `ASSM_DIMENSION_EXT` «DimensionExt» |
| `WebFormsExt` + `GetDimSelectionAttrValue` (526 стр.) | `analiz-tep/pefx/pef238.fore` | модуль `UNIT_WEBFORMS_EXT` «WebFormsExt» |
| `AppNs` (в нём `PHD = "BA_PHD"`) | `analiz-tep/pefx/pef153.fore` | модуль `UNIT_CONSTANTS_EXT` «Глобальные константы» |

То есть прикладная надстройка стенда — это **копия системного расширения** платформы
(`ASSM_OPEN_OBJECT_HYPERLINK_COPY1` «Генерация гиперссылки для открытия объекта» в папке
«Копии расширений форсайта»), а `WebFormsExt`/`TabExt`/`DimensionExt` — штатные расширители платформы,
которые просто не попали в локальный дамп справки.

---

## 2. Ответы на вопросы, которые были открыты

### 2.1 Два механизма обновления гиперссылки: побеждает `Generate` (дефект 1 закрыт)

Реализация `COpenHyperlink.Generate` (`pef248.fore:203–215`):

```fore
Public Sub Generate;
Var action: String;
Begin
    action := GetAction;                       // пересборка из менеджера параметров
    TabExt.SetTabHyperlink(Cell, Cell.Text, TabHyperlinkActionType.OpenObject, action, True);
    tst := action;
End Sub Generate;

Function GetAction: String;
Begin
    Return LinkBuilder.BuildOpenObjectLink(ParamManager.ObjectDescriptor, ParamManager.GetObjectParamValues);
End Function GetAction;
```

`Generate` **заново собирает строку действия из менеджера параметров и переписывает гиперссылку ячейки**.
При этом `Cell` — это ячейка `(0,0)` (`C_HYPERLINK_ROW/COLUMN = 0` из `pef251.fore`), т.е. **та же ячейка**,
которую настраивает `InitializeHlinkOpenObject` и в которую пишет ручной редактор `UpdateOpenDefHlink`.

Вывод: весь ручной разбор строки в форме (`UpdateOpenDefHlink` + 5 вложенных подпрограмм, ~120 строк)
**затирается** следующим же вызовом `Hyperlink.Generate` в том же обработчике. Источник истины —
`Hyperlink.SetParamValueFromSelection` / `SetParamValue` → `CObjectParamManager.Params`.

Строку собирает `CNavigationLinkBuilder.BuildOpenObjectLink` (`pef243.fore:142–154`) и
`CAppNavigationLinkBuilder.ComposeParamsLink` (`pef246.fore:6–100`):

```
"@" + <ObjectDescriptor.Id> + "(" + "ID=value;" … + ")"
```

* массивы — `[...]`, элементы через запятую, форматирование `CultureExt.FormatVariant`;
* `Null` и пустые массивы **пропускаются** (в ссылку не попадают);
* для `OpenObject` параметры `LinkParams` (`app=…`) не добавляются — они нужны только для URL-ссылок
  (`CUrlHyperlink` → `BuildOpenUrlLink`).

### 2.2 Где значения теряются молча (уточнение дефектов)

| Место | Поведение при проблеме |
|---|---|
| `COpenHyperlink.SetParamValueFromSelection` (`pef248.fore:162–179`) | атрибута с таким Id в справочнике нет → **тихий `Return`**; отметка не разбирается |
| `WebFormsExt.GetDimSelectionAttrValue` (`pef238.fore:146–163`) | `SelectedCount = 0` → `Null`; атрибут не найден → `Null` |
| `CObjectParamManager.GetObjectParamValues` (`pef250.fore:72–98`) | параметра нет в объекте → `Debug.WriteLine("$ Не найден параметр …")` и `Continue` (в ссылку не попадёт); несовместимый тип значения → исключение `CObjectParamManager.DefineObject: …` |
| `COpenHyperlink.SetParamValue` (`pef248.fore:186–189`) | **нет проверки на `Null`** у `ParamManager` (в отличие от `SetParamValueFromSelection`) — если `InitObject` не вызван, будет исключение |

Отсюда практическое правило: опечатка в имени параметра или в Id атрибута **не даёт ошибки** —
параметр просто исчезает из ссылки. Это касается и «потерянных» `ZPHD_NCH`/`ZPHD_KON`, и любых
расхождений с параметрами отчёта.

Пункт 3 прошлого разбора (`String.SubString(-1, …)` в `GetParamIndex`) теперь читается иначе:
ручной редактор исполняется **до** `Generate`, поэтому если `SubString` с отрицательным индексом падает,
обработчик оборвётся и параметры вообще не будут установлены. Проверяемый признак: содержит ли строка
действия «Ок»-ссылки параметры после выбора значений (в отладке — `TextArea1`).

### 2.3 `COpenHyperlink` — остальные детали

* Конструктор: `Create(hlinkReport: IPrxReport; namespaceId: String; linkText: String = "")`, при непустом
  `linkText` пишет `Cell.Text` (значение ячейки).
* `Action` — **только чтение** (`Cell.Style.Hyperlink.Action`); запись в `Action` в форме идёт через
  отдельный объект `_hlink: ITabHyperlink`, полученный из `InitializeHlinkOpenObject`.
* `InitObject(objectId)` создаёт `CObjectParamManager(objectId, NamespaceId)`.
* `Enable(isActive)` — активность и цвета (`ActiveColor`/`DisabledColor`).
* `DesingCell(cellColor)` — то самое оформление ячейки-кнопки (Roboto 14, белый текст), которое
  в форме продублировано в `InitializeHlinkOpenObject`.
* `LinkBuilder`: `LinkParams.App := NamespaceId`, `OpenObjectType := NavigationObjectType.Obj`.

### 2.4 `TabExt.SetTabHyperlink` — семантика последнего аргумента (дефект 13 закрыт)

`pef206.fore:123–147`:

```fore
Public Shared Sub SetTabHyperlink(cell: ITabRange; linkText: String; actionType: TabHyperlinkActionType;
                                  action: String; showModal: Boolean = False);
...
	link.Action := action;
	link.ActionType := actionType;
	link.Enable := TriState.OnOption;
	link.Active := TriState.OnOption;
	link.SeparateLinkText := TriState.OnOption;
	link.Text := linkText;
	link.Target := showModal ? TabHyperlinkTarget.Parent : TabHyperlinkTarget.Blank;
```

То есть последний `Boolean` — **`showModal`**: `True` → `Target = Parent` (открытие в родительском
окне/модально), `False` → `Blank` (новая вкладка). `COpenHyperlink.Generate` передаёт `True`;
закомментированный прототип в форме (`backup.txt:473`) — `False`. Дополнительно метод ставит
`Locked = On`, вертикальное выравнивание по центру, `Enable/Active/SeparateLinkText = On`,
подчёркивание и «общие настройки» — по значению `Undefined`.

### 2.5 `AppNs.PHD` = `"BA_PHD"`

`pef153.fore`: `Namespace AppNs … PHD = "BA_PHD"; … End Namespace AppNs;`

Значит `COpenHyperlink.Create(ReportBoxOk.Report, AppNs.PHD, "Ок")` — это
`namespaceId = "BA_PHD"` (бизнес-приложение «ПХД»), и целевой объект ищется как
`MbExt.ItemById("PRX_ANALYSIS_TEP", "BA_PHD")`. Если объект с таким Id в BA_PHD не найден —
`ObjectDescriptor` упадёт, а `Generate` не соберёт ссылку.

### 2.6 `WebFormsExt` — это штатный API всего сценария, а не только один метод

В модуле `UNIT_WEBFORMS_EXT` (`pef238.fore`) есть, помимо `GetDimSelectionAttrValue`:

| Метод | Назначение |
|---|---|
| `InvokeUserButton(report: IPrxReport; buttonName: String)` | «выполнение действия пользовательской кнопки РО из веб-формы» — штатный путь для пары «кнопка отчёта → веб-форма» |
| `InvokeUserButtonBeforeAction(repButton, Var cancel)` | действие до выполнения кнопки |
| `InvokeOpenWfrmUserButtonAction(report, repButton, sheetsKeys, command)` | обработка кнопки «Открытие объекта» |
| `ShowModalWfrm(wFormId, command, argument, namespaceId)` / `ShowBlankWfrm(...)` | открыть веб-форму с командой и аргументом |
| `GetReportSelectedRowAttrValue(reportBox: IWebReportBox, dimId, attrId, …)` | значение атрибута выбранной строки отчёта в веб-форме |
| `ReopenDimInstWithParamChangeFromSelection/FromValue/FromParamValues` | переподключение справочника с изменением параметров |
| `ShowInformation`, `ShowMessageBox`, `SetDimComboElementGroup` | сервисные |

То есть у задачи «кнопка в отчёте → подбор параметров в веб-форме» есть штатная механика
(команда + `onCommand` + `InvokeUserButton`), а разбираемая форма её не использует — обработчика
`onCommand` в модуле нет вообще. Это аргумент в пользу переписывания (§8 основного разбора), а не
латания ручной сборки строки.

---

## 3. Что ещё рассказывает выгрузка про объекты стенда

| Объект | Ключ | Класс | Что это |
|---|---:|---|---|
| `WFRM_PHD_ANALISIS_TEP_COPY_FOR_DEV` «Анализ значений ТЭП (копия для доработок)» | 3526155 | **1540 `KE_CLASS_WEBFORM`** | **сама веб-форма** (её модуль = `backup.txt`), папка `FLD_ANALIZ_TEP`, изменена 06.10.2026 11:21 |
| `PRX_ANALYSIS_TEP_BUTTON_OK` «Кнопка ОК» | 2757746 | 2562 (`KE_CLASS_PROCEDURALREPORT`) | процедурный отчёт-кнопка; ресурс `OBJ2757747` «Ресурсы» = содержимое отчёта, лист **«Лист2»** |
| `FLD_ANALIZ_TEP` «Анализ значений и данных по ТЭП СП» | 2561447 | 0 (папка) | папка в `FLDR_REPORTS` бизнес-приложения `BA_PHD` «ПХД» |
| `OBJ2764990` «Копии расширений форсайта» | 2764990 | 0 (папка) | здесь лежит копия расширения с `COpenHyperlink` и др. |

* **Отчёт-кнопка входит в зависимости веб-формы** (см. ниже) → `ReportBoxOk` показывает именно
  `PRX_ANALYSIS_TEP_BUTTON_OK`; это согласуется с тем, что отладочный `madeLinkForMyselfTst` ищет лист
  `«Лист2»` (он есть в ресурсе этого отчёта).
* **Целевого отчёта `PRX_ANALYSIS_TEP` в выгрузке нет** — состав его параметров по-прежнему проверяется
  только на стенде.
* `C_BUTTON_OK_ID = "PRX_ANALYZ_TEP_BUTTON_OK"` — **опечатка** (реальный Id `PRX_ANALYSIS_TEP_BUTTON_OK`).
  Константа нигде не используется, вреда нет, но путаницу создаёт.

**Зависимости веб-формы (58):** 50 справочников НСИ + 4 сборки (`DimensionExt`, `TabExt`, `ExpressExt`,
`ASSM_OPEN_OBJECT_HYPERLINK_COPY1`) + 2 модуля (`UNIT_CONSTANTS_EXT` «Глобальные константы» — там
`Namespace AppNs`, `UNIT_WEBFORMS_EXT`) + отчёт-кнопка.

Попутно снимаются два подозрения прошлого разбора — они не копипаста, а ярлыки на справочники:

* `D_ZORGUNIT` использует атрибут `ZORGU` — потому что справочник `RDSD_ZORGU` «Орг.единицы»;
* `D_ZUCVOLTTR` использует атрибут `UCVOLTLEVL` — потому что его источник `SHORTCUT_TO_RDSD_UCVOLTLEVL`
  «Уровень напряж. Продажи» (ярлык на `RDSD_UCVOLTLEVL`).

---

## 4. Чего в выгрузке нет

| Не хватает | Почему / что делать |
|---|---|
| Дерево компонентов и привязки событий формы | у объекта веб-формы в манифесте `<CONTENT/>` (пусто) — выгрузка сделана без содержимого; нужен дизайнер формы на стенде или `IForm.Content` с формы |
| Привязка события `onShow` | следствие предыдущего пункта — вопрос «вызывается ли `Sub ANALIZ_TEP_FORM_ON_SHOW`» остаётся открытым (см. дефект 10 основного разбора) |
| Отчёт `PRX_ANALYSIS_TEP` и его параметры | не входит в выгрузку — сверить 53 имени параметров на стенде |
| Поведение `IHashtable.Add` при повторном ключе | в справке не оговорено: ключ уникален по определению хеш-таблицы, поэтому повторная установка параметра должна перезаписывать значение (иначе форма ломалась бы на втором изменении отметки) — проверить на стенде |

---

## 5. Артефакты разбора выгрузки

| Файл | Что это |
|---|---|
| `analiz-tep/tools/pefx-extract.js` | разбор `.pefx`: манифест → карта объектов, CDATA → `*.fore` |
| `analiz-tep/tools/pefx-scan.js` | список объектов, структура XML, поиск описаний формы/событий |
| `analiz-tep/pefx/*.fore` | 78 извлечённых модулей (`pef248.fore` = COpenHyperlink и т.д.) |
| `analiz-tep/pefx/INDEX.md` | карта «файл → объект → что объявлено» |
| `analiz-tep/pefx/OBJECTS.md` | полный список объектов выгрузки (309) |
