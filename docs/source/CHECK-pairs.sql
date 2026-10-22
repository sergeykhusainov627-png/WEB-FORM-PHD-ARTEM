-- Проверка связей: ключ (колонка боковика) и наименование (справочник НСИ).
-- Наименования — это колонки src с суффиксом _name; для полей без справочника ключ = наименование.
WITH
src AS (
    SELECT D.*, TBL.zsiu_indv, TBL.zvalue_sng, TBL.period, TBL.zphd_stat, TBL.zind_sche, TBL.key_connect,
           n_rdsd_vendor.TXTMD AS vendor_name,
           n_rdsd_soldto.NAME AS sold_to_name,
           n_rdsd_zhrgrpmo.NAME AS zhrgrpmo_name,
           n_rdsd_profit_ctr.NAME AS profit_ctr_name,
           n_rdsd_acttype.NAME AS acttype_name,
           n_rdsd_zequi.NAME AS zequi_name,
           n_rdsd_zclsvobor.NAME AS zclsvobor_name,
           n_rdsd_material.NAME AS material_name,
           n_rdsd_zfunc_loc.NAME AS zfunc_loc_name,
           n_rdsd_zsiu_fld.NAME AS zsiu_fld_name,
           n_rdsd_posid.NAME AS posid_name,
           n_rdsd_infosystem.NAME AS zlib_infs_name,
           n_shortcut_to_rdsd_soldto_3.NAME AS zphd_usl1_name,
           n_shortcut_to_rdsd_soldto.NAME AS zdebitor_name,
           n_shortcut_to_rdsd_soldto_2.NAME AS zph_eso2_name,
           n_shortcut_to_rdsd_soldto_4.NAME AS zph_epok_name,
           n_shortcut_to_rdsd_soldto_5.NAME AS zphd_sk_name,
           n_rdsd_ucvoltlevl.NAME AS ucvoltlevl_name,
           n_shortcut_to_rdsd_ucvoltlevl.NAME AS zucvolttr_name,
           n_rdsd_z_cl_napr.NAME AS z_cl_napr_name,
           n_rdsd_zsiu_ty.NAME AS zsiu_ty_name,
           n_rdsd_zbur_lu.NAME AS zbur_lu_name,
           n_rdsd_zbur_area.NAME AS zbur_area_name,
           n_rdsd_zbur_plst.ZBUR_PLST AS zbur_plst_name,
           n_rdsd_zph_tehk.NAME AS name_name,
           n_shortcut_to_rdsd_soldto_7.NAME AS zgen_pod_name,
           n_shortcut_to_rdsd_soldto_6.NAME AS zgen_zak_name,
           n_shortcut_to_rdsd_soldto_8.NAME AS zpkr_subp_name,
           n_rdsd_zphd_sr.NAME AS zphd_sr_name,
           n_rdsd_zphd_grsr.NAME AS zphd_grsr_name,
           n_rdsd_zgaz_type.NAME AS zgaz_type_name,
           n_rdsd_zaviatype.NAME AS zaviatype_name,
           n_plant.TXTMD AS plant_name,
           n_period_type.NAME AS period_type_name,
           n_inds.SNAME AS zlib_indc_name
    FROM t1913698 D
    JOIN TBL_FAP_MULT TBL
      ON D."KEY" = TBL.KEY_CONNECT AND TBL.plant = D.plant AND TBL.year = D.calyear
    LEFT JOIN t2322857   n_rdsd_vendor
       ON n_rdsd_vendor.vendor = D.vendor
    LEFT JOIN t2301822   n_rdsd_soldto
       ON n_rdsd_soldto.code = D.sold_to
    LEFT JOIN t2306331   n_rdsd_zhrgrpmo
       ON n_rdsd_zhrgrpmo.zhrgrpmo = D.zhrgrpmo
    LEFT JOIN t2320954   n_rdsd_profit_ctr
       ON n_rdsd_profit_ctr.profit_ctr = D.profit_ctr
    LEFT JOIN t2320948   n_rdsd_acttype
       ON n_rdsd_acttype.acttype = D.acttype
      AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto
    LEFT JOIN t2338354   n_rdsd_zequi
       ON n_rdsd_zequi.zequi = D.zequi
      AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto
    LEFT JOIN t2308461   n_rdsd_zclsvobor
       ON n_rdsd_zclsvobor.zclsvobor = D.zclsvobor
    LEFT JOIN t2321329   n_rdsd_material
       ON n_rdsd_material.material = D.material
    LEFT JOIN t2335739   n_rdsd_zfunc_loc
       ON n_rdsd_zfunc_loc.zfunc_loc = D.zfunc_loc
      AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zfunc_loc.datefrom::date AND n_rdsd_zfunc_loc.dateto::date
    LEFT JOIN t2320973   n_rdsd_zsiu_fld
       ON n_rdsd_zsiu_fld.zsiu_fld = D.zsiu_fld
    LEFT JOIN t2337709   n_rdsd_posid
       ON n_rdsd_posid.posid = D.posid
    LEFT JOIN t1895288   n_rdsd_infosystem
       ON n_rdsd_infosystem.code_value = D.zlib_infs
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_3
       ON n_shortcut_to_rdsd_soldto_3.code = D.zphd_usl1
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto
       ON n_shortcut_to_rdsd_soldto.code = D.zdebitor
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_2
       ON n_shortcut_to_rdsd_soldto_2.code = D.zph_eso2
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_4
       ON n_shortcut_to_rdsd_soldto_4.code = D.zph_epok
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_5
       ON n_shortcut_to_rdsd_soldto_5.code = D.zphd_sk
    LEFT JOIN t2307584   n_rdsd_ucvoltlevl
       ON n_rdsd_ucvoltlevl.ucvoltlevl = D.ucvoltlevl
    LEFT JOIN t2307584   n_shortcut_to_rdsd_ucvoltlevl
       ON n_shortcut_to_rdsd_ucvoltlevl.ucvoltlevl = D.zucvolttr
    LEFT JOIN t2307947   n_rdsd_z_cl_napr
       ON n_rdsd_z_cl_napr.z_cl_napr = D.z_cl_napr
    LEFT JOIN t2307875   n_rdsd_zsiu_ty
       ON n_rdsd_zsiu_ty.zsiu_ty = D.zsiu_ty
    LEFT JOIN t2320979   n_rdsd_zbur_lu
       ON n_rdsd_zbur_lu.code = D.zbur_lu
    LEFT JOIN t2311573   n_rdsd_zbur_area
       ON n_rdsd_zbur_area.zbur_area = D.zbur_area
    LEFT JOIN t2337842    n_rdsd_zbur_plst
       ON n_rdsd_zbur_plst.zbur_plst = D.zbur_plst
    LEFT JOIN t2311619   n_rdsd_zph_tehk
       ON n_rdsd_zph_tehk.code = D.name
    LEFT JOIN t2311231   n_rdsd_zskv_st
       ON n_rdsd_zskv_st.zskv_st = D.name
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_7
       ON n_shortcut_to_rdsd_soldto_7.code = D.zgen_pod
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_6
       ON n_shortcut_to_rdsd_soldto_6.code = D.zgen_zak
    LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_8
       ON n_shortcut_to_rdsd_soldto_8.code = D.zpkr_subp
    LEFT JOIN t2311391   n_rdsd_zshifr
       ON n_rdsd_zshifr.zshifr = D.name
    LEFT JOIN t2335657   n_rdsd_zobjem
       ON n_rdsd_zobjem.zobjem = D.name
    LEFT JOIN t2335635   n_rdsd_zphd_sr
       ON n_rdsd_zphd_sr.zphd_sr = D.zphd_sr
    LEFT JOIN t2311629   n_rdsd_zphd_grsr
       ON n_rdsd_zphd_grsr.zphd_grsr = D.zphd_grsr
    LEFT JOIN t2290906   n_rdsd_zgaz_type
       ON n_rdsd_zgaz_type.code = D.zgaz_type
    LEFT JOIN t2307768   n_rdsd_zaviatype
       ON n_rdsd_zaviatype.zaviatype = D.zaviatype
    LEFT JOIN t2321022 n_zph_usr0
    on n_zph_usr0.zph_usr0 = D.zph_usr2
    LEFT JOIN t2312312 n_plant
       ON n_plant.plant = D.plant
    LEFT JOIN t2317517 n_period_type
       ON n_period_type.id = D.period_type
    LEFT JOIN t1895280 n_inds
       ON n_inds.code = D.zlib_indc
    LEFT JOIN t2494391 n_actvts
       ON n_actvts.code_value = n_inds.actvts
    LEFT JOIN t2364976 n_owners
       ON n_owners."KEY" = n_inds.owner
    WHERE D.IS_TEMPORARY = 2
AND
     	          (D.PLANT 		    	IN (:PLANT) 	 							OR COALESCE(:PLANT,'')='')
        AND (TBL.ZPHD_STAT     	IN (:ZPHD_STAT)   							OR COALESCE(:ZPHD_STAT,'')='')
        AND (TO_DATE(D.ZBUR_BEG, 'YYYY-MM-DD')
							IN (TO_DATE(:ZBUR_BEG, 'YYYY-MM-DD')) 	OR COALESCE(:ZBUR_BEG,'')='')
),
pairs AS (
SELECT
    v.zphd_pern                  AS "zphd_pern_КЛЮЧ",
    v.zphd_pern                  AS "zphd_pern_ИМЯ",
    v.sold_to                    AS "sold_to_КЛЮЧ",
    v.sold_to_name               AS "sold_to_ИМЯ",
    v.vendor                     AS "vendor_КЛЮЧ",
    v.vendor_name                AS "vendor_ИМЯ",
    v.zhrgrpmo                   AS "zhrgrpmo_КЛЮЧ",
    v.zhrgrpmo_name              AS "zhrgrpmo_ИМЯ",
    v.calyear                    AS "calyear_КЛЮЧ",
    v.calyear                    AS "calyear_ИМЯ",
    v.plant                      AS "plant_КЛЮЧ",
    v.plant_name                 AS "plant_ИМЯ",
    v.zlib_infs                  AS "zlib_infs_КЛЮЧ",
    v.zlib_infs_name             AS "zlib_infs_ИМЯ",
    v.zbur_lu                    AS "zbur_lu_КЛЮЧ",
    v.zbur_lu_name               AS "zbur_lu_ИМЯ",
    v.zsiu_fld                   AS "zsiu_fld_КЛЮЧ",
    v.zsiu_fld_name              AS "zsiu_fld_ИМЯ",
    v.zkust                      AS "zkust_КЛЮЧ",
    v.zkust                      AS "zkust_ИМЯ",
    v.z_skv_geo                  AS "z_skv_geo_КЛЮЧ",
    v.z_skv_geo                  AS "z_skv_geo_ИМЯ",
    v.zgen_zak                   AS "zgen_zak_КЛЮЧ",
    v.zgen_zak_name              AS "zgen_zak_ИМЯ",
    v.zphd_vnmr                  AS "zphd_vnmr_КЛЮЧ",
    v.zphd_vnmr                  AS "zphd_vnmr_ИМЯ",
    v.calcty                     AS "calcty_КЛЮЧ",
    v.calcty                     AS "calcty_ИМЯ",
    v.ztypeind                   AS "ztypeind_КЛЮЧ",
    v.ztypeind                   AS "ztypeind_ИМЯ",
    v.zorgunit                   AS "zorgunit_КЛЮЧ",
    v.zorgunit                   AS "zorgunit_ИМЯ",
    v.period_type                AS "period_type_КЛЮЧ",
    v.period_type_name           AS "period_type_ИМЯ",
    v.zzdop                      AS "zzdop_КЛЮЧ",
    v.zzdop                      AS "zzdop_ИМЯ",
    v.zphd_priz                  AS "zphd_priz_КЛЮЧ",
    v.zphd_priz                  AS "zphd_priz_ИМЯ",
    v.zregi_mvz                  AS "zregi_mvz_КЛЮЧ",
    v.zregi_mvz                  AS "zregi_mvz_ИМЯ",
    v.acttype                    AS "acttype_КЛЮЧ",
    v.acttype_name               AS "acttype_ИМЯ",
    v.material                   AS "material_КЛЮЧ",
    v.material_name              AS "material_ИМЯ",
    v.zph_usr2                   AS "zph_usr2_КЛЮЧ",
    v.zph_usr2                   AS "zph_usr2_ИМЯ",
    v.costcenter                 AS "costcenter_КЛЮЧ",
    v.costcenter                 AS "costcenter_ИМЯ",
    v.profit_ctr                 AS "profit_ctr_КЛЮЧ",
    v.profit_ctr_name            AS "profit_ctr_ИМЯ",
    v.zphd_is                    AS "zphd_is_КЛЮЧ",
    v.zphd_is                    AS "zphd_is_ИМЯ",
    v.zphd_comm                  AS "zphd_comm_КЛЮЧ",
    v.zphd_comm                  AS "zphd_comm_ИМЯ",
    v.zphd_phd                   AS "zphd_phd_КЛЮЧ",
    v.zphd_phd                   AS "zphd_phd_ИМЯ",
    v.zdebitor                   AS "zdebitor_КЛЮЧ",
    v.zdebitor_name              AS "zdebitor_ИМЯ",
    v.ucvoltlevl                 AS "ucvoltlevl_КЛЮЧ",
    v.ucvoltlevl_name            AS "ucvoltlevl_ИМЯ",
    v.zaviatype                  AS "zaviatype_КЛЮЧ",
    v.zaviatype_name             AS "zaviatype_ИМЯ",
    v.zucvolttr                  AS "zucvolttr_КЛЮЧ",
    v.zucvolttr_name             AS "zucvolttr_ИМЯ",
    v.zphd_dog                   AS "zphd_dog_КЛЮЧ",
    v.zphd_dog                   AS "zphd_dog_ИМЯ",
    v.zsiu_ty                    AS "zsiu_ty_КЛЮЧ",
    v.zsiu_ty_name               AS "zsiu_ty_ИМЯ",
    v.z_cl_napr                  AS "z_cl_napr_КЛЮЧ",
    v.z_cl_napr_name             AS "z_cl_napr_ИМЯ",
    v.zbur_plst                  AS "zbur_plst_КЛЮЧ",
    v.zbur_plst_name             AS "zbur_plst_ИМЯ",
    v.zequi                      AS "zequi_КЛЮЧ",
    v.zequi_name                 AS "zequi_ИМЯ",
    v.posid                      AS "posid_КЛЮЧ",
    v.posid_name                 AS "posid_ИМЯ",
    v.zgen_pod                   AS "zgen_pod_КЛЮЧ",
    v.zgen_pod_name              AS "zgen_pod_ИМЯ",
    v.zpkr_subp                  AS "zpkr_subp_КЛЮЧ",
    v.zpkr_subp_name             AS "zpkr_subp_ИМЯ",
    v.zshifr                     AS "zshifr_КЛЮЧ",
    v.zshifr                     AS "zshifr_ИМЯ",
    v.zdoglink                   AS "zdoglink_КЛЮЧ",
    v.zdoglink                   AS "zdoglink_ИМЯ",
    v.zph_eso2                   AS "zph_eso2_КЛЮЧ",
    v.zph_eso2_name              AS "zph_eso2_ИМЯ",
    v.zphd_usl1                  AS "zphd_usl1_КЛЮЧ",
    v.zphd_usl1_name             AS "zphd_usl1_ИМЯ",
    v.zph_epok                   AS "zph_epok_КЛЮЧ",
    v.zph_epok_name              AS "zph_epok_ИМЯ",
    v.zphd_sk                    AS "zphd_sk_КЛЮЧ",
    v.zphd_sk_name               AS "zphd_sk_ИМЯ",
    v.zfunc_loc                  AS "zfunc_loc_КЛЮЧ",
    v.zfunc_loc_name             AS "zfunc_loc_ИМЯ",
    v.zgaz_type                  AS "zgaz_type_КЛЮЧ",
    v.zgaz_type_name             AS "zgaz_type_ИМЯ",
    v.zphd_spr                   AS "zphd_spr_КЛЮЧ",
    v.zphd_spr                   AS "zphd_spr_ИМЯ",
    v.zphd_nop1                  AS "zphd_nop1_КЛЮЧ",
    v.zphd_nop1                  AS "zphd_nop1_ИМЯ",
    v.zphd_nch                   AS "zphd_nch_КЛЮЧ",
    v.zphd_nch                   AS "zphd_nch_ИМЯ",
    v.zphd_kon                   AS "zphd_kon_КЛЮЧ",
    v.zphd_kon                   AS "zphd_kon_ИМЯ",
    v.zskv_st                    AS "zskv_st_КЛЮЧ",
    v.zskv_st                    AS "zskv_st_ИМЯ",
    v.zskv_kust                  AS "zskv_kust_КЛЮЧ",
    v.zskv_kust                  AS "zskv_kust_ИМЯ",
    v.zbur_area                  AS "zbur_area_КЛЮЧ",
    v.zbur_area_name             AS "zbur_area_ИМЯ",
    v.zpilot                     AS "zpilot_КЛЮЧ",
    v.zpilot                     AS "zpilot_ИМЯ",
    v.zph_oplst                  AS "zph_oplst_КЛЮЧ",
    v.zph_oplst                  AS "zph_oplst_ИМЯ",
    v.zph_tehk                   AS "zph_tehk_КЛЮЧ",
    v.zph_tehk                   AS "zph_tehk_ИМЯ",
    v.zbur_end                   AS "zbur_end_КЛЮЧ",
    v.zbur_end                   AS "zbur_end_ИМЯ",
    v.zbur_beg                   AS "zbur_beg_КЛЮЧ",
    v.zbur_beg                   AS "zbur_beg_ИМЯ",
    v.zehs_wrkv                  AS "zehs_wrkv_КЛЮЧ",
    v.zehs_wrkv                  AS "zehs_wrkv_ИМЯ",
    v.zobjem                     AS "zobjem_КЛЮЧ",
    v.zobjem                     AS "zobjem_ИМЯ",
    v.zphd_sr                    AS "zphd_sr_КЛЮЧ",
    v.zphd_sr_name               AS "zphd_sr_ИМЯ",
    v.zphd_grsr                  AS "zphd_grsr_КЛЮЧ",
    v.zphd_grsr_name             AS "zphd_grsr_ИМЯ",
    v.zindtxt1                   AS "zindtxt1_КЛЮЧ",
    v.zindtxt1                   AS "zindtxt1_ИМЯ",
    v.zlim_lvlt                  AS "zlim_lvlt_КЛЮЧ",
    v.zlim_lvlt                  AS "zlim_lvlt_ИМЯ",
    v.zphd_id                    AS "zphd_id_КЛЮЧ",
    v.zphd_id                    AS "zphd_id_ИМЯ",
    v.hroktmo                    AS "hroktmo_КЛЮЧ",
    v.hroktmo                    AS "hroktmo_ИМЯ",
    v.hrokato                    AS "hrokato_КЛЮЧ",
    v.hrokato                    AS "hrokato_ИМЯ",
    v.z_subj_rf                  AS "z_subj_rf_КЛЮЧ",
    v.z_subj_rf                  AS "z_subj_rf_ИМЯ",
    v.zhrpos_sh                  AS "zhrpos_sh_КЛЮЧ",
    v.zhrpos_sh                  AS "zhrpos_sh_ИМЯ",
    v.hrposition                 AS "hrposition_КЛЮЧ",
    v.hrposition                 AS "hrposition_ИМЯ",
    v.zclsvobor                  AS "zclsvobor_КЛЮЧ",
    v.zclsvobor_name             AS "zclsvobor_ИМЯ",
    v.zlib_indc                  AS "zlib_indc_КЛЮЧ",
    v.zlib_indc_name             AS "zlib_indc_ИМЯ",
    v.act_unit                   AS "act_unit_КЛЮЧ",
    v.act_unit                   AS "act_unit_ИМЯ",
    v.zsiu_indv                  AS "zsiu_indv_КЛЮЧ",
    v.zsiu_indv                  AS "zsiu_indv_ИМЯ",
    v.zvalue_sng                 AS "zvalue_sng_КЛЮЧ",
    v.zvalue_sng                 AS "zvalue_sng_ИМЯ",
    v.period                     AS "period_КЛЮЧ",
    v.period                     AS "period_ИМЯ",
    v.zphd_stat                  AS "zphd_stat_КЛЮЧ",
    v.zphd_stat                  AS "zphd_stat_ИМЯ",
    v.zind_sche                  AS "zind_sche_КЛЮЧ",
    v.zind_sche                  AS "zind_sche_ИМЯ",
    v.key_connect                AS "key_connect_КЛЮЧ",
    v.key_connect                AS "key_connect_ИМЯ"
FROM src v
)
SELECT * FROM pairs LIMIT 100;