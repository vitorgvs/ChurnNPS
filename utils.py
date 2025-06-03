import pandas as pd
import duckdb as dd
from scipy.stats import spearmanr, kendalltau
import duckdb as dd
import os
import numpy as np
import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier,
                              BaggingClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier, HistGradientBoostingClassifier)
from xgboost import XGBClassifier, XGBRFClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.linear_model import (LogisticRegression, PassiveAggressiveClassifier,
                                  RidgeClassifier, RidgeClassifierCV, SGDClassifier, Perceptron)
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis, LinearDiscriminantAnalysis
from sklearn.semi_supervised import LabelSpreading, LabelPropagation
from sklearn.calibration import CalibratedClassifierCV
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

def tabela_analise_global(df,coluna1,coluna2):
    df = (df.groupby([f'{coluna1}', f'{coluna2}']) \
    .size() \
    .reset_index(name='Contagem') \
    .assign(Percentual=lambda x: (x['Contagem'] / x['Contagem'].sum()) * 100).sort_values(by="Percentual", ascending=False)
    )
    return df

def tabela_analise_condicional(df, coluna1, coluna2):
    tabela = (
        df.groupby([coluna1, coluna2])
        .size()
        .reset_index(name='Contagem')
    )
    
    tabela['Percentual'] = tabela.groupby(coluna1)['Contagem'].transform(lambda x: (x / x.sum()) * 100)
    
    return tabela.sort_values(by=['Contagem'], ascending=False)




def executa_query_dd(arquivo_sql,con):
    with open(arquivo_sql, 'r') as file:
            sql_query = file.read()
            return dd.sql(query=sql_query,connection=con).df()


def executa_query_dd(arquivo_sql, tabelas=None):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_sql = os.path.join(base_dir, arquivo_sql) if not os.path.isabs(arquivo_sql) else arquivo_sql

    if not os.path.isfile(caminho_sql):
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {caminho_sql}")

    with open(caminho_sql, 'r', encoding='utf-8') as f:
        sql_query = f.read()

    con = dd.connect()

    if tabelas:
        for nome, df in tabelas.items():
            con.register(nome, df)

    resultado = con.execute(sql_query).df()
    con.close()

    return resultado




# Definir a semente aleatória
sem_random = 3141592

# Criar dicionário com todos os modelos
model_dict = {


    # Modelos Baseados em Árvores
    'DecisionTreeClassifier': DecisionTreeClassifier(random_state=sem_random),
    'ExtraTreeClassifier': ExtraTreeClassifier(random_state=sem_random),
    'RandomForestClassifier': RandomForestClassifier(random_state=sem_random),
    'ExtraTreesClassifier': ExtraTreesClassifier(random_state=sem_random),
    'BaggingClassifier': BaggingClassifier(random_state=sem_random),
    
    # Modelos de Boosting
    'AdaBoostClassifier': AdaBoostClassifier(random_state=sem_random),
    'GradientBoostingClassifier': GradientBoostingClassifier(random_state=sem_random),
    'HistGradientBoostingClassifier': HistGradientBoostingClassifier(random_state=sem_random),
    'XGBClassifier': XGBClassifier(random_state=sem_random),

    'XGBRFClassifier':  XGBRFClassifier(random_state=sem_random),
    'LGBMClassifier': LGBMClassifier(random_state=sem_random),
    'CatBoostClassifier': CatBoostClassifier(verbose=0)

}

#for model_name in model_dict:
#    print(model_name, '->', model_dict[model_name])

########################################################################
# TREINANDO MODELOS

import time

def treina_modelos(x_treino, y_treino):
    tab_modelo_treinados = pd.DataFrame(columns=['Modelo', 'Status', 'Tempo'])
    for model_name, model_instance in model_dict.items():
        try:
            start_time = time.time()
            model_instance.fit(x_treino, y_treino)
            end_time = time.time()
            training_time = end_time - start_time
            tab_modelo_treinados.loc[len(tab_modelo_treinados)] = [model_name, 'OK', training_time]
        except Exception as e:
            tab_modelo_treinados.loc[len(tab_modelo_treinados)] = [model_name, 'Erro', np.nan]
        return tab_modelo_treinados
        

def adicionar_previsoes(x_teste, y_teste, **modelos):
    # Inicializa o DataFrame com a coluna `y`
    df = pd.DataFrame({'y': y_teste})

    # Para cada modelo, gera previsões e adiciona ao DataFrame
    for nome, modelo in modelos.items():
        try:
        #if hasattr(modelo, "predict_proba"):
            df[nome] = modelo.predict_proba(x_teste)[:, 1] * 100
        except:
            print('erro:', nome)

    return df



 























 
print('*'*30, 'NORMAL', '*'*30)
# Treinando todos os modelos
tab_modelo_treinados = pd.DataFrame(columns=['Modelo', 'Status', 'Tempo'])
for model_name, model_instance in model_dict.items():
    try:
        start_time = time.time()
        model_instance.fit(X_train, y_train)
        end_time = time.time()
        training_time = end_time - start_time
        tab_modelo_treinados.loc[len(tab_modelo_treinados)] = [model_name, 'OK', training_time]
    except Exception as e:
        tab_modelo_treinados.loc[len(tab_modelo_treinados)] = [model_name, 'Erro', np.nan]
        #del model_dict[model_name] # excluindo do dicionario # não pode modificar o dicionario durante iteracao


def adicionar_previsoes(x_teste, y_teste, **modelos):
    # Inicializa o DataFrame com a coluna `y`
    df = pd.DataFrame({'y': y_teste})

    # Para cada modelo, gera previsões e adiciona ao DataFrame
    for nome, modelo in modelos.items():
        try:
        #if hasattr(modelo, "predict_proba"):
            df[nome] = modelo.predict_proba(x_teste)[:, 1] * 100
        except:
            print('erro:', nome)

    return df

previsoes = adicionar_previsoes(X_test ,y_test, **model_dict)



df_modelos =  read_query_dd(r'avaliador_de_modelos.sql')

df_modelos.info()

tabela_analise = pd.DataFrame(df_modelos.groupby(["modelo","threshold"]).agg(
{"TP":"sum",
 "TN":"sum",
 "FP":"sum",
 "FN":"sum",
 }
).assign(SENSIBILIDADE = lambda x: x['TP'] / (x['TP'] + x['FN']),
         ESPECIFICIDADE = lambda x: x['TN'] / (x['TN'] + x['FP']),
         ACURACIA = lambda x: (x['TP'] + x['TN']) / (x['TP'] + x['TN'] + x['FP'] + x['FN']),
         PRECISAO = lambda x : x['TP'] / (x['TP'] + x['FP']),
         ).reset_index()).assign(F_BETA = lambda x : (1 + 2 **2) *  (x['PRECISAO'] * x['SENSIBILIDADE'] )/ ((2**2 * x['PRECISAO'] ) + x['SENSIBILIDADE']),
                                 CASOS_POR_DIA = lambda x : x['TP'] + x['FP'] / 46,
                                 ).reset_index()