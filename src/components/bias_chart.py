"""
Composant Plotly : motivations de biais (Table 1).
"""

import pandas as pd
import plotly.graph_objects as go
from config import COLORS


def make_bias_bar(
    t1_detail: pd.DataFrame,
    top_n: int = 15,
    category_filter: str = "Toutes",
) -> go.Figure:
    """
    Génère un graphique en barres horizontales des motivations de biais.

    Args:
        t1_detail:       DataFrame complet Table 1.
        top_n:           nombre de motivations à afficher.
        category_filter: filtre sur la grande catégorie (optionnel).

    Returns:
        Figure Plotly.
    """
    # Exclure les lignes agrégées
    exclude = [
        "Total", "Single-Bias Incidents", "Multiple-Bias Incidents",
        "Race/Ethnicity/Ancestry:", "Religion:", "Sexual Orientation:",
        "Disability:", "Gender:", "Gender Identity:",
    ]
    df = t1_detail[~t1_detail["Bias motivation"].isin(exclude)].copy()

    # Filtre optionnel par catégorie
    _cat_map = {
        "Race/Ethnicité/Ancestralité": ["Anti-Black or African American", "Anti-White",
                                         "Anti-Hispanic or Latino", "Anti-Asian",
                                         "Anti-Arab", "Anti-American Indian or Alaska Native",
                                         "Anti-Multiple Races, Group"],
        "Religion": ["Anti-Jewish", "Anti-Islamic (Muslim)", "Anti-Catholic",
                     "Anti-Protestant", "Anti-Other Religion"],
        "Orientation sexuelle": ["Anti-Gay (Male)", "Anti-Lesbian", "Anti-Bisexual",
                                  "Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group)",
                                  "Anti-Heterosexual"],
    }
    if category_filter != "Toutes" and category_filter in _cat_map:
        subset = _cat_map[category_filter]
        df = df[df["Bias motivation"].isin(subset)]

    top = df.nlargest(top_n, "Incidents").sort_values("Incidents")

    colors = [
        COLORS["primary"] if i >= len(top) - 5 else COLORS["secondary"]
        for i in range(len(top))
    ]

    fig = go.Figure(
        go.Bar(
            x=top["Incidents"],
            y=top["Bias motivation"],
            orientation="h",
            marker_color=colors,
            text=top["Incidents"].apply(lambda v: f"{int(v):,}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Incidents : %{x:,}<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"Top {top_n} des motivations de biais (incidents, 2024)",
        xaxis_title="Nombre d'incidents",
        yaxis_title="",
        height=max(400, top_n * 28),
        margin=dict(l=10, r=60, t=50, b=40),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FAFAFA",
    )
    return fig


def make_bias_pie(t1_detail: pd.DataFrame) -> go.Figure:
    """
    Génère un camembert de la répartition par grande catégorie de biais.

    Args:
        t1_detail: DataFrame complet Table 1.

    Returns:
        Figure Plotly.
    """
    cats_labels = [
        "Race/Ethnicity/Ancestry:", "Religion:", "Sexual Orientation:",
        "Gender Identity:", "Disability:", "Gender:",
    ]
    friendly = [
        "Race/Ethnicité", "Religion", "Orientation sexuelle",
        "Identité de genre", "Handicap", "Genre",
    ]

    values = []
    for c in cats_labels:
        row = t1_detail[t1_detail["Bias motivation"] == c]
        values.append(int(row["Incidents"].iloc[0]) if len(row) > 0 else 0)

    fig = go.Figure(
        go.Pie(
            labels=friendly,
            values=values,
            marker_colors=COLORS["palette"],
            hovertemplate="<b>%{label}</b><br>%{value:,} incidents (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        title="Répartition par grande catégorie de biais",
        height=360,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="#FAFAFA",
    )
    return fig
