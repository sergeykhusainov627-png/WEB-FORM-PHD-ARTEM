/*
   ПРОВЕРКА БЛОКА СОЕДИНЕНИЙ (автономный запрос, без параметров).
   Назначение: убедиться, что все LEFT JOIN валидны, и посмотреть наименования.
   Запускать как обычный запрос: SELECT ... FROM (источник) v LEFT JOIN ...
   Используется: боковик t1913698 (IS_TEMPORARY = 2) + факты TBL_FAP_MULT.
*/
SELECT
       v.plant            AS "RDSD_PLANT_key",
       n_plant.TXTMD        AS "RDSD_PLANT_name",
       v.sold_to          AS "RDSD_SOLDTO_key",
       n_soldto.NAME        AS "RDSD_SOLDTO_name",
       v.zlib_indc        AS "RDSD_INDS_key ",
       n_inds.SNAME         AS "RDSD_INDS_name",
       v.zph_usr2         AS "RDSD_ZPH_USR0_key",
       n_zph_usr0.NAME      AS "RDSD_ZPH_USR0_name",
       v.period_type      AS "DIC_TYPE_PERIOD_key",
       NULL                 AS "DIC_TYPE_PERIOD_name",
       v.vendor           AS "RDSD_VENDOR_key",
       n_rdsd_vendor.TXTMD  AS "RDSD_VENDOR_name",
       v.key              AS "RDSD_SOLDTO_key",
       n_rdsd_soldto.NAME   AS "RDSD_SOLDTO_name",
       v.zhrgrpmo         AS "RDSD_ZHRGRPMO_key",
       n_rdsd_zhrgrpmo.NAME AS "RDSD_ZHRGRPMO_name",
       v.profit_ctr       AS "RDSD_PROFIT_CTR_key",
       n_rdsd_profit_ctr.NAME AS "RDSD_PROFIT_CTR_name",
       v.acttype          AS "RDSD_ACTTYPE_key",
       n_rdsd_acttype.NAME  AS "RDSD_ACTTYPE_name",
       v.zequi            AS "RDSD_ZEQUI_key",
       n_rdsd_zequi.NAME    AS "RDSD_ZEQUI_name",
       v.material         AS "RDSD_MATERIAL_key",
       n_rdsd_material.NAME AS "RDSD_MATERIAL_name",
       v.zfunc_loc        AS "RDSD_ZFUNC_LOC_key",
       n_rdsd_zfunc_loc.NAME AS "RDSD_ZFUNC_LOC_name",
       v.zsiu_fld         AS "RDSD_ZSIU_FLD_key",
       n_rdsd_zsiu_fld.NAME AS "RDSD_ZSIU_FLD_name",
       v.posid            AS "RDSD_POSID_key",
       n_rdsd_posid.NAME    AS "RDSD_POSID_name",
       v.zlib_infs        AS "RDSD_INFOSYSTEM_key",
       n_rdsd_infosystem.NAME AS "RDSD_INFOSYSTEM_name",
       v.zphd_usl1        AS "SHORTCUT_TO_RDSD_SOLDTO_3_key",
       n_shortcut_to_rdsd_soldto_3.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_3_name",
       v.zdebitor         AS "SHORTCUT_TO_RDSD_SOLDTO_key",
       n_shortcut_to_rdsd_soldto.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_name",
       v.zph_eso2         AS "SHORTCUT_TO_RDSD_SOLDTO_2_key",
       n_shortcut_to_rdsd_soldto_2.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_2_name",
       v.zph_epok         AS "SHORTCUT_TO_RDSD_SOLDTO_4_key",
       n_shortcut_to_rdsd_soldto_4.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_4_name",
       v.zphd_sk          AS "SHORTCUT_TO_RDSD_SOLDTO_5_key",
       n_shortcut_to_rdsd_soldto_5.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_5_name",
       v.ucvoltlevl       AS "RDSD_UCVOLTLEVL_key",
       n_rdsd_ucvoltlevl.NAME AS "RDSD_UCVOLTLEVL_name",
       v.zucvolttr        AS "SHORTCUT_TO_RDSD_UCVOLTLEVL_key",
       n_shortcut_to_rdsd_ucvoltlevl.NAME AS "SHORTCUT_TO_RDSD_UCVOLTLEVL_name",
       v.z_cl_napr        AS "RDSD_Z_CL_NAPR_key",
       n_rdsd_z_cl_napr.NAME AS "RDSD_Z_CL_NAPR_name",
       v.zsiu_ty          AS "RDSD_ZSIU_TY_key",
       n_rdsd_zsiu_ty.NAME  AS "RDSD_ZSIU_TY_name",
       v.zbur_lu          AS "RDSD_ZBUR_LU_key",
       n_rdsd_zbur_lu.NAME  AS "RDSD_ZBUR_LU_name",
       v.zbur_area        AS "RDSD_ZBUR_AREA_key",
       n_rdsd_zbur_area.NAME AS "RDSD_ZBUR_AREA_name",
       v.zbur_plst        AS "RDSD_ZBUR_PLST_key",
       n_rdsd_zbur_plst.ZBUR_PLST AS "RDSD_ZBUR_PLST_name",
       v.name             AS "RDSD_ZPH_TEHK_key",
       n_rdsd_zph_tehk.NAME AS "RDSD_ZPH_TEHK_name",
       v.name             AS "RDSD_ZSKV_ST_key",
       n_rdsd_zskv_st.NAME  AS "RDSD_ZSKV_ST_name",
       v.zgen_pod         AS "SHORTCUT_TO_RDSD_SOLDTO_7_key",
       n_shortcut_to_rdsd_soldto_7.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_7_name",
       v.zgen_zak         AS "SHORTCUT_TO_RDSD_SOLDTO_6_key",
       n_shortcut_to_rdsd_soldto_6.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_6_name",
       v.zpkr_subp        AS "SHORTCUT_TO_RDSD_SOLDTO_8_key",
       n_shortcut_to_rdsd_soldto_8.NAME AS "SHORTCUT_TO_RDSD_SOLDTO_8_name",
       v.name             AS "RDSD_ZSHIFR_key",
       n_rdsd_zshifr.NAME   AS "RDSD_ZSHIFR_name",
       v.name             AS "RDSD_ZOBJEM_key",
       n_rdsd_zobjem.NAME   AS "RDSD_ZOBJEM_name",
       v.zphd_sr          AS "RDSD_ZPHD_SR_key",
       n_rdsd_zphd_sr.NAME  AS "RDSD_ZPHD_SR_name",
       v.zphd_grsr        AS "RDSD_ZPHD_GRSR_key",
       n_rdsd_zphd_grsr.NAME AS "RDSD_ZPHD_GRSR_name",
       v.zgaz_type        AS "RDSD_ZGAZ_TYPE_key",
       n_rdsd_zgaz_type.NAME AS "RDSD_ZGAZ_TYPE_name",
       v.zaviatype        AS "RDSD_ZAVIATYPE_key",
       n_rdsd_zaviatype.NAME AS "RDSD_ZAVIATYPE_name"
FROM (
    SELECT D.*, TBL.zsiu_indv, TBL.zvalue_sng, TBL.period, TBL.zphd_stat, TBL.key_connect
    FROM t1913698 D
    JOIN TBL_FAP_MULT TBL
      ON D."KEY" = TBL.KEY_CONNECT AND TBL.plant = D.plant AND TBL.year = D.calyear
    WHERE D.IS_TEMPORARY = 2
      AND D.calyear = '2026'          -- при необходимости поменяйте год
    LIMIT 100
) v
LEFT JOIN к справочникам наименований (реестр dict-tables.md + лист «Вывод полей в отчете»).
-- Цели соединений сверены со списком колонок боковика t1913698 (файл «Поля боковика»).
-- Условие даты: начало года отчёта (CALYEAR) попадает в интервал действия записи.
LEFT JOIN t2322857   n_rdsd_vendor                  -- RDSD_VENDOR
       ON n_rdsd_vendor.vendor = v.vendor
LEFT JOIN t2301822   n_rdsd_soldto                  -- RDSD_SOLDTO
       ON n_rdsd_soldto.code = v.key
LEFT JOIN t2306331   n_rdsd_zhrgrpmo                -- RDSD_ZHRGRPMO
       ON n_rdsd_zhrgrpmo.zhrgrpmo = v.zhrgrpmo
LEFT JOIN t2320954   n_rdsd_profit_ctr              -- RDSD_PROFIT_CTR
       ON n_rdsd_profit_ctr.profit_ctr = v.profit_ctr
LEFT JOIN t2320948   n_rdsd_acttype                 -- RDSD_ACTTYPE
       ON n_rdsd_acttype.acttype = v.acttype
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto
LEFT JOIN t2383584   n_rdsd_zequi                   -- RDSD_ZEQUI
       ON n_rdsd_zequi.zequi = v.zequi
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto
LEFT JOIN t2308461   n_rdsd_zclsvobor               -- RDSD_ZCLSVOBOR
       ON n_rdsd_zclsvobor.zclsvo_b or = v.zclsvobor
LEFT JOIN t2321329   n_rdsd_material                -- RDSD_MATERIAL
       ON n_rdsd_material.material = v.material
LEFT JOIN t2355739   n_rdsd_zfunc_loc               -- RDSD_ZFUNC_LOC
       ON n_rdsd_zfunc_loc.zfunc_loc = v.zfunc_loc
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zfunc_loc.datefrom AND n_rdsd_zfunc_loc.dateto
LEFT JOIN t2308973   n_rdsd_zsiu_fld                -- RDSD_ZSIU_FLD
       ON n_rdsd_zsiu_fld.zsiu_fld = v.zsiu_fld
LEFT JOIN t2337709   n_rdsd_posid                   -- RDSD_POSID
       ON n_rdsd_posid.posid = v.posid
LEFT JOIN t1895288   n_rdsd_infosystem              -- RDSD_INFOSYSTEM
       ON n_rdsd_infosystem.code_value = v.zlib_infs
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_3    -- SHORTCUT_TO_RDSD_SOLDTO_3
       ON n_shortcut_to_rdsd_soldto_3.code = v.zphd_usl1
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto      -- SHORTCUT_TO_RDSD_SOLDTO
       ON n_shortcut_to_rdsd_soldto.code = v.zdebitor
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_2    -- SHORTCUT_TO_RDSD_SOLDTO_2
       ON n_shortcut_to_rdsd_soldto_2.code = v.zph_eso2
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_4    -- SHORTCUT_TO_RDSD_SOLDTO_4
       ON n_shortcut_to_rdsd_soldto_4.code = v.zph_epok
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_5    -- SHORTCUT_TO_RDSD_SOLDTO_5
       ON n_shortcut_to_rdsd_soldto_5.code = v.zphd_sk
LEFT JOIN t2307584   n_rdsd_ucvoltlevl              -- RDSD_UCVOLTLEVL
       ON n_rdsd_ucvoltlevl.ucvoltlevl = v.ucvoltlevl
LEFT JOIN t2307584   n_shortcut_to_rdsd_ucvoltlevl  -- SHORTCUT_TO_RDSD_UCVOLTLEVL
       ON n_shortcut_to_rdsd_ucvoltlevl.key = v.zucvolttr
LEFT JOIN t2307947   n_rdsd_z_cl_napr               -- RDSD_Z_CL_NAPR
       ON n_rdsd_z_cl_napr.z_cl_napr = v.z_cl_napr
LEFT JOIN t2307875   n_rdsd_zsiu_ty                 -- RDSD_ZSIU_TY
       ON n_rdsd_zsiu_ty.zsiu_ty = v.zsiu_ty
LEFT JOIN t2320979   n_rdsd_zbur_lu                 -- RDSD_ZBUR_LU
       ON n_rdsd_zbur_lu.code = v.zbur_lu
LEFT JOIN t2311573   n_rdsd_zbur_area               -- RDSD_ZBUR_AREA
       ON n_rdsd_zbur_area.zbur_area = v.zbur_area
LEFT JOIN t237842    n_rdsd_zbur_plst               -- RDSD_ZBUR_PLST
       ON n_rdsd_zbur_plst.zbur_plst = v.zbur_plst
LEFT JOIN t2311619   n_rdsd_zph_tehk                -- RDSD_ZPH_TEHK
       ON n_rdsd_zph_tehk.code = v.name
LEFT JOIN t2311231   n_rdsd_zskv_st                 -- RDSD_ZSKV_ST
       ON n_rdsd_zskv_st.zskv_st = v.name
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_7    -- SHORTCUT_TO_RDSD_SOLDTO_7
       ON n_shortcut_to_rdsd_soldto_7.code = v.zgen_pod
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_6    -- SHORTCUT_TO_RDSD_SOLDTO_6
       ON n_shortcut_to_rdsd_soldto_6.code = v.zgen_zak
LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_8    -- SHORTCUT_TO_RDSD_SOLDTO_8
       ON n_shortcut_to_rdsd_soldto_8.code = v.zpkr_subp
LEFT JOIN t2311391   n_rdsd_zshifr                  -- RDSD_ZSHIFR
       ON n_rdsd_zshifr.zshifr = v.name
LEFT JOIN t2355657   n_rdsd_zobjem                  -- RDSD_ZOBJEM
       ON n_rdsd_zobjem.zobjem = v.name
LEFT JOIN t2356315   n_rdsd_zphd_sr                 -- RDSD_ZPHD_SR
       ON n_rdsd_zphd_sr.zphd_sr = v.zphd_sr
LEFT JOIN t2311629   n_rdsd_zphd_grsr               -- RDSD_ZPHD_GRSR
       ON n_rdsd_zphd_grsr.zphd_grsr = v.zphd_grsr
LEFT JOIN t2290906   n_rdsd_zgaz_type               -- RDSD_ZGAZ_TYPE
       ON n_rdsd_zgaz_type.code = v.zgaz_type
LEFT JOIN t2307768   n_rdsd_zaviatype               -- RDSD_ZAVIATYPE
       ON n_rdsd_zaviatype.zaviatype = v.zaviatype

-- ==== связи, подтверждённые заказчиком ====
-- СП: ключ SP лежит в TBL_FAP_MULT, значит доступен как v.sp
LEFT JOIN t2312312 n_plant                          -- RDSD_PLANT
       ON n_plant.plant = v.sp
-- Тип периода: v.period_type (в боковике period_type)
LEFT JOIN t2317517 n_period_type                    -- DIC_TYPE_PERIOD
       ON n_period_type.id = v.period_type
-- ТЭП: ключ zlib_indc боковика -> RDSD_INDS.code, наименование SNAME
LEFT JOIN t1895280 n_inds                           -- RDSD_INDS
       ON n_inds.code = v.zlib_indc
      AND n_inds.date_from <> 'invalid_date'
-- Вид деятельности: опосредованно через n_inds.actvts -> RDSD_ACTVTS.code_value
LEFT JOIN t2494931 n_actvts                         -- RDSD_ACTVTS
       ON n_actvts.code_value = n_inds.actvts
-- Владелец: опосредованно через n_inds.owner -> RDSD_OWNERS.key
LEFT JOIN t2364976 n_owners                         -- RDSD_OWNERS
       ON n_owners.key = n_inds.owner

LIMIT 20;