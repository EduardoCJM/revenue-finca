"""Paleta y tipografía Finca Vistabonita / Hotel Neptuno.

Inspirado en el logo (verde + azul, montaña) y el estilo rural canario.
"""
from __future__ import annotations

import plotly.graph_objects as go
import plotly.io as pio

# ─── Paleta Finca Vistabonita ───
VERDE_BOTANICO = "#3D6E47"   # primario, naturaleza
VERDE_CLARO    = "#6FA776"   # positivo / bien
AZUL_OCEANO    = "#2E5C7E"   # secundario, mar
AZUL_CLARO     = "#5B8FB9"   # acento frío
DORADO_ARENA   = "#C9A66B"   # acento cálido canario
TERRACOTA      = "#C0492B"   # crítico / negativo
AMBAR          = "#E0A458"   # atención
MARFIL         = "#FAF7F0"   # fondo
GRAFITO        = "#1F2937"   # texto
GRIS_NEUTRO    = "#9CA3AF"   # LY / referencia
GRIS_SUAVE     = "#E5E7EB"   # bordes / grids

# Semánticos
COLOR_CY      = VERDE_BOTANICO
COLOR_LY      = GRIS_NEUTRO
COLOR_BIEN    = VERDE_CLARO
COLOR_MAL     = TERRACOTA
COLOR_NEUTRO  = DORADO_ARENA

# Umbrales de habitaciones libres sobre 17
UMBRALES_LIBRES = [
    (4,  "Excelente",  VERDE_BOTANICO),
    (8,  "Bien",       VERDE_CLARO),
    (11, "Atención",   AMBAR),
    (17, "Crítico",    TERRACOTA),
]

FUENTE = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"


def color_por_libres(libres: float) -> str:
    for lim, _et, col in UMBRALES_LIBRES:
        if libres <= lim:
            return col
    return UMBRALES_LIBRES[-1][2]


def color_pickup(valor: float, ref_pos: float = 5.0) -> str:
    """Escala divergente: rojo si <=0, ámbar si bajo, verde si alto."""
    if valor <= 0:
        return TERRACOTA
    if valor < ref_pos / 2:
        return AMBAR
    if valor < ref_pos:
        return DORADO_ARENA
    return VERDE_CLARO


# ─── Plantilla Plotly ───
TEMPLATE = go.layout.Template()
TEMPLATE.layout = go.Layout(
    font=dict(family=FUENTE, color=GRAFITO, size=13),
    title=dict(font=dict(family=FUENTE, size=16, color=GRAFITO), x=0.0, xanchor="left"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    colorway=[VERDE_BOTANICO, AZUL_OCEANO, DORADO_ARENA, TERRACOTA, AMBAR, AZUL_CLARO, VERDE_CLARO],
    xaxis=dict(
        showgrid=False, showline=True, linecolor=GRIS_SUAVE, linewidth=1,
        ticks="outside", tickcolor=GRIS_SUAVE, tickfont=dict(family=FUENTE, size=12),
    ),
    yaxis=dict(
        showgrid=True, gridcolor=GRIS_SUAVE, gridwidth=1,
        showline=False, ticks="", tickfont=dict(family=FUENTE, size=12),
        zerolinecolor=GRIS_SUAVE,
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0)", bordercolor="rgba(0,0,0,0)",
        font=dict(family=FUENTE, size=12),
    ),
    margin=dict(l=50, r=30, t=70, b=50),
    hoverlabel=dict(bgcolor="white", bordercolor=GRIS_SUAVE, font=dict(family=FUENTE, size=12)),
)
pio.templates["vistabonita"] = TEMPLATE
pio.templates.default = "vistabonita"


# ─── CSS para Streamlit ───
CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp, .stMarkdown, .stMetric, .stButton, .stSelectbox, .stRadio {{
    font-family: {FUENTE};
}}

h1, h2, h3, h4 {{
    font-family: {FUENTE};
    font-weight: 700;
    color: {GRAFITO};
    letter-spacing: -0.01em;
}}

h1 {{
    border-bottom: 3px solid {VERDE_BOTANICO};
    padding-bottom: 0.4rem;
    display: inline-block;
}}

[data-testid="stMetricValue"] {{
    font-family: {FUENTE};
    font-weight: 700;
    color: {GRAFITO};
    font-size: 1.6rem;
}}

[data-testid="stMetricLabel"] {{
    font-family: {FUENTE};
    font-weight: 500;
    color: #6B7280;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

[data-testid="stMetricDelta"] {{
    font-family: {FUENTE};
    font-weight: 600;
    font-size: 0.9rem;
}}

[data-testid="stSidebar"] {{
    background-color: {MARFIL};
    border-right: 1px solid {GRIS_SUAVE};
}}

.stDataFrame, .stTable {{
    font-family: {FUENTE};
}}

div[data-testid="stExpander"] {{
    border: 1px solid {GRIS_SUAVE};
    border-radius: 8px;
}}

/* Bandera de marca arriba */
.brand-bar {{
    background: linear-gradient(90deg, {VERDE_BOTANICO} 0%, {AZUL_OCEANO} 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-family: {FUENTE};
    font-weight: 600;
    letter-spacing: 0.03em;
}}

.legend-pill {{
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 0.4rem;
    color: white;
    font-family: {FUENTE};
}}
</style>
"""
