SELECT A.*,

CASE WHEN "resposta_pesquisa_desse atendimento" >= 0 AND "resposta_pesquisa_desse atendimento" < 3  THEN 'DETRATORES'
                                         
                 WHEN "resposta_pesquisa_desse atendimento" = 3 THEN 'NEUTROS'
                 WHEN "resposta_pesquisa_desse atendimento" > 3 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS resposta_tempo_atendimento,
                 "duração do contato (seg)" AS "DURACAO_CONTATO_EM_SEG"

FROM df_base_principal A