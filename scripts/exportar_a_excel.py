import pandas as pd
import sqlite3

conn = sqlite3.connect('data/database/banca_digital.db')

# Cargar todas las tablas
clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
productos = pd.read_sql_query("SELECT * FROM productos", conn)
transacciones = pd.read_sql_query("SELECT * FROM transacciones", conn)
canales = pd.read_sql_query("SELECT * FROM canales", conn)

# Exportar a Excel (Power BI lo lee fácil)
with pd.ExcelWriter('data/processed/banca_digital.xlsx') as writer:
    clientes.to_excel(writer, sheet_name='clientes', index=False)
    productos.to_excel(writer, sheet_name='productos', index=False)
    transacciones.to_excel(writer, sheet_name='transacciones', index=False)
    canales.to_excel(writer, sheet_name='canales', index=False)

print("Datos exportados a data/processed/banca_digital.xlsx")