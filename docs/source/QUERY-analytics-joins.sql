-- Блок LEFT JOIN к справочникам наименований (реестр dict-tables.md + лист «Вывод полей в отчете»).
-- Цели соединений сверены со списком колонок боковика t1913698 (файл «Поля боковика»).
-- Условие даты: начало года отчёта (CALYEAR) попадает в интервал действия записи.

LEFT JOIN t2322857   n_rdsd_vendor                -- RDSD_VENDOR
       ON n_rdsd_vendor.vendor = v.vendor

LEFT JOIN t2301822   n_rdsd_soldto                -- RDSD_SOLDTO
       ON n_rdsd_soldto.code = v.key

LEFT JOIN t2306331   n_rdsd_zhrgrpmo              -- RDSD_ZHRGRPMO
       ON n_rdsd_zhrgrpmo.zhrgrpmo = v.zhrgrpmo

LEFT JOIN t2320954   n_rdsd_profit_ctr            -- RDSD_PROFIT_CTR
       ON n_rdsd_profit_ctr.profit_ctr = v.profit_ctr

LEFT JOIN t2320948   n_rdsd_acttype               -- RDSD_ACTTYPE
       ON n_rdsd_acttype.acttype = v.acttype
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto

LEFT JOIN t2383584   n_rdsd_zequi                 -- RDSD_ZEQUI
       ON n_rdsd_zequi.zequi = v.zequi
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto

LEFT JOIN t2308461   n_rdsd_zclsvobor             -- RDSD_ZCLSVOBOR
       ON n_rdsd_zclsvobor.zclsvo_b or = v.zclsvobor

LEFT JOIN t2321329   n_rdsd_material              -- RDSD_MATERIAL
       ON n_rdsd_material.material = v.material

LEFT JOIN t2355739   n_rdsd_zfunc_loc             -- RDSD_ZFUNC_LOC
       ON n_rdsd_zfunc_loc.zfunc_loc = v.zfunc_loc
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zfunc_loc.datefrom AND n_rdsd_zfunc_loc.dateto

LEFT JOIN t2308973   n_rdsd_zsiu_fld              -- RDSD_ZSIU_FLD
       ON n_rdsd_zsiu_fld.zsiu_fld = v.zsiu_fld

LEFT JOIN t2337709   n_rdsd_posid                 -- RDSD_POSID
       ON n_rdsd_posid.posid = v.posid

LEFT JOIN t1895288   n_rdsd_infosystem            -- RDSD_INFOSYSTEM
       ON n_rdsd_infosystem.code_value = v.zlib_infs

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_3  -- SHORTCUT_TO_RDSD_SOLDTO_3
       ON n_shortcut_to_rdsd_soldto_3.code = v.zphd_usl1

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto    -- SHORTCUT_TO_RDSD_SOLDTO
       ON n_shortcut_to_rdsd_soldto.code = v.zdebitor

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_2  -- SHORTCUT_TO_RDSD_SOLDTO_2
       ON n_shortcut_to_rdsd_soldto_2.code = v.zph_eso2

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_4  -- SHORTCUT_TO_RDSD_SOLDTO_4
       ON n_shortcut_to_rdsd_soldto_4.code = v.zph_epok

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_5  -- SHORTCUT_TO_RDSD_SOLDTO_5
       ON n_shortcut_to_rdsd_soldto_5.code = v.zphd_sk

LEFT JOIN t2307584   n_rdsd_ucvoltlevl            -- RDSD_UCVOLTLEVL
       ON n_rdsd_ucvoltlevl.ucvoltlevl = v.ucvoltlevl

LEFT JOIN t2307584   n_shortcut_to_rdsd_ucvoltlevl -- SHORTCUT_TO_RDSD_UCVOLTLEVL
       ON n_shortcut_to_rdsd_ucvoltlevl.key = v.zucvolttr

LEFT JOIN t2307947   n_rdsd_z_cl_napr             -- RDSD_Z_CL_NAPR
       ON n_rdsd_z_cl_napr.z_cl_napr = v.z_cl_napr

LEFT JOIN t2307875   n_rdsd_zsiu_ty               -- RDSD_ZSIU_TY
       ON n_rdsd_zsiu_ty.zsiu_ty = v.zsiu_ty

LEFT JOIN t2320979   n_rdsd_zbur_lu               -- RDSD_ZBUR_LU
       ON n_rdsd_zbur_lu.code = v.zbur_lu

LEFT JOIN t2311573   n_rdsd_zbur_area             -- RDSD_ZBUR_AREA
       ON n_rdsd_zbur_area.zbur_area = v.zbur_area

LEFT JOIN t237842    n_rdsd_zbur_plst             -- RDSD_ZBUR_PLST
       ON n_rdsd_zbur_plst.zbur_plst = v.zbur_plst

LEFT JOIN t2311619   n_rdsd_zph_tehk              -- RDSD_ZPH_TEHK
       ON n_rdsd_zph_tehk.code = v.name

LEFT JOIN t2311231   n_rdsd_zskv_st               -- RDSD_ZSKV_ST
       ON n_rdsd_zskv_st.zskv_st = v.name

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_7  -- SHORTCUT_TO_RDSD_SOLDTO_7
       ON n_shortcut_to_rdsd_soldto_7.code = v.zgen_pod

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_6  -- SHORTCUT_TO_RDSD_SOLDTO_6
       ON n_shortcut_to_rdsd_soldto_6.code = v.zgen_zak

LEFT JOIN t2301822   n_shortcut_to_rdsd_soldto_8  -- SHORTCUT_TO_RDSD_SOLDTO_8
       ON n_shortcut_to_rdsd_soldto_8.code = v.zpkr_subp

LEFT JOIN t2311391   n_rdsd_zshifr                -- RDSD_ZSHIFR
       ON n_rdsd_zshifr.zshifr = v.name

LEFT JOIN t2355657   n_rdsd_zobjem                -- RDSD_ZOBJEM
       ON n_rdsd_zobjem.zobjem = v.name

LEFT JOIN t2356315   n_rdsd_zphd_sr               -- RDSD_ZPHD_SR
       ON n_rdsd_zphd_sr.zphd_sr = v.zphd_sr

LEFT JOIN t2311629   n_rdsd_zphd_grsr             -- RDSD_ZPHD_GRSR
       ON n_rdsd_zphd_grsr.zphd_grsr = v.zphd_grsr

LEFT JOIN t2290906   n_rdsd_zgaz_type             -- RDSD_ZGAZ_TYPE
       ON n_rdsd_zgaz_type.code = v.zgaz_type

LEFT JOIN t2307768   n_rdsd_zaviatype             -- RDSD_ZAVIATYPE
       ON n_rdsd_zaviatype.zaviatype = v.zaviatype
