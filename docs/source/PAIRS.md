# Связи пар «ключ / наименование» — до источников

Цепочка: поле в `ANALYTIC_SET` → колонка боковика `t1913698` → справочник НСИ (объект) →
физическая таблица `t<ключ>` → поле-ключ в справочнике → поле наименования.

| Поле | Ключ (боковик) | Справочник НСИ | t-таблица | Ключ в справочнике | Наименование |
|---|---|---|---|---|---|
| zphd_pern | `zphd_pern` | — | — | — | (то же поле) |
| sold_to | `sold_to` | `RDSD_SOLDTO` | `t2301822` | `code` | `NAME` |
| vendor | `vendor` | `RDSD_VENDOR` | `t2322857` | `vendor` | `TXTMD` |
| zhrgrpmo | `zhrgrpmo` | `RDSD_ZHRGRPMO` | `t2306331` | `zhrgrpmo` | `NAME` |
| calyear | `calyear` | — | — | — | (то же поле) |
| plant | `plant` | `RDSD_PLANT` | `t2312312` | `plant` | `TXTMD` |
| zlib_infs | `zlib_infs` | `RDSD_INFOSYSTEM` | `t1895288` | `code_value` | `NAME` |
| zbur_lu | `zbur_lu` | `RDSD_ZBUR_LU` | `t2320979` | `code` | `NAME` |
| zsiu_fld | `zsiu_fld` | `RDSD_ZSIU_FLD` | `t2308973` | `zsiu_fld` | `NAME` |
| zkust | `zkust` | — | — | — | (то же поле) |
| z_skv_geo | `z_skv_geo` | — | — | — | (то же поле) |
| zgen_zak | `zgen_zak` | `SHORTCUT_TO_RDSD_SOLDTO_6` | `t2301822` | `code` | `NAME` |
| zphd_vnmr | `zphd_vnmr` | — | — | — | (то же поле) |
| calcty | `calcty` | — | — | — | (то же поле) |
| ztypeind | `ztypeind` | — | — | — | (то же поле) |
| zorgunit | `zorgunit` | — | — | — | (то же поле) |
| period_type | `period_type` | `DIC_TYPE_PERIOD` | `t2317517` | `—` | `NAME` |
| zzdop | `zzdop` | — | — | — | (то же поле) |
| zphd_priz | `zphd_priz` | — | — | — | (то же поле) |
| zregi_mvz | `zregi_mvz` | — | — | — | (то же поле) |
| acttype | `acttype` | `RDSD_ACTTYPE` | `t2320948` | `acttype` | `NAME` |
| material | `material` | `RDSD_MATERIAL` | `t2321329` | `material` | `NAME` |
| zph_usr2 | `zph_usr2` | — | — | — | (то же поле) |
| costcenter | `costcenter` | — | — | — | (то же поле) |
| profit_ctr | `profit_ctr` | `RDSD_PROFIT_CTR` | `t2320954` | `profit_ctr` | `NAME` |
| zphd_is | `zphd_is` | — | — | — | (то же поле) |
| zphd_comm | `zphd_comm` | — | — | — | (то же поле) |
| zphd_phd | `zphd_phd` | — | — | — | (то же поле) |
| zdebitor | `zdebitor` | `SHORTCUT_TO_RDSD_SOLDTO` | `t2301822` | `code` | `NAME` |
| ucvoltlevl | `ucvoltlevl` | `RDSD_UCVOLTLEVL` | `t2307584` | `ucvoltlevl` | `NAME` |
| zaviatype | `zaviatype` | `RDSD_ZAVIATYPE` | `t2307768` | `zaviatype` | `NAME` |
| zucvolttr | `zucvolttr` | `SHORTCUT_TO_RDSD_UCVOLTLEVL` | `t2307584` | `key` | `NAME` |
| zphd_dog | `zphd_dog` | — | — | — | (то же поле) |
| zsiu_ty | `zsiu_ty` | `RDSD_ZSIU_TY` | `t2307875` | `zsiu_ty` | `NAME` |
| z_cl_napr | `z_cl_napr` | `RDSD_Z_CL_NAPR` | `t2307947` | `z_cl_napr` | `NAME` |
| zbur_plst | `zbur_plst` | `RDSD_ZBUR_PLST` | `t237842` | `zbur_plst` | `ZBUR_PLST` |
| zequi | `zequi` | `RDSD_ZEQUI` | `t2383584` | `zequi` | `NAME` |
| posid | `posid` | `RDSD_POSID` | `t2337709` | `posid` | `NAME` |
| zgen_pod | `zgen_pod` | `SHORTCUT_TO_RDSD_SOLDTO_7` | `t2301822` | `code` | `NAME` |
| zpkr_subp | `zpkr_subp` | `SHORTCUT_TO_RDSD_SOLDTO_8` | `t2301822` | `code` | `NAME` |
| zshifr | `zshifr` | — | — | — | (то же поле) |
| zdoglink | `zdoglink` | — | — | — | (то же поле) |
| zph_eso2 | `zph_eso2` | `SHORTCUT_TO_RDSD_SOLDTO_2` | `t2301822` | `code` | `NAME` |
| zphd_usl1 | `zphd_usl1` | `SHORTCUT_TO_RDSD_SOLDTO_3` | `t2301822` | `code` | `NAME` |
| zph_epok | `zph_epok` | `SHORTCUT_TO_RDSD_SOLDTO_4` | `t2301822` | `code` | `NAME` |
| zphd_sk | `zphd_sk` | `SHORTCUT_TO_RDSD_SOLDTO_5` | `t2301822` | `code` | `NAME` |
| zfunc_loc | `zfunc_loc` | `RDSD_ZFUNC_LOC` | `t2355739` | `zfunc_loc` | `NAME` |
| zgaz_type | `zgaz_type` | `RDSD_ZGAZ_TYPE` | `t2290906` | `code` | `NAME` |
| zphd_spr | `zphd_spr` | — | — | — | (то же поле) |
| zphd_nop1 | `zphd_nop1` | — | — | — | (то же поле) |
| zphd_nch | `zphd_nch` | — | — | — | (то же поле) |
| zphd_kon | `zphd_kon` | — | — | — | (то же поле) |
| zskv_st | `zskv_st` | — | — | — | (то же поле) |
| zskv_kust | `zskv_kust` | — | — | — | (то же поле) |
| zbur_area | `zbur_area` | `RDSD_ZBUR_AREA` | `t2311573` | `zbur_area` | `NAME` |
| zpilot | `zpilot` | — | — | — | (то же поле) |
| zph_oplst | `zph_oplst` | — | — | — | (то же поле) |
| zph_tehk | `zph_tehk` | — | — | — | (то же поле) |
| zbur_end | `zbur_end` | — | — | — | (то же поле) |
| zbur_beg | `zbur_beg` | — | — | — | (то же поле) |
| zehs_wrkv | `zehs_wrkv` | — | — | — | (то же поле) |
| zobjem | `zobjem` | — | — | — | (то же поле) |
| zphd_sr | `zphd_sr` | `RDSD_ZPHD_SR` | `t2356315` | `zphd_sr` | `NAME` |
| zphd_grsr | `zphd_grsr` | `RDSD_ZPHD_GRSR` | `t2311629` | `zphd_grsr` | `NAME` |
| zindtxt1 | `zindtxt1` | — | — | — | (то же поле) |
| zlim_lvlt | `zlim_lvlt` | — | — | — | (то же поле) |
| zphd_id | `zphd_id` | — | — | — | (то же поле) |
| hroktmo | `hroktmo` | — | — | — | (то же поле) |
| hrokato | `hrokato` | — | — | — | (то же поле) |
| z_subj_rf | `z_subj_rf` | — | — | — | (то же поле) |
| zhrpos_sh | `zhrpos_sh` | — | — | — | (то же поле) |
| hrposition | `hrposition` | — | — | — | (то же поле) |
| zclsvobor | `zclsvobor` | `RDSD_ZCLSVOBOR` | `t2308461` | `zclsvo_b or` | `NAME` |
| zlib_indc | `zlib_indc` | `RDSD_INDS` | `t1895280` | `code` | `SNAME` |
| act_unit | `act_unit` | — | — | — | (то же поле) |
| zsiu_indv | `zsiu_indv` | — | — | — | (то же поле) |
| zvalue_sng | `zvalue_sng` | — | — | — | (то же поле) |
| period | `period` | — | — | — | (то же поле) |
| zphd_stat | `zphd_stat` | — | — | — | (то же поле) |
| zind_sche | `zind_sche` | — | — | — | (то же поле) |
| key_connect | `key_connect` | — | — | — | (то же поле) |

## Источник данных (CTE `src`)

```
t1913698 D                      -- боковик DICT_PHD_LEFT (IS_TEMPORARY = 2), все колонки-ключи
  JOIN TBL_FAP_MULT TBL         -- OBJECT: TBL_PHD_FAP_MULT, физическая таблица TBL_FAP_MULT (не t-таблица)
    ON D."KEY" = TBL.KEY_CONNECT
   AND TBL.plant = D.plant
   AND TBL.year  = D.calyear
```

* **`t1913698`** (объект `DICT_PHD_LEFT`) — боковик: в нём лежат все колонки-ключи аналитик (`sold_to`, `vendor`, `plant`, …) и `KEY` для связи с фактами;
* **`TBL_FAP_MULT`** (объект `TBL_PHD_FAP_MULT`) — факты: `zsiu_indv`, `zvalue_sng`, `period`, `zphd_stat`, `zind_sche`, `key_connect`, а также `sp`, `plant`, `year`;
* динамические колонки периодов/статусов (`EXTRA_FIELDS`) строятся из полей `TBL_FAP_MULT`:
  `SUM(TBL.zsiu_indv) FILTER (WHERE TBL.period = N AND TBL.ztypeind = '…')`,
  `SUM(TBL.zvalue_sng) FILTER (…)`, статус — `TBL.zphd_stat`;
* наименования аналитик (`…_name`) получаются соединением боковика со справочниками НСИ (см. таблицу выше), а `TBL_FAP_MULT` в этих соединениях не участвует — только в фильтрах по периоду/статусу и в суммах.

