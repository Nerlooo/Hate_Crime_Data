"""
Composant : pied de page du dashboard.
"""

from dash import html
import dash_bootstrap_components as dbc
from config import NUM_AGENCIES, POP_COVERED


def build_footer() -> dbc.Container:
    """
    Construit le pied de page avec la source des données.

    Returns:
        Composant Dash de pied de page.
    """
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P(
                    [
                        "Source: ",
                        html.A(
                            "FBI Uniform Crime Reporting - Hate Crime Statistics 2024",
                            href="https://ucr.fbi.gov/hate-crime/2024",
                            target="_blank",
                        ),
                        f" | {NUM_AGENCIES:,} agencies | "
                        f"Population covered: {POP_COVERED:,}",
                    ],
                    className="text-muted small text-center mb-0",
                ),
                width=12,
            )
        ),
        fluid=True,
        className="border-top py-3 mt-4 px-4",
    )
