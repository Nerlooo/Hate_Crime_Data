"""
Composants Plotly : profil des auteurs (Table 9) et lieux (Table 10).
"""

import pandas as pd
import plotly.graph_objects as go
from config import COLORS


def make_offender_race_bar(t9_race: pd.DataFrame) -> go.Figure:
    """
    Barres de la répartition raciale des auteurs connus.

    Args:
        t9_race: sous-table race de la Table 9.

    Returns:
        Figure Plotly.
    """
    labels = t9_race.iloc[:, 0].astype(str).str.strip().tolist()
    values = pd.to_numeric(t9_race.iloc[:, 1], errors="coerce").fillna(0).tolist()
    total  = sum(values)
    pcts   = [v / total * 100 if total > 0 else 0 for v in values]

    fig = go.Figure(
        go.Bar(
            x=labels,
            y=values,
            marker_color=COLORS["palette"][: len(labels)],
            text=[f"{int(v):,}<br>({p:.1f}%)" for v, p in zip(values, pcts)],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>%{y:,} auteurs<extra></extra>",
        )
    )
    fig.update_layout(
        title="Race des auteurs connus (Table 9)",
        yaxis_title="Nombre d'auteurs",
        height=400,
        margin=dict(l=10, r=10, t=50, b=80),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FAFAFA",
    )
    return fig


def make_locations_bar(t10_locations: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """
    Barres horizontales des lieux d'incidents les plus fréquents.

    Args:
        t10_locations: DataFrame Table 10 nettoyé.
        top_n:         nombre de lieux à afficher.

    Returns:
        Figure Plotly.
    """
    val_col = "Total incidents"
    top = t10_locations.head(top_n).sort_values(val_col)

    blues = [
        f"rgba(41, {128 - i * 8}, {185 - i * 10}, 0.85)"
        for i in range(len(top))
    ]

    fig = go.Figure(
        go.Bar(
            x=pd.to_numeric(top[val_col], errors="coerce"),
            y=top["Location"].astype(str).str.strip(),
            orientation="h",
            marker_color=blues,
            text=pd.to_numeric(top[val_col], errors="coerce").apply(lambda v: f"{int(v):,}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>%{x:,} incidents<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Lieux les plus fréquents (top {top_n})",
        xaxis_title="Incidents",
        yaxis_title="",
        height=400,
        margin=dict(l=10, r=60, t=50, b=40),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FAFAFA",
    )
    return fig
