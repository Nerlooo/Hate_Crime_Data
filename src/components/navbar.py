"""
Composant : barre de navigation et mise en page globale de la figure.
"""

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def build_figure_layout(
    figsize: tuple[int, int] = (22, 28),
    nrows: int = 4,
    ncols: int = 2,
    hspace: float = 0.45,
    wspace: float = 0.35,
) -> tuple[plt.Figure, GridSpec]:
    """
    Crée la figure et retourne la grille de sous-graphiques.

    Args:
        figsize: dimensions de la figure en pouces.
        nrows:   nombre de lignes de la grille.
        ncols:   nombre de colonnes de la grille.
        hspace:  espacement vertical entre sous-graphiques.
        wspace:  espacement horizontal entre sous-graphiques.

    Returns:
        (fig, gs) : figure et GridSpec prêts à recevoir les axes.
    """
    fig = plt.figure(figsize=figsize)
    gs  = fig.add_gridspec(nrows, ncols, hspace=hspace, wspace=wspace)
    return fig, gs