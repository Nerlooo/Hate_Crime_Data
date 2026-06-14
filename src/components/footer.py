"""
Composant : pied de figure avec la source et les métadonnées.
"""

import matplotlib.pyplot as plt
from config import COLORS, NUM_AGENCIES, POP_COVERED


def add_figure_footer(fig: plt.Figure) -> None:
    """
    Ajoute la mention de source en bas de la figure.

    Args:
        fig: figure matplotlib cible.
    """
    fig.text(
        0.5, 0.01,
        f"Source : FBI Uniform Crime Reporting — Hate Crime Statistics 2024  |  "
        f"{NUM_AGENCIES:,} agences participantes  |  "
        f"Population couverte : {POP_COVERED:,}",
        ha="center",
        fontsize=9,
        color=COLORS["neutral"],
    )