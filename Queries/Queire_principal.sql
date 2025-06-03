WITH TABELA_CANAL_VOZ AS (
SELECT 
    "código aluno (chave)", 
    ANY_VALUE(MEDIA_TEMPO_POR_ALUNO) AS MEDIA_TEMPO_POR_ALUNO_CANAL_VOZ,
    ANY_VALUE("Decil Tempo Atendimento") AS DECIL_TEMPO_ATEND_CANAL_VOZ
FROM df_estudo_tempo_atendimento
GROUP BY "código aluno (chave)")
,
TABELA_ATENDIMENTO AS (
SELECT 
    "código aluno (chave)", 
    ANY_VALUE(MEDIA_TEMPO_POR_ALUNO) AS MEDIA_TEMPO_POR_ALUNO,
    ANY_VALUE("Decil Tempo Atendimento") AS DECIL_TEMPO_ATENDIMENTO
FROM df_estudo_tempo_atendimento
GROUP BY "código aluno (chave)"

)



SELECT 
        NPS_CATEGORIA NPS_FINAL, (EXTRACT('hour' FROM duração_entrevista) * 3600) +
(EXTRACT('minute' FROM duração_entrevista) * 60) +
EXTRACT('second' FROM duração_entrevista) AS duracao_entrevista_segundos,
data_pesquisa, sexo,
       curso, tipo_aluno, area_curso, modalidade_micro, sistema,
       fl_inadimplente, situacao_academica, canal, 
       csat_marca, csat_academico, csat_atend_geral, csat_fin_geral,
       CSAT_MARCA_CATEGORIA, CSAT_ACADEMICO_CATEGORIA,
       CSAT_ATEND_GERAL_CATEGORIA, CSAT_FINAL_GERAL



        from df_nps A 
        LEFT JOIN TABELA_ATENDIMENTO B ON
        A."código aluno (chave)" = B."código aluno (chave)"
        LEFT JOIN TABELA_CANAL_VOZ C ON 
        A."código aluno (chave)" = C."código aluno (chave)"