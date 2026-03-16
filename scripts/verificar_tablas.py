import sqlite3
import pandas as pd

conn = sqlite3.connect('data/database/banca_digital.db')

# Ver todas las tablas
query = "SELECT name FROM sqlite_master WHERE type='table';"
tablas = pd.read_sql_query(query, conn)
print("Tablas existentes en la BD:")
print(tablas)

# Ver estructura de cada tabla
for tabla in tablas['name']:
    print(f"\nEstructura de {tabla}:")
    info = pd.read_sql_query(f"PRAGMA table_info({tabla})", conn)
    print(info)

conn.close()