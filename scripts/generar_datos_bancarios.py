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

# Tabla de clientes
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
        ingreso = np.random.normal(80000, 20000)
    elif segmento == 'Alto':
        ingreso = np.random.normal(45000, 10000)
    elif segmento == 'Medio':
        ingreso = np.random.normal(25000, 5000)
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

# Tabla de productos por cliente

# Definir productos
productos = [
    'cuenta_nomina',
    'cuenta_ahorro',
    'tarjeta_credito',
    'inversion',
    'prestamo_personal',
    'seguro_vida'
]

df_productos_cliente = []

# Generar índices con iterrows, no requiero índice
for _, row in df_clientes.iterrows():
    cliente_id = row['cliente_id']
    segmento = row['segmento']
    antiguedad = row['antiguedad_dias']

    # probabilidad base por segmento
    if segmento == 'Premium':
        probs = [0.99, 0.80, 0.95, 0.70, 0.50, 0.85]
    elif segmento == 'Alto':
        probs = [0.98, 0.70, 0.85, 0.40, 0.60, 0.60]
    elif segmento == 'Medio':
        probs = [0.90, 0.50, 0.60, 0.10, 0.40, 0.20]
    else:  # Masivo
        probs = [0.70, 0.30, 0.25, 0.02, 0.15, 0.05]

    # Ajuste por antigüedad (más tiempo = más productos)
    factor_antiguedad = min(1.5, max(0.8, antiguedad / 365))
    probs = [min(1, p * factor_antiguedad) for p in probs]

    # Decidir productos
    productos_cliente = np.random.random(len(productos)) < probs

    # Crear registro por producto
    for j, tiene_producto in enumerate(productos_cliente):
        if tiene_producto:
            # Fecha contratación (entre 0 y antiguedad_dias atrás)
            dias_contratacion = np.random.randint(1, max(1, antiguedad + 1))
            fecha_contratacion = fecha_fin - timedelta(days=dias_contratacion)
            
            df_productos_cliente.append([
                cliente_id, 
                productos[j], 
                fecha_contratacion.strftime('%Y-%m-%d')
            ])

df_productos = pd.DataFrame(df_productos_cliente, columns=['cliente_id', 'producto', 'fecha_contratacion'])
df_productos.to_csv('data/raw/productos_cliente.csv', index=False)
print(f"productos_cliente.csv creado con {len(df_productos):,} registros")

# Tabla transacciones
transacciones = []
canales = ['App Móvil', 'Web', 'Sucursal', 'Cajero']
tipos = ['Compra', 'Retiro', 'Transferencia', 'Pago de Servicio', 'Depósito']

num_transacciones = 100000

for i in range(1, num_transacciones + 1):
    cliente_id = np.random.randint(1, num_clientes + 1)
    
    # Fecha aleatoria en el último año
    dias_atras = np.random.randint(0, 365)
    fecha = fecha_fin - timedelta(days=dias_atras)
    
    # Monto (distribución normal, pero siempre positivo)
    monto = abs(np.random.normal(1500, 800))
    
    tipo = np.random.choice(tipos)
    canal = np.random.choice(canales)
    
    # Reglas de negocio para canales lógicos
    if tipo == 'Retiro' and canal == 'Web':
        canal = np.random.choice(['Cajero', 'Sucursal'])
    if tipo == 'Pago de Servicio' and canal == 'Cajero':
        canal = np.random.choice(['App Móvil', 'Web'])
    
    # ERRORES REALISTAS (intencionales para practicar limpieza)
    error = random.random()
    
    # 0.5% montos negativos (error)
    if error < 0.005:
        monto = -monto
    
    # 1% fechas en formato raro
    elif error < 0.015:
        fecha = fecha.strftime('%d/%m/%Y')  # Formato DD/MM/YYYY
    
    # 1% valores nulos en canal
    elif error < 0.025:
        canal = np.nan
    
    # Formato normal de fecha
    else:
        fecha = fecha.strftime('%Y-%m-%d')
    
    transacciones.append([
        i, 
        cliente_id, 
        fecha, 
        round(monto, 2), 
        tipo, 
        canal
    ])

df_transacciones = pd.DataFrame(transacciones, columns=['transaccion_id', 'cliente_id', 'fecha', 'monto', 'tipo', 'canal'])
df_transacciones.to_csv('data/raw/transacciones.csv', index=False)
print(f"transacciones.csv creado con {len(df_transacciones):,} registros")

# Tabla uso de canales digitales
eventos_digitales = []
acciones_app = ['Login', 'Consulta Saldo', 'Pago', 'Transferencia', 'Inversión', 'Soporte']
num_eventos = 200000

for i in range(1, num_eventos + 1):
    cliente_id = np.random.randint(1, num_clientes + 1)
    
    # Eventos en los últimos 3 meses (más realista)
    dias_atras = np.random.randint(0, 90)
    horas = np.random.randint(0, 24)
    minutos = np.random.randint(0, 60)
    segundos = np.random.randint(0, 60)
    
    fecha_evento = fecha_fin - timedelta(days=dias_atras, hours=horas, 
                                         minutes=minutos, seconds=segundos)
    
    accion = np.random.choice(acciones_app, p=[0.4, 0.3, 0.1, 0.1, 0.05, 0.05])
    
    # Tiempo de sesión (solo para login)
    if accion == 'Login':
        tiempo_sesion = np.random.randint(30, 1800)  # 30 seg a 30 min
    else:
        tiempo_sesion = 0
    
    eventos_digitales.append([
        i, 
        cliente_id, 
        fecha_evento.strftime('%Y-%m-%d %H:%M:%S'), 
        accion, 
        tiempo_sesion
    ])

df_canales = pd.DataFrame(eventos_digitales, columns=['evento_id', 'cliente_id', 'fecha_hora', 'accion', 'tiempo_sesion_seg'])
df_canales.to_csv('data/raw/uso_canales_digitales.csv', index=False)
print(f"uso_canales_digitales.csv creado con {len(df_canales):,} registros")

print("\nArchivos creados en 'data/raw/':")
print(f" - clientes.csv: {len(df_clientes):>6,} registros")
print(f" - productos_cliente.csv: {len(df_productos):>6,} registros")
print(f" - transacciones.csv: {len(df_transacciones):>6,} registros")
print(f" - uso_canales_digitales.csv: {len(df_canales):>6,} registros")