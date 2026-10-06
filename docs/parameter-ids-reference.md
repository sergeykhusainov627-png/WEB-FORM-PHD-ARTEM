# Справочник идентификаторов параметров отчёта (из эталонного модуля)

Константы `C_PARAM_*` в модуле формы объявлялись, но в живом коде не использовались —
компилятор Форсайта выдавал по ним предупреждения «Константа ... не используется».
При очистке модуля (tools/cleanup-unused.py) они удалены; список сохранён здесь, чтобы
идентификаторы не потерялись. Актуальная таблица полей — `InitOutputFieldIds` в модуле.

| Константа | Значение | Осталась в модуле |
|---|---|---|
| `C_BUTTON_OK_ID` | `PRX_ANALYZ_TEP_BUTTON_OK` | нет (удалена как неиспользуемая) |
| `C_ANALYZ_TEP_REP_ID` | `PRX_ANALYSIS_TEP` | да |
| `C_PARAM_ZLIB_INDC` | `ZLIB_INDC` | нет (удалена как неиспользуемая) |
| `C_PARAM_PLANT` | `PLANT` | да |
| `C_PARAM_CALYEAR` | `CALYEAR` | да |
| `C_PARAM_ZTYPEIND` | `ZTYPEIND` | да |
| `C_PARAM_P_ANALYTIC_SET` | `P_ANALYTIC_SET` | да |
| `C_PARAM_ZPHD_STAT` | `ZPHD_STAT` | нет (удалена как неиспользуемая) |
| `C_PARAM_VENDOR` | `VENDOR` | нет (удалена как неиспользуемая) |
| `C_PARAM_SOLD_TO` | `SOLD_TO` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZHRGRPMO` | `ZHRGRPMO` | нет (удалена как неиспользуемая) |
| `C_PARAM_PROFIT_CTR` | `PROFIT_CTR` | нет (удалена как неиспользуемая) |
| `C_PARAM_COSTCENTER` | `COSTCENTER` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZORGUNIT` | `ZORGUNIT` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPH_USR2` | `ZPH_USR2` | нет (удалена как неиспользуемая) |
| `C_PARAM_ACTTYPE` | `ACTTYPE` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZEQUI` | `ZEQUI` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZCLSVOBOR` | `ZCLSVOBOR` | нет (удалена как неиспользуемая) |
| `C_PARAM_MATERIAL` | `MATERIAL` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZFUNC_LOC` | `ZFUNC_LOC` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZSIU_FLD` | `ZSIU_FLD` | нет (удалена как неиспользуемая) |
| `C_PARAM_POSID` | `POSID` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZLIB_INFS` | `ZLIB_INFS` | да |
| `C_PARAM_PERIOD_TYPE` | `PERIOD_TYPE` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_DOG` | `ZPHD_DOG` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_USL1` | `ZPHD_USL1` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZDEBITOR` | `ZDEBITOR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPH_ESO2` | `ZPH_ESO2` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_SK` | `ZPHD_SK` | нет (удалена как неиспользуемая) |
| `C_PARAM_UCVOLTLEVL` | `UCVOLTLEVL` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZUCVOLTTR` | `ZUCVOLTTR` | нет (удалена как неиспользуемая) |
| `C_PARAM_Z_CL_NAPR` | `Z_CL_NAPR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZSIU_TY` | `ZSIU_TY` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZDOGLINK` | `ZDOGLINK` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZBUR_LU` | `ZBUR_LU` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZBUR_AREA` | `ZBUR_AREA` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZSKV_KUST` | `ZSKV_KUST` | нет (удалена как неиспользуемая) |
| `C_PARAM_Z_SKV_GEO` | `Z_SKV_GEO` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZBUR_PLST` | `ZBUR_PLST` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPH_TEHK` | `ZPH_TEHK` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPH_OPLST` | `ZPH_OPLST` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPILOT` | `ZPILOT` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZSKV_ST` | `ZSKV_ST` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZGEN_POD` | `ZGEN_POD` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZGEN_ZAK` | `ZGEN_ZAK` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZSHIFR` | `ZSHIFR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZOBJEM` | `ZOBJEM` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_SR` | `ZPHD_SR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_GRSR` | `ZPHD_GRSR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZGAZ_TYPE` | `ZGAZ_TYPE` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZAVIATYPE` | `ZAVIATYPE` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZPHD_SPR` | `ZPHD_SPR` | нет (удалена как неиспользуемая) |
| `C_PARAM_ZBUR_BEG` | `ZBUR_BEG` | да |
| `C_PARAM_ZBUR_END` | `ZBUR_END` | да |
| `C_PARAM_ZPKR_SUBP` | `ZPKR_SUBP` | да |
