"""
Composant : graphique des 15 principales motivations de biais (Table 1).
"""

import matplotlib.patches as mpatches
import pandas as pd
from config import COLORS
from src.utils.common_functions import bar_label


def plot_bias_motivations(ax, t1_detail: pd.DataFrame) -> None:
    """
    Trace un graphique en barres horizontales des 15 motivations de biais
    les plus fréquentes.

    Args:
        ax:        axes matplotlib sur lequel tracer.
        t1_detail: DataFrame complet de la Table 1 (incluant les agrégats).
    """
    top15 = t1_detail.nlargest(15, "Incidents").sort_values("Incidents")
    bar_colors = [
        COLORS["primary"] if i >= 10 else COLORS["secondary"]
        for i in range(len(top15))
    ]

    bars = ax.barh(
        top15["Bias motivation"],
        top15["Incidents"],
        color=bar_colors,
        edgecolor="white",
    )
    bar_label(ax, bars, offset=15)

    ax.set_xlabel("Nombre d'incidents")
    ax.set_title("Top 15 des motivations de biais (incidents, 2024)", fontweight="bold")
    ax.set_xlim(0, top15["Incidents"].max() * 1.15)
    ax.axvline(x=500, color=COLORS["accent"], lw=1, ls="--", alpha=0.5)

    patch1 = mpatches.Patch(color=COLORS["primary"],   label="Top 5")
    patch2 = mpatches.Patch(color=COLORS["secondary"], label="6e–15e")
    ax.legend(handles=[patch1, patch2], loc="lower right")