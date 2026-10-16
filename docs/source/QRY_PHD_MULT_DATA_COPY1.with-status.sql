/*
   Параметры, которые должны быть заведены на объекте ЗАПРОС и на ОТЧЁТЕ:
     :ANALYTIC_SET  - массив строк, выбранные аналитики (без псевдонимов)      [как было]
     :EXTRA_FIELDS  - массив строк, колонки периодов и статусов С ПСЕВДОНИМАМИ  [новый]
                      пример элемента:
                        SUM(zsiu_indv) FILTER (WHERE period = 1 AND ztypeind = '0000000001') AS "Январь (План)"
                        MAX(zphd_stat) FILTER (WHERE period = 1 AND ztypeind = '0000000001') AS "Январь. Статус (План)"
     :EXTRA_NAMES   - массив строк, те же псевдонимы в кавычках для финальной проекции [новый]
                        "Январь (План)", "Январь. Статус (План)", ...
     :P_STATUS      - строка, признак чек-бокса «Выводить информацию по статусам»: 1 или 0 [новый]
                      при 0 статусы схлопываются в одну группу «Итого» — общая сумма по всем статусам

   Число колонок задаёт форма: (периоды x типы x 2) — значения и статусы.
*/
/*
WITH TMP_TBL AS (
    SELECT
        :ANALYTIC_SET,
        (SELECT ACTVTS FROM t1895280 WHERE CODE = zlib_indc AND now() BETWEEN DATE_FROM AND DATE_TO) AS "Код вида деятельности", 
        (SELECT SNAME FROM t1895280 WHERE CODE = zlib_indc AND now() BETWEEN DATE_FROM AND DATE_TO) AS "Наименование вида деятельности",
        
        (
    	SELECT STRING_AGG(distinct ZF_NUMB, ', ') FILTER (WHERE ZF_NUMB IS NOT NULL AND ZF_NUMB <> '')
		FROM TBL_ZIDNFORM 
    		WHERE 
    		(ZLIB_INDC IN (:ZLIB_INDC) OR (COALESCE(:ZLIB_INDC, '') = '' AND ZLIB_INDC = zlib_indc))
    		AND (GJAHR IN (:CALYEAR) OR (COALESCE(:CALYEAR, '') = '' AND GJAHR = CALYEAR))
    		AND (PLANT IN (:PLANT) OR (COALESCE(:PLANT, '') = '' AND PLANT = PLANT))
    		
        ) AS "Формы ТЭП СНГ",
	
        SUM(CASE WHEN PERIOD = 1 THEN ZSIU_INDV ELSE 0 END) AS "Январь",
        SUM(CASE WHEN PERIOD = 2 THEN ZSIU_INDV ELSE 0 END) AS "Февраль",
        SUM(CASE WHEN PERIOD = 3 THEN ZSIU_INDV ELSE 0 END) AS "Март",
        SUM(CASE WHEN PERIOD = 4 THEN ZSIU_INDV ELSE 0 END) AS "Апрель",
        SUM(CASE WHEN PERIOD = 5 THEN ZSIU_INDV ELSE 0 END) AS "Май",
        SUM(CASE WHEN PERIOD = 6 THEN ZSIU_INDV ELSE 0 END) AS "Июнь",
        SUM(CASE WHEN PERIOD = 7 THEN ZSIU_INDV ELSE 0 END) AS "Июль",
        SUM(CASE WHEN PERIOD = 8 THEN ZSIU_INDV ELSE 0 END) AS "Август",
        SUM(CASE WHEN PERIOD = 9 THEN ZSIU_INDV ELSE 0 END) AS "Сентябрь",
        SUM(CASE WHEN PERIOD = 10 THEN ZSIU_INDV ELSE 0 END) AS "Октябрь",
        SUM(CASE WHEN PERIOD = 11 THEN ZSIU_INDV ELSE 0 END) AS "Ноябрь",
        SUM(CASE WHEN PERIOD = 12 THEN ZSIU_INDV ELSE 0 END) AS "Декабрь",
        SUM(CASE WHEN PERIOD IN (1, 2, 3) THEN ZSIU_INDV ELSE 0 END) AS "I кв.",
        SUM(CASE WHEN PERIOD IN (4, 5, 6) THEN ZSIU_INDV ELSE 0 END) AS "II кв.",
        SUM(CASE WHEN PERIOD IN (7, 8, 9) THEN ZSIU_INDV ELSE 0 END) AS "III кв.",
        SUM(CASE WHEN PERIOD IN (10, 11, 12) THEN ZSIU_INDV ELSE 0 END) AS "IV кв.",
        SUM(CASE WHEN PERIOD IN (1,2,3,4,5,6,7,8,9,10,11,12) THEN ZSIU_INDV ELSE 0 END) AS "Год",
        
        SUM(CASE WHEN PERIOD = 1 THEN ZVALUE_SNG ELSE 0 END) AS "Январь. С нач.года",
        SUM(CASE WHEN PERIOD = 2 THEN ZVALUE_SNG ELSE 0 END) AS "Февраль. С нач.года",
        SUM(CASE WHEN PERIOD = 3 THEN ZVALUE_SNG ELSE 0 END) AS "Март. С нач.года",
        SUM(CASE WHEN PERIOD = 4 THEN ZVALUE_SNG ELSE 0 END) AS "Апрель. С нач.года",
        SUM(CASE WHEN PERIOD = 5 THEN ZVALUE_SNG ELSE 0 END) AS "Май. С нач.года",
        SUM(CASE WHEN PERIOD = 6 THEN ZVALUE_SNG ELSE 0 END) AS "Июнь. С нач.года",
        SUM(CASE WHEN PERIOD = 7 THEN ZVALUE_SNG ELSE 0 END) AS "Июль. С нач.года",
        SUM(CASE WHEN PERIOD = 8 THEN ZVALUE_SNG ELSE 0 END) AS "Август. С нач.года",
        SUM(CASE WHEN PERIOD = 9 THEN ZVALUE_SNG ELSE 0 END) AS "Сентябрь. С нач.года",
        SUM(CASE WHEN PERIOD = 10 THEN ZVALUE_SNG ELSE 0 END) AS "Октябрь. С нач.года",
        SUM(CASE WHEN PERIOD = 11 THEN ZVALUE_SNG ELSE 0 END) AS "Ноябрь. С нач.года",
        SUM(CASE WHEN PERIOD = 12 THEN ZVALUE_SNG ELSE 0 END) AS "Декабрь. С нач.года",
        SUM(CASE WHEN PERIOD IN (1, 2, 3) THEN ZVALUE_SNG ELSE 0 END) AS "I кв. С нач.года.",
        SUM(CASE WHEN PERIOD IN (4, 5, 6) THEN ZVALUE_SNG ELSE 0 END) AS "II кв. С нач.года.",
        SUM(CASE WHEN PERIOD IN (7, 8, 9) THEN ZVALUE_SNG ELSE 0 END) AS "III кв. С нач.года.",
        SUM(CASE WHEN PERIOD IN (10, 11, 12) THEN ZVALUE_SNG ELSE 0 END) AS "IV кв.. С нач.года",
        SUM(CASE WHEN PERIOD IN (1,2,3,4,5,6,7,8,9,10,11,12) THEN ZVALUE_SNG ELSE 0 END) AS "Год. С нач.года"

    FROM 
        VIEW_PHD_MULT_LEFT
    WHERE 
        (PLANT IN (:PLANT) OR COALESCE(:PLANT,'')='') 
        AND (ZLIB_INDC IN (:ZLIB_INDC) OR COALESCE(:ZLIB_INDC,'')='') 
        AND (CALYEAR IN (:CALYEAR) OR COALESCE(:CALYEAR,'')='') 
        AND (ZPHD_STAT IN (:ZPHD_STAT) OR COALESCE(:ZPHD_STAT,'')='') 
        AND (VENDOR IN (:VENDOR) OR COALESCE(:VENDOR,'')='') 
        AND (SOLD_TO IN (:SOLD_TO) OR COALESCE(:SOLD_TO,'')='') 
        AND (ZHRGRPMO IN (:ZHRGRPMO) OR COALESCE(:ZHRGRPMO,'')='') 
        AND (PROFIT_CTR IN (:PROFIT_CTR) OR COALESCE(:PROFIT_CTR,'')='') 
        AND (COSTCENTER IN (:COSTCENTER) OR COALESCE(:COSTCENTER,'')='') 
        AND (ZORGUNIT IN (:ZORGUNIT) OR COALESCE(:ZORGUNIT,'')='') 
        AND (ZPH_USR2 IN (:ZPH_USR2) OR COALESCE(:ZPH_USR2,'')='') 
        AND (ACTTYPE IN (:ACTTYPE) OR COALESCE(:ACTTYPE,'')='') 
        AND (ZEQUI IN (:ZEQUI) OR COALESCE(:ZEQUI,'')='') 
        AND (ZCLSVOBOR IN (:ZCLSVOBOR) OR COALESCE(:ZCLSVOBOR,'')='') 
        AND (MATERIAL IN (:MATERIAL) OR COALESCE(:MATERIAL,'')='') 
        AND (ZFUNC_LOC IN (:ZFUNC_LOC) OR COALESCE(:ZFUNC_LOC,'')='') 
        AND (ZSIU_FLD IN (:ZSIU_FLD) OR COALESCE(:ZSIU_FLD,'')='') 
        AND (POSID IN (:POSID) OR COALESCE(:POSID,'')='') 
        AND (ZLIB_INFS IN (:ZLIB_INFS) OR COALESCE(:ZLIB_INFS,'')='') 
        AND (PERIOD_TYPE IN (:PERIOD_TYPE) OR COALESCE(:PERIOD_TYPE,'')='') 
        AND (ZPHD_DOG IN (:ZPHD_DOG) OR COALESCE(:ZPHD_DOG,'')='') 
        AND (ZPHD_USL1 IN (:ZPHD_USL1) OR COALESCE(:ZPHD_USL1,'')='') 
        AND (ZDEBITOR IN (:ZDEBITOR) OR COALESCE(:ZDEBITOR,'')='') 
        AND (ZPH_ESO2 IN (:ZPH_ESO2) OR COALESCE(:ZPH_ESO2,'')='') 
        AND (ZPHD_SK IN (:ZPHD_SK) OR COALESCE(:ZPHD_SK,'')='') 
        AND (UCVOLTLEVL IN (:UCVOLTLEVL) OR COALESCE(:UCVOLTLEVL,'')='') 
        AND (ZUCVOLTTR IN (:ZUCVOLTTR) OR COALESCE(:ZUCVOLTTR,'')='') 
        AND (Z_CL_NAPR IN (:Z_CL_NAPR) OR COALESCE(:Z_CL_NAPR,'')='') 
        AND (ZSIU_TY IN (:ZSIU_TY) OR COALESCE(:ZSIU_TY,'')='') 
        AND (ZDOGLINK IN (:ZDOGLINK) OR COALESCE(:ZDOGLINK,'')='') 
        AND (ZBUR_LU IN (:ZBUR_LU) OR COALESCE(:ZBUR_LU,'')='') 
        AND (ZBUR_AREA IN (:ZBUR_AREA) OR COALESCE(:ZBUR_AREA,'')='') 
        AND (ZSKV_KUST IN (:ZSKV_KUST) OR COALESCE(:ZSKV_KUST,'')='') 
        AND (Z_SKV_GEO IN (:Z_SKV_GEO) OR COALESCE(:Z_SKV_GEO,'')='') 
        AND (ZBUR_PLST IN (:ZBUR_PLST) OR COALESCE(:ZBUR_PLST,'')='') 
        AND (ZPH_TEHK IN (:ZPH_TEHK) OR COALESCE(:ZPH_TEHK,'')='') 
        AND (ZPH_OPLST IN (:ZPH_OPLST) OR COALESCE(:ZPH_OPLST,'')='') 
        AND (ZPHD_COMM IN (:ZPHD_COMM) OR COALESCE(:ZPHD_COMM,'')='') 
        AND (TO_DATE(ZBUR_BEG, 'YYYY-MM-DD') in (TO_DATE(:ZBUR_BEG, 'YYYY-MM-DD')) OR COALESCE(:ZBUR_BEG,'')='') 
        AND (ZPILOT IN (:ZPILOT) OR COALESCE(:ZPILOT,'')='') 
        AND (ZSKV_ST IN (:ZSKV_ST) OR COALESCE(:ZSKV_ST,'')='') 
        AND (ZINDTXT1 IN (:ZINDTXT1) OR COALESCE(:ZINDTXT1,'')='') 
        AND (ZGEN_POD IN (:ZGEN_POD) OR COALESCE(:ZGEN_POD,'')='') 
        AND (ZGEN_ZAK IN (:ZGEN_ZAK) OR COALESCE(:ZGEN_ZAK,'')='') 
        AND (ZSHIFR IN (:ZSHIFR) OR COALESCE(:ZSHIFR,'')='') 
        AND (ZOBJEM IN (:ZOBJEM) OR COALESCE(:ZOBJEM,'')='') 
        AND (ZPHD_SR IN (:ZPHD_SR) OR COALESCE(:ZPHD_SR,'')='') 
        AND (ZPHD_GRSR IN (:ZPHD_GRSR) OR COALESCE(:ZPHD_GRSR,'')='') 
        AND (ZGAZ_TYPE IN (:ZGAZ_TYPE) OR COALESCE(:ZGAZ_TYPE,'')='') 
        AND (ZAVIATYPE IN (:ZAVIATYPE) OR COALESCE(:ZAVIATYPE,'')='') 
        AND (ZPHD_NCH IN (:ZPHD_NCH) OR COALESCE(:ZPHD_NCH,'')='') 
        AND (ZPHD_SPR IN (:ZPHD_SPR) OR COALESCE(:ZPHD_SPR,'')='') 
    GROUP BY 
        :ANALYTIC_SET,
        zlib_indc, CALYEAR, PLANT
)

SELECT * FROM TMP_TBL */


WITH 
-- 1. Агрегируем формы ТЭП
Forms_Agg AS (
    SELECT 
        ZLIB_INDC, GJAHR, PLANT,
        STRING_AGG(DISTINCT ZF_NUMB, ', ') FILTER (WHERE ZF_NUMB IS NOT NULL AND ZF_NUMB <> '') AS forms_text
    FROM TBL_ZIDNFORM 
    WHERE 
        ZLIB_INDC IN (:ZLIB_INDC)
        AND GJAHR IN (:CALYEAR)
        AND PLANT IN (:PLANT)
    GROUP BY ZLIB_INDC, GJAHR, PLANT
),

-- 2. Основной расчет сумм
Main_Data AS (
    SELECT
        :ANALYTIC_SET, 
        
        (SELECT t.ACTVTS FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Код вида деятельности",
        (SELECT t.SNAME FROM t1895280 t WHERE t.CODE = v.zlib_indc AND now() BETWEEN t.DATE_FROM AND t.DATE_TO LIMIT 1) AS "Наименование вида деятельности",
        (SELECT f.forms_text FROM Forms_Agg f WHERE f.ZLIB_INDC = v.zlib_indc AND f.GJAHR = v.calyear AND f.PLANT = v.plant LIMIT 1) AS "Формы ТЭП СНГ"
        
        :EXTRA_FIELDS            -- каждый элемент начинается с ', ' (запятая внутри значения)
    FROM 
        VIEW_PHD_MULT_LEFT v
    WHERE           
     	          (PLANT 		    	IN (:PLANT) 	 							OR COALESCE(:PLANT,'')='') 
        AND (ZLIB_INDC	    	IN (:ZLIB_INDC)  							OR COALESCE(:ZLIB_INDC,'')='') 
        AND (CALYEAR 	    	IN (:CALYEAR) 	 							OR COALESCE(:CALYEAR,'')='') 
        AND (ZPHD_STAT     	IN (:ZPHD_STAT)   							OR COALESCE(:ZPHD_STAT,'')='')
        AND (ZTYPEIND     	IN (:ZTYPEIND)   							OR COALESCE(:ZTYPEIND,'')='')
        AND (VENDOR 	    	IN (:VENDOR) 	  							OR COALESCE(:VENDOR,'')='') 
        AND (SOLD_TO 	    	IN (:SOLD_TO) 	  							OR COALESCE(:SOLD_TO,'')='') 
        AND (ZHRGRPMO       	IN (:ZHRGRPMO) 	  						OR COALESCE(:ZHRGRPMO,'')='') 
        AND (PROFIT_CTR     	IN (:PROFIT_CTR)  							OR COALESCE(:PROFIT_CTR,'')='') 
        AND (COSTCENTER     IN (:COSTCENTER)  						OR COALESCE(:COSTCENTER,'')='') 
        AND (ZORGUNIT 	    	IN (:ZORGUNIT) 	  						OR COALESCE(:ZORGUNIT,'')='') 
        AND (ZPH_USR2 	    	IN (:ZPH_USR2) 	  						OR COALESCE(:ZPH_USR2,'')='') 
        AND (ACTTYPE  	    	IN (:ACTTYPE) 	  							OR COALESCE(:ACTTYPE,'')='') 
        AND (ZEQUI 		    	IN (:ZEQUI) 	  								OR COALESCE(:ZEQUI,'')='') 
        AND (ZCLSVOBOR      	IN (:ZCLSVOBOR)   							OR COALESCE(:ZCLSVOBOR,'')='') 
        AND (MATERIAL 	    	IN (:MATERIAL) 	  						OR COALESCE(:MATERIAL,'')='') 
        AND (ZFUNC_LOC 	    	IN (:ZFUNC_LOC)   							OR COALESCE(:ZFUNC_LOC,'')='') 
        AND (ZSIU_FLD 	    	IN (:ZSIU_FLD)    							OR COALESCE(:ZSIU_FLD,'')='') 
        AND (POSID 		    	IN (:POSID) 	  								OR COALESCE(:POSID,'')='') 
        AND (ZLIB_INFS 	    	IN (:ZLIB_INFS)   							OR COALESCE(:ZLIB_INFS,'')='') 
        AND (PERIOD_TYPE    IN (:PERIOD_TYPE) 						OR COALESCE(:PERIOD_TYPE,'')='') 
        AND (ZPHD_DOG 	    	IN (:ZPHD_DOG) 	  						OR COALESCE(:ZPHD_DOG,'')='') 
        AND (ZPHD_USL1 	    	IN (:ZPHD_USL1)   							OR COALESCE(:ZPHD_USL1,'')='') 
        AND (ZDEBITOR 	    	IN (:ZDEBITOR) 	  						OR COALESCE(:ZDEBITOR,'')='') 
        AND (ZPH_ESO2 	    	IN (:ZPH_ESO2) 	  						OR COALESCE(:ZPH_ESO2,'')='') 
        AND (ZPHD_SK 	    	IN (:ZPHD_SK) 	  							OR COALESCE(:ZPHD_SK,'')='') 
        AND (UCVOLTLEVL     	IN (:UCVOLTLEVL)  							OR COALESCE(:UCVOLTLEVL,'')='') 
        AND (ZUCVOLTTR      	IN (:ZUCVOLTTR)   							OR COALESCE(:ZUCVOLTTR,'')='') 
        AND (Z_CL_NAPR      	IN (:Z_CL_NAPR)   							OR COALESCE(:Z_CL_NAPR,'')='') 
        AND (ZSIU_TY 	    	IN (:ZSIU_TY)     							OR COALESCE(:ZSIU_TY,'')='') 
        AND (ZDOGLINK 	    	IN (:ZDOGLINK) 	  						OR COALESCE(:ZDOGLINK,'')='') 
        AND (ZBUR_LU 	    	IN (:ZBUR_LU) 	  							OR COALESCE(:ZBUR_LU,'')='') 
        AND (ZBUR_AREA      	IN (:ZBUR_AREA)   							OR COALESCE(:ZBUR_AREA,'')='') 
        AND (ZSKV_KUST 	   	IN (:ZSKV_KUST)   							OR COALESCE(:ZSKV_KUST,'')='') 
        AND (Z_SKV_GEO 	  	IN (:Z_SKV_GEO)   							OR COALESCE(:Z_SKV_GEO,'')='') 
        AND (ZBUR_PLST 	   	IN (:ZBUR_PLST)   							OR COALESCE(:ZBUR_PLST,'')='') 
        AND (ZPH_TEHK 	   	IN (:ZPH_TEHK) 	  						OR COALESCE(:ZPH_TEHK,'')='') 
        AND (ZPH_OPLST 	    	IN (:ZPH_OPLST)   							OR COALESCE(:ZPH_OPLST,'')='') 
        AND (ZPHD_COMM      IN (:ZPHD_COMM)   						OR COALESCE(:ZPHD_COMM,'')='') 
        AND (TO_DATE(ZBUR_BEG, 'YYYY-MM-DD') 
							IN (TO_DATE(:ZBUR_BEG, 'YYYY-MM-DD')) 	OR COALESCE(:ZBUR_BEG,'')='') 
        AND (ZPILOT 	    		IN (:ZPILOT) 	  							OR COALESCE(:ZPILOT,'')='') 
        AND (ZSKV_ST 	    	IN (:ZSKV_ST) 	  							OR COALESCE(:ZSKV_ST,'')='') 
        AND (ZGEN_POD 	    	IN (:ZGEN_POD) 	  						OR COALESCE(:ZGEN_POD,'')='') 
        AND (ZGEN_ZAK 	    	IN (:ZGEN_ZAK) 	  						OR COALESCE(:ZGEN_ZAK,'')='') 
        AND (ZSHIFR 			IN (:ZSHIFR) 	  							OR COALESCE(:ZSHIFR,'')='') 
        AND (ZOBJEM 	    		IN (:ZOBJEM) 	  							OR COALESCE(:ZOBJEM,'')='') 
        AND (ZPHD_SR 	    	IN (:ZPHD_SR) 	  							OR COALESCE(:ZPHD_SR,'')='') 
        AND (ZPHD_GRSR      IN (:ZPHD_GRSR)   							OR COALESCE(:ZPHD_GRSR,'')='') 
        AND (ZGAZ_TYPE 	    	IN (:ZGAZ_TYPE)   							OR COALESCE(:ZGAZ_TYPE,'')='') 
        AND (ZAVIATYPE 	    	IN (:ZAVIATYPE)   							OR COALESCE(:ZAVIATYPE,'')='') 
        AND (ZPHD_NCH 	    	IN (:ZPHD_NCH) 	  						OR COALESCE(:ZPHD_NCH,'')='') 
        AND (ZPHD_SPR 	    	IN (:ZPHD_SPR) 	  						OR COALESCE(:ZPHD_SPR,'')='') 
	 AND (ZINDTXT1 	    	ILIKE '%' || :ZINDTXT1 || '%' 					OR COALESCE(:ZINDTXT1,'')='') -- поиск по маске

    GROUP BY 
        :ANALYTIC_SET, 
        CASE WHEN COALESCE(:P_STATUS, '0') = '1' THEN COALESCE(zphd_stat, '') ELSE 'Итого' END,
        zlib_indc, calyear, plant
        limit 100
)

-- 3. Финальный вывод
SELECT
    :ANALYTIC_SET,          -- выбранные аналитики (у параметра есть значение по умолчанию)
    "Код вида деятельности",
    "Наименование вида деятельности",
    "Формы ТЭП СНГ"
    :EXTRA_NAMES            -- динамические колонки; каждый элемент начинается с ', '
FROM Main_Data;