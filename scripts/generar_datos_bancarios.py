"""
Generar datos sintéticos para banca digital
Crea 4 archivos CSV con datos clientes, productos, transacciones y uso digital
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Guardar seed de reproducibilidad
random.seed(42)
np.random.seed(42)

# Definir fechas de referencia
fecha_fin = datetime(2025, 1, 1)
fecha_inicio = datetime(2024, 1, 1)

# Datos para tabla de clientes
num_clientes = 5000
generos = ['M', 'F']
estados_mexico = ['CDMX', 'Jalisco', 'Nuevo León', 'Puebla',
                 'Guanajuato', 'Chihuahua', 'Oaxaca', 'Yucatán',
                 'Baja California', 'Sinaloa']

segmentos = ['Masivo', 'Medio', 'Alto', 'Premium ']
antiguedad_max = 365 * 5 # hasta 5 años de antigüedad

clientes = []
for i in range(1, num_clientes + 1):
    cliente_id = i
    edad = random.randint(18, 80)
    genero = np.random.choice(generos, p=[0.48,0.52]) # Considerando pesos

    # Generar clientes sin ubicación
    if random.random() < 0.02: # 2% sin ubicación
        ubicacion = np.nan
    else:
        ubicacion = np.random.randint(1,antiguedad_max)

    antiguedad_dias = np.random.randint(1,antiguedad_max)

    # Segmento designado por antiguedad y edad
    if antiguedad_dias < 365  * 3 and edad < 35:
        segmento = np.random.choice(['Alto', 'Premium'], p=[0.6, 0.4])
    elif antiguedad_dias < 365:
        segmento = np.random.choice(['Masivo', 'Medio'], p=[0.5, 0.5])
    else:
        segmento = 'Masivo'

    # Definir ingreso mensual estimado, acorde con el segmento
    if segmento == 'Premium':
        ingreso = random.normal(80000, 20000)
    elif segmento == 'Alto':
        ingreso = random.normal(45000, 10000)
    elif segmento == 'Medio':
        ingreso = random.normal(25000, 5000)
    else:
        ingreso = np.random.normal(12000, 3000)

    ingreso = max(6000, round(ingreso, -2))

    clientes.append([
        cliente_id, 
        edad, 
        genero, 
        ubicacion, 
        antiguedad_dias, 
        segmento, 
        ingreso
    ])

df_clientes = pd.DataFrame(clientes, columns=['cliente_id', 'edad', 'genero', 'ubicacion', 
                                              'antiguedad_dias', 'segmento', 'ingreso_mensual'])

# Guardar CSV de clientes
df_clientes.to_csv('data/raw/clientes.csv', index=False)
print(f"clientes.csv creado con {len(df_clientes):,} registros.")