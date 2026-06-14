"""
Page : profil des auteurs connus (race) et lieux d'incidents.
"""

import seaborn as sns
import pandas as pd
from config import COLORS


def add_offenders_section(
    ax5,
    ax6,
    t9_race: pd.DataFrame,
    t10_locations: pd.DataFrame,
) -> None:
    """
    Peuple ax5 (profil racial) et ax6 (lieux d'incidents).

    Args:
        ax5:           axes pour le graphique racial.
        ax6:           axes pour le graphique des lieux.
        t9_race:       sous-table race de la Table 9.
        t10_locations: table des lieux nettoyée (Table 10).
    """
    _plot_offender_race(ax5, t9_race)
    _plot_incident_locations(ax6, t10_locations)


def _plot_offender_race(ax, t9_race: pd.DataFrame) -> None:
    race_labels = t9_race["Race/Ethnicity/Age"].str.strip().tolist()
    race_vals   = t9_race["Total"].tolist()
    total_race  = sum(race_vals)
    pcts        = [v / total_race * 100 for v in race_vals]

    bars5 = ax.bar(
        range(len(race_labels)), race_vals,
        color=COLORS["palette"], edgecolor="white",
    )
    ax.set_xticks(range(len(race_labels)))
    ax.set_xticklabels(
        [l.replace(" or ", "\nor ").replace(" and ", "\nand ") for l in race_labels],
        fontsize=7.5, rotation=15, ha="right",
    )
    for i, (v, p) in enumerate(zip(race_vals, pcts)):
        ax.text(i, v + 30, f"{int(v):,}\n({p:.1f}%)", ha="center", fontsize=7.5)

    ax.set_ylabel("Nombre d'auteurs")
    ax.set_title("Race des auteurs connus (Table 9)", fontweight="bold")


def _plot_incident_locations(ax, t10_locations: pd.DataFrame) -> None:
    top_loc  = t10_locations.head(12).sort_values("Total\nincidents")
    palette6 = sns.color_palette("Blues_r", len(top_loc))

    ax.barh(top_loc["Location"].str.strip(), top_loc["Total\nincidents"], color=palette6)
    for i, (_, row) in enumerate(top_loc.iterrows()):
        ax.text(
            row["Total\nincidents"] + 5, i,
            f"{int(row['Total\nincidents']):,}",
            va="center", fontsize=8.5,
        )

    ax.set_xlabel("Incidents")
    ax.set_title("Lieux les plus fréquents (top 12)", fontweight="bold")