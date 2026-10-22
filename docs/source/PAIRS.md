# Связи пар «ключ / наименование» (ANALYTIC_SET при выводе кодов)

Ключ — колонка боковика `t1913698`; наименование — колонка CTE `src` с суффиксом `_name`
(получается соединением с справочником НСИ). Для полей без справочника ключ и наименование совпадают.

| Поле (MULT) | Ключ | Наименование | Справочник → поле |
|---|---|---|---|
| zphd_pern | `v.zphd_pern` | `v.zphd_pern` (то же поле) | — |
| sold_to | `v.sold_to` | `v.sold_to_name` | `RDSD_SOLDTO` → `NAME` |
| vendor | `v.vendor` | `v.vendor_name` | `RDSD_VENDOR` → `TXTMD` |
| zhrgrpmo | `v.zhrgrpmo` | `v.zhrgrpmo_name` | `RDSD_ZHRGRPMO` → `NAME` |
| calyear | `v.calyear` | `v.calyear` (то же поле) | — |
| plant | `v.plant` | `v.plant_name` | `n_plant` → `TXTMD` |
| zlib_infs | `v.zlib_infs` | `v.zlib_infs_name` | `RDSD_INFOSYSTEM` → `NAME` |
| zbur_lu | `v.zbur_lu` | `v.zbur_lu_name` | `RDSD_ZBUR_LU` → `NAME` |
| zsiu_fld | `v.zsiu_fld` | `v.zsiu_fld_name` | `RDSD_ZSIU_FLD` → `NAME` |
| zkust | `v.zkust` | `v.zkust` (то же поле) | — |
| z_skv_geo | `v.z_skv_geo` | `v.z_skv_geo` (то же поле) | — |
| zgen_zak | `v.zgen_zak` | `v.zgen_zak_name` | `SHORTCUT_TO_RDSD_SOLDTO_6` → `NAME` |
| zphd_vnmr | `v.zphd_vnmr` | `v.zphd_vnmr` (то же поле) | — |
| calcty | `v.calcty` | `v.calcty` (то же поле) | — |
| ztypeind | `v.ztypeind` | `v.ztypeind` (то же поле) | — |
| zorgunit | `v.zorgunit` | `v.zorgunit` (то же поле) | — |
| period_type | `v.period_type` | `v.period_type_name` | `n_period_type` → `NAME` |
| zzdop | `v.zzdop` | `v.zzdop` (то же поле) | — |
| zphd_priz | `v.zphd_priz` | `v.zphd_priz` (то же поле) | — |
| zregi_mvz | `v.zregi_mvz` | `v.zregi_mvz` (то же поле) | — |
| acttype | `v.acttype` | `v.acttype_name` | `RDSD_ACTTYPE` → `NAME` |
| material | `v.material` | `v.material_name` | `RDSD_MATERIAL` → `NAME` |
| zph_usr2 | `v.zph_usr2` | `v.zph_usr2` (то же поле) | — |
| costcenter | `v.costcenter` | `v.costcenter` (то же поле) | — |
| profit_ctr | `v.profit_ctr` | `v.profit_ctr_name` | `RDSD_PROFIT_CTR` → `NAME` |
| zphd_is | `v.zphd_is` | `v.zphd_is` (то же поле) | — |
| zphd_comm | `v.zphd_comm` | `v.zphd_comm` (то же поле) | — |
| zphd_phd | `v.zphd_phd` | `v.zphd_phd` (то же поле) | — |
| zdebitor | `v.zdebitor` | `v.zdebitor_name` | `SHORTCUT_TO_RDSD_SOLDTO` → `NAME` |
| ucvoltlevl | `v.ucvoltlevl` | `v.ucvoltlevl_name` | `RDSD_UCVOLTLEVL` → `NAME` |
| zaviatype | `v.zaviatype` | `v.zaviatype_name` | `RDSD_ZAVIATYPE` → `NAME` |
| zucvolttr | `v.zucvolttr` | `v.zucvolttr_name` | `SHORTCUT_TO_RDSD_UCVOLTLEVL` → `NAME` |
| zphd_dog | `v.zphd_dog` | `v.zphd_dog` (то же поле) | — |
| zsiu_ty | `v.zsiu_ty` | `v.zsiu_ty_name` | `RDSD_ZSIU_TY` → `NAME` |
| z_cl_napr | `v.z_cl_napr` | `v.z_cl_napr_name` | `RDSD_Z_CL_NAPR` → `NAME` |
| zbur_plst | `v.zbur_plst` | `v.zbur_plst_name` | `RDSD_ZBUR_PLST` → `ZBUR_PLST` |
| zequi | `v.zequi` | `v.zequi_name` | `RDSD_ZEQUI` → `NAME` |
| posid | `v.posid` | `v.posid_name` | `RDSD_POSID` → `NAME` |
| zgen_pod | `v.zgen_pod` | `v.zgen_pod_name` | `SHORTCUT_TO_RDSD_SOLDTO_7` → `NAME` |
| zpkr_subp | `v.zpkr_subp` | `v.zpkr_subp_name` | `SHORTCUT_TO_RDSD_SOLDTO_8` → `NAME` |
| zshifr | `v.zshifr` | `v.zshifr` (то же поле) | — |
| zdoglink | `v.zdoglink` | `v.zdoglink` (то же поле) | — |
| zph_eso2 | `v.zph_eso2` | `v.zph_eso2_name` | `SHORTCUT_TO_RDSD_SOLDTO_2` → `NAME` |
| zphd_usl1 | `v.zphd_usl1` | `v.zphd_usl1_name` | `SHORTCUT_TO_RDSD_SOLDTO_3` → `NAME` |
| zph_epok | `v.zph_epok` | `v.zph_epok_name` | `SHORTCUT_TO_RDSD_SOLDTO_4` → `NAME` |
| zphd_sk | `v.zphd_sk` | `v.zphd_sk_name` | `SHORTCUT_TO_RDSD_SOLDTO_5` → `NAME` |
| zfunc_loc | `v.zfunc_loc` | `v.zfunc_loc_name` | `RDSD_ZFUNC_LOC` → `NAME` |
| zgaz_type | `v.zgaz_type` | `v.zgaz_type_name` | `RDSD_ZGAZ_TYPE` → `NAME` |
| zphd_spr | `v.zphd_spr` | `v.zphd_spr` (то же поле) | — |
| zphd_nop1 | `v.zphd_nop1` | `v.zphd_nop1` (то же поле) | — |
| zphd_nch | `v.zphd_nch` | `v.zphd_nch` (то же поле) | — |
| zphd_kon | `v.zphd_kon` | `v.zphd_kon` (то же поле) | — |
| zskv_st | `v.zskv_st` | `v.zskv_st` (то же поле) | — |
| zskv_kust | `v.zskv_kust` | `v.zskv_kust` (то же поле) | — |
| zbur_area | `v.zbur_area` | `v.zbur_area_name` | `RDSD_ZBUR_AREA` → `NAME` |
| zpilot | `v.zpilot` | `v.zpilot` (то же поле) | — |
| zph_oplst | `v.zph_oplst` | `v.zph_oplst` (то же поле) | — |
| zph_tehk | `v.zph_tehk` | `v.zph_tehk` (то же поле) | — |
| zbur_end | `v.zbur_end` | `v.zbur_end` (то же поле) | — |
| zbur_beg | `v.zbur_beg` | `v.zbur_beg` (то же поле) | — |
| zehs_wrkv | `v.zehs_wrkv` | `v.zehs_wrkv` (то же поле) | — |
| zobjem | `v.zobjem` | `v.zobjem` (то же поле) | — |
| zphd_sr | `v.zphd_sr` | `v.zphd_sr_name` | `RDSD_ZPHD_SR` → `NAME` |
| zphd_grsr | `v.zphd_grsr` | `v.zphd_grsr_name` | `RDSD_ZPHD_GRSR` → `NAME` |
| zindtxt1 | `v.zindtxt1` | `v.zindtxt1` (то же поле) | — |
| zlim_lvlt | `v.zlim_lvlt` | `v.zlim_lvlt` (то же поле) | — |
| zphd_id | `v.zphd_id` | `v.zphd_id` (то же поле) | — |
| hroktmo | `v.hroktmo` | `v.hroktmo` (то же поле) | — |
| hrokato | `v.hrokato` | `v.hrokato` (то же поле) | — |
| z_subj_rf | `v.z_subj_rf` | `v.z_subj_rf` (то же поле) | — |
| zhrpos_sh | `v.zhrpos_sh` | `v.zhrpos_sh` (то же поле) | — |
| hrposition | `v.hrposition` | `v.hrposition` (то же поле) | — |
| zclsvobor | `v.zclsvobor` | `v.zclsvobor_name` | `RDSD_ZCLSVOBOR` → `NAME` |
| zlib_indc | `v.zlib_indc` | `v.zlib_indc_name` | `n_inds` → `SNAME` |
| act_unit | `v.act_unit` | `v.act_unit` (то же поле) | — |
| zsiu_indv | `v.zsiu_indv` | `v.zsiu_indv` (то же поле) | — |
| zvalue_sng | `v.zvalue_sng` | `v.zvalue_sng` (то же поле) | — |
| period | `v.period` | `v.period` (то же поле) | — |
| zphd_stat | `v.zphd_stat` | `v.zphd_stat` (то же поле) | — |
| zind_sche | `v.zind_sche` | `v.zind_sche` (то же поле) | — |
| key_connect | `v.key_connect` | `v.key_connect` (то же поле) | — |
