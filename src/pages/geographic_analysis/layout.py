"""
Analyse géographique : mise en page de la section États.
"""

import pandas as pd
import matplotlib.patches as mpatches
from config import COLORS


def add_geographic_section(ax, t12_states: pd.DataFrame) -> None:
    """
    Trace le graphique des 15 États avec le taux d'incidents pour 100k hab.

    Args:
        ax:          axes matplotlib sur lequel tracer.
        t12_states:  DataFrame Table 12 nettoyé avec colonne incidents_per_100k.
    """
    from src.pages.state_chart import plot_states_rate
    plot_states_rate(ax, t12_states)