"""
generar_datos.py
================
Genera ventas_2023.csv con 1.200 registros realistas de una tienda
de tecnología colombiana. Ejecutar UNA VEZ antes de analisis.py
"""

import pandas as pd
import numpy as np
import random
from datetime import date, timedelta
import os

random.seed(42)
np.random.seed(42)

# ── Catálogo ──────────────────────────────────────────────────
CATALOGO = {
    "Laptops": {
        "Laptop Lenovo IdeaPad 3i":      2_800_000,
        "Laptop HP Pavilion 15":          3_100_000,
        "MacBook Air M1 256GB":           5_200_000,
        "Laptop ASUS VivoBook 15":        2_500_000,
        "Laptop Dell Inspiron 15":        3_400_000,
    },
    "Celulares": {
        "Samsung Galaxy A54 128GB":         950_000,
        "iPhone 13 128GB":               3_400_000,
        "Xiaomi Redmi Note 12 128GB":      680_000,
        "Motorola Edge 30":              1_200_000,
        "Samsung Galaxy S23":            3_800_000,
    },
    "Periféricos": {
        "Mouse Logitech MX Master 3":      180_000,
        "Teclado Mecánico Redragon K552":  220_000,
        "Audífonos Sony WH-1000XM4":       650_000,
        "Webcam Logitech C920":            280_000,
        "Monitor LG 24 FHD":             1_100_000,
    },
    "Almacenamiento": {
        "Disco SSD Samsung 1TB":           380_000,
        "Memoria USB Kingston 64GB":        42_000,
        "Disco Externo Seagate 2TB":       320_000,
        "Tarjeta SD SanDisk 128GB":         85_000,
        "NAS WD My Cloud 4TB":             820_000,
    },
    "Redes": {
        "Router TP-Link AX1800":           260_000,
        "Switch Cisco 8 puertos":          380_000,
        "Cable UTP Cat6 (rollo 305m)":     220_000,
        "Access Point Ubiquiti UniFi":     650_000,
        "Repetidor WiFi TP-Link":          120_000,
    },
    "Accesorios": {
        'Funda Laptop 15"':                 45_000,
        "Hub USB-C 7 en 1":                 95_000,
        "Cable HDMI 2.0 2m":                28_000,
        "Mousepad XL Gaming":               65_000,
        "Soporte Laptop Ajustable":          88_000,
    },
}

CIUDADES  = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga"]
VENDEDORES = ["Camila Torres", "Andrés Ruiz", "Valentina Gómez",
              "Luis Martínez", "Diana Pérez"]
CANALES   = ["Tienda física", "Página web", "WhatsApp Business", "Mercado Libre"]

def generar_registros(n=1200):
    rows = []
    inicio = date(2023, 1, 1)
    fin    = date(2023, 12, 31)
    total_dias = (fin - inicio).days

    cat_list = list(CATALOGO.keys())
    # Distribución de ventas por categoría (no uniforme — más realista)
    cat_pesos = [0.12, 0.25, 0.22, 0.15, 0.12, 0.14]

    for _ in range(n):
        dias   = random.randint(0, total_dias)
        fecha  = inicio + timedelta(days=dias)
        cat    = random.choices(cat_list, weights=cat_pesos)[0]
        prod   = random.choice(list(CATALOGO[cat].keys()))
        precio = CATALOGO[cat][prod]

        # Variación de precio ±8 %
        precio_venta = round(precio * random.uniform(0.92, 1.08), -3)

        # Cantidades: artículos caros → 1; baratos → 1–4
        if precio >= 1_000_000:
            cantidad = random.choices([1, 2], weights=[0.85, 0.15])[0]
        elif precio >= 300_000:
            cantidad = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        else:
            cantidad = random.choices([1, 2, 3, 4, 5], weights=[0.35, 0.3, 0.2, 0.1, 0.05])[0]

        # Descuento (solo algunos registros)
        descuento = random.choices([0, 5, 10, 15, 20], weights=[0.55, 0.2, 0.15, 0.07, 0.03])[0]
        total = round(precio_venta * cantidad * (1 - descuento / 100), 0)

        rows.append({
            "fecha":         fecha,
            "categoria":     cat,
            "producto":      prod,
            "precio_unitario": precio_venta,
            "cantidad":      cantidad,
            "descuento_pct": descuento,
            "total_venta":   total,
            "ciudad":        random.choices(CIUDADES, weights=[0.40, 0.22, 0.18, 0.11, 0.09])[0],
            "canal_venta":   random.choices(CANALES, weights=[0.38, 0.32, 0.18, 0.12])[0],
            "vendedor":      random.choice(VENDEDORES),
        })

    df = pd.DataFrame(rows).sort_values("fecha").reset_index(drop=True)
    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generar_datos = generar_registros(1200)
    df.to_csv("data/ventas_2023.csv", index=False)
    print(f"✅ data/ventas_2023.csv generado — {len(df)} registros, "
          f"${df['total_venta'].sum():,.0f} COP en ventas totales.")
