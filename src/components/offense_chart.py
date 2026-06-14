"""
Composants : types d'infractions (Table 2) et camembert des catégories de biais.
"""

import seaborn as sns
import pandas as pd
from config import COLORS


def plot_offense_types(ax, t2_clean: pd.DataFrame) -> None:
    """
    Trace les 10 types d'infractions les plus fréquents (barres horizontales).

    Args:
        ax:       axes matplotlib sur lequel tracer.
        t2_clean: DataFrame nettoyé de la Table 2.
    """
    top_off  = t2_clean.nlargest(10, "Offenses").sort_values("Offenses")
    palette2 = sns.color_palette("Reds_r", len(top_off))

    ax.barh(top_off["Offense type"], top_off["Offenses"], color=palette2)

    for i, (_, row) in enumerate(top_off.iterrows()):
        ax.text(
            row["Offenses"] + 20, i,
            f"{int(row['Offenses']):,}",
            va="center", fontsize=8.5,
        )

    ax.set_title("Types d'infractions (top 10)", fontweight="bold")
    ax.set_xlabel("Nombre d'infractions")


def plot_bias_categories(ax, t1: pd.DataFrame) -> None:
    """
    Trace un camembert de la répartition par grande catégorie de biais.

    Args:
        ax: axes matplotlib sur lequel tracer.
        t1: DataFrame Table 1 sans les lignes agrégées.
    """
    def _val(label: str) -> int:
        return t1[t1["Bias motivation"] == label]["Incidents"].values[0]

    categories = {
        "Race/Ethnicité/\nAncestralité": _val("Race/Ethnicity/Ancestry:"),
        "Religion":                      _val("Religion:"),
        "Orientation\nsexuelle":         _val("Sexual Orientation:"),
        "Identité\nde genre":            _val("Gender Identity:"),
        "Handicap":                      _val("Disability:"),
        "Genre":                         _val("Gender:"),
    }

    cats = pd.Series(categories).sort_values(ascending=False)
    wedges, texts, autotexts = ax.pie(
        cats.values,
        labels=cats.index,
        autopct="%1.1f%%",
        colors=COLORS["palette"],
        startangle=140,
        textprops={"fontsize": 8.5},
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_fontsize(8)

    ax.set_title("Répartition par grande catégorie de biais", fontweight="bold")