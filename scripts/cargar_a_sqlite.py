import sqlite3
import pandas as pd
import os

# Conexión a la base de datos SQLite, crear si no existe.
conn = sqlite3.connect('data/database/banca_digital.db')

# Carga de archivos CSV
print("Carga de archivos CSV...")

clientes = pd.read_csv('data/raw/clientes.csv')
productos = pd.read_csv('data/raw/productos_cliente.csv')
transacciones = pd.read_csv('data/raw/transacciones.csv')
canales = pd.read_csv('data/raw/uso_canales_digitales.csv')

# Guardar en sqlite
clientes.to_sql('clientes', conn, if_exists='replace', index=False)
productos.to_sql('productos', conn, if_exists='replace', index=False)
transacciones.to_sql('transacciones', conn, if_exists='replace', index=False)
canales.to_sql('canales', conn, if_exists='replace', index=False)

print("Carga completada. Tablas creadas en SQLite.")
conn.close()