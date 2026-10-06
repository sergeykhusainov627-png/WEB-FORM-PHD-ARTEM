# ANALIZ_TEP form — on-disk research (Part A) + offline-help platform facts (Part B)

Scope of the investigation (read-only roots): `F:\Scheduler Tasks`, `F:\BackUp_PHD`, `F:\backup sched`,
`F:\Export button Forsite`, `F:\testt`, `C:\Users\Manya\Downloads`.
File types searched: `*.fore *.txt *.md *.xml *.pas *.cs *.sql *.htm *.html *.js *.py`
(+ `7z l` listings of 12 archives). Write target: this workspace only.

**Headline result:** the form itself is on disk at `C:\Users\Manya\Downloads\backup.txt`
(1574 lines, `Class ANALIZ_TEP_FORM_ON_SHOW: WebForm`). **None of the stand helpers it calls
(`COpenHyperlink`, `WebFormsExt`, `TabExt`, `DimensionExt`, `GetDimSelectionAttrValue`,
`SetTabHyperlink`, `InitObject`, `SetParamValue`, `ParamManager`, `DesingCell`, `tst`) is defined
anywhere on disk, and none of them exists in the offline help.** The only members of the same family
that *are* documented are `ITabHyperlink` + `TabHyperlinkActionType.OpenObject` + the `@ID(PARAM=value;…)`
action string — which the form also uses directly and correctly at line 435.

---

# PART A — On-disk findings

## A.0 The form under review (the only file that mentions the stand helpers)

| Path | Lines | Excerpt |
|---|---|---|
| `C:\Users\Manya\Downloads\backup.txt` | 4 | `Class ANALIZ_TEP_FORM_ON_SHOW: WebForm` |
| ″ | 2, 338 | `fieldList: IStringList;` … `fieldList := New StringList.Create;` |
| ″ | 262 | `Const C_ANALYZ_TEP_REP_ID = "PRX_ANALYSIS_TEP";` |
| ″ | 261 | `Const C_BUTTON_OK_ID = "PRX_ANALYZ_TEP_BUTTON_OK";` |
| ″ | 264–316 | 50 `Const C_PARAM_* = "<ID>"` — the СЭ parameter list of the report |
| ″ | 318–319 | `_AnalyzTepHyperlink: COpenHyperlink; // CUrlHyperlink` / `_hlink: ITabHyperlink;` |

Definition site of the undocumented class (verbatim, lines 324–333):

```fore
Property Hyperlink: COpenHyperlink
Get
Begin
    If IsNull(_AnalyzTepHyperlink) Then
        _AnalyzTepHyperlink := New COpenHyperlink.Create(ReportBoxOk.Report, AppNs.PHD, "Ок");
        _AnalyzTepHyperlink.InitObject(C_ANALYZ_TEP_REP_ID);
    End If;
    Return _AnalyzTepHyperlink;
End Get
End Property Hyperlink;
```

Verbatim call sites / commented prototypes of the undocumented API:

| Line | Excerpt |
|---|---|
| 328 | `_AnalyzTepHyperlink := New COpenHyperlink.Create(ReportBoxOk.Report, AppNs.PHD, "Ок");` |
| 329 | `_AnalyzTepHyperlink.InitObject(C_ANALYZ_TEP_REP_ID);` |
| 350 | `// Hyperlink.SetParamValueFromSelection("CALYEAR", D_CALYEAR.Selection, "NAME");` |
| 351 / 1561 | `// Hyperlink.Generate;` / `Hyperlink.Generate;` |
| 378 | `TextArea1.Lines.Add(Hyperlink.tst);` |
| 403 | `//Hyperlink.DesingCell(ButtonCancel.Color);` |
| 448–452 | `{Sub UpdateOpenDefHlink(...); … _AnalyzTepHyperlink.SetParamValue(paramId, paramValue); _AnalyzTepHyperlink.Generate; End Sub …;}` (commented-out *old* implementation) |
| 629–630 | `//PM := _AnalyzTepHyperlink.ParamManager;` / `//TextArea1.Text := _AnalyzTepHyperlink.ParamManager.Params.Count;` |
| 628 | `// _AnalyzTepHyperlink := New COpenHyperlink.Create(ReportBoxOk.Report, AppNs.PHD, "Ок");` |
| 1560 | `Hyperlink.SetParamValue("P_FIELD_LIST", fieldList.Text(", "));` |
| 1562 | `TextArea1.Text := Hyperlink.Action;` |

`Sub` named exactly like its enclosing class (line 392) and the **real** (non-commented) body:

```fore
Sub ANALIZ_TEP_FORM_ON_SHOW;                // line 392 — same identifier as Class on line 4
Var  openReportTab: ITabSheet; optionReport: IPrxReport; MObj:IMetabaseObject;
Begin
    _hlink := InitializeHlinkOpenObject(ReportBoxOk.Report, "  Ок  ", C_ANALYZ_TEP_REP_ID);   // 398
    setDefaultDimensionValue;                                                                  // 400
End Sub ANALIZ_TEP_FORM_ON_SHOW;            // line 416
```

The **working, documented** alternative that the same file uses (lines 418–446) — this is the
hand-rolled equivalent of the missing `COpenHyperlink`/`TabExt` helpers:

```fore
Sub madeLinkForMyselfTst;                   // line 418
Var link: ITabHyperlink; style: ITabCellStyle; openReportTab: ITabSheet; ...
Begin
    openReportTab := ReportBoxOk.Report.ActiveSheet.Sheets.FindByName("Лист2") As ITabSheet;   // 428
    style := openReportTab.Cell(0, 0).Style;                                                   // 432
    link  := style.Hyperlink;                                                                  // 433
    link.ActionType := TabHyperlinkActionType.OpenObject;                                      // 434
    link.Action := String.Format("@{0}(PLANT={1};CALYEAR={2};ZLIB_INDC={3})",
                                 C_ANALYZ_TEP_REP_ID, "6500", "2026", "IND00005000");           // 435
    link.Enable := TriState.OnOption;                                                          // 442
    link.Color  := GxColor.FromName("Blue");                                                   // 443
    openReportTab.Cell(0, 0).Value := "tst";                                                   // 444
End Sub madeLinkForMyselfTst;
```

The other undefined call sites:

| Line | Excerpt |
|---|---|
| 1392 | `Sub UpdateOpenDefHlinkFromSelection(paramId: String; dimSel: IDimSelection; attrId: String = "");` |
| 1396 | `paramValue := WebFormsExt.GetDimSelectionAttrValue(dimSel, attrId);` |
| 1400–1518 | `Sub UpdateOpenDefHlink(paramId: String; paramValue: Variant);` — contains **5 nested** `Sub`/`Function` in its declaration part (`InsertParam` 1405, `UpdateParam` 1415, `RemoveParam` 1434, `GetParamIndex` 1455, `UpdateArrayToValue` 1472) |
| 1520–1545 | `Function InitializeHlinkOpenObject(report: IPrxReport; hlinkText, hlinkAction: String): ITabHyperlink;` |
| 1539 | `TabExt.SetTabHyperlink(hlinkCell, hlinkText, TabHyperlinkActionType.OpenObject, hlinkAction, True);` |
| 473 | `TabExt.SetTabHyperlink(hlinkCell, hlinkText, TabHyperlinkActionType.OpenObject, hlinkAction, False);` (inside the commented duplicate) |
| 346/355/363/370 | `// Index := DimensionExt.GetElementIndexByAttributeValue(D_CALYEAR.DimInstance, "NAME", "2024");` … |
| 536/539 | `// path.Add(DimensionExt.GetAttributeValueByElementIndex(groupDim, C_ATTR_NAME_ID, elemIndex));` / `//DimensionExt.GetAttributeValueByElementId(groupDim, "CODE");` |

### Verdict per symbol (Part A)

| Symbol | Definition found? | Usages found |
|---|---|---|
| `COpenHyperlink` | **NO — nowhere on disk** | `backup.txt:318,324,328,628` |
| `COpenHyperlink.Create(report, appNs, text)` | **NO** | `backup.txt:328,628` |
| `COpenHyperlink.InitObject(id)` | **NO** | `backup.txt:329` |
| `COpenHyperlink.SetParamValue` | **NO** | `backup.txt:450` (commented) |
| `COpenHyperlink.SetParamValueFromSelection` | **NO** | `backup.txt:350` (commented), 359/366/492/499/… (live) |
| `COpenHyperlink.Generate` | **NO** | `backup.txt:351,374,451,493,500,636,643,651,1561` |
| `COpenHyperlink.Action` (property) | **NO** | `backup.txt:406,1562` |
| `COpenHyperlink.tst` | **NO** | `backup.txt:378` |
| `COpenHyperlink.DesingCell` | **NO** | `backup.txt:403` (commented) |
| `COpenHyperlink.ParamManager` | **NO** | `backup.txt:629,630` (commented) |
| `WebFormsExt` | **NO** | `backup.txt:1396` |
| `WebFormsExt.GetDimSelectionAttrValue` | **NO** | `backup.txt:1396` |
| `TabExt` | **NO** | `backup.txt:473,1539` |
| `TabExt.SetTabHyperlink` | **NO** | `backup.txt:473,1539` |
| `DimensionExt` | **NO** | `backup.txt:346,355,363,370,536,539` (all commented) |
| `DimensionExt.GetElementIndexByAttributeValue` | **NO** | `backup.txt:346,355,363,370` |
| `DimensionExt.GetAttributeValueByElementIndex` | **NO** | `backup.txt:536` |
| `DimensionExt.GetAttributeValueByElementId` | **NO** | `backup.txt:539` |
| `AppNs` | **NO namespace named `AppNs` anywhere** | `backup.txt:328,628` only |
| `AppNs.PHD` | **NO** | `backup.txt:328,628` |
| `ANALIZ_TEP` | only inside the same file | `backup.txt:4,392,416,1573` |
| `PRX_ANALYSIS_TEP` | only inside the same file | `backup.txt:262` |
| `P_FIELD_LIST` | only inside the same file | `backup.txt:1560` |
| `UpdateOpenDefHlink` / `…FromSelection` | defined in the file itself (not a platform helper) | `backup.txt:448,452,1392,1398,1400,1518` + ~55 call sites |
| `InitializeHlinkOpenObject` | defined in the file itself | `backup.txt:398,454,479,1520,1545` |

## A.1 `MOD_PHD_STDDIM_BACKUP` — what the module does

**It has nothing to do with the form.** It is a PHD-stand *table-dimension backup* module.

| Path | Line | Excerpt |
|---|---|---|
| `F:\Scheduler Tasks\Fore\MOD_PHD_STDDIM_BACKUP.fore` | 2 | `// STDDIM_BACKUP — бэкап табличных справочников (KE_CLASS_STDDIM).` |
| ″ | 32 | `Sub StdDimBackup;` (entry point) |
| ″ | 295 | `Sub StdDimSwitchToBackup;` |
| ″ | 498 | `Function OrigIdOf(Id_: String): String;` |
| ″ | 519 | `Function FindTableByName(TabName: String; Db_: IDatabase): IMetabaseObjectDescriptor;` |
| `F:\BackUp_PHD\docs\BACKUP-DECOMPOSITION.md` | 70 | `## Программа 3 — `Fore/MOD_PHD_STDDIM_BACKUP.fore` (табличные справочники `KE_CLASS_STDDIM`)` |
| `F:\BackUp_PHD\docs\BACKUP-ACCEPTANCE.md` | 36 | `MOD_PHD_STDDIM_BACKUP.fore         61,5 КБ  1256 строк  2B56C7E9…` |
| `F:\BackUp_PHD\Fore\BackUp from stand\MOD_PHD_STDDIM_BACKUP_COPY2_COPY1.fore` | — | stand-unloaded copy (61 962 bytes) |
| `F:\BackUp_PHD\Fore\MOD_PHD_BACKUP_QUEUE.fore` | 28 | `Return "обработчик табличных справочников (MOD_PHD_STDDIM_BACKUP)";` |

Docs say it (a) finds table dimensions in a backup folder, (b) resolves their basis among
`dependencies(True)` (`KE_CLASS_TABLE` / `KE_CLASS_QUERY`), (c) creates `<X>_BACKUP` copies plus
`DELETE + INSERT SELECT *` SQL commands in folder `FLDR_PHD_TECH_STDDIM_BACKUP`, (d) never modifies
the originals (`F:\Scheduler Tasks\Fore\MOD_PHD_STDDIM_BACKUP.fore:1-29`).
**It defines no hyperlink/WebForm helpers.** The `MOD_PHD_*` prefix is simply the PHD-stand module
naming convention — which is consistent with the form's `AppNs.PHD` reference, but the helper
modules themselves (`WebFormsExt`, `TabExt`, `DimensionExt`, `COpenHyperlink`) are still absent.

## A.2 Other `MOD_PHD_*` / PHD-stand artefacts found

| Path | Note |
|---|---|
| `F:\BackUp_PHD\Fore\` (17 `.fore`) | `MOD_PHD_BACKUP_QUEUE`, `MOD_PHD_BACKUP_TECH_CONSTANTS`, `MOD_PHD_BACKUP_TECH_MAIN`, `MOD_PHD_BACKUP_TOOLS`, `MOD_PHD_RESTORE`, `MOD_PHD_SQL_PARSE`, `ETL_TABLES_BACKUP`, `ETL_NSI_T.fore` |
| `F:\BackUp_PHD\Fore\MOD_PHD_BACKUP_TOOLS.fore:866,890` | `Report: IPrxReport;` … `Report := ObjDesc.Bind As IPrxReport;` — the only on-disk example of obtaining an `IPrxReport` in the PHD stand |
| `C:\Users\Manya\Downloads\MOD_PHD_BACKUP_TECH_CONSTANTS.txt` | 25 lines, SQL-command template constants |
| `C:\Users\Manya\Downloads\MOD_PHD_BACKUP_TECH_MAIN.txt` | 7 lines |
| `C:\Users\Manya\Downloads\MOD_PHD_BACKUP_TOOLS.txt` | 450 lines; line 99: `// Поиск объекта репозитория по идентификатору: сперва через пространство имён (ItemByIdNamespace —` |
| `C:\Users\Manya\Downloads\OBJ3318911.fixed.fore` | 528 lines; PHD→SAP OData export; line 29: `C_NAMESPACE_ID = "BA_PHD"; // идентификатор контейнера бизнес-приложения` |

None of these contain `COpenHyperlink`, `WebFormsExt`, `TabExt` or `DimensionExt`.

## A.3 `: WebForm`-derived modules — none on disk

Every `.fore` on disk derives from the **desktop** `Form`, never `WebForm`:

```
F:\Scheduler Tasks\Fore\DeployToolForm.fore        ┐
F:\Scheduler Tasks\Fore\EditorForm.fore            │
F:\Scheduler Tasks\Fore\PlanParamsForm.fore        │  Public Class PlanParamsForm: Form
F:\Scheduler Tasks\Fore\PLANTEXTForm.fore          │
F:\Scheduler Tasks\Fore\ResponsibleForm.fore       │
F:\Scheduler Tasks\Fore\SCHEDULERForm.fore         │
F:\Scheduler Tasks\Fore\UISCREENDEMOForm.fore      │
F:\Scheduler Tasks\Fore\EDITORSPIKEForm.fore       │
F:\Scheduler Tasks\Fore\FOREDITORForm.fore         │
F:\Scheduler Tasks\Fore\UnavailabilityRecordsForm.fore
F:\Scheduler Tasks\DeployTool\DEPLOYTOOL.fore
F:\Scheduler Tasks\MyCodeEditor1\EditorForm.fore   ┘
```

Search results: `': WebForm'` across all six roots → **exactly 1 hit, `backup.txt:4`**.
`WebForm` / `WebReportBox` / `WebDimensionCombo` / `WebCheckBox` / `WebButton` anywhere in
`F:\Scheduler Tasks` → only `IWebForm` in `docs\forsite\online\Online-KeSom__10.md:7430`
(a *Metabase* interface, unrelated to forms).

## A.4 Archives (`7z l`) — no additional sources

| Archive | Contents relevant to this task |
|---|---|
| `F:\Scheduler Tasks\Fore.7z`, `Fore22 unload by deploytool.7z`, `DeployTool.7z`, `DeployToolForm.7z` | same `*.fore`/`*.form.xml` already on disk; no hyperlink helpers |
| `F:\Scheduler Tasks\docs\sql.7z` | 6 PostgreSQL scripts (unavailability / responsible-for-task); no Fore |
| `F:\Scheduler Tasks\AgentService\docs\forsite-online.zip` | the same `Online-*.md` set already present |
| `F:\backup sched\{Fore,Fore15 (from me),qFore,Fore до форматирования}.7z`, `Fore.zip` | older revisions of the scheduler forms only |
| `F:\backup sched\Scheduler Tasks.7z` (1.15 MB) | contains `docs/forsite/**`, `FORELANG.md`, `REFERENCE.md`, `TaskConf/**`, `_extract/**` — all already extracted on disk |

## A.5 Other roots

| Root | Result |
|---|---|
| `F:\Scheduler Tasks` (303 files) | **zero** hits for any stand helper. Contains the offline help (`docs\forsite`), `REFERENCE.md` (440 KB), `FORELANG.md`, `tools\fore-lint-check.js`, `fore-refs-check.js`, `fore-spec.js`, `fore-ui-spec-check.js` — none mention `TabExt`/`WebFormsExt`/`DimensionExt` |
| `F:\BackUp_PHD` (147 files) | **zero** hits for the helpers; only `MOD_PHD_STDDIM_BACKUP` references (A.1) |
| `F:\backup sched` (5 982 files) | **zero** hits. Notably contains `OldDocumentsForsite\` — the raw CHM extraction (`Fore`, `Fore — копия`, `KeFore — копия`, `KeReport`, `KeSom`, `KnowledgeBase`, `Report`, `TabSheet`; 5 287 `.htm`) that the `docs\forsite\*.md` mirrors were built from |
| `F:\Export button Forsite` (19 files) | **zero** hits for the helpers. `Description technical task (expanded).md` (70 KB) and `REFERENCE.md` discuss `IPrxReport`, `IPrxReportExporter`, report export — no hyperlinks |
| `F:\testt` (24 610 files) | **zero** hits. It is a text2sql ML dataset (`.h`, `.py`, `.pyc`, `.dll`, `.cuh`, `.f90`) — no Fore at all |
| `C:\Users\Manya\Downloads` (4 539 files) | **only** `backup.txt` (the form) + the `MOD_PHD_BACKUP_*` / `OBJ3318911` PHD modules (A.2) |

## A.6 Authoritative negative check — `api-index.txt`

`F:\Scheduler Tasks\docs\forsite\api-index.txt` is a machine-generated index of every
assembly / type / member in the offline help (assemblies present: `Collections Dal Db ExtCtrls Fore
Forms IO Metabase Net Reports Ui`). Substring counts:

```
TabExt                    hits=0        COpenHyperlink             hits=0
DimensionExt              hits=0        OpenHyperlink              hits=0
WebFormsExt               hits=0        GetDimSelectionAttrValue   hits=0
                                        SetTabHyperlink            hits=0
```

Every `*Hyperlink*` identifier that *does* exist in the help is:
`ITabHyperlink`, `ITabHyperlinkClickBaseEventArgs`, `ITabHyperlinkClickEventArgs`,
`TabHyperlinkActionType`, `TabHyperlinkClickBaseEventArgs`, `TabHyperlinkClickEventArgs`,
`TabHyperlinkObjectType`, `TabHyperlinkTarget`, `ITabCellStyle.Hyperlink`,
`ReportHyperlinkClickEventArgs`, `IReportHyperlinkClickEventArgs`,
`OnHyperlinkClick`, `OnHyperlinkClickIReportBoxEventsDelegate`,
`OnHyperlinkClickITabSheetBoxEventsDelegate`, `TabSheetBoxOnHyperlinkClick`,
`ITabView.EmulateHyperlinkClick`, `ITabView.EnableHyperlinks`, `ITabPageSettings.PrintHyperlinks`,
`IPrxReportOptions.HyperlinkFont`, `IPrxReportOptions.SetDefaultHyperlinkFont`,
`IPrxReportExporter.ExportHyperlinkOpenURLAction`.
There is **no** `COpenHyperlink`, `CUrlHyperlink`, `WebFormsExt`, `TabExt` or `DimensionExt` name
in that list — this is a definitive "not on disk, not in help" for those four.

---

# PART B — Platform facts from the offline help

Sources are under `F:\Scheduler Tasks\docs\forsite\` (built from the extracted CHM
`F:\backup sched\OldDocumentsForsite\`). Citations are `file:line` relative to that folder.

## B.1 `ITabHyperlink` and `TabHyperlinkActionType`

### The interface — `TabSheet__Interface.md:10436`

```
## ITabHyperlink
ITabHyperlink
Описание
Интерфейс  ITabHyperlink  определяет
параметры гиперссылки в ячейке.
Свойства
... Action ... ActionType ... Active ... Color ... Enable ...
    SeparateLinkText ... Target ... Text ... Underline ... UseGlobalSettings
Методы
... Apply ... Assign ... Equal
Интерфейсы сборки Tab
```
(`TabSheet__Interface.md:10436-10515`)

| Member | Syntax | Citation + quote |
|---|---|---|
| `Action` | `Action: String;` | `TabSheet__Interface.md:10140,10144,10146` — «Свойство **Action** определяет действие, производимое при срабатывании гиперссылки.» |
| `ActionType` | `ActionType: TabHyperlinkActionType;` | `TabSheet__Interface.md:10265,10269,10271` — «определяет тип действия, выполняемого при щелчке по гиперссылке» |
| `Active` | `Active: TriState;` | `TabSheet__Interface.md:10298,10302,10307` — по умолчанию `TriState.OffOption` |
| `Apply` | `Apply(Value: ITabHyperlink);` | `TabSheet__Interface.md:10314,10318,10322` — «применяет параметры указанной гиперссылки к текущей» |
| `Assign` | `Assign(Value: ITabHyperlink);` | `TabSheet__Interface.md:10351,10355,10359` |
| `Color` | `Color: IGxColor;` | `TabSheet__Interface.md:10367,10371,10373` |
| `Enable` | `Enable: TriState;` | `TabSheet__Interface.md:10395,10399,10401` — «будет ли текст ячейки рассматриваться как гиперссылка» |
| `Equal` | `Equal(Value: ITabHyperlink): Boolean;` | `TabSheet__Interface.md:10426,10430,10434` |
| `SeparateLinkText` | `SeparateLinkText: TriState;` | `TabSheet__Interface.md:10517,10521,10523` — «определяет использование отдельного текста для гиперссылки. Используется вместе со свойством `ITabHyperlink.Text`» |
| `Target` | `Target: TabHyperlinkTarget;` | `TabSheet__Interface.md:10548,10552,10554` |
| `Text` | `Text: String;` | `TabSheet__Interface.md:10599,10603,10605` |
| `Underline` | `Underline: TriState;` | `TabSheet__Interface.md:10630,10634,10636` |
| `UseGlobalSettings` | `UseGlobalSettings: TriState;` | `TabSheet__Interface.md:10678,10682,10684` |

Canonical online version of the same page: `online/Online-TabSheet__12.md:2798` (`ITabHyperlink`),
`:2499` (`Action`), `:2620` (`ActionType`), `:2633` (`Active`), `:2651` (`Apply`), `:2696` (`Assign`),
`:2718` (`Color`), `:2750` (`Enable`), `:2786` (`Equal`), `:2881` (`SeparateLinkText`),
`:2918` (`Target`), `:2970` (`Text`), `:3006` (`Underline`), `:3048` (`UseGlobalSettings`).

**Important:** there is no member named `tst`, `DesingCell`, `ParamManager`, `InitObject`,
`SetParamValue`, `SetParamValueFromSelection` or `Generate` on `ITabHyperlink`. Those belong to the
missing `COpenHyperlink`.

### `TabHyperlinkActionType` — `TabSheet__Enums.md:1698`

```
## TabHyperlinkActionType
Перечисление  TabHyperlinkActionType
содержит типы действий, выполняемого при щелчке по гиперссылке.
Используется следующими свойствами и методами:
ITabHyperlink.ActionType ;
IPrxDimensionDrill.ActionType ;
IEaxDrillSettings.ActionType .
Возможные значения
-1 | None . Не определено.
1  | OpenFile . Открыть файл.
2  | OpenURL . Открыть ссылку.
3  | GoToSheet . Открыть лист отчета.
4  | ShowRange . Показать диапазон ячеек.
5  | ShowObject . Показать объект в центре экрана.
6  | OpenObject . Открыть объект репозитория.          ← TabSheet__Enums.md:1727
7  | RunMacros . Выполнить процедуру/функцию.
```
(`TabSheet__Enums.md:1698-1731`; online mirror `online/Online-TabSheet__11.md:4087`, `OpenObject` at `:4116`.)

Note the numeric value: **`OpenObject = 6`**, and `-1 = None`.

Related enums: `TabHyperlinkObjectType` (`TabSheet__Enums.md:1646`, values `0 Text`, `1 Picture`),
`TabHyperlinkTarget` (`TabSheet__Enums.md:1662`, values `-1 Undefined`, `0 Blank` (default),
`1 Self`, `2 Parent`, `3 Top`; commented at `:1693` that targets are ignored for input-form tables).

### `ITabCellStyle.Hyperlink`

Section `TabSheet__Interface.md:3898` (`## ITabCellStyle.Hyperlink`), also listed in the class doc
`TabSheet__Class.md:1635`: «Свойство `Hyperlink` … `ITabHyperlink`». Usage pattern
(`TabSheet__Interface.md:10253-10256`):

```fore
Tab := Rep.ActiveSheet.Table;
Range := Tab.Cell(0, 0);
Hyperlink := Range.Style.Hyperlink;
Hyperlink.Action := "=Лист2";
```

## B.2 `TabExt` extender — NOT DOCUMENTED

| Query | Result |
|---|---|
| `TabExt` in all `*.md` under `docs\forsite` | **0 matches** |
| `DimensionExt` | **0 matches** |
| `WebFormsExt` | **0 matches** |
| `\bРасширител` (Russian "extender") | **0 matches** |
| `Extender` / `расширител` | only `IMetabaseCustomExtender` — a *repository custom-class* extender (`KeSom__Interface.md:18226`, `KeSom__Examples.md:23-82`, `KeSom__Enums.md:2594` `CustomExtender . Пользовательские…`), and `IMetabaseCustomObject.Extender` (`KeSom__Interface.md:19547`). **This is a different concept** and has nothing to do with `TabExt`/`DimensionExt` |

There is **no topic, class, or general description of "расширители" (property/method extenders such
as `TabExt`, `DimensionExt`, `WebFormsExt`) anywhere in the offline help.** Assembly list in
`docs\forsite\README.md` / `TOPICS.md` covers: `Fore, KeFore, KeReport, KeSom, KnowledgeBase, Report,
TabSheet` (+ online mirrors: Dal, dhtmlReport, KeABAC, KeBISearch, KeCubes, KeDb, kedims, KeDt, KeEtl,
KeExpress, KeExtCtrls, KeMs, KePivot, KePython, KeRds, ModCollections, ModDrawing, ModForms, ModIo,
ModNet, UiLib, ForeSys, KnowledgeBase).
`online/Online-ModForms.md` is the *desktop* `Form` assembly (TOC at `:48-8472`: `IButton`,
`ICheckBox`, `IComboBox`, `ITreeList`, …) — no web form components, no extenders.

**Consequence for the review:** `TabExt.SetTabHyperlink(...)` and
`WebFormsExt.GetDimSelectionAttrValue(...)` cannot be validated against the help. They must be
either (a) stand-local modules in namespace `AppNs.PHD` that were not in any of the searched roots,
or (b) a newer/extended API. `TabExt.SetTabHyperlink(cell, text, actionType, action, flag)` is a
5-argument convenience wrapper whose documented equivalent is written by hand in
`backup.txt:1526-1542` using `ITabRange.Style.Hyperlink` + `ITabHyperlink.ActionType/Action` — i.e.
the same file proves the underlying `ITabHyperlink` API is sufficient and documented.

## B.3 The action string `@OBJECT_ID(PARAM=value;PARAM2=value)` — FULLY DOCUMENTED

This is the single most useful find. **Two documented variants exist.**

### Variant 1 — current online help (10.8), `online/Online-TabSheet__12.md:2534-2548`

```
Открыть объект репозитория |
Идентификатор объекта с префиксом '@', например: "@STD_DIM". |
Открыть объект репозитория с передачей параметров |
Идентификатор объекта с префиксом '@' и список значений параметров.
Параметры объекта передаются в круглых скобках в виде конструкции
<идентификатор параметра>=<значение параметра> и отделяются
друг от друга точкой с запятой. Параметр может принимать единичное
или множественное значение. Множественное значение указывается
в квадратных скобках в виде массива.
Пример единичных значений параметров:
"@STD_DIM(P_STRING=a;P_INT=1;P_FLOAT=0.01;P_DATE=09.02.2021 00:00:00)"
Пример множественных значений параметров:
"@STD_DIM(P_STRING=[a,b];P_INT=[1,2];P_FLOAT=[0.01,0.02];P_DATE=[09.02.2021
00:00:00,10.02.2021 00:00:00])"
```

### Variant 2 — offline CHM (9.9), `TabSheet__Interface.md:10167-10180`

```
Открытие объекта репозитория | "@Dim" | Будет открыт объект с идентификатором «Dim».
Открытие объекта репозитория с передачей параметров |
"@Dim(STRING=a;INT=1;FLOAT=0.01;DATE=09.02.2021 00:00:00)" |
Будет открыт объект с идентификатором «Dim» и указанными параметрами.
Параметры объекта передаются в круглых скобках
в виде конструкции <идентификатор параметра>=<значение
параметра> и отделяются друг от друга точкой с запятой. Значение
параметра может принимать единичное и множественное значение.
Множественное значение указывается в квадратных скобках в виде
массива: "@Dim(STRING=[q,e];INT=[1,2];FLOAT=[0.01,0.02];DATE=[09.02.2021
00:00:00,10.02.2021 00:00:00])"
```

### Macro-call variant of the same property

* Offline (`TabSheet__Interface.md:10181-10241`): `<идентификатор модуля/формы>.<наименование макроса>`
  or `<идентификатор сборки>.<наименование макроса>`, e.g. `<OBJ3331.MyFunc>`; JS variant
  `<alert("Функция JavaScript")>`; «В модулях/формах репозитория реализация пользовательских
  макросов должна производиться в глобальном пространстве имен (Global Scope).»
* Online (`online/Online-TabSheet__12.md:2562-2580`) — **prefixes are mandatory**:
  «для вызова Fore-функции: `fore:<идентификатор модуля/формы/сборки.наименование метода>`;
  для вызова JS-функции: `javascript:<наименование функции (пользовательские параметры, args)>`.
  Префиксы fore/javascript и угловые скобки являются обязательными.» Examples:
  `"fore:<M_MODULE.TestFunction>"`, `"javascript:<TestJSFunction()>"`.
  Also `:2577`: «Выполняемые методы/функции могут иметь параметры … `"fore:<M_MODULE.TestParamFunction(100, "A")>"`».
  Desktop vs web: «при работе в настольном приложении по гиперссылке выполняется Fore-функция;
  при работе в веб-приложении по гиперссылке выполняется JS-функция» (`:2554-2558`).

### Report drill-down copy of the same table — `KeReport__Interface.md:13520-13559`

```
в свойстве Action указывается одно из следующих значений:
Открытие файла зарегистрированным приложением | "C:\Image.jpg"
Открытие адреса URL в браузере                 | "http://www.example.com"
Переход на лист отчета                          | "=Лист2"
Позиционирование на диапазон ячеек              | "=a0:b3;d0:f3"
Позиционирование объекта в центре экрана        | "#Лист2!PrxChart1"
Открытие объекта навигатора                     | "@Dim"            ← KeReport__Interface.md:13550-13553
Выполнение макроса                              | "MOD_FUNCTION.TestFunction"
```
(`IPrxDimensionDrill.Action`, used with `IPrxDimensionDrill.ActionType: TabHyperlinkActionType` — `KeReport__Interface.md:13564-13571`.)

### `pp.prx` / `PP.Prx` / `dhtmlReport`

`online/Online-dhtmlReport.md` is the **web-client namespace for regular reports**:

```
File: online/Online-dhtmlReport.md:3      > Source: https://help.fsight.ru/10.8/ru/mergedProjects/dhtmlReport/
File: online/Online-dhtmlReport.md:10-12  PP.Prx / Описание / Пространство имен содержит классы для работы с регламентным отчетом.
File: online/Online-dhtmlReport.md:18-36  Classes: Control, DimControl, PrxMdService, Report,
                                          TableDataSource; Enums: ControlType, Property
```
Fetched from `.../mergedProjects/dhtmlReport/classes/pp.prx.htm` (`online/_log-urls-extra2.txt:1`).
It is a **JavaScript client-side** namespace (`PP.Prx.Report` etc.) — it does **not** document the
`@ID(params)` Fore action string; that is documented only in the `TabSheet` / `KeReport` help above.
Report **parameters** as first-class objects do exist as `IPrxOpenObjectParam`,
`IPrxOpenObjectParams`, `IPrxOpenObjectParamControl`, `IPrxOpenObjectConstantParamControl`,
`IPrxOpenObjectDimAttributeParamControl`, `IPrxOpenObjectReportParamControl`,
`IPrxUserButtonActionOpenObject` (`online/Online-kereport__05.md:9077-9103`, `:9390-9392`;
enums `PrxOpenObjectParamType`, `PrxOpenObjectSelectionType` at `online/Online-kereport__02.md:9988-9993`),
but the *string* form of the hyperlink action is only the `@…(…)` syntax quoted above.

**Matches the form exactly:** `backup.txt:434-435` sets
`link.ActionType := TabHyperlinkActionType.OpenObject;` and
`link.Action := "@PRX_ANALYSIS_TEP(PLANT=6500;CALYEAR=2026;ZLIB_INDC=IND00005000)"`
— precisely Variant 1/Variant 2 syntax, with the report id `PRX_ANALYSIS_TEP` as the object id.
The form's own hand-rolled string editor (`backup.txt:1400-1518`) builds exactly this grammar
(`(` insertion at 1497, `;` separator at 1411, `)` terminator scan at 1421/1440, `[a,b]` array form
at 1483-1488) — so it is writing a documented format.

## B.4 `IDimSelection` and the Dimensions interfaces

`online/Online-kedims.md:315` — «Интерфейс **IDimSelection** используется для работы с отметкой
справочника.» (Assembly: Dimensions; hierarchy `IDimSelection` → itself; thread-unsafe, `:335-340`.)

Requested members — all present in the summary table:

| Member | Citation | Quote |
|---|---|---|
| `ToVariant` | `online/Online-kedims.md:585-587` | «Метод **ToVariant** формирует значение отметки по значениям атрибута Идентификатор.» |
| `MultiSelect` | `online/Online-kedims.md:403-406` | «Свойство **MultiSelect** определяет, есть ли возможность выделения более одного элемента в отметке.» |
| `SelectedCount` | `online/Online-kedims.md:413-415` | «Свойство **SelectedCount** возвращает количество элементов в отметке.» |
| `AttributeToVariant` | `online/Online-kedims.md:439-441` | «Метод **AttributeToVariant** формирует значение отметки по значениям указанного атрибута элементов.» (variant OI at `:443-446`) |
| `Dimension` | `online/Online-kedims.md:370-372` | «Свойство **Dimension** возвращает объект, содержащий элементы справочника.» |
| `SelectElement` | `online/Online-kedims.md:562-564` | «Метод **SelectElement** осуществляет добавление элемента в отметку.» (also `SelectElementWithoutExcep` `:566`, `IsElementSelected` `:517`, `DeselectAll` `:471`, `SelectAll` `:549`) |
| `ToString` | `online/Online-kedims.md:580-583` | «Метод **ToString** формирует значение отметки в строковом виде в соответствии с установленными параметрами.» |

Other useful members: `Element` (`:374`), `FirstDimElement`/`LastDimElement` (`:383`, `:399`),
`SelectedElementArray` (`:417`), `Iterator` (`:395`), `CreateCopy` (`:467`), `CopyTo` (`:457`),
`ExternalSave`/`ExternalLoad` (`:488-494`), `ParseAttribute` (`:535`), `SelectAttributeRange` (`:553`).
`IDimSelectionSet` follows at `online/Online-kedims.md:591`.

### `IDimElements` — `online/Online-kedims.md:11`

```
Интерфейс  IDimElements  содержит свойства и методы коллекции элементов справочника.
...
Elements := DimInst.Elements;
Iterator := Elements.Iterator;
While  Iterator.Next  Do
//... Работа с элементами
End   While ;
```
(`online/Online-kedims.md:11-39`; `AttributeValue` at `:50` — «возвращает значение атрибута
элемента по индексам элемента и атрибута», `AttributeValueO` at `:54`.)

### `IDimInstance` — `online/Online-kedims.md:164`

`IDimInstance` follows at `:164`; its `Attributes` collection yields `IDimAttributesInstance`,
whose `Item(idx)` is an `IDimAttributeInstance`.

### `IDimAttributeInstance` — **summary only, no member page**

`online/Online-kedims__ifaces.md:185-187`:
«**IDimAttributeInstance** — Интерфейс `IDimAttributeInstance` содержит свойства и методы для
работы со значениями атрибута справочника.»
Listed with `IDimElementArray` (`:279-280`), `IDimElements` (`:291-292`), `IDimIterator`
(`:374-375`), `IDimAttributesInstance` (`:198-200`), `IDimAttributeInstanceValuesLoader` (`:202`).
There is **no `## IDimAttributeInstance`, `## IDimElementArray` or `## IDimIterator` topic** in the
offline set (grep for those headers → 0 matches; only `## IDimElements` `:11` and
`## IDimInstance` `:164` exist in `online/Online-kedims.md`).

**`LookupDisplayValue` — 0 matches in all `*.md`.** It is undocumented in this help set. What *is*
documented, and is what the missing `DimensionExt` helpers are thin wrappers over, is the
`KnowledgeBase` recipe:

```fore
DimInstance := DimensionTree1.Dimension.DimInstance;
Attribute := DimInstance.Attributes.FindById("NAME");
SelectedElements := DimensionTree1.Selection.SelectedElementArray(NULL);
ElementCount := SelectedElements.Count - 1;
For ElementIndex := 0 To ElementCount Do
    DimensionElement := SelectedElements.Element(ElementIndex);
    Memo1.Lines.Add(Attribute.Value(DimensionElement) As String);
End For;
```
(`KnowledgeBase__01_Fore.md:1915-1933`; identical online at `online/Online-KnowledgeBase.md:2158` region,
section «Получение значений указанных атрибутов для отмеченных элементов справочника» `:1904`.)

```fore
AtIndex := 1;
AtValue := "Пятый элемент";
DimInstance := DimensionTree1.Dimension.DimInstance;
Attributes := DimInstance.Attributes;
DimensionElement := Attributes.Item(AtIndex).LookupValue(AtValue);
Memo1.Lines.Add(DimensionElement.ToString);
```
(`KnowledgeBase__01_Fore.md:1945-1963`, section «Получение индекса элемента по указанному значению его
атрибута» `:1934`; note `:1963` «Вместо `Item(AtIndex)` можно использовать `FindById("NAME")`».)
**This is exactly `DimensionExt.GetElementIndexByAttributeValue` / `GetAttributeValueByElementIndex`.**

## B.5 `IStringList` and `StringList`

`online/Online-ModCollections.md:796-805`:
«Интерфейс **IStringList** содержит свойства и методы для работы с динамическим массивом строк.
Иерархия наследования: `IEnumerable` → `ICollection` → `IStringList`».

| Member | Citation | Quote |
|---|---|---|
| `Add` | `online/Online-ModCollections.md:841-844` | «Метод **Add** добавляет новый элемент с указанным значением в конец массива и возвращает его индекс.» |
| `Remove` | `online/Online-ModCollections.md:910-912` | «Метод **Remove** осуществляет удаление элемента с указанным значением.» (`RemoveAt` `:914`, `RemoveRange` `:918`) |
| `Text` | `online/Online-ModCollections.md:824-827` | «Свойство **Text** определяет массив как текстовую строку, используя разделитель, передаваемый в качестве входного параметра.» |
| `Clear` | `online/Online-ModCollections.md:858-860` | «Метод **Clear** осуществляет очистку массива.» |
| `Count` | `online/Online-ModCollections.md:833-835` | «возвращает количество элементов в массиве» (inherited from `ICollection`) |
| `AsString` | `online/Online-ModCollections.md:811-814` | carriage-return separated |
| `Item`, `ItemLength` | `:816`, `:820` | |
| `AddRange`, `Insert`, `IndexOf`, `Sort`, `ToArray`, `Contains`, `Clone`, `CopyFrom`, `GetRange`, `Reverse` | `:846`–`:940` | |

Class instantiation — `online/Online-ModCollections.md:379`:
```fore
StrList: IStringList;
...
StrList := New StringList.Create;      // line 379
StrList.Add("Один");                   // 380
StrList.Add("Два");
StrList.Add("Три");
```

**Matches the form:** `backup.txt:2` `fieldList: IStringList;`, `:338`
`fieldList := New StringList.Create;`, `:1556` `fieldList.Add(fieldName);`, `:1558`
`fieldList.Remove(fieldName);`, `:1560` `fieldList.Text(", ")`. All five usages are documented and
type-correct. Note `fieldList` is declared at **module scope** (`Var` before the class, `:1-2`),
not as a class field — legal, and visible inside the class methods.

## B.6 `IPrxReport` and `IReportBox.Report`

### `IPrxReport` — `KeReport__Interface.md:17216`

```
## IPrxReport
IPrxReport
Сборка : Report;
Описание
Интерфейс  IPrxReport  содержит свойства и методы объекта репозитория «Регламентный отчёт».
Иерархия наследования
IPrxReport
Комментарии
Для доступа к активному регламентному отчету используйте свойство  IPrxReportClass.ActiveReport.
```
(`KeReport__Interface.md:17216-17227`)

Key members (TOC, `KeReport__Interface.md`): `ActiveSheet` `:16706`/`:17233`,
`Sheets` `:17975`, `Controls` `:16872`, `DataArea` `:16991`, `DataIslands` `:17005`,
`DataSources` `:17030`, `Options` `:17639`, `Recalc` `:17728`, `ParseCell` `:17662`,
`ParseRange` `:17695`, `LoadFromFile` `:17498`, `SaveToFile` `:17866`, `MetabaseObject` `:17586`.
Note `## IPrxReport.ActiveSheet` at `:16706` and the pattern
`Tab := Rep.ActiveSheet.Table;` / `Tab := (Rep.ActiveSheet As IprxTable).TabSheet;`
(`TabSheet__Interface.md:10253`, `:10286`). `IReportBox.Report` is `IUiReport`
(see below), so `ReportBoxOk.Report.ActiveSheet` is an `IPrxSheet` — the form's
`ReportBoxOk.Report.ActiveSheet As ITabSheet` casts (`backup.txt:409,428`) mirror
`(Rep.ActiveSheet As IprxTable).TabSheet` from the docs.

### `IReportBox.Report` — `KeReport__Interface.md:34241`

```
## IReportBox.Report
Синтаксис
Report:  IUiReport ;
Описание
Свойство  Report  определяет компонент UiReport, который будет использоваться как источник данных.
Пример
ReportBox1.Report := UiReport1;              // lines 34253-34254
```
(`KeReport__Interface.md:34241-34259`; TOC `:33986` `IReportBox`, `:34241` `IReportBox.Report`.)

So the declared type of `Report` is **`IUiReport`** (Reports assembly, `api-index.txt` row
`Reports  IUiReport  interface  Report`), **not** `IPrxReport`. This matters for the form:
`backup.txt:328` passes `ReportBoxOk.Report` to `COpenHyperlink.Create(...)` (whose first parameter
is documented nowhere), and `backup.txt:1520` declares
`Function InitializeHlinkOpenObject(report: IPrxReport; ...)`. Passing a `WebReportBox.Report`
(web counterpart of `IReportBox.Report`) where `IPrxReport` is expected is a **type-compatibility
question that cannot be answered from this help set** — `IUiReport`'s relation to `IPrxReport` is
not stated in the offline docs, and `WebReportBox` is not documented at all.

### Opening a report with parameters

The offline set does **not** contain an `IPrxReport`-with-parameters *opening* recipe in the searched
topics. What it does contain:
* the hyperlink action-string route (`@ID(PARAM=value;…)`, B.3) — the documented way to open a report
  with parameters from a form/report hyperlink;
* `IPrxOpenObjectParam` / `IPrxOpenObjectParams` / `IPrxUserButtonActionOpenObject`
  (`online/Online-kereport__05.md:9077-9103`, `:9390-9392`) — «Интерфейс `IPrxUserButtonActionOpenObject`
  предназначен для настройки открытия объекта репозитория в качестве обработчика пользовательской кнопки»;
* the PHD-stand's own on-disk example `F:\BackUp_PHD\Fore\MOD_PHD_BACKUP_TOOLS.fore:866,890`
  (`Report := ObjDesc.Bind As IPrxReport;`) — bind, not open-with-params.

## B.7 Fore language rules relevant to reviewing this code

Source of truth: `F:\Scheduler Tasks\FORELANG.md` (§§5, 11, 19) and
`F:\Scheduler Tasks\docs\forsite\Fore-Language__06_SyntRules.md`,
`Fore-Language__11_Compiler_Errors.md`, `online/Online-Fore.md`.

### (a) Declaration form of `Sub` / `Function`

```
Sub <Наименование>[(<формальные параметры>)];
Begin
End Sub <Наименование>;
Function <Наименование>[(<формальные параметры>)]: <тип значения>
Begin
Return <значение>
End Function <Наименование>;
```
(`Fore-Language__06_SyntRules.md:736-750`)

### (b) Nested `Sub`/`Function` inside a procedure body — **EXPLICITLY LEGAL**

```
Все константы, переменные, процедуры/функции, описанные в теле процедуры
или функции, являются локальными для неё.
```
(`Fore-Language__06_SyntRules.md:751-752`)

```
В добавление к локально определенным объектам и формальным параметрам,
объекты, определенные во внешнем для процедуры/функции блоке, также видны
внутри тела, за исключением тех объектов, которые имеют те же идентификаторы,
что и локальные объекты и параметры процедуры/функции.
Использование идентификатора процедуры/функции внутри её тела приведет
к её рекурсивному вызову.
Предварительное описание процедур/функций отсутствует. Любая процедура/функция
может быть вызвана, если её описание находится в текущем блоке кода, или
в одном из объемлющих блоков кода.
```
(`Fore-Language__06_SyntRules.md:753-761`)

**Conclusion for the review:** `Sub InsertParam` / `Sub UpdateParam` / `Sub RemoveParam` /
`Function GetParamIndex` / `Sub UpdateArrayToValue` declared between the `Var` block and `Begin` of
`Sub UpdateOpenDefHlink` (`backup.txt:1405-1490`) are **legal**, are local to
`UpdateOpenDefHlink`, and are correctly called from its body. Two caveats from the same passage:
1. Declaration order matters only in that a local hides an outer identifier of the same name
   (`:753-756`) — none of the five names shadows anything here.
2. Recursion: naming a nested sub and then calling that name from inside its own body recurses
   (`:757-758`). None of the five does that.

The examples in the help show the same layout — `Sub Main;` with the nested
`Sub SimpleSub(a, b: Integer; var c: Integer);` / `Function SimpleFunc(a, b: Integer): Double;`
declared before `Var`/`Begin` (`Fore-Language__06_SyntRules.md:764-789`).

### (c) Default (optional) parameter values — **LEGAL for by-value parameters, at the end of the list**

```
Формальный параметр, передаваемый по значению, может быть необязательным.
Параметр считается необязательным, если для него определено значение по
умолчанию. Все необязательные параметры должны обязательно следовать в
конце списка параметров. Значение по умолчанию не может быть присвоено
списку параметров.
```
(`Fore-Language__06_SyntRules.md:408-412`)

```
Sub MyProc(a: Integer; Var b: String; c: String = "a");   // :448
```
(`Fore-Language__06_SyntRules.md:444-452`; same example in `FORELANG.md:260-264`.)
Positional vs named calling: `Fore-Language__06_SyntRules.md:426-443` — «При этом не допускается
пропуск параметров», «Позиционные параметры могут быть совмещены с именованными, но указание
позиционных параметров после именованных недопустимо». `FORELANG.md:254`:
«Необязательные параметры (со значением по умолчанию) идут **в конце** списка.»

**Conclusion:** `Sub UpdateOpenDefHlinkFromSelection(paramId: String; dimSel: IDimSelection;
attrId: String = "")` (`backup.txt:1392`) is **legal** — `attrId` is by value, optional, and last.

Compiler error that delimits this (`Fore-Language__11_Compiler_Errors.md:67`, `:1824`):
```
1824  Параметр, передаваемый по ссылке, не может иметь значения по умолчанию
```
(`FORELANG.md:549` lists the same wording.) So `Var x: String = "…"` would be an error; a plain
by-value default is not.

### (d) Is a `Sub` allowed to have the same name as its enclosing class? — **NOT ADDRESSED ANYWHERE**

Every relevant search came back empty:

| Query (all `*.md` in `F:\Scheduler Tasks`) | Result |
|---|---|
| `совпадает с именем` / `совпадать с именем` / `одноимен` / `одноимён` / `именем класса` | 0 matches (only `KeSom__Interface.md:50222` «ProcedureName — физическое имя процедуры в БД», unrelated) |
| any rule that a class member's identifier must differ from the class identifier | **none** |
| any sample with `Class X … Sub X;` | **none** |

What *is* documented, and is the closest thing to a rule:

* The module/scope rule for duplicate identifiers — `Fore-Language__11_Compiler_Errors.md:1844-1851`
  (mirror `online/Online-Fore.md:5005-5024`):
  ```
  Повторное определение идентификатора
  Описание
  В рамках одного пространства имен присутствует более одного описания
  типа (члена типа) с одинаковым идентификатором.
  Способ устранения
  Удалите или измените все дублирующиеся идентификаторы.
  ```
  This constrains **two declarations in the same namespace**, and the worked example is a `Const i`
  plus a `Var i` inside one `Sub` (`:1853-1863`). A class name lives in the enclosing namespace and a
  method name lives in the class's member namespace, so this rule does not, on its written terms,
  prohibit `Class X` + `Sub X`. **But the help never states this either way** — treat "same name as
  the enclosing class" as **undocumented**, and verify with the compiler.
* The documented *form* event-handler naming convention is `<FormName>On<Event>(Sender, Args)`:
  `Sub TestFormOnShow(Sender: Object; Args: IEventArgs);` (`KeReport__Samples.md:42`,
  `KnowledgeBase__01_Fore.md:1391`, `KeReport__Interface.md:4102` `Sub OBJ1FormOnShow(...)`,
  `:5186` `Sub OBJ46841FormOnShow(...)`; the online `OnShow` event itself at
  `online/Online-ModForms.md:995-997`). So `ANALIZ_TEP_FORM_ON_SHOW` (`backup.txt:392`) is **not**
  the form's `OnShow` handler — it takes no parameters and does not carry the `OnShow` suffix;
  as written it is a plain method that happens to share the class's identifier.
* Scoping/member-visibility facts that do apply: «**По умолчанию класс — `Private`.**»
  (`FORELANG.md:119`) and the member-access modifiers table
  (`Fore-Language__06_SyntRules.md:793-846`). `Class ANALIZ_TEP_FORM_ON_SHOW` at `backup.txt:4`
  carries **no** access specifier.

### (e) Compiler errors that this file will actually hit

| Code | Message | Citation | Why it applies |
|---|---|---|---|
| 1337 | `Неизвестный идентификатор <идентификатор>` | `Fore-Language__11_Compiler_Errors.md:44`, `:1337`; `online/Online-Fore.md:4456` | `COpenHyperlink`, `WebFormsExt`, `TabExt`, `DimensionExt`, `AppNs`, `WebForm`, `IWebCheckBox` are not resolvable unless the stand supplies them |
| 2602 | `Недоступно для использования в веб` | `Fore-Language__11_Compiler_Errors.md:104`, `:2602`; `online/Online-Fore.md:5827-5838` — «При разработке веб-приложения была попытка использования ресурсов, запрещенных для использования в веб» | This is a **web** form; any desktop-only resource in it will trip this. Note the help's own warning at `online/Online-TabSheet__12.md:2559-2561`: «Если указана только JS-функция, то гиперссылка будет работать только в веб-приложении. Если указан только Fore-метод, то гиперссылка будет работать и в настольном приложении, и в веб-приложении» |
| 1844 | `Повторное определение идентификатора` | `Fore-Language__11_Compiler_Errors.md:68`, `:1844-1851` | only if `ANALIZ_TEP_FORM_ON_SHOW` (Sub) collides with `ANALIZ_TEP_FORM_ON_SHOW` (Class) in the compiler's model — undocumented, see (d) |
| 1824 | `Параметр, передаваемый по ссылке, не может иметь значения по умолчанию` | `Fore-Language__11_Compiler_Errors.md:67`, `:1824` | **not** triggered — `attrId: String = ""` is by value |
| 2353 | `Ожидается определение метода, поля или свойства класса` | `Fore-Language__11_Compiler_Errors.md:92`, `:2353` | if a class body contains a stray declaration |
| 1061 | `<имяТипа> не является подпрограммой` | `Fore-Language__11_Compiler_Errors.md:33`, `:1061` | e.g. calling `Hyperlink.tst` / `Hyperlink.Generate` if the object resolves to `ITabHyperlink` (which has neither member) |
| 2762 | `Свойство/метод <имяЧлена> является устаревшим` | `Fore-Language__11_Compiler_Errors.md:111` | possible warning for legacy members |
| 2754 | `Переменная/Константа <наименование> не используется` | `Fore-Language__11_Compiler_Errors.md:110` | warning only; the file has many unused `Const C_PARAM_*` and unused `Var`s (e.g. `optionReport`, `MObj`, `openReportTab` at `:394-396`) |

Also relevant, from `FORELANG.md:520-578` (§19, the author's own consolidated list of the same
message texts): `:522` «Неизвестный идентификатор `<идентификатор>`; Повторное определение
идентификатора», `:577` «…Недоступно для использования в веб», `:549` the by-reference default rule.

---

# PART C — Symbols / topics that could NOT be found anywhere

## C.1 Symbols with **no definition on disk and no entry in the offline help**

Verified against all six roots (all listed file types), the 12 archives, and the machine-generated
`F:\Scheduler Tasks\docs\forsite\api-index.txt` (0 substring hits each):

| Symbol | Searched for as | Status |
|---|---|---|
| `COpenHyperlink` | class/identifier, `api-index.txt`, all roots | **NOT FOUND** |
| `COpenHyperlink.Create(report, appNs, text)` | member | **NOT FOUND** |
| `COpenHyperlink.InitObject(id)` | member | **NOT FOUND** |
| `COpenHyperlink.SetParamValue(id, value)` | member | **NOT FOUND** |
| `COpenHyperlink.SetParamValueFromSelection(id, sel, attr)` | member | **NOT FOUND** |
| `COpenHyperlink.Generate` | member | **NOT FOUND** |
| `COpenHyperlink.Action` | property | **NOT FOUND** |
| `COpenHyperlink.tst` | member | **NOT FOUND** |
| `COpenHyperlink.DesingCell(...)` | member | **NOT FOUND** |
| `COpenHyperlink.ParamManager(.Params.Count)` | member | **NOT FOUND** |
| `CUrlHyperlink` (the name in the comment at `backup.txt:318`) | class | **NOT FOUND** |
| `WebFormsExt` | class/namespace | **NOT FOUND** |
| `WebFormsExt.GetDimSelectionAttrValue(dimSel, attrId)` | member | **NOT FOUND** |
| `TabExt` | class/extender | **NOT FOUND** |
| `TabExt.SetTabHyperlink(cell, text, actionType, action, bool)` | member | **NOT FOUND** |
| `DimensionExt` | class/extender | **NOT FOUND** |
| `DimensionExt.GetElementIndexByAttributeValue(dimInst, attrId, value)` | member | **NOT FOUND** |
| `DimensionExt.GetAttributeValueByElementIndex(dim, attrId, elemIndex)` | member | **NOT FOUND** |
| `DimensionExt.GetAttributeValueByElementId(dim, attrId)` | member | **NOT FOUND** |
| `AppNs` / `AppNs.PHD` (as a namespace) | namespace | **NOT FOUND** — `AppNs.PHD` appears only in `backup.txt:328,628`; note `C_NAMESPACE_ID = "BA_PHD"` in `OBJ3318911.fixed.fore:29` shows the PHD container is `BA_PHD`, not `AppNs.PHD` |
| `ANALIZ_TEP_FORM_ON_SHOW` (as a repository object) | identifier | **NOT FOUND outside `backup.txt`** |
| `PRX_ANALYSIS_TEP` (as a report) | identifier | **NOT FOUND outside `backup.txt:262`** — cannot confirm the report exists or which `C_PARAM_*` it declares |
| `P_FIELD_LIST` (as a report parameter) | identifier | **NOT FOUND outside `backup.txt:1560`** |
| `MOD_PHD_STDDIM_BACKUP` | module | **FOUND** (see A.1) — but it is a table-dimension backup module, unrelated to hyperlinks |
| `: WebForm` subclass in any `.fore` | declaration | **NOT FOUND** — only `backup.txt:4`; every other form on disk is `: Form` |

## C.2 Topics with **no coverage in the offline help**

| Topic | Status |
|---|---|
| `TabExt` extender and the general concept of Fore "расширители" (extenders) | **NO TOPIC EXISTS**. `Extender` in the help means only `IMetabaseCustomExtender` / `IMetabaseCustomObject.Extender` (`KeSom__Interface.md:18226`, `:19547`), an unrelated repository-custom-class feature |
| `DimensionExt`, `WebFormsExt` | **NO TOPIC EXISTS** |
| `WebForm`, `WebReportBox`, `WebDimensionCombo`, `IWebCheckBox`, and any web-form component model | **NO TOPIC EXISTS** in this help set. `online/Online-ModForms.md` is the desktop `Form` assembly only. The single `IWebForm` hit (`online/Online-KeSom__10.md:7430`) is a Metabase interface |
| `IStringList.Text` full member page | summary-table entry only (`online/Online-ModCollections.md:824`); no `## IStringList.Text` topic |
| `## IDimAttributeInstance`, `## IDimAttributeInstance.LookupDisplayValue`, `## IDimElementArray`, `## IDimIterator` | **NO MEMBER PAGES** — only the one-line summaries in `online/Online-kedims__ifaces.md:185,279,374`. `LookupDisplayValue` has **0 matches** anywhere in the help |
| Report "opening with parameters" recipe for `IPrxReport` (as opposed to the hyperlink string) | **NOT FOUND** as such; `IPrxOpenObjectParam(s)` interfaces exist but no end-to-end recipe in the searched topics |
| Rule about a `Sub` sharing its enclosing class's name | **NOT DOCUMENTED** (see B.7(d)) |
| `Hyperlink.SetParamValue` / `SetParamValueFromSelection` / `Generate` on `ITabHyperlink` | **NOT MEMBERS** of `ITabHyperlink` (compare the full member list at `TabSheet__Interface.md:10442-10515` / `api-index.txt`) — these exist only on the missing `COpenHyperlink` |

## C.3 Methodology note / limitations

* The `grep` tool timed out on the whole `F:\` drive; searches were therefore run per-root with
  PowerShell `Select-String` over a fixed extension whitelist, plus the `grep` tool on individual
  directories. `F:\backup sched` (5 982 files) and `F:\testt` were covered by that
  extension-filtered pass.
* Binary/unknown-extension files were not text-searched. Archives were **listed** with
  `C:\Program Files\7-Zip\7z.exe l`, not extracted — their listings show no file that could hold the
  missing helpers.
* `OldDocumentsForsite` (`F:\backup sched\OldDocumentsForsite`, 5 287 `.htm`) is the raw source of
  the `docs\forsite\*.md` mirrors; header names such as `ITabHyperlink.*.htm` were used to confirm
  the mirror's completeness for the TabSheet assembly.
* Nothing outside the session workspace was modified.

## C.4 Practical implication for the code review (one paragraph)

The part of the form that actually works is built on documented API: `ITabRange.Style.Hyperlink`
(`ITabHyperlink`) + `TabHyperlinkActionType.OpenObject` + the `@OBJECT_ID(PARAM=value;PARAM2=value)`
action string — the form writes that string both directly (`backup.txt:435`) and through its own
parser (`backup.txt:1400-1518`). The part that cannot be verified — and that is the only reason the
form would fail to compile — is the thin stand layer: `COpenHyperlink` (a stateful wrapper holding a
param manager, exposing `SetParamValue`, `SetParamValueFromSelection`, `Generate`, `Action`, `tst`,
`DesingCell`, `ParamManager`), `WebFormsExt.GetDimSelectionAttrValue`, `TabExt.SetTabHyperlink` and
`DimensionExt.*`. Two of the four have documented, hand-writable equivalents already present in the
same file (`backup.txt:418-446` replaces `TabExt.SetTabHyperlink`; `KnowledgeBase__01_Fore.md:1915-1963`
replaces `DimensionExt.Get*By*`), so a stand-independent rewrite is feasible without the missing modules.
