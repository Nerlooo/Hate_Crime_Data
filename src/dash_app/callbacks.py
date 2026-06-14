"""
Registration of all Dash callbacks (dashboard interactivity).
"""

from dash import Input, Output, html
import dash_bootstrap_components as dbc
import pandas as pd

from src.dash_app.app import app
from src.components.bias_chart    import make_bias_bar, make_bias_pie
from src.components.offense_chart import make_offense_bar
from src.pages.geographic_analysis.layout import make_states_bar, make_states_choropleth
from src.pages.offenders          import make_offender_race_bar, make_locations_bar
from src.pages.home import (
    build_tab_biais, build_tab_infractions,
    build_tab_geo, build_tab_auteurs,
)


def register_callbacks(data: dict[str, pd.DataFrame]) -> None:
    """
    Register all callbacks by capturing DataFrames in closure.

    Args:
        data: dictionary {name: DataFrame} produced by the cleaning pipeline.
    """

    # Tab routing
    @app.callback(
        Output("tab-content", "children"),
        Input("main-tabs", "active_tab"),
    )
    def render_tab(active_tab: str) -> html.Div:
        """Display the layout corresponding to the active tab."""
        if active_tab == "tab-biais":
            return build_tab_biais()
        if active_tab == "tab-infractions":
            return build_tab_infractions()
        if active_tab == "tab-geo":
            return build_tab_geo()
        if active_tab == "tab-auteurs":
            return build_tab_auteurs()
        return html.Div("Unknown tab")

    # Bias tab: main chart
    @app.callback(
        Output("graph-bias-bar", "figure"),
        Input("slider-top-n-biais",  "value"),
        Input("dropdown-category",   "value"),
    )
    def update_bias_bar(top_n: int, category: str):
        """Update the bias motivations bar chart."""
        return make_bias_bar(data["t1_detail"], top_n=top_n, category_filter=category)

    # Bias tab: pie chart
    @app.callback(
        Output("graph-bias-pie", "figure"),
        Input("main-tabs", "active_tab"),
    )
    def update_bias_pie(_tab):
        """Update the pie chart (independent of filters)."""
        return make_bias_pie(data["t1_detail"])

    # Bias tab: statistics card
    @app.callback(
        Output("card-bias-stats", "children"),
        Input("dropdown-category", "value"),
    )
    def update_bias_stats(category: str) -> list:
        """Display key statistics based on selected category."""
        t1d = data["t1_detail"]
        total_row = t1d[t1d["Bias motivation"] == "Total"]
        if len(total_row) == 0:
            return [html.P("Data unavailable")]

        total_inc = int(total_row["Incidents"].iloc[0])
        total_off = int(total_row["Offenses"].iloc[0]) if "Offenses" in total_row.columns else "N/A"

        exclude = [
            "Total", "Single-Bias Incidents", "Multiple-Bias Incidents",
            "Race/Ethnicity/Ancestry:", "Religion:", "Sexual Orientation:",
            "Disability:", "Gender:", "Gender Identity:",
        ]
        df_detail = t1d[~t1d["Bias motivation"].isin(exclude)]
        top_motive = df_detail.nlargest(1, "Incidents")["Bias motivation"].values[0]

        return [
            dbc.ListGroup([
                dbc.ListGroupItem([html.Strong("Total incidents: "), f"{total_inc:,}"]),
                dbc.ListGroupItem([html.Strong("Total offenses: "), f"{total_off:,}"]),
                dbc.ListGroupItem([html.Strong("Top motivation: "), top_motive]),
                dbc.ListGroupItem([html.Strong("Filtered category: "), category]),
            ], flush=True),
        ]

    # Offense tab
    @app.callback(
        Output("graph-offense-bar", "figure"),
        Input("slider-top-n-offenses", "value"),
    )
    def update_offense_bar(top_n: int):
        """Update the offense types chart."""
        return make_offense_bar(data["t2_clean"], top_n=top_n)

    # Geography tab
    @app.callback(
        Output("graph-geo", "figure"),
        Input("slider-top-n-states", "value"),
        Input("radio-geo-view",       "value"),
    )
    def update_geo(top_n: int, view: str):
        """Toggle between choropleth map and bars based on radio button."""
        if view == "map":
            return make_states_choropleth(data["t12_states"])
        return make_states_bar(data["t12_states"], top_n=top_n)

    # Offender tab: race
    @app.callback(
        Output("graph-offender-race", "figure"),
        Input("main-tabs", "active_tab"),
    )
    def update_offender_race(_tab):
        """Display the racial distribution of known offenders."""
        return make_offender_race_bar(data["t9_race"])

    # Offender tab: locations
    @app.callback(
        Output("graph-locations", "figure"),
        Input("slider-top-n-locations", "value"),
    )
    def update_locations(top_n: int):
        """Update the incident locations chart."""
        return make_locations_bar(data["t10_locations"], top_n=top_n)
