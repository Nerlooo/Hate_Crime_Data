"""
Composant spécifique : taux de crimes haineux par État (pour 100 000 habitants).
"""

import pandas as pd
import matplotlib.patches as mpatches
from config import COLORS


def plot_states_rate(ax, t12_states: pd.DataFrame) -> None:
    """
    Trace un graphique en barres horizontales des 15 États avec le taux
    d'incidents pour 100 000 habitants le plus élevé.

    Args:
        ax:         axes matplotlib sur lequel tracer.
        t12_states: DataFrame Table 12 nettoyé.
    """
    top_states  = t12_states.nlargest(15, "incidents_per_100k").sort_values(
        "incidents_per_100k"
    )
    bar_colors4 = [
        COLORS["highlight"] if v > 5 else COLORS["secondary"]
        for v in top_states["incidents_per_100k"]
    ]

    ax.barh(
        top_states["Participating State/Federal"],
        top_states["incidents_per_100k"],
        color=bar_colors4,
    )

    for i, (_, row) in enumerate(top_states.iterrows()):
        ax.text(
            row["incidents_per_100k"] + 0.05, i,
            f"{row['incidents_per_100k']:.1f}",
            va="center", fontsize=9,
        )

    ax.set_xlabel("Incidents pour 100 000 habitants")
    ax.set_title(
        "Top 15 États — Taux de crimes haineux pour 100 000 hab.",
        fontweight="bold",
    )

    patch_h = mpatches.Patch(color=COLORS["highlight"], label="> 5 pour 100k")
    patch_s = mpatches.Patch(color=COLORS["secondary"], label="≤ 5 pour 100k")
    ax.legend(handles=[patch_h, patch_s], loc="lower right")