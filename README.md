# Análisis Exploratorio de Ventas — Tienda de Tecnología (2023)

Analisis de datos en Python sobre ventas anuales de una tienda de tecnología colombiana. Incluye limpieza, EDA, 8 gráficas profesionales y exportación a Excel con múltiples hojas formateadas.

##  Descripción

El proyecto simula un caso real de análisis de datos de negocio:
- **1.200 registros** de ventas con 6 categorías, 30 productos, 5 ciudades y 4 canales de venta
- Distribución de ventas no uniforme para simular comportamiento real del mercado colombiano
- Pipeline modular con etapas bien definidas: carga → limpieza → EDA → visualización → exportación

##  Estructura del Proyecto

```
02-analisis-ventas-python/
├── generar_datos.py            → Genera ventas_2023.csv (ejecutar primero)
├── analisis.py                 → Pipeline principal de análisis
├── requirements.txt
├── data/
│   └── ventas_2023.csv         → Dataset generado (no incluido en git)
└── output/
    ├── graficas/               → 8 gráficas PNG generadas
    │   ├── 01_evolucion_mensual.png
    │   ├── 02_categorias.png
    │   ├── 03_top10_productos.png
    │   ├── 04_heatmap_dia_mes.png
    │   ├── 05_ciudades.png
    │   ├── 06_canales_venta.png
    │   ├── 07_vendedores.png
    │   └── 08_tendencia_semanal.png
    └── reporte_ventas_2023.xlsx → Excel con 6 hojas de análisis
```

## Ejecutar

```bash
# 1. Clonar e instalar dependencias
git clone https://github.com/tu-usuario/02-analisis-ventas-python.git
cd 02-analisis-ventas-python
pip install -r requirements.txt

# 2. Generar el dataset de prueba
python generar_datos.py

# 3. Ejecutar el pipeline completo
python analisis.py
```

##  Gráficas Generadas

| # | Nombre | Tipo | Variables |
|---|--------|------|-----------|
| 1 | Evolución mensual | Barras + línea (2 ejes) | Ingresos vs Unidades/mes |
| 2 | Categorías | Pie + barras horizontales | Participación e ingresos |
| 3 | Top 10 productos | Barras horizontales | Ingresos totales por producto |
| 4 | Mapa de calor | Heatmap | Ventas por día de semana × mes |
| 5 | Ciudades | Barras agrupadas (3 métricas) | Ingresos, transacciones, ticket |
| 6 | Canales de venta | Barras con porcentaje | Ingresos por canal |
| 7 | Vendedores | Barras dobles (2 ejes) | Ingresos vs ticket promedio |
| 8 | Tendencia semanal | Área + media móvil | Tendencia 4 semanas |

## Hojas del Excel Exportado

| Hoja | Contenido |
|------|-----------|
| Datos | Dataset limpio completo (1.200 filas) |
| Resumen Mensual | Métricas agregadas por mes y trimestre |
| Categoría x Mes | Tabla cruzada de ingresos (pivot) |
| Productos | Ranking de productos con métricas |
| Ciudad x Canal | Pivot de ciudad por canal de venta |
| Vendedores | Desempeño individual de cada vendedor |

## Tecnologías y Librerías

| Librería | Uso |
|----------|-----|
| **pandas** | Carga, limpieza, agregación y pivots |
| **numpy** | Cálculos numéricos y media móvil |
| **matplotlib** | Todas las visualizaciones (8 gráficas) |
| **openpyxl** | Exportación a Excel multihojas |

## Conceptos Aplicados

- Limpieza de datos (nulos, outliers, validación de dominio)
- Enriquecimiento: extracción de año, mes, trimestre, día de semana, semana ISO
- Distribución ponderada con `random.choices` para datos realistas
- `pivot_table` con margins para totales automáticos
- Gráficas con doble eje Y (`twinx`)
- Media móvil con `rolling(window=4)`
- `ExcelWriter` con múltiples hojas
