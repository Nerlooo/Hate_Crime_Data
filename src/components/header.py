"""
Composant : en-tête Dash du dashboard.
"""

from dash import html
import dash_bootstrap_components as dbc
from config import NUM_AGENCIES, POP_COVERED


def build_header() -> dbc.Container:
    """
    Construit l'en-tête principal du dashboard.

    Returns:
        Composant Dash contenant titre + sous-titre.
    """
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div([
                    html.H1(
                        "FBI Hate Crime Statistics 2024",
                        className="text-white fw-bold mb-1",
                    ),
                    html.P(
                        f"Analysis | {NUM_AGENCIES:,} participating agencies | "
                        f"Population covered: {POP_COVERED:,}",
                        className="text-white-50 mb-0",
                    ),
                ]),
                width=12,
            )
        ),
        fluid=True,
        className="bg-dark py-3 px-4 mb-4",
    )
