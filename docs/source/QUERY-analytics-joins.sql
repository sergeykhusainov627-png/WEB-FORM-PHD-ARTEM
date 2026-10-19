-- Блок LEFT JOIN к справочникам наименований (реестр dict-tables.md + лист «Вывод полей в отчете»).
-- Вставлять после inline-версии VIEW_PHD_MULT как CTE src:  FROM src D  LEFT JOIN ...
-- Условие даты: начало года отчёта (CALYEAR) попадает в интервал действия записи.

    LEFT JOIN t2312312 n_rdsd_plant ON n_rdsd_plant.plant = D.sp
    LEFT JOIN t1913698 n_dict_phd_left ON n_dict_phd_left.KEY = D.zlib_indc
    LEFT JOIN t1895280 n_rdsd_inds ON n_rdsd_inds.code = D.sname AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_inds.datefrom AND n_rdsd_inds.dateto AND n_rdsd_inds.date_from <> 'invalid_date'
    LEFT JOIN t2322857 n_rdsd_vendor ON n_rdsd_vendor.vendor = D.vendor
    LEFT JOIN t2301822 n_rdsd_soldto ON n_rdsd_soldto.code = D.key
    LEFT JOIN t2306331 n_rdsd_zhrgrpmo ON n_rdsd_zhrgrpmo.zhrgrpmo = D.zhrgrpmo
    LEFT JOIN t2320954 n_rdsd_profit_ctr ON n_rdsd_profit_ctr.profit_ctr = D.profit_ctr
    LEFT JOIN t2355561 n_rdsd_zorgu ON n_rdsd_zorgu.zorgu = D.zorgu AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zorgu.datefrom AND n_rdsd_zorgu.dateto
    LEFT JOIN t2310122 n_rdsd_zph_usr0 ON n_rdsd_zph_usr0.zph_usr0 = D.code_zph_usr0 AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zph_usr0.zbegda AND n_rdsd_zph_usr0.zendda
    LEFT JOIN t2320948 n_rdsd_acttype ON n_rdsd_acttype.acttype = D.acttype AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto
    LEFT JOIN t2383584 n_rdsd_zequi ON n_rdsd_zequi.zequi = D.zequi AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto
    LEFT JOIN t2308461 n_rdsd_zclsvobor ON n_rdsd_zclsvobor.zclsvo_b or = D.zclsvobor
    LEFT JOIN t2321329 n_rdsd_material ON n_rdsd_material.material = D.material
    LEFT JOIN t2355739 n_rdsd_zfunc_loc ON n_rdsd_zfunc_loc.zfunc_loc = D.zfunc_loc AND to_date(D.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zfunc_loc.datefrom AND n_rdsd_zfunc_loc.dateto
    LEFT JOIN t2308973 n_rdsd_zsiu_fld ON n_rdsd_zsiu_fld.zsiu_fld = D.zsiu_fld
    LEFT JOIN t2337709 n_rdsd_posid ON n_rdsd_posid.posid = D.posid
    LEFT JOIN t1895288 n_rdsd_infosystem ON n_rdsd_infosystem.code_value = D.zlib_infs
    LEFT JOIN t2317517 n_dic_type_period ON n_dic_type_period.— = D.period_ty
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_3 ON n_shortcut_to_rdsd_soldto_3.code = D.zphd_usl1
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto ON n_shortcut_to_rdsd_soldto.code = D.zdebitor
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_2 ON n_shortcut_to_rdsd_soldto_2.code = D.zph_eso2
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_4 ON n_shortcut_to_rdsd_soldto_4.code = D.zph_epok
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_5 ON n_shortcut_to_rdsd_soldto_5.code = D.zphd_sk
    LEFT JOIN t2307584 n_rdsd_ucvoltlevl ON n_rdsd_ucvoltlevl.ucvoltlevl = D.ucvoltlevl
    LEFT JOIN t2307584 n_shortcut_to_rdsd_ucvoltlevl ON n_shortcut_to_rdsd_ucvoltlevl.key = D.zucvolttr
    LEFT JOIN t2307947 n_rdsd_z_cl_napr ON n_rdsd_z_cl_napr.z_cl_napr = D.z_cl_napr
    LEFT JOIN t2307875 n_rdsd_zsiu_ty ON n_rdsd_zsiu_ty.zsiu_ty = D.zsiu_ty
    LEFT JOIN t2320979 n_rdsd_zbur_lu ON n_rdsd_zbur_lu.code = D.zbur_lu
    LEFT JOIN t2311573 n_rdsd_zbur_area ON n_rdsd_zbur_area.zbur_area = D.zbur_area
    LEFT JOIN t237842 n_rdsd_zbur_plst ON n_rdsd_zbur_plst.zbur_plst = D.zbur_plst
    LEFT JOIN t2311619 n_rdsd_zph_tehk ON n_rdsd_zph_tehk.code = D.name
    LEFT JOIN t2311231 n_rdsd_zskv_st ON n_rdsd_zskv_st.zskv_st = D.name
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_7 ON n_shortcut_to_rdsd_soldto_7.code = D.zgen_pod
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_6 ON n_shortcut_to_rdsd_soldto_6.code = D.zgen_zak
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_8 ON n_shortcut_to_rdsd_soldto_8.code = D.zpkr_subp
    LEFT JOIN t2311391 n_rdsd_zshifr ON n_rdsd_zshifr.zshifr = D.name
    LEFT JOIN t2355657 n_rdsd_zobjem ON n_rdsd_zobjem.zobjem = D.name
    LEFT JOIN t2356315 n_rdsd_zphd_sr ON n_rdsd_zphd_sr.zphd_sr = D.zphd_sr
    LEFT JOIN t2311629 n_rdsd_zphd_grsr ON n_rdsd_zphd_grsr.zphd_grsr = D.zphd_grsr
    LEFT JOIN t2290906 n_rdsd_zgaz_type ON n_rdsd_zgaz_type.code = D.zgaz_type
    LEFT JOIN t2307768 n_rdsd_zaviatype ON n_rdsd_zaviatype.zaviatype = D.zaviatype
    LEFT JOIN t2335720 n_rdsd_zphd_spr ON n_rdsd_zphd_spr.zphd_spr = D.zphd_nop1 при zphd_spr = gtm_skv
    LEFT JOIN t2494931 n_rdsd_actvts ON n_rdsd_actvts.code_value = D.actvts
    LEFT JOIN t2364976 n_rdsd_owners ON n_rdsd_owners.key = D.owner
