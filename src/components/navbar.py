"""
Composant : barre de navigation avec onglets.
"""

from dash import dcc, html
import dash_bootstrap_components as dbc


def build_navbar() -> dbc.Container:
    """
    Construit la barre de navigation par onglets du dashboard.

    Returns:
        Composant Dash contenant les onglets de navigation.
    """
    return dbc.Container(
        dbc.Tabs(
            id="main-tabs",
            active_tab="tab-biais",
            children=[
                dbc.Tab(label="Bias Motivations", tab_id="tab-biais"),
                dbc.Tab(label="Offense Types", tab_id="tab-infractions"),
                dbc.Tab(label="Geographic Analysis", tab_id="tab-geo"),
                dbc.Tab(label="Offender Profile", tab_id="tab-auteurs"),
            ],
            className="mb-3",
        ),
        fluid=True,
        className="px-4",
    )
