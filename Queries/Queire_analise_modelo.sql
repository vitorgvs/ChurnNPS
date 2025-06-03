WITH BASE AS (
    SELECT 
        ROW_NUMBER() OVER () AS rowid,
        *,
        CASE y
            WHEN 'PROMOTORES' THEN '0'
            WHEN 'DETRATORES' THEN '1'
            WHEN 'NEUTROS' THEN '2' -- se houver
            ELSE NULL
        END AS y_numerico
    FROM previsoes_multiclasse
),

UNPIVOTADO AS (
    SELECT 
        rowid,
        y_numerico AS classe_real,
        CASE 
            WHEN column_name LIKE 'XGBClassifier%' THEN 'XGBClassifier'
            WHEN column_name LIKE 'XGBRFClassifier%' THEN 'XGBRFClassifier'
        END AS modelo,
        CASE 
            WHEN column_name LIKE '%_0' THEN '0'
            WHEN column_name LIKE '%_1' THEN '1'
            WHEN column_name LIKE '%_2' THEN '2'
        END AS classe_predita,
        value AS probabilidade
    FROM BASE
    UNPIVOT (value FOR column_name IN (
        'XGBClassifier_0', 'XGBClassifier_1',
        'XGBRFClassifier_0', 'XGBRFClassifier_1'
    ))
),

PREDICAO AS (
    SELECT 
        rowid,
        classe_real,
        modelo,
        classe_predita,
        probabilidade,
        ROW_NUMBER() OVER (PARTITION BY modelo, rowid ORDER BY probabilidade DESC) AS rn
    FROM UNPIVOTADO
),

PREDICAO_FINAL AS (
    SELECT 
        rowid,
        classe_real,
        modelo,
        classe_predita,
        CASE 
            WHEN classe_real = classe_predita THEN 1
            ELSE 0
        END AS acerto
    FROM PREDICAO
    WHERE rn = 1
)

SELECT * FROM PREDICAO_FINAL
ORDER BY modelo, rowid;
