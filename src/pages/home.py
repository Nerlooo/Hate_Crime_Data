"""
Page principale : assemble tous les graphiques dans une figure unique.
"""

import matplotlib.pyplot as plt

from src.components.navbar       import build_figure_layout
from src.components.header       import add_figure_title
from src.components.footer       import add_figure_footer
from src.components.bias_chart   import plot_bias_motivations
from src.components.offense_chart import plot_offense_types, plot_bias_categories
from src.pages.geographic_analysis.layout import add_geographic_section
from src.pages.offenders import add_offenders_section
from config import OUTPUT_PNG


def render_home(data: dict) -> plt.Figure:
    """
    Construit et retourne la figure complète de l'analyse.

    Args:
        data: dictionnaire contenant les DataFrames nettoyés :
              t1_detail, t1, t2_clean, t9_race, t10_locations, t12_states.

    Returns:
        Figure matplotlib avec tous les graphiques.
    """
    fig, gs = build_figure_layout()
    add_figure_title(fig)

    # ── Ligne 0 : motivations de biais (pleine largeur) ──────────────────
    ax1 = fig.add_subplot(gs[0, :])
    plot_bias_motivations(ax1, data["t1_detail"])

    # ── Ligne 1 : types d'infractions + camembert catégories ─────────────
    ax2 = fig.add_subplot(gs[1, 0])
    plot_offense_types(ax2, data["t2_clean"])

    ax3 = fig.add_subplot(gs[1, 1])
    plot_bias_categories(ax3, data["t1_detail"])

    # ── Ligne 2 : top 15 États (pleine largeur) ───────────────────────────
    ax4 = fig.add_subplot(gs[2, :])
    add_geographic_section(ax4, data["t12_states"])

    # ── Ligne 3 : profil auteurs + lieux ─────────────────────────────────
    ax5 = fig.add_subplot(gs[3, 0])
    ax6 = fig.add_subplot(gs[3, 1])
    add_offenders_section(ax5, ax6, data["t9_race"], data["t10_locations"])

    add_figure_footer(fig)
    return fig


def save_home(fig: plt.Figure) -> None:
    """Sauvegarde la figure dans le dossier images/."""
    fig.savefig(OUTPUT_PNG, dpi=150, bbox_inches="tight")
    print(f"Graphique sauvegardé -> {OUTPUT_PNG}")