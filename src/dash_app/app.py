"""
Central Dash instance and callback registration.
"""

import dash
import dash_bootstrap_components as dbc

# Shared Dash instance - imported by main.py and pages
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    title="FBI Hate Crime 2024",
)
server = app.server
