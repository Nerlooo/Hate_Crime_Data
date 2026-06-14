"""
Component: hate crime rate by state (per 100,000 population).
"""

import pandas as pd
import matplotlib.patches as mpatches
from config import COLORS


def plot_states_rate(ax, t12_states: pd.DataFrame) -> None:
    """
    Plot a horizontal bar chart of the top 15 states with the highest
    incident rate per 100,000 population.

    Args:
        ax:         matplotlib axes to plot on.
        t12_states: Cleaned DataFrame Table 12.
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

    ax.set_xlabel("Incidents per 100,000 population")
    ax.set_title(
        "Top 15 States - Hate Crime Rate per 100,000 Population",
        fontweight="bold",
    )

    patch_h = mpatches.Patch(color=COLORS["highlight"], label="> 5 per 100k")
    patch_s = mpatches.Patch(color=COLORS["secondary"], label="<= 5 per 100k")
    ax.legend(handles=[patch_h, patch_s], loc="lower right")