import pandas as pd
import duckdb as dd
import seaborn as sns
import matplotlib.pyplot as plt

from utils import tabela_analise_global, tabela_analise_condicional, executa_query_dd
df_pesquisa = pd.read_excel(r"base_case.xlsx", sheet_name="base_pesquisa")
df_base_canal_voz = pd.read_excel(r"base_Case.xlsx", sheet_name="base_canal_voz")
df_base_principal = pd.read_excel(r"base_Case.xlsx", sheet_name="base_case_1")



df_base_canal_voz['Motivo Macro'].nunique()

df_base_principal['código aluno (chave)'].value_counts()
df_base_canal_voz['código aluno (chave)'].value_counts()
df_pesquisa['código aluno (chave)'].value_counts().sort_values(ascending=False)


df_nps = executa_query_dd(
    'Queries/querie_pesquisa.sql',
    tabelas={'df_pesquisa': df_pesquisa,
             "df_base_principal": df_base_principal,
             "df_base_canal_voz": df_base_canal_voz
             })





df_estudo_tempo_atendimento = executa_query_dd(
    'Queries/querie_analise_contato.sql',
    tabelas={
             "df_base_principal": df_base_principal
             })


df_estudo_canal_voz = executa_query_dd(
    'Queries/querie_analise_contato.sql',
    tabelas={
             "df_base_principal": df_base_principal
             })




plt.figure(figsize=(10,6))


sns.set_style("whitegrid")

ax = sns.boxplot(
    data=df_estudo_tempo_atendimento,
    x='resposta_pesquisa_tempo_atendimento',      
    y='DURACAO_CONTATO_EM_SEG',          
    palette='pastel',   
    width=0.6,          
    fliersize=5,        
    linewidth=1.5       
)


ax.set_title("Boxplot Do NPS por tempo de atendimento", fontsize=16, fontweight='bold')
ax.set_xlabel("Classificação do NPS", fontsize=14, fontweight='bold')
ax.set_ylabel("tempo de atendimento (em segundos)", fontsize=14)

sns.despine()

plt.tight_layout()
plt.show()



df_nps['csat_marca'].describe()

pd.DataFrame(df_nps['NPS_CATEGORIA'].value_counts()) \
  .rename(columns={'NPS_CATEGORIA': 'Contagem'}) \
  .rename_axis('Classificação') \
  .reset_index().assign(Percentual = lambda x: (x['count'] / x['count'].sum()) * 100)


df_nps['NPS_CATEGORIA'].unique()


est_por_sexo = tabela_analise_global(df_nps, 'NPS_CATEGORIA', 'sexo')
est_cond_por_sexo = tabela_analise_condicional(df_nps, 'NPS_CATEGORIA', 'sexo')


analise_por_csat_academico = tabela_analise_global(df_nps, 'NPS_CATEGORIA', 'CSAT_ACADEMICO_CATEGORIA') 

tabela = analise_por_csat_academico.pivot(index='NPS_CATEGORIA', columns='CSAT_ACADEMICO_CATEGORIA', values='Percentual')

sns.heatmap(tabela, annot=True, fmt='.0f', cmap='Blues')

plt.title('Heatmap de Contagem por NPS e CSAT ACADEMICO')
plt.show()


analise_por_csat_marca = tabela_analise_condicional(df_nps, 'NPS_CATEGORIA', 'CSAT_MARCA_CATEGORIA')

tabela = analise_por_csat_marca.pivot(index='NPS_CATEGORIA', columns='CSAT_MARCA_CATEGORIA', values='Percentual')

sns.heatmap(tabela, annot=True, fmt='.0f', cmap='Blues')

plt.title('Heatmap de Contagem por NPS e CSAT CSAT_MARCA_CATEGORIA')
plt.show()



analise_por_csat_atend_geral = tabela_analise_condicional(df_nps, 'NPS_CATEGORIA', 'CSAT_ATEND_GERAL_CATEGORIA')

tabela = analise_por_csat_atend_geral.pivot(index='NPS_CATEGORIA', columns='CSAT_ATEND_GERAL_CATEGORIA', values='Percentual')

sns.heatmap(tabela, annot=True, fmt='.0f', cmap='Blues')

plt.title('Heatmap de Contagem por NPS e CSAT do Atendimento Geral')
plt.show()


analise_por_csat_atend_final_geral = tabela_analise_condicional(df_nps, 'NPS_CATEGORIA', 'CSAT_FINAL_GERAL')

tabela = analise_por_csat_atend_final_geral.pivot(index='NPS_CATEGORIA', columns='CSAT_FINAL_GERAL', values='Percentual')

sns.heatmap(tabela, annot=True, fmt='.2f', cmap='Blues')

plt.title('Heatmap de Contagem por NPS e CSAT do Atendimento Final Geral')
plt.show()





analise_por_csat_atend_final_geral = df_nps.groupby(['NPS_CATEGORIA', 'CSAT_FINAL_GERAL']) \
    .size() \
    .reset_index(name='Contagem') \
    .assign(Percentual=lambda x: (x['Contagem'] / x['Contagem'].sum()) * 100).sort_values(by="Percentual", ascending=False)


analise_por_sexo_pivot = analise_por_sexo.pivot_table(index='NPS_CATEGORIA', columns='sexo', values='Contagem', fill_value=0)

sns.heatmap(analise_por_sexo_pivot, annot=True, fmt='.0f', cmap='Blues')
plt.title('Heatmap de Contagem por NPS e Sexo')
plt.show()

(analise_por_sexo_pivot.T / analise_por_sexo_pivot.sum(axis=1) * 100).T.plot(kind='bar', figsize=(10, 6))
plt.show()





import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(data=df_nps, x='NPS_CATEGORIA', y='Tempo_Resposta')
plt.title('Distribuição do Tempo de Resposta por NPS')
plt.show()


df_nps.info()