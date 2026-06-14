"""
Analyse géographique Plotly : taux d'incidents par État.
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS


def make_states_bar(t12_states: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """
    Horizontal bars of the N states with the highest rate per 100k population.

    Args:
        t12_states: Cleaned DataFrame Table 12 (must have incidents_per_100k).
        top_n:      number of states to display.

    Returns:
        Plotly Figure.
    """
    df = t12_states.dropna(subset=["incidents_per_100k"])
    top = df.nlargest(top_n, "incidents_per_100k").sort_values("incidents_per_100k")

    bar_colors = [
        COLORS["primary"] if v > 5 else COLORS["highlight"]
        for v in top["incidents_per_100k"]
    ]

    fig = go.Figure(
        go.Bar(
            x=top["incidents_per_100k"],
            y=top["Participating State/Federal"],
            orientation="h",
            marker_color=bar_colors,
            text=top["incidents_per_100k"].apply(lambda v: f"{v:.1f}"),
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Rate: %{x:.2f} per 100k<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title=f"Top {top_n} States - Hate Crime Rate per 100,000 Population",
        xaxis_title="Incidents per 100,000 inhabitants",
        yaxis_title="",
        height=max(380, top_n * 28),
        margin=dict(l=10, r=60, t=50, b=40),
        plot_bgcolor="#FAFAFA",
        paper_bgcolor="#FAFAFA",
    )
    return fig


def make_states_choropleth(t12_states: pd.DataFrame) -> go.Figure:
    """
    Choropleth map of US states colored by incident rate.

    Args:
        t12_states: Cleaned DataFrame Table 12.

    Returns:
        Plotly choropleth Figure.
    """
    # Correspondance nom → code 2 lettres
    _abbr = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
        "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
        "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
        "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
        "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
        "District of Columbia": "DC",
    }

    df = t12_states.dropna(subset=["incidents_per_100k"]).copy()
    df["state_code"] = df["Participating State/Federal"].map(_abbr)
    df = df.dropna(subset=["state_code"])

    fig = px.choropleth(
        df,
        locations="state_code",
        locationmode="USA-states",
        color="incidents_per_100k",
        scope="usa",
        color_continuous_scale="Reds",
        hover_name="Participating State/Federal",
        hover_data={"incidents_per_100k": ":.2f", "state_code": False},
        labels={"incidents_per_100k": "Per 100k population"},
        title="Hate Crime Rate by State (2024)",
    )
    fig.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="#FAFAFA",
        coloraxis_colorbar_title="Per 100k",
    )
    return fig
