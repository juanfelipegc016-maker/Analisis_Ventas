"""
analisis.py
===========
Pipeline de análisis exploratorio de datos de ventas (EDA).

Etapas:
  1. Carga y validación del dataset
  2. Limpieza y enriquecimiento de datos
  3. Estadísticas descriptivas
  4. Análisis por dimensión (categoría, ciudad, canal, vendedor, tiempo)
  5. Generación de 8 gráficas profesionales → /output/graficas/
  6. Exportación de resúmenes a Excel con formato → /output/reporte_ventas.xlsx

Autor : Juan Felipe González Castro
Curso : Análisis de Datos — Ingeniería de Sistemas
Univ  : Universidad Libre · Bogotá
"""

import os
import sys
import warnings

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.gridspec import GridSpec

warnings.filterwarnings("ignore")

# ── Rutas ─────────────────────────────────────────────────────
DATA_PATH   = "data/ventas_2023.csv"
OUTPUT_DIR  = "output"
GRAFICAS_DIR = os.path.join(OUTPUT_DIR, "graficas")
EXCEL_PATH  = os.path.join(OUTPUT_DIR, "reporte_ventas_2023.xlsx")

os.makedirs(GRAFICAS_DIR, exist_ok=True)

# ── Paleta de colores coherente ────────────────────────────────
COLORES = ["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51",
           "#457b9d", "#a8dadc", "#e63946"]
plt.rcParams.update({
    "figure.dpi": 130,
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "--",
})


# ══════════════════════════════════════════════════════════════
# 1. CARGA Y VALIDACIÓN
# ══════════════════════════════════════════════════════════════

def cargar_datos(ruta: str) -> pd.DataFrame:
    if not os.path.exists(ruta):
        sys.exit(f"❌ No se encontró {ruta}. Ejecuta primero: python generar_datos.py")

    df = pd.read_csv(ruta, parse_dates=["fecha"])
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    print(f"📂 Dataset cargado: {len(df):,} filas × {df.shape[1]} columnas")
    return df


# ══════════════════════════════════════════════════════════════
# 2. LIMPIEZA Y ENRIQUECIMIENTO
# ══════════════════════════════════════════════════════════════

def limpiar_enriquecer(df: pd.DataFrame) -> pd.DataFrame:
    antes = len(df)

    # Eliminar nulos en columnas críticas
    df = df.dropna(subset=["fecha", "producto", "cantidad", "precio_unitario", "total_venta"])

    # Eliminar valores imposibles
    df = df[(df["cantidad"] > 0) & (df["precio_unitario"] > 0) & (df["total_venta"] > 0)]

    # Columnas de tiempo
    df["anio"]       = df["fecha"].dt.year
    df["mes"]        = df["fecha"].dt.month
    df["mes_nombre"] = df["fecha"].dt.strftime("%b")
    df["trimestre"]  = df["fecha"].dt.quarter.map({1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"})
    df["dia_semana"] = df["fecha"].dt.day_name()
    df["semana"]     = df["fecha"].dt.isocalendar().week.astype(int)

    print(f"🧹 Limpieza: {antes} → {len(df)} filas (eliminadas: {antes - len(df)})")
    return df.reset_index(drop=True)


# ══════════════════════════════════════════════════════════════
# 3. ESTADÍSTICAS DESCRIPTIVAS
# ══════════════════════════════════════════════════════════════

def mostrar_resumen(df: pd.DataFrame) -> None:
    sep = "=" * 55

    print(f"\n{sep}")
    print("  RESUMEN EJECUTIVO — VENTAS 2023")
    print(sep)
    print(f"  Período         : {df['fecha'].min().date()} → {df['fecha'].max().date()}")
    print(f"  Transacciones   : {len(df):,}")
    print(f"  Ingresos totales: ${df['total_venta'].sum():,.0f} COP")
    print(f"  Ticket promedio : ${df['total_venta'].mean():,.0f} COP")
    print(f"  Ticket mediano  : ${df['total_venta'].median():,.0f} COP")
    print(f"  Unidades vendidas:{df['cantidad'].sum():,}")
    print(f"  Productos únicos: {df['producto'].nunique()}")
    print(f"  Ciudades cubiert: {df['ciudad'].nunique()}")
    print(sep)

    # Mejor mes
    mejor_mes = df.groupby("mes_nombre")["total_venta"].sum().idxmax()
    print(f"\n  📈 Mejor mes       : {mejor_mes}")
    print(f"  🏆 Categoría líder : {df.groupby('categoria')['total_venta'].sum().idxmax()}")
    print(f"  🥇 Producto top    : {df.groupby('producto')['total_venta'].sum().idxmax()}")
    print(f"  🌆 Ciudad líder    : {df.groupby('ciudad')['total_venta'].sum().idxmax()}")
    print(f"  📦 Canal principal : {df.groupby('canal_venta')['total_venta'].sum().idxmax()}")
    print(f"{sep}\n")


# ══════════════════════════════════════════════════════════════
# 4. GRÁFICAS
# ══════════════════════════════════════════════════════════════

MESES_ES = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]

def _guardar(fig, nombre):
    ruta = os.path.join(GRAFICAS_DIR, nombre)
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    print(f"  📊 {nombre}")


def g1_evolucion_mensual(df):
    ventas = df.groupby("mes")["total_venta"].sum()
    unids  = df.groupby("mes")["cantidad"].sum()

    fig, ax1 = plt.subplots(figsize=(11, 4))
    ax2 = ax1.twinx()

    ax1.bar(ventas.index, ventas.values / 1_000_000,
            color=COLORES[0], alpha=0.85, label="Ingresos (M COP)")
    ax2.plot(unids.index, unids.values, color=COLORES[2],
             marker="o", linewidth=2, label="Unidades vendidas")

    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(MESES_ES)
    ax1.set_ylabel("Ingresos (millones COP)")
    ax2.set_ylabel("Unidades vendidas")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.set_title("Evolución Mensual: Ingresos vs Unidades Vendidas", fontsize=13, fontweight="bold")
    fig.tight_layout()
    _guardar(fig, "01_evolucion_mensual.png")


def g2_participacion_categoria(df):
    por_cat = df.groupby("categoria")["total_venta"].sum().sort_values(ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Pie
    wedges, texts, autotexts = ax1.pie(
        por_cat.values,
        labels=por_cat.index,
        autopct="%1.1f%%",
        colors=COLORES[:len(por_cat)],
        startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    for at in autotexts:
        at.set_fontsize(9)
    ax1.set_title("Participación en Ingresos", fontweight="bold")

    # Barras horizontales con valor
    bars = ax2.barh(por_cat.index, por_cat.values / 1_000_000,
                    color=COLORES[:len(por_cat)])
    ax2.bar_label(bars, labels=[f"${v/1e6:.1f}M" for v in por_cat.values], padding=4, fontsize=9)
    ax2.set_xlabel("Ingresos (millones COP)")
    ax2.set_title("Ingresos por Categoría", fontweight="bold")
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))

    fig.suptitle("Análisis por Categoría de Producto", fontsize=13, fontweight="bold", y=1.01)
    fig.tight_layout()
    _guardar(fig, "02_categorias.png")


def g3_top10_productos(df):
    top = (df.groupby("producto")["total_venta"].sum()
             .sort_values(ascending=True).tail(10))

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top.index, top.values / 1_000_000, color=COLORES[1])
    ax.bar_label(bars, labels=[f"${v/1e6:.2f}M" for v in top.values], padding=4, fontsize=9)
    ax.set_xlabel("Ingresos (millones COP)")
    ax.set_title("Top 10 Productos por Ingresos Totales", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
    fig.tight_layout()
    _guardar(fig, "03_top10_productos.png")


def g4_heatmap_semana_mes(df):
    pivot = df.pivot_table(
        index="mes", columns="dia_semana",
        values="total_venta", aggfunc="sum"
    ).reindex(columns=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    pivot.index = MESES_ES

    fig, ax = plt.subplots(figsize=(11, 6))
    im = ax.imshow(pivot.values / 1_000_000, cmap="YlOrRd", aspect="auto")
    plt.colorbar(im, ax=ax, label="Ingresos (M COP)")

    ax.set_xticks(range(7))
    ax.set_xticklabels(["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"])
    ax.set_yticks(range(12))
    ax.set_yticklabels(MESES_ES)
    ax.set_title("Mapa de Calor: Ventas por Día de la Semana y Mes", fontsize=13, fontweight="bold")

    # Anotaciones
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"${val/1e6:.1f}M", ha="center", va="center",
                        fontsize=7, color="black")
    fig.tight_layout()
    _guardar(fig, "04_heatmap_dia_mes.png")


def g5_ciudades(df):
    ciudad = df.groupby("ciudad").agg(
        ingresos=("total_venta", "sum"),
        transacciones=("total_venta", "count"),
        ticket_prom=("total_venta", "mean")
    ).sort_values("ingresos", ascending=False)

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    for ax, col, titulo, fmt in zip(
        axes,
        ["ingresos", "transacciones", "ticket_prom"],
        ["Ingresos Totales", "N° Transacciones", "Ticket Promedio"],
        ["M COP", "txn", "COP"]
    ):
        vals = ciudad[col]
        color_bars = [COLORES[0] if i == 0 else COLORES[6] for i in range(len(ciudad))]
        ax.bar(ciudad.index, vals, color=color_bars, edgecolor="white")
        ax.set_title(titulo, fontweight="bold")
        ax.tick_params(axis="x", rotation=20)
        if fmt == "M COP":
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        elif fmt == "COP":
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    fig.suptitle("Desempeño por Ciudad", fontsize=13, fontweight="bold")
    fig.tight_layout()
    _guardar(fig, "05_ciudades.png")


def g6_canales_canal(df):
    canal = df.groupby("canal_venta").agg(
        ingresos=("total_venta", "sum"),
        transacciones=("total_venta", "count"),
    ).sort_values("ingresos", ascending=False)
    canal["pct"] = canal["ingresos"] / canal["ingresos"].sum() * 100

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(canal.index, canal["ingresos"] / 1_000_000,
                  color=COLORES[:len(canal)], edgecolor="white")
    ax.bar_label(bars,
                 labels=[f"${v/1e6:.1f}M\n({p:.1f}%)"
                         for v, p in zip(canal["ingresos"], canal["pct"])],
                 padding=4, fontsize=9)
    ax.set_ylabel("Ingresos (millones COP)")
    ax.set_title("Ingresos por Canal de Venta", fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))
    fig.tight_layout()
    _guardar(fig, "06_canales_venta.png")


def g7_vendedores(df):
    vend = df.groupby("vendedor").agg(
        ingresos=("total_venta", "sum"),
        transacciones=("total_venta", "count"),
        unidades=("cantidad", "sum"),
        ticket_prom=("total_venta", "mean"),
    ).sort_values("ingresos", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 4))
    x = np.arange(len(vend))
    w = 0.35
    b1 = ax.bar(x - w/2, vend["ingresos"] / 1_000_000,
                w, label="Ingresos (M COP)", color=COLORES[0])
    ax2 = ax.twinx()
    ax2.bar(x + w/2, vend["ticket_prom"] / 1_000,
            w, label="Ticket prom (miles)", color=COLORES[2], alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(vend.index, rotation=15, ha="right")
    ax.set_ylabel("Ingresos (M COP)")
    ax2.set_ylabel("Ticket promedio (miles COP)")
    ax.set_title("Desempeño por Vendedor", fontsize=13, fontweight="bold")

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="lower right")
    fig.tight_layout()
    _guardar(fig, "07_vendedores.png")


def g8_tendencia_semanal(df):
    semanal = df.groupby("semana")["total_venta"].sum()
    rolling = semanal.rolling(window=4, min_periods=1).mean()

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.fill_between(semanal.index, semanal.values / 1_000_000,
                    alpha=0.3, color=COLORES[0])
    ax.plot(semanal.index, semanal.values / 1_000_000,
            color=COLORES[0], linewidth=1.2, alpha=0.6, label="Ventas semanales")
    ax.plot(rolling.index, rolling.values / 1_000_000,
            color=COLORES[4], linewidth=2.5, label="Tendencia (media móvil 4 sem.)")

    ax.set_xlabel("Semana del año")
    ax.set_ylabel("Ingresos (millones COP)")
    ax.set_title("Tendencia Semanal de Ventas — 2023", fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
    ax.legend()
    fig.tight_layout()
    _guardar(fig, "08_tendencia_semanal.png")


# ══════════════════════════════════════════════════════════════
# 5. EXPORTACIÓN A EXCEL CON FORMATO
# ══════════════════════════════════════════════════════════════

def exportar_excel(df: pd.DataFrame) -> None:
    with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:

        # Hoja 1: Datos limpios
        cols_export = ["fecha","categoria","producto","precio_unitario",
                       "cantidad","descuento_pct","total_venta",
                       "ciudad","canal_venta","vendedor"]
        df[cols_export].to_excel(writer, sheet_name="Datos", index=False)

        # Hoja 2: Resumen mensual
        resumen_mes = df.groupby(["mes","mes_nombre","trimestre"]).agg(
            transacciones=("total_venta","count"),
            unidades=("cantidad","sum"),
            ingresos=("total_venta","sum"),
            ticket_promedio=("total_venta","mean"),
        ).reset_index().sort_values("mes")
        resumen_mes.to_excel(writer, sheet_name="Resumen Mensual", index=False)

        # Hoja 3: Por categoría y mes
        cat_mes = df.pivot_table(
            index="mes_nombre", columns="categoria",
            values="total_venta", aggfunc="sum", margins=True, margins_name="TOTAL"
        ).reindex(MESES_ES + ["TOTAL"])
        cat_mes.to_excel(writer, sheet_name="Categoría x Mes")

        # Hoja 4: Top productos
        top_prod = (df.groupby(["categoria","producto"]).agg(
            transacciones=("total_venta","count"),
            unidades=("cantidad","sum"),
            ingresos=("total_venta","sum"),
            pct_descuento_prom=("descuento_pct","mean"),
        ).reset_index().sort_values("ingresos", ascending=False))
        top_prod.to_excel(writer, sheet_name="Productos", index=False)

        # Hoja 5: Por ciudad y canal
        ciudad_canal = df.pivot_table(
            index="ciudad", columns="canal_venta",
            values="total_venta", aggfunc="sum", margins=True, margins_name="TOTAL"
        )
        ciudad_canal.to_excel(writer, sheet_name="Ciudad x Canal")

        # Hoja 6: Vendedores
        vendedores = df.groupby("vendedor").agg(
            transacciones=("total_venta","count"),
            unidades=("cantidad","sum"),
            ingresos=("total_venta","sum"),
            ticket_promedio=("total_venta","mean"),
        ).sort_values("ingresos", ascending=False)
        vendedores.to_excel(writer, sheet_name="Vendedores")

    print(f"  📗 {EXCEL_PATH}")


# ══════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n🔄 Iniciando pipeline de análisis...\n")

    df = cargar_datos(DATA_PATH)
    df = limpiar_enriquecer(df)
    mostrar_resumen(df)

    print("🎨 Generando gráficas:")
    g1_evolucion_mensual(df)
    g2_participacion_categoria(df)
    g3_top10_productos(df)
    g4_heatmap_semana_mes(df)
    g5_ciudades(df)
    g6_canales_canal(df)
    g7_vendedores(df)
    g8_tendencia_semanal(df)

    print("\n📗 Exportando a Excel:")
    exportar_excel(df)

    print("\n✅ Pipeline completado exitosamente.")
    print(f"   Gráficas → {GRAFICAS_DIR}/")
    print(f"   Excel    → {EXCEL_PATH}\n")
