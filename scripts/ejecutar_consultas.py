import sqlite3
import pandas as pd

conn = sqlite3.connect('data\\database\\banca_digital.db')

# Lectura y ejecución del script sql
with open('scripts\\consultas_banca.sql', 'r') as f:
    queries = f.read().split(';')

# -1 para ignorar última vacía
for i, query in enumerate(queries[:-1]):
    print(f"\nResultado consulta {i+1}:")
    df = pd.read_sql_query(query,conn)
    print(df)

conn.close()