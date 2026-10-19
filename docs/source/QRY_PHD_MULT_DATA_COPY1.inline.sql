/*
   Запрос QRY_PHD_MULT_DATA_COPY1 — версия БЕЗ VIEW_PHD_MULT (inline-источник) и с наименованиями/ключами аналитик.
   Параметры:
     :ANALYTIC_SET — массив строк: аналитики/пары «ключ, наименование» (формирует форма)
     :EXTRA_FIELDS — массив строк: динамические колонки периодов и статусов (с псевдонимами)
     :EXTRA_NAMES  — массив строк: их псевдонимы для финальной проекции
     :P_STATUS     — 1/0: признак чек-бокса «Выводить информацию по статусам»
     + все фильтры СЭ (PLANT, CALYEAR, ZLIB_INDC, …)
   Источник: t1913698 (НСИ DICT_PHD_LEFT, IS_TEMPORARY = 2) + TBL_FAP_MULT (факты).
   Наименования аналитик — LEFT JOIN к справочникам по реестру dict-tables.md (условие даты: начало CALYEAR в интервале).
*/
WITH
-- 0. Формы ТЭП СНГ (агрегат по TBL_ZIDNFORM)
Forms_Agg AS (
    SELECT ZLIB_INDC, GJAHR, PLANT,
           STRING_AGG(DISTINCT ZF_NUMB, ', ') FILTER (WHERE ZF_NUMB IS NOT NULL AND ZF_NUMB <> '') AS forms_text
    FROM TBL_ZIDNFORM
    WHERE ZLIB_INDC IN (:ZLIB_INDC) AND GJAHR IN (:CALYEAR) AND PLANT IN (:PLANT)
    GROUP BY ZLIB_INDC, GJAHR, PLANT
),
-- 1. Источник вместо VIEW_PHD_MULT: та же выборка, плюс фильтры СЭ внутри CTE (чтобы не было неоднозначности с join'ами)
src AS (
    SELECT D.*, TBL.zsiu_indv, TBL.zvalue_sng, TBL.period, TBL.zphd_stat, TBL.zind_sche, TBL.key_connect
    FROM t1913698 D
    JOIN TBL_FAP_MULT TBL
      ON D."KEY" = TBL.KEY_CONNECT AND TBL.plant = D.plant AND TBL.year = D.calyear
    WHERE D.IS_TEMPORARY = 2
AND           
     	          (D.PLANT 		    	IN (:PLANT) 	 							OR COALESCE(:PLANT,'')='') 
        AND (D.ZLIB_INDC	    	IN (:ZLIB_INDC)  							OR COALESCE(:ZLIB_INDC,'')='') 
        AND (D.CALYEAR 	    	IN (:CALYEAR) 	 							OR COALESCE(:CALYEAR,'')='') 
        AND (TBL.ZPHD_STAT     	IN (:ZPHD_STAT)   							OR COALESCE(:ZPHD_STAT,'')='')
        AND (D.ZTYPEIND     	IN (:ZTYPEIND)   							OR COALESCE(:ZTYPEIND,'')='')
        AND (D.VENDOR 	    	IN (:VENDOR) 	  							OR COALESCE(:VENDOR,'')='') 
        AND (D.SOLD_TO 	    	IN (:SOLD_TO) 	  							OR COALESCE(:SOLD_TO,'')='') 
        AND (D.ZHRGRPMO       	IN (:ZHRGRPMO) 	  						OR COALESCE(:ZHRGRPMO,'')='') 
        AND (D.PROFIT_CTR     	IN (:PROFIT_CTR)  							OR COALESCE(:PROFIT_CTR,'')='') 
        AND (D.COSTCENTER     IN (:COSTCENTER)  						OR COALESCE(:COSTCENTER,'')='') 
        AND (D.ZORGUNIT 	    	IN (:ZORGUNIT) 	  						OR COALESCE(:ZORGUNIT,'')='') 
        AND (D.ZPH_USR2 	    	IN (:ZPH_USR2) 	  						OR COALESCE(:ZPH_USR2,'')='') 
        AND (D.ACTTYPE  	    	IN (:ACTTYPE) 	  							OR COALESCE(:ACTTYPE,'')='') 
        AND (D.ZEQUI 		    	IN (:ZEQUI) 	  								OR COALESCE(:ZEQUI,'')='') 
        AND (D.ZCLSVOBOR      	IN (:ZCLSVOBOR)   							OR COALESCE(:ZCLSVOBOR,'')='') 
        AND (D.MATERIAL 	    	IN (:MATERIAL) 	  						OR COALESCE(:MATERIAL,'')='') 
        AND (D.ZFUNC_LOC 	    	IN (:ZFUNC_LOC)   							OR COALESCE(:ZFUNC_LOC,'')='') 
        AND (D.ZSIU_FLD 	    	IN (:ZSIU_FLD)    							OR COALESCE(:ZSIU_FLD,'')='') 
        AND (D.POSID 		    	IN (:POSID) 	  								OR COALESCE(:POSID,'')='') 
        AND (D.ZLIB_INFS 	    	IN (:ZLIB_INFS)   							OR COALESCE(:ZLIB_INFS,'')='') 
        AND (D.PERIOD_TYPE    IN (:PERIOD_TYPE) 						OR COALESCE(:PERIOD_TYPE,'')='') 
        AND (D.ZPHD_DOG 	    	IN (:ZPHD_DOG) 	  						OR COALESCE(:ZPHD_DOG,'')='') 
        AND (D.ZPHD_USL1 	    	IN (:ZPHD_USL1)   							OR COALESCE(:ZPHD_USL1,'')='') 
        AND (D.ZDEBITOR 	    	IN (:ZDEBITOR) 	  						OR COALESCE(:ZDEBITOR,'')='') 
        AND (D.ZPH_ESO2 	    	IN (:ZPH_ESO2) 	  						OR COALESCE(:ZPH_ESO2,'')='') 
        AND (D.ZPHD_SK 	    	IN (:ZPHD_SK) 	  							OR COALESCE(:ZPHD_SK,'')='') 
        AND (D.UCVOLTLEVL     	IN (:UCVOLTLEVL)  							OR COALESCE(:UCVOLTLEVL,'')='') 
        AND (D.ZUCVOLTTR      	IN (:ZUCVOLTTR)   							OR COALESCE(:ZUCVOLTTR,'')='') 
        AND (D.Z_CL_NAPR      	IN (:Z_CL_NAPR)   							OR COALESCE(:Z_CL_NAPR,'')='') 
        AND (D.ZSIU_TY 	    	IN (:ZSIU_TY)     							OR COALESCE(:ZSIU_TY,'')='') 
        AND (D.ZDOGLINK 	    	IN (:ZDOGLINK) 	  						OR COALESCE(:ZDOGLINK,'')='') 
        AND (D.ZBUR_LU 	    	IN (:ZBUR_LU) 	  							OR COALESCE(:ZBUR_LU,'')='') 
        AND (D.ZBUR_AREA      	IN (:ZBUR_AREA)   							OR COALESCE(:ZBUR_AREA,'')='') 
        AND (D.ZSKV_KUST 	   	IN (:ZSKV_KUST)   							OR COALESCE(:ZSKV_KUST,'')='') 
        AND (D.Z_SKV_GEO 	  	IN (:Z_SKV_GEO)   							OR COALESCE(:Z_SKV_GEO,'')='') 
        AND (D.ZBUR_PLST 	   	IN (:ZBUR_PLST)   							OR COALESCE(:ZBUR_PLST,'')='') 
        AND (D.ZPH_TEHK 	   	IN (:ZPH_TEHK) 	  						OR COALESCE(:ZPH_TEHK,'')='') 
        AND (D.ZPH_OPLST 	    	IN (:ZPH_OPLST)   							OR COALESCE(:ZPH_OPLST,'')='') 
        AND (D.ZPHD_COMM      IN (:ZPHD_COMM)   						OR COALESCE(:ZPHD_COMM,'')='') 
        AND (TO_DATE(D.ZBUR_BEG, 'YYYY-MM-DD') 
							IN (TO_DATE(:ZBUR_BEG, 'YYYY-MM-DD')) 	OR COALESCE(:ZBUR_BEG,'')='') 
        AND (D.ZPILOT 	    		IN (:ZPILOT) 	  							OR COALESCE(:ZPILOT,'')='') 
        AND (D.ZSKV_ST 	    	IN (:ZSKV_ST) 	  							OR COALESCE(:ZSKV_ST,'')='') 
        AND (D.ZGEN_POD 	    	IN (:ZGEN_POD) 	  						OR COALESCE(:ZGEN_POD,'')='') 
        AND (D.ZGEN_ZAK 	    	IN (:ZGEN_ZAK) 	  						OR COALESCE(:ZGEN_ZAK,'')='') 
        AND (D.ZSHIFR 			IN (:ZSHIFR) 	  							OR COALESCE(:ZSHIFR,'')='') 
        AND (D.ZOBJEM 	    		IN (:ZOBJEM) 	  							OR COALESCE(:ZOBJEM,'')='') 
        AND (D.ZPHD_SR 	    	IN (:ZPHD_SR) 	  							OR COALESCE(:ZPHD_SR,'')='') 
        AND (D.ZPHD_GRSR      IN (:ZPHD_GRSR)   							OR COALESCE(:ZPHD_GRSR,'')='') 
        AND (D.ZGAZ_TYPE 	    	IN (:ZGAZ_TYPE)   							OR COALESCE(:ZGAZ_TYPE,'')='') 
        AND (D.ZAVIATYPE 	    	IN (:ZAVIATYPE)   							OR COALESCE(:ZAVIATYPE,'')='') 
        AND (D.ZPHD_NCH 	    	IN (:ZPHD_NCH) 	  						OR COALESCE(:ZPHD_NCH,'')='') 
        AND (D.ZPHD_SPR 	    	IN (:ZPHD_SPR) 	  						OR COALESCE(:ZPHD_SPR,'')='') 
	 AND (D.ZINDTXT1 	    	ILIKE '%' || :ZINDTXT1 || '%' 					OR COALESCE(:ZINDTXT1,'')='') -- поиск по маске

    
),
-- 2. Основной расчёт: аналитики/наименования/ключи + динамические колонки периодов и статусов
Main_Data AS (
    SELECT
        :ANALYTIC_SET,
        (SELECT t.ACTVTS FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Код вида деятельности",
        (SELECT t.SNAME FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Наименование вида деятельности",
        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS "Формы ТЭП СНГ",
        :EXTRA_FIELDS
    FROM src v
    -- наименования/ключи аналитик: соединения со справочниками (проверено на стенде)
LEFT JOIN t2322857   n_rdsd_vendor                  -- RDSD_VENDOR
       ON n_rdsd_vendor.vendor = v.vendor
LEFT JOIN t2301822   n_rdsd_soldto                  -- RDSD_SOLDTO
       ON n_rdsd_soldto.code = v.sold_to
LEFT JOIN t2306331   n_rdsd_zhrgrpmo                -- RDSD_ZHRGRPMO
       ON n_rdsd_zhrgrpmo.zhrgrpmo = v.zhrgrpmo
LEFT JOIN t2320954   n_rdsd_profit_ctr              -- RDSD_PROFIT_CTR
       ON n_rdsd_profit_ctr.profit_ctr = v.profit_ctr
LEFT JOIN t2320948   n_rdsd_acttype                 -- RDSD_ACTTYPE
       ON n_rdsd_acttype.acttype = v.acttype
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto
LEFT JOIN t2338354   n_rdsd_zequi                   -- RDSD_ZEQUI
       ON n_rdsd_zequi.zequi = v.zequi
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto
LEFT JOIN t2308461   n_rdsd_zclsvobor               -- RDSD_ZCLSVOBOR
       ON n_rdsd_zclsvobor.zclsvobor = v.zclsvobor
LEFT JOIN t2321329   n_rdsd_material                -- RDSD_MATERIAL
       ON n_rdsd_material.material = v.material
LEFT JOIN t2335739   n_rdsd_zfunc_loc               -- RDSD_ZFUNC_LOC
       ON n_rdsd_zfunc_loc.zfunc_loc = v.zfunc_loc
      AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD')
          BETWEEN n_rdsd_zfunc_loc.datefrom::date AND n_rdsd_zfunc_loc.dateto::date
LEFT JOIN t2320973   n_rdsd_zsiu_fld                -- RDSD_ZSIU_FLD
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
       ON n_shortcut_to_rdsd_ucvoltlevl.ucvoltlevl = v.zucvolttr --------------------------------------проверить
LEFT JOIN t2307947   n_rdsd_z_cl_napr               -- RDSD_Z_CL_NAPR
       ON n_rdsd_z_cl_napr.z_cl_napr = v.z_cl_napr
LEFT JOIN t2307875   n_rdsd_zsiu_ty                 -- RDSD_ZSIU_TY
       ON n_rdsd_zsiu_ty.zsiu_ty = v.zsiu_ty
LEFT JOIN t2320979   n_rdsd_zbur_lu                 -- RDSD_ZBUR_LU
       ON n_rdsd_zbur_lu.code = v.zbur_lu
LEFT JOIN t2311573   n_rdsd_zbur_area               -- RDSD_ZBUR_AREA
       ON n_rdsd_zbur_area.zbur_area = v.zbur_area
LEFT JOIN t2337842    n_rdsd_zbur_plst               -- RDSD_ZBUR_PLST
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
LEFT JOIN t2335657   n_rdsd_zobjem                  -- RDSD_ZOBJEM
       ON n_rdsd_zobjem.zobjem = v.name
LEFT JOIN t2335635   n_rdsd_zphd_sr                 -- RDSD_ZPHD_SR
       ON n_rdsd_zphd_sr.zphd_sr = v.zphd_sr
LEFT JOIN t2311629   n_rdsd_zphd_grsr               -- RDSD_ZPHD_GRSR
       ON n_rdsd_zphd_grsr.zphd_grsr = v.zphd_grsr
LEFT JOIN t2290906   n_rdsd_zgaz_type               -- RDSD_ZGAZ_TYPE
       ON n_rdsd_zgaz_type.code = v.zgaz_type
LEFT JOIN t2307768   n_rdsd_zaviatype               -- RDSD_ZAVIATYPE
       ON n_rdsd_zaviatype.zaviatype = v.zaviatype


LEFT JOIN t2321022 n_zph_usr0
	on n_zph_usr0.zph_usr0 = v.zph_usr2 --------------------------------------------------------проверить
-- СП: ключ SP лежит в TBL_FAP_MULT, значит доступен как v.sp
LEFT JOIN t2312312 n_plant                          -- RDSD_PLANT
       ON n_plant.plant = v.plant
-- Тип периода: v.period_type (в боковике period_type)
LEFT JOIN t2317517 n_period_type                    -- DIC_TYPE_PERIOD
       ON n_period_type.id = v.period_type
-- ТЭП: ключ zlib_indc боковика -> RDSD_INDS.code, наименование SNAME
LEFT JOIN t1895280 n_inds                           -- RDSD_INDS
       ON n_inds.code = v.zlib_indc
-- Вид деятельности: опосредованно через n_inds.actvts -> RDSD_ACTVTS.code_value
LEFT JOIN t2494391 n_actvts                         -- RDSD_ACTVTS
       ON n_actvts.code_value = n_inds.actvts
-- Владелец: опосредованно через n_inds.owner -> RDSD_OWNERS.key
LEFT JOIN t2364976 n_owners                         -- RDSD_OWNERS
       ON n_owners."KEY" = n_inds.owner
    GROUP BY ZLIB_INDC, GJAHR, PLANT
),
-- 1. Источник вместо VIEW_PHD_MULT: та же выборка, плюс фильтры СЭ внутри CTE (чтобы не было неоднозначности с join'ами)
src AS (
    SELECT D.*, TBL.zsiu_indv, TBL.zvalue_sng, TBL.period, TBL.zphd_stat, TBL.zind_sche, TBL.key_connect
    FROM t1913698 D
    JOIN TBL_FAP_MULT TBL
      ON D."KEY" = TBL.KEY_CONNECT AND TBL.plant = D.plant AND TBL.year = D.calyear
    WHERE D.IS_TEMPORARY = 2
AND           
     	          (D.PLANT 		    	IN (:PLANT) 	 							OR COALESCE(:PLANT,'')='') 
        AND (D.ZLIB_INDC	    	IN (:ZLIB_INDC)  							OR COALESCE(:ZLIB_INDC,'')='') 
        AND (D.CALYEAR 	    	IN (:CALYEAR) 	 							OR COALESCE(:CALYEAR,'')='') 
        AND (TBL.ZPHD_STAT     	IN (:ZPHD_STAT)   							OR COALESCE(:ZPHD_STAT,'')='')
        AND (D.ZTYPEIND     	IN (:ZTYPEIND)   							OR COALESCE(:ZTYPEIND,'')='')
        AND (D.VENDOR 	    	IN (:VENDOR) 	  							OR COALESCE(:VENDOR,'')='') 
        AND (D.SOLD_TO 	    	IN (:SOLD_TO) 	  							OR COALESCE(:SOLD_TO,'')='') 
        AND (D.ZHRGRPMO       	IN (:ZHRGRPMO) 	  						OR COALESCE(:ZHRGRPMO,'')='') 
        AND (D.PROFIT_CTR     	IN (:PROFIT_CTR)  							OR COALESCE(:PROFIT_CTR,'')='') 
        AND (D.COSTCENTER     IN (:COSTCENTER)  						OR COALESCE(:COSTCENTER,'')='') 
        AND (D.ZORGUNIT 	    	IN (:ZORGUNIT) 	  						OR COALESCE(:ZORGUNIT,'')='') 
        AND (D.ZPH_USR2 	    	IN (:ZPH_USR2) 	  						OR COALESCE(:ZPH_USR2,'')='') 
        AND (D.ACTTYPE  	    	IN (:ACTTYPE) 	  							OR COALESCE(:ACTTYPE,'')='') 
        AND (D.ZEQUI 		    	IN (:ZEQUI) 	  								OR COALESCE(:ZEQUI,'')='') 
        AND (D.ZCLSVOBOR      	IN (:ZCLSVOBOR)   							OR COALESCE(:ZCLSVOBOR,'')='') 
        AND (D.MATERIAL 	    	IN (:MATERIAL) 	  						OR COALESCE(:MATERIAL,'')='') 
        AND (D.ZFUNC_LOC 	    	IN (:ZFUNC_LOC)   							OR COALESCE(:ZFUNC_LOC,'')='') 
        AND (D.ZSIU_FLD 	    	IN (:ZSIU_FLD)    							OR COALESCE(:ZSIU_FLD,'')='') 
        AND (D.POSID 		    	IN (:POSID) 	  								OR COALESCE(:POSID,'')='') 
        AND (D.ZLIB_INFS 	    	IN (:ZLIB_INFS)   							OR COALESCE(:ZLIB_INFS,'')='') 
        AND (D.PERIOD_TYPE    IN (:PERIOD_TYPE) 						OR COALESCE(:PERIOD_TYPE,'')='') 
        AND (D.ZPHD_DOG 	    	IN (:ZPHD_DOG) 	  						OR COALESCE(:ZPHD_DOG,'')='') 
        AND (D.ZPHD_USL1 	    	IN (:ZPHD_USL1)   							OR COALESCE(:ZPHD_USL1,'')='') 
        AND (D.ZDEBITOR 	    	IN (:ZDEBITOR) 	  						OR COALESCE(:ZDEBITOR,'')='') 
        AND (D.ZPH_ESO2 	    	IN (:ZPH_ESO2) 	  						OR COALESCE(:ZPH_ESO2,'')='') 
        AND (D.ZPHD_SK 	    	IN (:ZPHD_SK) 	  							OR COALESCE(:ZPHD_SK,'')='') 
        AND (D.UCVOLTLEVL     	IN (:UCVOLTLEVL)  							OR COALESCE(:UCVOLTLEVL,'')='') 
        AND (D.ZUCVOLTTR      	IN (:ZUCVOLTTR)   							OR COALESCE(:ZUCVOLTTR,'')='') 
        AND (D.Z_CL_NAPR      	IN (:Z_CL_NAPR)   							OR COALESCE(:Z_CL_NAPR,'')='') 
        AND (D.ZSIU_TY 	    	IN (:ZSIU_TY)     							OR COALESCE(:ZSIU_TY,'')='') 
        AND (D.ZDOGLINK 	    	IN (:ZDOGLINK) 	  						OR COALESCE(:ZDOGLINK,'')='') 
        AND (D.ZBUR_LU 	    	IN (:ZBUR_LU) 	  							OR COALESCE(:ZBUR_LU,'')='') 
        AND (D.ZBUR_AREA      	IN (:ZBUR_AREA)   							OR COALESCE(:ZBUR_AREA,'')='') 
        AND (D.ZSKV_KUST 	   	IN (:ZSKV_KUST)   							OR COALESCE(:ZSKV_KUST,'')='') 
        AND (D.Z_SKV_GEO 	  	IN (:Z_SKV_GEO)   							OR COALESCE(:Z_SKV_GEO,'')='') 
        AND (D.ZBUR_PLST 	   	IN (:ZBUR_PLST)   							OR COALESCE(:ZBUR_PLST,'')='') 
        AND (D.ZPH_TEHK 	   	IN (:ZPH_TEHK) 	  						OR COALESCE(:ZPH_TEHK,'')='') 
        AND (D.ZPH_OPLST 	    	IN (:ZPH_OPLST)   							OR COALESCE(:ZPH_OPLST,'')='') 
        AND (D.ZPHD_COMM      IN (:ZPHD_COMM)   						OR COALESCE(:ZPHD_COMM,'')='') 
        AND (TO_DATE(D.ZBUR_BEG, 'YYYY-MM-DD') 
							IN (TO_DATE(:ZBUR_BEG, 'YYYY-MM-DD')) 	OR COALESCE(:ZBUR_BEG,'')='') 
        AND (D.ZPILOT 	    		IN (:ZPILOT) 	  							OR COALESCE(:ZPILOT,'')='') 
        AND (D.ZSKV_ST 	    	IN (:ZSKV_ST) 	  							OR COALESCE(:ZSKV_ST,'')='') 
        AND (D.ZGEN_POD 	    	IN (:ZGEN_POD) 	  						OR COALESCE(:ZGEN_POD,'')='') 
        AND (D.ZGEN_ZAK 	    	IN (:ZGEN_ZAK) 	  						OR COALESCE(:ZGEN_ZAK,'')='') 
        AND (D.ZSHIFR 			IN (:ZSHIFR) 	  							OR COALESCE(:ZSHIFR,'')='') 
        AND (D.ZOBJEM 	    		IN (:ZOBJEM) 	  							OR COALESCE(:ZOBJEM,'')='') 
        AND (D.ZPHD_SR 	    	IN (:ZPHD_SR) 	  							OR COALESCE(:ZPHD_SR,'')='') 
        AND (D.ZPHD_GRSR      IN (:ZPHD_GRSR)   							OR COALESCE(:ZPHD_GRSR,'')='') 
        AND (D.ZGAZ_TYPE 	    	IN (:ZGAZ_TYPE)   							OR COALESCE(:ZGAZ_TYPE,'')='') 
        AND (D.ZAVIATYPE 	    	IN (:ZAVIATYPE)   							OR COALESCE(:ZAVIATYPE,'')='') 
        AND (D.ZPHD_NCH 	    	IN (:ZPHD_NCH) 	  						OR COALESCE(:ZPHD_NCH,'')='') 
        AND (D.ZPHD_SPR 	    	IN (:ZPHD_SPR) 	  						OR COALESCE(:ZPHD_SPR,'')='') 
	 AND (D.ZINDTXT1 	    	ILIKE '%' || :ZINDTXT1 || '%' 					OR COALESCE(:ZINDTXT1,'')='') -- поиск по маске

    
),
-- 2. Основной расчёт: аналитики/наименования/ключи + динамические колонки периодов и статусов
Main_Data AS (
    SELECT
        :ANALYTIC_SET,
        (SELECT t.ACTVTS FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Код вида деятельности",
        (SELECT t.SNAME FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Наименование вида деятельности",
        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS "Формы ТЭП СНГ",
        :EXTRA_FIELDS
    FROM src v
-- Блок LEFT JOIN к справочникам наименований (реестр dict-tables.md + лист «Вывод полей в отчете»).
-- Вставлять после inline-версии VIEW_PHD_MULT как CTE src:  FROM src D  LEFT JOIN ...
    LEFT JOIN t2312312 n_rdsd_plant ON n_rdsd_plant.plant = v.sp  -- RDSD_PLANT
    LEFT JOIN t1895280 n_rdsd_inds ON n_rdsd_inds.code = v.sname AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_inds.datefrom AND n_rdsd_inds.dateto AND n_rdsd_inds.date_from <> 'invalid_date'  -- RDSD_INDS
    LEFT JOIN t2322857 n_rdsd_vendor ON n_rdsd_vendor.vendor = v.vendor  -- RDSD_VENDOR
    LEFT JOIN t2301822 n_rdsd_soldto ON n_rdsd_soldto.code = v.key  -- RDSD_SOLDTO
    LEFT JOIN t2306331 n_rdsd_zhrgrpmo ON n_rdsd_zhrgrpmo.zhrgrpmo = v.zhrgrpmo  -- RDSD_ZHRGRPMO
    LEFT JOIN t2320954 n_rdsd_profit_ctr ON n_rdsd_profit_ctr.profit_ctr = v.profit_ctr  -- RDSD_PROFIT_CTR
    LEFT JOIN t2355561 n_rdsd_zorgu ON n_rdsd_zorgu.zorgu = v.zorgu AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zorgu.datefrom AND n_rdsd_zorgu.dateto  -- RDSD_ZORGU
    LEFT JOIN t2310122 n_rdsd_zph_usr0 ON n_rdsd_zph_usr0.zph_usr0 = v.code_zph_usr0 AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zph_usr0.zbegda AND n_rdsd_zph_usr0.zendda  -- RDSD_ZPH_USR0
    LEFT JOIN t2320948 n_rdsd_acttype ON n_rdsd_acttype.acttype = v.acttype AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_acttype.datefrom AND n_rdsd_acttype.dateto  -- RDSD_ACTTYPE
    LEFT JOIN t2383584 n_rdsd_zequi ON n_rdsd_zequi.zequi = v.zequi AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zequi.datefrom AND n_rdsd_zequi.dateto  -- RDSD_ZEQUI
    LEFT JOIN t2308461 n_rdsd_zclsvobor ON n_rdsd_zclsvobor.zclsvo_b or = v.zclsvobor  -- RDSD_ZCLSVOBOR
    LEFT JOIN t2321329 n_rdsd_material ON n_rdsd_material.material = v.material  -- RDSD_MATERIAL
    LEFT JOIN t2355739 n_rdsd_zfunc_loc ON n_rdsd_zfunc_loc.zfunc_loc = v.zfunc_loc AND to_date(v.calyear || '-01-01', 'YYYY-MM-DD') BETWEEN n_rdsd_zfunc_loc.datefrom AND n_rdsd_zfunc_loc.dateto  -- RDSD_ZFUNC_LOC
    LEFT JOIN t2308973 n_rdsd_zsiu_fld ON n_rdsd_zsiu_fld.zsiu_fld = v.zsiu_fld  -- RDSD_ZSIU_FLD
    LEFT JOIN t2337709 n_rdsd_posid ON n_rdsd_posid.posid = v.posid  -- RDSD_POSID
    LEFT JOIN t1895288 n_rdsd_infosystem ON n_rdsd_infosystem.code_value = v.zlib_infs  -- RDSD_INFOSYSTEM
    LEFT JOIN t2317517 n_dic_type_period ON n_dic_type_period.— = v.period_ty  -- DIC_TYPE_PERIOD
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_3 ON n_shortcut_to_rdsd_soldto_3.code = v.zphd_usl1  -- SHORTCUT_TO_RDSD_SOLDTO_3
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto ON n_shortcut_to_rdsd_soldto.code = v.zdebitor  -- SHORTCUT_TO_RDSD_SOLDTO
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_2 ON n_shortcut_to_rdsd_soldto_2.code = v.zph_eso2  -- SHORTCUT_TO_RDSD_SOLDTO_2
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_4 ON n_shortcut_to_rdsd_soldto_4.code = v.zph_epok  -- SHORTCUT_TO_RDSD_SOLDTO_4
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_5 ON n_shortcut_to_rdsd_soldto_5.code = v.zphd_sk  -- SHORTCUT_TO_RDSD_SOLDTO_5
    LEFT JOIN t2307584 n_rdsd_ucvoltlevl ON n_rdsd_ucvoltlevl.ucvoltlevl = v.ucvoltlevl  -- RDSD_UCVOLTLEVL
    LEFT JOIN t2307584 n_shortcut_to_rdsd_ucvoltlevl ON n_shortcut_to_rdsd_ucvoltlevl.key = v.zucvolttr  -- SHORTCUT_TO_RDSD_UCVOLTLEVL
    LEFT JOIN t2307947 n_rdsd_z_cl_napr ON n_rdsd_z_cl_napr.z_cl_napr = v.z_cl_napr  -- RDSD_Z_CL_NAPR
    LEFT JOIN t2307875 n_rdsd_zsiu_ty ON n_rdsd_zsiu_ty.zsiu_ty = v.zsiu_ty  -- RDSD_ZSIU_TY
    LEFT JOIN t2320979 n_rdsd_zbur_lu ON n_rdsd_zbur_lu.code = v.zbur_lu  -- RDSD_ZBUR_LU
    LEFT JOIN t2311573 n_rdsd_zbur_area ON n_rdsd_zbur_area.zbur_area = v.zbur_area  -- RDSD_ZBUR_AREA
    LEFT JOIN t237842 n_rdsd_zbur_plst ON n_rdsd_zbur_plst.zbur_plst = v.zbur_plst  -- RDSD_ZBUR_PLST
    LEFT JOIN t2311619 n_rdsd_zph_tehk ON n_rdsd_zph_tehk.code = v.name  -- RDSD_ZPH_TEHK
    LEFT JOIN t2311231 n_rdsd_zskv_st ON n_rdsd_zskv_st.zskv_st = v.name  -- RDSD_ZSKV_ST
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_7 ON n_shortcut_to_rdsd_soldto_7.code = v.zgen_pod  -- SHORTCUT_TO_RDSD_SOLDTO_7
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_6 ON n_shortcut_to_rdsd_soldto_6.code = v.zgen_zak  -- SHORTCUT_TO_RDSD_SOLDTO_6
    LEFT JOIN t2301822 n_shortcut_to_rdsd_soldto_8 ON n_shortcut_to_rdsd_soldto_8.code = v.zpkr_subp  -- SHORTCUT_TO_RDSD_SOLDTO_8
    LEFT JOIN t2311391 n_rdsd_zshifr ON n_rdsd_zshifr.zshifr = v.name  -- RDSD_ZSHIFR
    LEFT JOIN t2355657 n_rdsd_zobjem ON n_rdsd_zobjem.zobjem = v.name  -- RDSD_ZOBJEM
    LEFT JOIN t2356315 n_rdsd_zphd_sr ON n_rdsd_zphd_sr.zphd_sr = v.zphd_sr  -- RDSD_ZPHD_SR
    LEFT JOIN t2311629 n_rdsd_zphd_grsr ON n_rdsd_zphd_grsr.zphd_grsr = v.zphd_grsr  -- RDSD_ZPHD_GRSR
    LEFT JOIN t2290906 n_rdsd_zgaz_type ON n_rdsd_zgaz_type.code = v.zgaz_type  -- RDSD_ZGAZ_TYPE
    LEFT JOIN t2307768 n_rdsd_zaviatype ON n_rdsd_zaviatype.zaviatype = v.zaviatype  -- RDSD_ZAVIATYPE
    LEFT JOIN t2335720 n_rdsd_zphd_spr ON n_rdsd_zphd_spr.zphd_spr = v.zphd_nop1 при zphd_spr = gtm_skv  -- RDSD_ZPHD_SPR
    LEFT JOIN t2494931 n_rdsd_actvts ON n_rdsd_actvts.code_value = v.actvts  -- RDSD_ACTVTS
    LEFT JOIN t2364976 n_rdsd_owners ON n_rdsd_owners.key = v.owner  -- RDSD_OWNERS
    GROUP BY
        :ANALYTIC_SET,
        CASE WHEN COALESCE(:P_STATUS, '0') = '1' THEN COALESCE(zphd_stat, '') ELSE 'Итого' END,
        v.zlib_indc, v.calyear, v.plant
)
-- 3. Финальный вывод
SELECT
    :ANALYTIC_SET,
    :EXTRA_NAMES,
    "Код вида деятельности",
    "Наименование вида деятельности",
    "Формы ТЭП СНГ"
FROM Main_Data;