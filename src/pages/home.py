"""
Main dashboard layout: tabs and containers.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

from src.components.header import build_header
from src.components.navbar import build_navbar
from src.components.footer import build_footer


def build_tab_biais() -> html.Div:
    """
    Build the Bias Motivations tab layout.

    Returns:
        Div Dash with controls and charts.
    """
    return html.Div([
        dbc.Row([
            # Controls
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters"),
                    dbc.CardBody([
                        html.Label("Number of bias motivations"),
                        dcc.Slider(
                            id="slider-top-n-biais",
                            min=5, max=30, step=5, value=15,
                            marks={i: str(i) for i in range(5, 31, 5)},
                        ),
                        html.Hr(),
                        html.Label("Bias category"),
                        dcc.Dropdown(
                            id="dropdown-category",
                            options=[
                                {"label": "All", "value": "Toutes"},
                                {"label": "Race/Ethnicity/Ancestry", "value": "Race/Ethnicité/Ancestralité"},
                                {"label": "Religion", "value": "Religion"},
                                {"label": "Sexual orientation", "value": "Orientation sexuelle"},
                            ],
                            value="Toutes",
                            clearable=False,
                        ),
                    ]),
                ], className="mb-3"),
            ], md=3),

            # Main chart
            dbc.Col([
                dcc.Graph(id="graph-bias-bar"),
            ], md=9),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="graph-bias-pie"), md=6),
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Key Statistics"),
                    dbc.CardBody(id="card-bias-stats"),
                ]),
                md=6,
            ),
        ]),
    ])


def build_tab_infractions() -> html.Div:
    """
    Build the Offense Types tab layout.

    Returns:
        Div Dash with control and chart.
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters"),
                    dbc.CardBody([
                        html.Label("Number of offense types"),
                        dcc.Slider(
                            id="slider-top-n-offenses",
                            min=5, max=20, step=5, value=10,
                            marks={i: str(i) for i in range(5, 21, 5)},
                        ),
                    ]),
                ]),
            ], md=3),
            dbc.Col(dcc.Graph(id="graph-offense-bar"), md=9),
        ]),
    ])


def build_tab_geo() -> html.Div:
    """
    Build the Geographic Analysis tab layout.

    Returns:
        Div Dash with choropleth map and state bars.
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters"),
                    dbc.CardBody([
                        html.Label("Top N States"),
                        dcc.Slider(
                            id="slider-top-n-states",
                            min=5, max=51, step=5, value=15,
                            marks={i: str(i) for i in range(5, 52, 10)},
                        ),
                        html.Hr(),
                        html.Label("View"),
                        dcc.RadioItems(
                            id="radio-geo-view",
                            options=[
                                {"label": "Bars", "value": "bar"},
                                {"label": "Map", "value": "map"},
                            ],
                            value="bar",
                            inline=True,
                        ),
                    ]),
                ]),
            ], md=3),
            dbc.Col(dcc.Graph(id="graph-geo"), md=9),
        ]),
    ])


def build_tab_auteurs() -> html.Div:
    """
    Build the Offender Profile tab layout.

    Returns:
        Div Dash with two charts side by side.
    """
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters"),
                    dbc.CardBody([
                        html.Label("Top N locations"),
                        dcc.Slider(
                            id="slider-top-n-locations",
                            min=5, max=30, step=5, value=12,
                            marks={i: str(i) for i in range(5, 31, 5)},
                        ),
                    ]),
                ]),
            ], md=3),
            dbc.Col(dcc.Graph(id="graph-offender-race"), md=9),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id="graph-locations"), md=12),
        ], className="mt-3"),
    ])


def build_layout() -> html.Div:
    """
    Build the complete dashboard layout.

    Returns:
        Root Div of the Dash dashboard.
    """
    return html.Div([
        build_header(),
        build_navbar(),
        dbc.Container(
            html.Div(id="tab-content"),
            fluid=True,
            className="px-4",
        ),
        build_footer(),
    ])
