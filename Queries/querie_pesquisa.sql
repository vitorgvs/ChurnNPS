

SELECT A.*,CASE WHEN NPS_NOTA  >= 0 AND NPS_NOTA < 6  THEN 'DETRATORES'
                 WHEN NPS_NOTA > 6 AND NPS_NOTA < 9 THEN 'NEUTROS'
                 WHEN NPS_NOTA > 8 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS NPS_CATEGORIA,
                
                
                 CASE WHEN csat_marca  >= 0 AND csat_marca < 6  THEN 'DETRATORES'
                 WHEN csat_marca > 6 AND csat_marca < 9 THEN 'NEUTROS'
                 WHEN csat_marca > 8 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS CSAT_MARCA_CATEGORIA,

                 CASE WHEN csat_academico  >= 0 AND csat_academico < 6  THEN 'DETRATORES'
                 WHEN csat_academico > 6 AND csat_academico < 9 THEN 'NEUTROS'
                 WHEN csat_academico > 8 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS CSAT_ACADEMICO_CATEGORIA,

                CASE WHEN csat_atend_geral  >= 0 AND csat_atend_geral < 3  THEN 'DETRATORES'
                 WHEN csat_atend_geral = 3 THEN 'NEUTROS'
                 WHEN csat_atend_geral > 3 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS CSAT_ATEND_GERAL_CATEGORIA,

                 CASE WHEN csat_fin_geral  >= 0 AND csat_fin_geral < 3  THEN 'DETRATORES'
                 WHEN csat_fin_geral = 3 THEN 'NEUTROS'
                 WHEN csat_fin_geral > 3 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS CSAT_FINAL_GERAL

       



                                 


                 FROM df_pesquisa A 
                 