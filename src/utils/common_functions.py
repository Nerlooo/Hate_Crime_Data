"""
Fonctions utilitaires partagées entre les différentes pages et composants.
"""

import pandas as pd
import matplotlib.pyplot as plt
from config import MPL_PARAMS, COLORS, NUM_AGENCIES, POP_COVERED


def apply_mpl_style() -> None:
    """Applique la configuration matplotlib globale du projet."""
    plt.rcParams.update(MPL_PARAMS)


def print_national_summary(total_row: pd.Series) -> None:
    """
    Affiche le résumé national dans la console.

    Args:
        total_row: ligne « Total » de t1_detail.
    """
    print("\n" + "═" * 55)
    print("  RÉSUMÉ NATIONAL 2024")
    print("═" * 55)
    print(f"  Incidents totaux       : {int(total_row['Incidents']):>8,}")
    print(f"  Infractions totales    : {int(total_row['Offenses']):>8,}")
    print(f"  Victimes totales       : {int(total_row['Victims1']):>8,}")
    print(f"  Auteurs connus         : {int(total_row['Known\noffenders2']):>8,}")
    print(f"  Agences participantes  : {NUM_AGENCIES:>8,}")
    print(f"  Population couverte    : {POP_COVERED:>8,}")
    print("═" * 55)


def print_complementary_analyses(
    t12_states: pd.DataFrame,
    t2_clean: pd.DataFrame,
    total_row: pd.Series,
) -> None:
    """
    Affiche les analyses complémentaires textuelles.

    Args:
        t12_states: table 12 nettoyée.
        t2_clean:   table 2 nettoyée.
        total_row:  ligne « Total » de t1_detail.
    """
    print("\n" + "═" * 55)
    print("  ANALYSES COMPLÉMENTAIRES")
    print("═" * 55)

    avg_report = t12_states["reporting_rate"].mean()
    top5_report = t12_states.nlargest(5, "reporting_rate")[
        ["Participating State/Federal", "reporting_rate"]
    ]
    print(f"\n📍 Taux moyen de signalement des agences : {avg_report:.1f}%")
    print("  États avec le meilleur taux de signalement :")
    print(top5_report.to_string(index=False))

    print("\n📊 Top 10 États par nombre absolu d'incidents :")
    top10 = t12_states.nlargest(10, "Total\nnumber of\nincidents\nreported")[
        ["Participating State/Federal", "Total\nnumber of\nincidents\nreported", "incidents_per_100k"]
    ]
    print(top10.to_string(index=False))

    violent = [
        "Murder and nonnegligent manslaughter",
        "Rape", "Aggravated assault", "Robbery",
    ]
    violent_sum = t2_clean[t2_clean["Offense type"].isin(violent)]["Offenses"].sum()
    print(f"\n⚠️  Infractions violentes (persons) : {violent_sum:.0f} infractions")

    victims   = int(total_row["Victims1"])
    incidents = int(total_row["Incidents"])
    print(f"\n👥 Ratio moyen victimes/incident : {victims / incidents:.2f}")
    print("\n✅ Analyse terminée.")


def bar_label(ax, bars, fmt: str = "{:,}", offset: float = 15) -> None:
    """
    Ajoute des étiquettes à droite de barres horizontales.

    Args:
        ax:     axes matplotlib.
        bars:   résultat de ax.barh().
        fmt:    format des valeurs.
        offset: décalage horizontal en unités données.
    """
    for bar in bars:
        w = bar.get_width()
        ax.text(
            w + offset,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(int(w)),
            va="center",
            fontsize=9,
        )