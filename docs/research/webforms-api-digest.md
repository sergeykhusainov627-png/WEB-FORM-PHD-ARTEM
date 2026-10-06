# API-дайджест сборки **WebForms** (веб-формы «Форсайт. Аналитическая платформа»)

**Назначение:** справочник по API веб-форм для чтения/разбора существующего модуля веб-формы на языке **Fore** (объявление класса формы, состав компонентов, свойства/методы/события, открытие объектов репозитория).

**Дата сбора (fetch date):** 06.10.2026.
**Прочитанная версия справки:** `help.fsight.ru`, ветка **`/ru/`** (без номерной ветки). Все страницы в подвале отдают «*Справочная система на версию 10.12 от 21/09/2026*». EN-зеркало (`/en/`) отдаёт «*Help system 10.11 LTS of 15/07/2026*». Номерные ветки (`/10.9/`, `/10.8/`, `/10.7/`) **не использовались** — страницы в `/ru/` открылись (HTTP 200), 404 не было. Локальные CHM-дампы `F:\Scheduler Tasks\docs\forsite\` темы сборки WebForms **не содержат** (grep: единственное совпадение — интерфейс `IWebForm` сборки Metabase в `online\Online-KeSom__10.md:7430`).

**Правила достоверности:** все члены API ниже взяты со страниц справки (URL указан у каждого раздела). Факты, которых нет в
справке, помечены `⚠ НЕ ПРОВЕРЕНО`. Ничего не додумано.

---

## 0. Сводка ключевых фактов (для быстрого старта)

| Вопрос | Ответ |
| --- | --- |
| Как объявляется класс формы? | `Class <ИмяКласса>: WebForm ... End Class` |
| Как называется класс формы? | «*Название класса должно совпадать со значением свойства name веб-формы*» |
| Сколько корневых разделов в справочной сборке WebForms? | Три: интерфейсы, перечисления, классы. **Раздела «расширители» нет.** |
| Где перечислены события? | **Не в сборке WebForms.** В страницах классов/интерфейсов WebForms раздела «События» нет вообще. События перечислены в описаниях компонентов (проект UiDevEnv) и в статье «Создание веб-формы…» |
| События самой формы | `onShow`, `onCommand` |
| Тип `WebReportBox.Report` | `IPrxReport` (сборка Report) |
| Тип `WebDimensionCombo.Selection` | `IDimSelection` (сборка Dimensions) |
| Тип `WebTextArea.Lines` | `IStringList` (сборка Collections) |
| Открыть объект репозитория из кода формы | `Self.ShowObject(MDesc[, Context])` |
| Строка гиперссылки на объект с параметрами | `"@STD_DIM(P_STRING=a;P_INT=1;P_FLOAT=0.01;P_DATE=09.02.2021 00:00:00)"` |
| Расширитель `WebFormsExt` | **НЕ НАЙДЕНО / НЕ ДОКУМЕНТИРОВАНО** (см. §9) |

---

## 1. `WebForm` (класс) / `IWebFormComponent` (интерфейс) / `IWebForm` (Metabase)

### 1.1. Назначение

- **`WebForm`** — «*Класс WebForm предоставляет веб-форму*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/class/webform/webform.htm>
- **`IWebFormComponent`** — «*Интерфейс IWebFormComponent содержит свойства и методы веб-формы как компонента среды разработки*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.htm>
- **`IWebForm`** — это **другая сборка**: «*Сборка: Metabase*», «*Интерфейс IWebForm содержит свойства и методы объекта среды
  разработки - веб-форма*». Веб-форма как объект репозитория (открытие/редактирование/команды).
  Источник: <https://help.fsight.ru/ru/mergedProjects/KeSom/Interface/IWebForm/IWebForm.htm>

> ℹ️ В сборке WebForms интерфейса `IWebForm` **НЕТ**. Роль «интерфейса веб-формы» играет `IWebFormComponent` (среда разработки)
> плюс `IWebForm` из сборки Metabase (объект репозитория).

### 1.2. Класс формы, именование и привязка обработчиков

Цитата (источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/01_development_environment/02_work_in_development_environment/devenv_object/web_form.htm>):

> «Веб-форма является инструментом для создания визуального интерфейса веб-приложений. … **Каждой веб-форме соответствует модуль,
> содержащий описание класса формы. Название класса должно совпадать со значением свойства name веб-формы.**»
> «На панели **Свойства/События** задаются свойства компонентов и обработчики для событий. … **В коде для компонентов будут
> доступны только те свойства, которые можно изменить во время выполнения веб-формы.**»

Наблюдаемая схема кода (из примеров в справке — правило именования обработчиков **выведено из примеров**, отдельной статьи
с формулировкой правила найти не удалось, см. §11):

```fore
Class TESTWebForm: WebForm          // имя класса = значение свойства name веб-формы
    bSave: WebButton;               // компоненты объявляются полями класса (без New)
    MDesc: IMetabaseObjectDescriptor;
    Sub TESTWebFormOnShow;          // <ИмяКласса> + OnShow
    Begin
        ...
    End Sub TESTWebFormOnShow;
    Sub bSaveOnClick;               // <ИмяКомпонента> + OnClick
    Begin
        MDesc.SaveDescriptor;
        Self.Close;                 // закрытие формы
    End Sub bSaveOnClick;
End Class TESTWebForm;
```

Источник примера: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web/features_web_form.htm> (там же второй пример —
`Sub TESTWebFormOnShow(Args: ISortedList);`).
Дополнительное подтверждение схемы «класс = имя формы»: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.text.htm>
(пример: `Class TESTWebForm: WebForm … Sub TESTWebFormOnShow;`).
Подтверждение схемы «обработчик = имя компонента + имя события»: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.components.htm>
(`Sub Button1OnClick;`) и <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.showobject.htm>
(`Sub Button1OnClick;`).

### 1.3. Свойства

| Свойство | Сигнатура | Источник |
| --- | --- | --- |
| `Clipboard` | `Clipboard: IWebClipboard` ⚠ тип не выгружен отдельно (по индексу интерфейсов — `IWebClipboard` «предназначен для работы с буфером обмена веб-формы») | [iwebformcomponent.clipboard.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.clipboard.htm) |
| `Components` | `Components: IWebComponents` | [iwebformcomponent.components.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.components.htm) |
| `Parent` | `Parent` — «возвращает родительскую веб-форму, из которой была открыта текущая форма» ⚠ сигнатура не выгружена | [iwebformcomponent.parent.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.parent.htm) |
| `StartupObject` | `StartupObject` — «описание текущего запущенного объекта» ⚠ тип не выгружен | [iwebformcomponent.startupobject.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.startupobject.htm) |
| `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Text`, `Visible` | унаследованы от `IWebControl` (см. §8) | [webform.htm](https://help.fsight.ru/ru/mergedProjects/webforms/class/webform/webform.htm) |
| `Name` | унаследовано от `IWebComponent` (см. §8) | [webform.htm](https://help.fsight.ru/ru/mergedProjects/webforms/class/webform/webform.htm) |

### 1.4. Методы

| Метод | Сигнатура | Источник |
| --- | --- | --- |
| `Close` | `Close` — «осуществляет закрытие текущей веб-формы» ⚠ сигнатура не выгружена; в примерах — `Self.Close;` | [iwebformcomponent.close.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.close.htm) |
| `ShowObject` | `ShowObject(Object: IMetabaseObjectDescriptor; [Ctx: IWebOpenContext])` | [iwebformcomponent.showobject.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.showobject.htm) |

### 1.5. События (самое важное)

**В сборке WebForms события не документированы** (в `webform.htm` разделов «События» нет). Полный список событий формы найден в
статье «Создание веб-формы и размещение компонентов» (проект UiDevEnv), вкладка **«События»**:

| Событие | Цитата из справки | Источник |
| --- | --- | --- |
| `onShow` | «**onShow. Событие наступает непосредственно перед выводом веб-формы на экран**» | [web_form.htm](https://help.fsight.ru/ru/mergedProjects/uidevenv/01_development_environment/02_work_in_development_environment/devenv_object/web_form.htm) |
| `onCommand` | «**onCommand. Событие наступает во время получения веб-формой команды, которая может быть отправлена с помощью метода SendCommand**» | там же |

`onShow` может принимать необязательный аргумент (для веб-форм, назначенных обработчиками операций пользовательских классов):
`OnShow(Args: ISortedList)`, где в `Args` доступны ключи `Values` (`IMetabaseObjectParamValues`), `Descriptor`
(`IMetabaseObjectDescriptor`), `Operation` (`String`).
Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web/features_web_form.htm>

Аргумент события `onCommand` — интерфейс `IWebCommandEventArgs` со свойствами `Argument`, `Command`, `Result`
(см. §8.3). Команда отправляется методом `IWebForm.SendCommand` (сборка Metabase, §1.6).

### 1.6. Режим дизайнера / режим выполнения (что доступно в коде)

По статье [web_form.htm](https://help.fsight.ru/ru/mergedProjects/uidevenv/01_development_environment/02_work_in_development_environment/devenv_object/web_form.htm)
в **режиме дизайнера** задаются (в коде недоступны): `text`, `name`, `alignItems`, `color`, `flexDirection`, `imageCollection`,
`justifyContent`, `modal`, `padding`, `popupMenu`, `resizeEnabled`, `size`. Модальность: «*Веб-формы по умолчанию открываются
модально… Максимальное количество открытых относительно друг друга модальных веб-форм - 5 штук*»; `modal = False` → отдельная
вкладка браузера.
**Режим выполнения (доступно в коде):** `Clipboard`, `Color`, `Components`, `Enabled`, `Name`, `PopupMenu`, `StartupObject`, `Text`,
`Visible`; методы `Close`, `ShowObject`; события `onShow`, `onCommand`.

### 1.7. `IWebForm` (Metabase) — кратко

Свойства унаследованы от `IModule`: `Assembly`, `Modified`, `ParentAssembly`, `Standalone`, `Text`. Методы: `SendCommand`
(«*осуществляет отправку команды веб-форме и получает результаты её выполнения*»), `ShowModal` («*открывает веб-форму модально
относительно того объекта, из которого выполняется код*»).
Источник: <https://help.fsight.ru/ru/mergedProjects/KeSom/Interface/IWebForm/IWebForm.htm>

---

## 2. `WebReportBox` / `IWebReportBox`

**Назначение:** «*Компонент ReportBox предназначен для отображения и работы с регламентными отчётами репозитория*». Источники: описание компонента <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/reportbox.htm>; класс <https://help.fsight.ru/ru/mergedProjects/webforms/class/webreportbox/webreportbox.htm>; интерфейс <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebreportbox/iwebreportbox.htm>

### Свойства

| Свойство | Сигнатура | Источник |
| --- | --- | --- |
| `Report` | `Report: IPrxReport;` (сборка **Report**) | [iwebreportbox.report.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebreportbox/iwebreportbox.report.htm) |
| + унаследованные `IWebControl` / `IWebComponent` | `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Text`, `Visible`, `Name` | [iwebreportbox.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebreportbox/iwebreportbox.htm) |

**Точная цитата типа (`Report`):**

> `Report: IPrxReport;`

Пример из справки (обработчик `OnShow`; сборки Metabase, Report, Tab):

```fore
MB := MetabaseClass.Active;                              // MB: IMetabase
Rep := MB.ItemById("REPORT").Open(Null) As IPrxReport;   // Rep: IPrxReport
ReportBox1.Report := Rep;                                // подключение отчёта к компоненту
```

### События

- `onCellChange` — «*Компонент имеет событие onCellChange, которое генерируется при изменении значения в какой-либо ячейке.
  **Событие не предоставляет информации об изменяемой ячейке** и предназначено для взаимодействия с другими компонентами веб-формы.
  Если требуется информация об изменяемой ячейке, то используйте обработчик событий регламентного отчёта и соответствующий метод
  класса `ReportEvents`*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/reportbox.htm>

### Про клики/гиперссылки внутри ReportBox

«Клик по гиперссылке внутри ReportBox» отдельно не документирован; механика гиперссылок/расшифровки описана для таблиц отчётов (§10) и через обработчики событий регламентного отчёта (`ReportEvents`). На интерактивность влияют свойства дизайнера `showControlPanel`, `showTabs`, `showHeaders`, `mobj` (ключ отображаемого регламентного отчёта). Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/reportbox.htm>

Важная особенность сессии (источник <https://help.fsight.ru/ru/mergedProjects/uidevenv/web/features_web_form.htm>): «*Если по пользовательской кнопке открывается веб-форма, то в системе… фиксируется активный регламентный отчёт. Активный отчёт возвращает статическое свойство `PrxReport.ActiveReport`… Для работы с отчётом из веб-формы рекомендуется сохранять активный отчёт в глобальную переменную, объявленную на уровне класса веб-формы. Запись активного отчёта в переменную осуществлять в событии onShow*».

---

## 3. `WebDimensionCombo` / `IWebDimensionCombo`

**Назначение:** «*Компонент DimensionCombo реализует раскрывающийся список элементов справочника репозитория*». Источники: описание <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/dimensioncombo.htm>; класс <https://help.fsight.ru/ru/mergedProjects/webforms/class/webdimensioncombo/webdimensioncombo.htm>; интерфейс <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdimensioncombo/iwebdimensioncombo.htm>

### Свойства

| Свойство | Сигнатура | Источник |
| --- | --- | --- |
| `Columns` | `Columns: IWebDimensionColumns` — «возвращает коллекцию столбцов компонента» ⚠ сигнатура выгружена из текста страницы `columns.htm` не полностью (тип взят из описания интерфейса `IWebDimensionColumns`) | [iwebdimensioncombo.columns.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdimensioncombo/iwebdimensioncombo.columns.htm) |
| `DimInstance` | `DimInstance: IDimInstance;` (сборка **Dimensions**) | [iwebdimensioncombo.diminstance.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdimensioncombo/iwebdimensioncombo.diminstance.htm) |
| `Selection` | `Selection: IDimSelection;` (сборка **Dimensions**) | [iwebdimensioncombo.selection.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdimensioncombo/iwebdimensioncombo.selection.htm) |
| + унаследованные | `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Text`, `Visible`, `Name` | [iwebdimensioncombo.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdimensioncombo/iwebdimensioncombo.htm) |

**Точная цитата типа (`Selection`):**

> `Selection: IDimSelection;`

Пример из справки (обработчик `OnShow`; сборки Dimensions, Metabase):

```fore
Dim := Mb.ItemById("DICT_1").Open(Null) As IDimInstance;    // Открытие справочника
Sel := Dim.CreateSelection;                                 // Создание отметки
Sel.SelectElement(2, False);  Sel.SelectElement(4, False);  Sel.SelectElement(6, False);
DimensionCombo1.DimInstance := Dim;                         // Подключение справочника
DimensionCombo1.Selection := Sel;
```

### Мультивыбор

- В API мультивыбор обеспечивается типом отметки `IDimSelection` (несколько `SelectElement`).
- Для компонента есть **свойство режима дизайнера** `selectionMode` («*Режим отметки в компоненте*») — в коде недоступно.
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/dimensioncombo.htm>
- Источник данных: «*Для работы компонента определите свойство `mobj` в режиме дизайнера или свойство `DimInstance` в режиме
  выполнения веб-формы*». По умолчанию отображается атрибут с назначением «Наименование». Прочие свойства дизайнера:
  `displayAttribute`, `searchEnable`, `showColumnHeaders`, `gridLines`, `font`, `hint`, `showHint`, `mobj`, `columns`.

### События

- `onSelectionChange` — «*Компонент имеет событие onSelectionChange, в котором может отслеживаться изменение отметки элементов*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/dimensioncombo.htm>

---

## 4. `WebTextArea` / `IWebTextArea`

**Назначение:** «*Компонент TextArea реализует многострочный редактор текста*».
Источники: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/textarea.htm>,
<https://help.fsight.ru/ru/mergedProjects/webforms/class/webtextarea/webtextarea.htm>,
<https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtextarea/iwebtextarea.htm>

### Свойства

| Свойство | Сигнатура | Источник |
| --- | --- | --- |
| `Lines` | `Lines: IStringList;` (сборка **Collections**) | [iwebtextarea.lines.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtextarea/iwebtextarea.lines.htm) |
| `SelStart` | `SelStart` — «возвращает позицию, в которой расположен курсор или начинается выделение текста» ⚠ тип не выгружен (по смыслу — целочисленный) | [iwebtextarea.selstart.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtextarea/iwebtextarea.selstart.htm) |
| `SelEnd` | `SelEnd` — «возвращает позицию, в которой заканчивается выделение текста» ⚠ тип не выгружен | [iwebtextarea.selend.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtextarea/iwebtextarea.selend.htm) |
| `Text` | `Text: String;` (унаследовано от `IWebControl`) | [iwebcontrol.text.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.text.htm) |
| + прочие унаследованные | `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Visible`, `Name` | [iwebtextarea.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtextarea/iwebtextarea.htm) |

**Точная цитата типа (`Lines`):**

> `Lines: IStringList;`

Пример из справки: `Lines := New StringList.Create; Lines.Add(...); TextArea1.Lines := Lines;`

### `ReadOnly` — ВАЖНО

- В интерфейсе `IWebTextArea` (сборка WebForms) свойства `ReadOnly` **НЕТ**.
- В описании компонента `readOnly` («*Признак доступности текста для редактирования*») указан **только в списке «Режим дизайнера»**, а в списке «Режим выполнения» его нет. Учитывая правило «*В коде для компонентов будут доступны только те свойства, которые можно изменить во время выполнения веб-формы*», из Fore-кода `readOnly` текстовой области недоступен. Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/textarea.htm>
- Аналог в коде — `Enabled := False` (см. пример в §8.2).
- Для сравнения: у `DateTimePicker` `readOnly` тоже только в режиме дизайнера (<https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/datetimepicker.htm>).

### События

- `onTextChanged` — «*Компонент имеет событие onTextChanged, которое наступает при изменении текста в компоненте*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/textarea.htm>

---

## 5. `WebCheckBox` / `IWebCheckBox`

**Назначение:** «*Компонент CheckBox реализует флажок с текстом…*». Источники: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/checkbox.htm>, <https://help.fsight.ru/ru/mergedProjects/webforms/class/webcheckbox/webcheckbox.htm>, <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.htm>

### Свойства

| Свойство | Сигнатура | Источник |
| --- | --- | --- |
| `Checked` | `Checked: Boolean;` | [iwebcheckbox.checked.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.checked.htm) |
| `State` | `State: WebCheckBoxState;` (перечисление, см. §7.5) | [iwebcheckbox.state.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.state.htm) |
| `BoxBorderColor` | «цвет границы области флажка» ⚠ тип не выгружен (вероятно `IGxColor`) | [iwebcheckbox.boxbordercolor.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.boxbordercolor.htm) |
| `CheckColor` | «цвет флажка» ⚠ тип не выгружен | [iwebcheckbox.checkcolor.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.checkcolor.htm) |
| `CheckedBoxColor` | «цвет заливки области флажка» ⚠ тип не выгружен | [iwebcheckbox.checkedboxcolor.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.checkedboxcolor.htm) |
| + унаследованные | `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Text`, `Visible`, `Name` | [iwebcheckbox.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcheckbox/iwebcheckbox.htm) |

Комментарий из справки по `State`: «*В отличии от свойства Checked, данное свойство позволяет выставить промежуточное состояние флажка*». Промежуточное состояние включается свойством дизайнера `allowIndeterminate`.

Пример: `CheckBox1.Checked := True; CheckBox1.CheckColor := GxColor.FromKnownColor(GxKnownColor.Green);` (сборки Drawing, WebForms).

### События

- `onChange` — «*Компонент имеет событие onChange, в котором может отслеживаться состояние флажка*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/checkbox.htm>
- ⚠ Отдельной страницы-описания события `onChange` (с аргументами) в сборке WebForms найти не удалось — **аргументы события не
  проверены**.

---

## 6. `WebButton` / `IWebButton`

**Назначение:** «*Компонент Button реализует кнопку, позволяющую инициировать выполнение какого-либо прикладного кода*».
Источники: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/button.htm>,
<https://help.fsight.ru/ru/mergedProjects/webforms/class/webbutton/webbutton.htm>,
<https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebbutton/iwebbutton.htm>

### Свойства

Собственных свойств у класса/интерфейса нет — только унаследованные: `BorderColor`, `Color`, `Enabled`, `PopupMenu`, `Text`
(`String`), `Visible` (`Boolean`), `Name` (`String`).
### События

- `onClick` — «*Компонент имеет событие onClick, в котором может осуществляться запуск какого-либо кода*».
  Источник: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/button.htm>
- Пример обработчика (имя компонента + имя события): `Sub Button1OnClick;`
  Источники: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.showobject.htm>,
  <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.components.htm>
- ⚠ Аргументы события не проверены (страницы с описанием события в сборке WebForms нет).

Свойства дизайнера (в коде недоступны): `coordinate`, `disabledState`, `flexGrow`, `font`, `hint`, `hoverState`, `imageLayout`,
`normalState`, `padding`, `position`, `pushedState`, `showHint`, `size`, `wordWrap`; изображения кнопки берутся из `imageCollection`
формы. В `Text` кнопки поддерживаются коды переноса строки `#10`, `#13+#10`, `#10+#13`
(<https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.text.htm>).

---

## 7. Остальные компоненты (кратко)

### 7.1. `WebDateTimePicker` / `IWebDateTimePicker`

Описание: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/datetimepicker.htm> · Интерфейс:
<https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdatetimepicker/iwebdatetimepicker.htm>

| Член | Сигнатура | Источник |
| --- | --- | --- |
| `Value` | `Value: DateTime;` | [value.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdatetimepicker/iwebdatetimepicker.value.htm) |
| `MinValue` / `MaxValue` | «минимальное/максимальное значение, доступное для ввода» ⚠ типы не выгружены (вероятно `DateTime`) | [minvalue.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdatetimepicker/iwebdatetimepicker.minvalue.htm), [maxvalue.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdatetimepicker/iwebdatetimepicker.maxvalue.htm) |
| `Valid` | «признак корректности даты» ⚠ тип не выгружен (вероятно `Boolean`) | [valid.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebdatetimepicker/iwebdatetimepicker.valid.htm) |
| Событие | `OnValueChanged` — «*наступает при изменении значения в компоненте*» | [datetimepicker.htm](https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/datetimepicker.htm) |

Диапазон календаря: `[14.09.1752 00:00:00, 18.12.3001 23:59:59]`; `Text` зависит от формата `format` (дизайнер); `readOnly` — только
в дизайнере. Пример: `DateTimePicker1.Value := DateTime.Now;`

### 7.2. `WebInput` / `IWebInput`

Описание: <https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/input.htm> · Класс:
<https://help.fsight.ru/ru/mergedProjects/webforms/class/webinput/webinput.htm>

Собственных членов у класса/интерфейса нет — только унаследованные `Text` (`String`), `Enabled`, `Visible`, `Color`, `BorderColor`,
`PopupMenu`, `Name`. Значение, введённое пользователем, читается/пишется через **`Text`** (собственного `Value` у `WebInput` нет).
Событие `onTextChanged` — «*может отслеживаться вводимый текст*»; свойства дизайнера `isPassword`, `placeholder`, `hint`, `font`.
Пример отключения редактирования из справки: `(Component As IWebInput).Enabled := False;`
Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.components.htm>

### 7.3. `WebPanel` (класс)

Класс: <https://help.fsight.ru/ru/mergedProjects/webforms/class/webpanel/webpanel.htm> · Описание:
<https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/panel.htm>

Собственных членов в сборке WebForms не перечислено; доступны унаследованные `Name`, `Text`, `Enabled`, `Visible`, `Color`,
`BorderColor`, `PopupMenu`. ⚠ События панели в прочитанных страницах **не указаны** (не найдено).

### 7.4. `WebTabControl` / `IWebTabControl`, `WebTabPage` / `IWebTabPage`

Интерфейс: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtabcontrol/iwebtabcontrol.htm> · Класс:
<https://help.fsight.ru/ru/mergedProjects/webforms/class/webtabcontrol/webtabcontrol.htm> · Класс вкладки:
<https://help.fsight.ru/ru/mergedProjects/webforms/class/webtabpage/webtabpage.htm>

| Член | Сигнатура | Источник |
| --- | --- | --- |
| `ActiveTab` | `ActiveTab: IWebTabPage;` | [activetab.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtabcontrol/iwebtabcontrol.activetab.htm) |
| `Pages` | `Pages: IWebTabPages;` | [pages.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebtabcontrol/iwebtabcontrol.pages.htm) |
| `WebTabPage` | собственных членов нет; только унаследованные от `IWebControl`/`IWebComponent` | [webtabpage.htm](https://help.fsight.ru/ru/mergedProjects/webforms/class/webtabpage/webtabpage.htm) |

⚠ События `TabControl`/`TabPage` в прочитанных страницах **не указаны** (не найдено). Описание компонента:
<https://help.fsight.ru/ru/mergedProjects/uidevenv/web_components/tabcontrol.htm>

### 7.5. Прочие классы и перечисления (не разбирались детально)

Классы — индекс <https://help.fsight.ru/ru/mergedProjects/webforms/class/webforms_class.htm>: `WebComboBox`, `WebDataGridView`,
`WebDimensionTree`, `WebFileOpenDialog`, `WebFileSaveDialog`, `WebFloatEdit`, `WebFrame`, `WebIntegerEdit`, `WebLabel`,
`WebMessageBox`, `WebMetabaseTreeCombo`, `WebOpenContext`, `WebPopupMenu`, `WebRadioButton`, `WebTreeCombo`, `WebTreeList`.
Перечисления — индекс <https://help.fsight.ru/ru/mergedProjects/webforms/enums/webforms_enums.htm>: `WebCheckBoxState`,
`WebDialogResult`, `WebInsertMode`, `WebMessageBoxButtons`, `WebMessageBoxIcon`.

---

## 8. Базовые интерфейсы (общие члены)

Индекс интерфейсов: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/webforms_interface.htm>

### 8.1. `IWebComponent` — «*базовый для всех визуальных и невизуальных компонентов веб-форм*»

| Член | Сигнатура | Источник |
| --- | --- | --- |
| `Name` | `Name: String;` — «*Наименование компонента можно изменить только в режиме дизайнера веб-формы*» | [iwebcomponent.name.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcomponent/iwebcomponent.name.htm) |

> ⚠ Свойства `ID` в API **НЕТ** (в индексе интерфейсов и на странице `IWebComponent` не встречается).

### 8.2. `IWebControl` — «*базовые свойства и методы всех визуальных компонентов веб-форм*»

Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.htm>

| Член | Сигнатура | Источник |
| --- | --- | --- |
| `Text` | `Text: String;` — по умолчанию совпадает с наименованием компонента; для формы задаёт заголовок | [text.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.text.htm) |
| `Visible` | `Visible: Boolean;` (True по умолчанию; False — «*Компонент скрыт, но доступен в коде приложения*») | [visible.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.visible.htm) |
| `Enabled` | `Enabled: Boolean;` | [enabled.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.enabled.htm) |
| `Color` | `Color: IGxColor;` (сборка Drawing) | [color.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.color.htm) |
| `BorderColor` | «цвет границы компонента» ⚠ тип не выгружен (вероятно `IGxColor`) | [bordercolor.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.bordercolor.htm) |
| `PopupMenu` | `PopupMenu: IWebPopupMenu;` | [popupmenu.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.popupmenu.htm) |
| `Name` | унаследовано от `IWebComponent` | [iwebcontrol.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcontrol/iwebcontrol.htm) |

Наследники `IWebControl` (по справке): `IWebButton`, `IWebCheckBox`, `IWebComboBox`, `IWebDimensionCombo`, `IWebDimensionTree`,
`IWebFloatEdit`, **`IWebFormComponent`**, `IWebInput`, `IWebLabel`, `IWebMetabaseTreeCombo`, `IWebPanel`, `IWebRadioButton`,
`IWebReportBox`, `IWebTabControl`, `IWebTabPage`, `IWebTextArea`, `IWebTreeControl`.

Пример перебора компонентов формы (показывает и `Count`, и `Item`, и проверку типа через `Is`):

```fore
AllComponents := Self.Components;          // IWebComponents — коллекция компонентов формы
c := AllComponents.Count;
For i := 0 To c - 1 Do
    Component := AllComponents.Item(i);    // IWebComponent
    If Component Is IWebInput Then
        (Component As IWebInput).Enabled := False;
    End If;
End For;
```

Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.components.htm>
(`IWebComponents` — «*коллекция компонентов, расположенных на веб-форме*»; методы `Count`/`Item` видны из примера, ⚠ отдельная
страница `iwebcomponents.htm` не выгружалась).

### 8.3. `IWebCommandEventArgs` — аргумент события `onCommand`

| Член | Описание | Источник |
| --- | --- | --- |
| `Command` | «*возвращает наименование команды, посланной веб-форме*» | [iwebcommandeventargs.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebcommandeventargs/iwebcommandeventargs.htm) |
| `Argument` | «*возвращает значение аргумента команды*» | там же |
| `Result` | «*определяет значение результата выполнения команды*» | там же |

⚠ Типы этих свойств не выгружены (не проверены). Команда отправляется методом `IWebForm.SendCommand`.

### 8.4. `IWebOpenContext` — контекст открытия объекта из веб-формы

Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebopencontext/iwebopencontext.htm>
Создание: «*Для получения контекста открытия объекта инициализируйте объект класса `WebOpenContext`*» → `New WebOpenContext.Create`.

| Член | Сигнатура | Источник |
| --- | --- | --- |
| `CurrentTab` | `CurrentTab: Boolean;` (True — текущая вкладка (по умолчанию), False — новая) | [currenttab.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebopencontext/iwebopencontext.currenttab.htm) |
| `Edit` | «признак открытия объекта на редактирование» ⚠ тип не выгружен (вероятно `Boolean`) | [edit.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebopencontext/iwebopencontext.edit.htm) |
| `ParamValues` | `ParamValues: IMetabaseObjectParamValues;` | [paramvalues.htm](https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebopencontext/iwebopencontext.paramvalues.htm) |

Прочие интерфейсы (не разбирались): `IWebClipboard`, `IWebComponents`, `IWebDimensionColumn(s)`, `IWebFileDialog`,
`IWebTabPages`, `IWebTreeControl`, `IWebTreeNode(s)`, `IWebTreeSelection`, `IWebTreeCombo/List`, `IWebPopupMenu`, `IWebMessageBox`.

---

## 9. Расширители сборки WebForms (`WebFormsExt`) — НЕ НАЙДЕНО

**Результат: расширитель `WebFormsExt` (и метод вида `GetDimSelectionAttrValue(dimSel, attrId)`) в справке help.fsight.ru
НЕ НАЙДЕН и НЕ ДОКУМЕНТИРОВАН.** Ни одной страницы с таким именем не обнаружено; поисковые запросы по строкам `WebFormsExt`,
`GetDimSelectionAttrValue`, «Расширители сборки WebForms» не вернули ни одного документа справки «Форсайт» (единственные
совпадения — сторонние материалы по ASP.NET Web Forms).

Что проверено (ни в одном месте расширители WebForms не упоминаются):

- **Корень сборки** (<https://help.fsight.ru/ru/mergedProjects/webforms/webforms_title.htm>) — перечислены **только три**
  подраздела: «Интерфейсы сборки WebForms», «Перечисления сборки WebForms», «Классы сборки WebForms». Раздела расширителей нет.
- **«Описание системных сборок»** (<https://help.fsight.ru/ru/mergedProjects/assembly/system_assembly.htm>) — для сборки
  **WebForms** ссылка ведёт на `WebForms/WebForms_Title.htm` с описанием «*Стандартные и дополнительные компоненты (дизайнер
  веб-форм)*» (речь о компонентах, не о расширителях); отдельного раздела расширителей нет.
- **«Описание API расширений»** (<https://help.fsight.ru/ru/mergedProjects/assembly/api_extentions.htm>) — слово «расширения»
  здесь означает **расширения продукта** (единственная ссылка — «API форм ввода»), а не Fore-расширители.
- **Угаданные URL** `…/webforms/extenders/extenders.htm` и `…/webforms/extenders/webforms_extenders.htm` — HTTP **404**.
- **«Руководство по языку Fore»** (<https://help.fsight.ru/ru/mergedProjects/Fore/Fore_Title.htm>) — раздела «Расширители» в
  оглавлении нет.
- **Локальные CHM-дампы** `F:\Scheduler Tasks\docs\forsite\` — grep `WebFormsExt` → 0 совпадений, grep `расширител` → 0 совпадений.
- **EN-зеркало** (<https://help.fsight.ru/en/mergedProjects/webforms/webforms_title.htm>) — те же три подраздела.

**Вывод для чтения модуля:** если в существующем модуле веб-формы используется объект вида `WebFormsExt` — этот API в публичной
справке не описан; искать его описание нужно в другом месте (внутренняя документация, `IntelliSense` среды разработки,
инспектор сборок, метаданные сборки `.NET`/Fore). **Из справки подтвердить существование и сигнатуры `WebFormsExt` нельзя.**

---

## 10. Открытие объекта репозитория (в т.ч. `PRX_…`) с параметрами; гиперссылка `@OBJECT_ID(PARAM=value;…)`

### 10.1. Из кода веб-формы (Fore API) — проверенный способ

Метод `IWebFormComponent.ShowObject(Object: IMetabaseObjectDescriptor; [Ctx: IWebOpenContext])`.
Полный пример из справки (открытие регламентного отчёта `REPORT` с двумя параметрами `P_START`, `P_FINISH` в новой вкладке):

```fore
Sub Button1OnClick;
Var  Mb: IMetabase;  MDesc: IMetabaseObjectDescriptor;
     Values: IMetabaseObjectParamValues;  Context: IWebOpenContext;
Begin
    Mb := MetabaseClass.Active;
    MDesc := Mb.ItemById("REPORT");
    Context := New WebOpenContext.Create;      // Настройка контекста открытия объекта
    Context.CurrentTab := False;               // новая вкладка браузера
    Context.Edit := False;                     // на просмотр
    Values := MDesc.Params.CreateEmptyValues;
    Values.FindById("P_START").Value := 2010;
    Values.FindById("P_FINISH").Value := 2020;
    Context.ParamValues := Values;
    Self.ShowObject(MDesc, Context);           // Открытие объекта
End Sub Button1OnClick;
```

Источник: <https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebopencontext/iwebopencontext.currenttab.htm>
(аналогичный пример без параметров — `Self.ShowObject(MDesc);` —
<https://help.fsight.ru/ru/mergedProjects/webforms/interface/iwebformcomponent/iwebformcomponent.showobject.htm>)

Ограничения метода (цитаты из справки): «*Метод может быть выполнен только из кода веб-формы*»; нельзя открывать объекты типов
Модуль, Python-модуль, Сборка, Карта, Документ, Связь с репозиторием, База данных, Модель данных, Журнал, Бизнес-приложение,
Пользовательские объекты; «*Если параметр Ctx не указан, то объект открывается на просмотр в текущей вкладке браузера*»;
«*Справочники, используемые в коде веб-форм при открытии объектов с параметрами, будут закрываться только при закрытии сессии*».

### 10.2. Строка действия гиперссылки `@OBJECT_ID(...)` — формат

Документируется в свойстве `ITabHyperlink.Action` (сборка **Tab**), тип действия — «Открыть объект репозитория» /
«Открыть объект репозитория с передачей параметров»; формат применяется и в веб-приложении.
Источник: <https://help.fsight.ru/ru/mergedProjects/tabsheet/interface/itabhyperlink/itabhyperlink.action.htm>

Цитаты (значения свойства `Action`):

> «Открыть объект репозитория — *Идентификатор объекта с префиксом '@', например: "@STD_DIM"*»
> «Открыть объект репозитория с передачей параметров — *Идентификатор объекта с префиксом '@' и список значений параметров. Параметры
> объекта передаются в круглых скобках в виде конструкции <идентификатор параметра>=<значение параметра> и отделяются друг от друга
> точкой с запятой. Параметр может принимать единичное или множественное значение. Множественное значение указывается в квадратных
> скобках в виде массива.*»

Примеры (дословно из справки):

```
"@STD_DIM"
"@STD_DIM(P_STRING=a;P_INT=1;P_FLOAT=0.01;P_DATE=09.02.2021 00:00:00)"
"@STD_DIM(P_STRING=[a,b];P_INT=[1,2];P_FLOAT=[0.01,0.02];P_DATE=[09.02.2021 00:00:00,10.02.2021 00:00:00])"
```

Тип действия задаётся в `ITabHyperlink.ActionType` (задействованное значение — `TabHyperlinkActionType.OpenObject`, проверено по
<https://help.fsight.ru/ru/mergedProjects/uianalyticalarea/hyperlinks/hyperlinks_sub.htm>). ⚠ Точное имя значения перечисления для
варианта «с передачей параметров» **не проверено** (страница `itabhyperlink.actiontype.htm` не выгружалась).

Подстановки в строке действия (для разных объектов/значений параметров), источник
<https://help.fsight.ru/ru/mergedProjects/uianalyticalarea/hyperlinks/hyperlinks_sub.htm>:

| Подстановка | Смысл |
| --- | --- |
| `&[DIMENSION.<id>]` | значение атрибута измерения (для «Открыть ссылку»/«Открыть файл») |
| `@&[DIMENSION.<id>]` | открыть объект, ключ/идентификатор которого хранится в значении атрибута |
| `@&[DIMENSION.OBJ_ID](A=10;B="Start")` | открыть объект и передать два фиксированных значения входных параметров |
| `@[DIMENSION.OBJ_ID](PARAM0=&[OBJECTPARAM.PARAM0];PARAM1=&[OBJECTPARAM.PARAM1])` | передать в параметры значения параметров текущего объекта |
| `&[OBJECTPARAM.<id>]` | параметр регламентного отчёта |
| `&[SOURCEPARAM.<id>]` | параметр источника данных |

Примечание из справки: «*Подстановки расшифровки являются регистронезависимыми*».

### 10.3. Гиперссылки/расшифровка в веб-клиенте (UI)

«*Расшифровка элементов измерения*» настраивается на вкладке «Расшифровка» боковой панели (экспресс-отчёт, аналитическая панель, регламентный отчёт). Доступные действия: смена отметки; переход на другой лист/объект; выделение ячеек; **открытие ссылки/файла/объекта репозитория**; «Выполнить функцию» (только регламентный отчёт — задаются Модуль, Функция, JS-функция). Источник: <https://help.fsight.ru/ru/mergedProjects/uianalyticalarea/hyperlinks/working_with_hyperlinks.htm>

«*Открытие объекта репозитория с параметрами*»: в боковой панели в поле «Параметры» отображается список всех параметров объекта; значение задаётся как «Значение атрибута», «Параметр отчета», «Параметр источника данных» или «Вручную». Примечание справки: «*Возможность передачи параметров в отчёт реализована только для параметров отчёта, передавать значения в параметры источника возможности нет*». Источник: <https://help.fsight.ru/ru/mergedProjects/uianalyticalarea/hyperlinks/open_objects_with_params.htm>

Callback-функции на гиперссылке: `"fore:<M_MODULE.TestFunction>"` / `"javascript:<TestJSFunction()>"`; в веб-приложении выполняется JS-функция, Fore-метод работает и в настольном, и в веб-приложении (<https://help.fsight.ru/ru/mergedProjects/tabsheet/interface/itabhyperlink/itabhyperlink.action.htm>). ⚠ Отдельной страницы проекта `dhtmlReport` именно про гиперссылки веб-клиента найти не удалось.

---

## 11. ОТКРЫТЫЕ ВОПРОСЫ / НЕ НАЙДЕНО

1. **`WebFormsExt` (расширитель) — не найден и не документирован.** Подтверждения существования, списка методов и сигнатуры `GetDimSelectionAttrValue(dimSel, attrId)` в справке нет; см. §9 (перечень выполненных проверок).
2. **Страницы «Расширители сборки WebForms» не существует.** В сборке WebForms только три раздела: интерфейсы, перечисления, классы. Проверены корень сборки, оглавление системных сборок, «Описание API расширений», угаданные URL (404), поиск, EN-зеркало, локальные CHM-дампы.
3. **События не документированы как члены API.** В страницах классов/интерфейсов сборки WebForms нет разделов «События»; список событий собран из описаний компонентов (UiDevEnv). Однозначного соответствия «событие → страница API» нет.
4. **Аргументы событий компонентов не описаны** для `onClick`, `onChange`, `onTextChanged`, `onSelectionChange`, `onCellChange`, `OnValueChanged`. Документированы только `onCommand` (`IWebCommandEventArgs`) и вариант `OnShow(Args: ISortedList)`. Для `onCellChange` справка прямо указывает, что событие **не** передаёт информацию о ячейке.
5. **Правило именования обработчиков не сформулировано явной фразой.** Схема `<ИмяКласса|ИмяКомпонента> + <ИмяСобытия>` (`TESTWebFormOnShow`, `bSaveOnClick`, `Button1OnClick`) выведена из примеров справки; статьи с формальным правилом найти не удалось.
6. **Не выгружены точные типы/сигнатуры** (в тексте помечены `⚠`): `IWebFormComponent.Parent`, `.StartupObject`, `.Clipboard`, `.Close`; `IWebControl.BorderColor`; `IWebCheckBox.BoxBorderColor` / `.CheckColor` / `.CheckedBoxColor`; `IWebTextArea.SelStart` / `.SelEnd`; `IWebDateTimePicker.MinValue` / `.MaxValue` / `.Valid`; `IWebOpenContext.Edit`; `IWebCommandEventArgs.Command` / `.Argument` / `.Result`; `IWebDimensionCombo.Columns`.
7. **Свойства `ID` у компонентов нет** — только `Name: String`, изменяемое лишь в дизайнере.
8. **`WebTextArea.ReadOnly` и `WebDateTimePicker.readOnly`** — только режим дизайнера, в коде недоступны (§4). Если в модуле встречается `ReadOnly` у этих компонентов, это требует уточнения.
9. **События `WebPanel`, `WebTabControl`, `WebTabPage`** в прочитанных страницах не указаны (возможно, их нет либо описаны в невыгруженных подстраницах).
10. **Клики/гиперссылки внутри `WebReportBox`** отдельно не документированы: справка отсылает к обработчикам событий регламентного отчёта и классу `ReportEvents`; механизм «клик по ячейке отчёта → код Fore» через события веб-формы не описан.
11. **Отдельной статьи проекта `dhtmlReport` про гиперссылки веб-клиента найти не удалось.** Формат `@OBJECT_ID(...)` подтверждён по сборке Tab (`ITabHyperlink.Action`) и разделу «Аналитическая область», а не по статье веб-клиента.
12. **Имя значения `TabHyperlinkActionType` для действия «Открыть объект репозитория с передачей параметров»** не проверено (страница `itabhyperlink.actiontype.htm` не выгружалась).
13. **Состав методов коллекций** `IWebComponents`, `IWebTabPages`, `IWebDimensionColumns` (кроме `Count`/`Item`, видимых в примерах) не проверялся.

---

## Приложение. Полный список прочитанных страниц (источники)

Базовый префикс: `https://help.fsight.ru/ru/mergedProjects/`.

- **Индексы:** `webforms/class/webforms_class.htm` · `webforms/interface/webforms_interface.htm` · `webforms/enums/webforms_enums.htm` · `webforms/webforms_title.htm`
- **Классы:** `webforms/class/<имя>/<имя>.htm` — `webform`, `webreportbox`, `webdimensioncombo`, `webtextarea`, `webbutton`, `webinput`, `webpanel`, `webtabcontrol`, `webtabpage`.
- **Интерфейсы:** `webforms/interface/<имя>/<имя>.htm` — `iwebformcomponent`, `iwebcomponent`, `iwebcontrol`, `iwebreportbox`, `iwebbutton`, `iwebdimensioncombo`, `iwebtextarea`, `iwebcheckbox`, `iwebtabcontrol`, `iwebdatetimepicker`, `iwebopencontext`, `iwebcommandeventargs`.
- **Отдельные члены:** `webforms/interface/<интерфейс>/<интерфейс>.<член>.htm` — `iwebreportbox.report`, `iwebdimensioncombo.selection`, `iwebdimensioncombo.diminstance`, `iwebtextarea.lines`, `iwebcheckbox.checked`, `iwebcheckbox.state`, `iwebcontrol.text|visible|enabled|color|popupmenu`, `iwebcomponent.name`, `iwebtabcontrol.activetab|pages`, `iwebdatetimepicker.value`, `iwebformcomponent.components|showobject`, `iwebopencontext.currenttab|paramvalues`.
- **Компоненты (UiDevEnv):** `uidevenv/web_components/web_components.htm` и `…/button.htm`, `…/checkbox.htm`, `…/datetimepicker.htm`, `…/dimensioncombo.htm`, `…/input.htm`, `…/reportbox.htm`, `…/textarea.htm`, `…/tabcontrol.htm`.
- **Разработка веб-форм:** `uidevenv/01_development_environment/02_work_in_development_environment/devenv_object/web_form.htm` · `uidevenv/web/features_web_form.htm` · `uidevenv/01_development_environment/02_work_in_development_environment/devenv_object/devenv_assembly.htm` · `developer/devenv_title.htm` · `developer/developer_intro.htm`
- **Смежные сборки и веб-клиент:** `KeSom/Interface/IWebForm/IWebForm.htm` · `tabsheet/interface/itabhyperlink/itabhyperlink.action.htm` · `uianalyticalarea/hyperlinks/working_with_hyperlinks.htm` · `uianalyticalarea/hyperlinks/open_objects_with_params.htm` · `uianalyticalarea/hyperlinks/hyperlinks_sub.htm` · `assembly/system_assembly.htm` · `assembly/api_extentions.htm` · `Fore/Fore_Title.htm`
- **404 (не существуют):** `webforms/extenders/extenders.htm`, `webforms/extenders/webforms_extenders.htm`
