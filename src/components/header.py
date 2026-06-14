"""
Composant : en-tête de la figure principale.
"""

import matplotlib.pyplot as plt
from config import COLORS


def add_figure_title(fig: plt.Figure) -> None:
    """
    Ajoute le titre principal centré en haut de la figure.

    Args:
        fig: figure matplotlib cible.
    """
    fig.suptitle(
        "FBI Hate Crime Statistics 2024 — Analyse Complète",
        fontsize=20,
        fontweight="bold",
        color=COLORS["secondary"],
        y=0.98,
    )