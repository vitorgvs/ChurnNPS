SELECT A.*,

CASE WHEN "resposta_pesquisa_desse atendimento" >= 0 AND "resposta_pesquisa_desse atendimento" < 3  THEN 'DETRATORES'
                                         
                 WHEN "resposta_pesquisa_desse atendimento" = 3 THEN 'NEUTROS'
                 WHEN "resposta_pesquisa_desse atendimento" > 3 THEN 'PROMOTORES'
                 ELSE 'SEM AVALIACAO'
                 END AS NPS_CANAL_VOZ,
                 "duração do contato (seg)" AS "DURACAO_CONTATO_EM_SEG_CANAL_VOZ",
                 upper("Motivo Macro") Motivo_Macro
FROM df_base_canal_voz A