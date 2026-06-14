"""
Composant Plotly : types d'infractions (Table 2).
"""

import pandas as pd
import plotly.graph_objects as go
from config import COLORS


def make_offense_bar(t2_clean: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Trace les N types d'infractions les plus fréquents (barres horizontales).

    Args:
        t2_clean: DataFrame nettoyé Table 2.
        top_n:    nombre d'infractions à afficher.

    Returns:
        Figure Plotly.
    """
    top = t2_clean.nlargest(top_n, "Offenses").sort_values("Offenses")

    reds = [
        f"rgba(192, {57 + i * 18}, {43 + i * 5}, 0.85)"
        for i in range(len(top))
    ]

    fig = go.Figure(
        go.Bar(
            x=top["Offenses"],
            y=top["Offense type"],
            orientation="h",
            marker_color=reds,
            text=top["Offenses"].apply(lambda v: f"{int(v):,}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Infractions : %{x:,}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Types d'infractions (top {top_n})",
        xaxis_title="Nombre d'infractions",
        yaxis_title="",
        height=max(340, top_n * 32),
        margin=dict(l=10, r=60, t=50, b=40),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FAFAFA",
    )
    return fig
