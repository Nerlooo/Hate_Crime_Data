# FBI Hate Crime Statistics 2024 Dashboard

## Overview

This project provides an interactive dashboard analyzing FBI hate crime statistics for 2024. The dashboard presents data through multiple visualizations including bias motivations, offense types, geographic distribution, and offender profiles. Built with Python, Dash, and Plotly, it enables exploration of public data on hate crimes reported across the United States.

## User Guide

### Prerequisites

- Python 3.9 or higher
- git
- uv (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository_url>
cd projet_dash
```

2. Install dependencies:
```bash
uv sync
```

3. Run the dashboard:
```bash
uv run python main.py
```

4. Open your browser and navigate to:
```
http://localhost:8050
```

### Dashboard Features

The dashboard consists of four main tabs:

- **Bias Motivations**: Explore the top bias motivations behind hate crimes. Filter by category (all, race/ethnicity, religion, sexual orientation) and adjust the number of displayed motivations. The tab shows a bar chart with top motivations and a pie chart showing the distribution across major bias categories.

- **Offense Types**: Analyze the distribution of offense types reported in hate crime incidents. Adjust the slider to see the top N offense types.

- **Geographic Analysis**: View hate crime rates by state. Toggle between a bar chart of top states and a choropleth map showing the geographic distribution. Rates are normalized per 100,000 population for comparative analysis.

- **Offender Profile**: Examine the demographics of known offenders and the most common locations where hate crimes occur.

### Troubleshooting

If the dashboard fails to start:
1. Verify all dependencies are installed: `uv sync`
2. Ensure port 8050 is available
3. Check that the database file exists in the data/ directory

## Data

### Data Source

- **Source**: FBI Uniform Crime Reporting (UCR) - Hate Crime Statistics 2024
- **URL**: https://ucr.fbi.gov/hate-crime/2024
- **Type**: Public open data, accessed and used without modification
- **Coverage**: 12,400 participating agencies across the United States

### Data Processing

The data pipeline consists of three stages:

1. **Raw Data**: Original FBI hate crime tables are downloaded and stored in `data/db.sqlite` (table `raw_*`)

2. **Data Cleaning**: Raw tables are processed to:
   - Remove missing values and inconsistencies
   - Standardize column names and formats
   - Filter out aggregate rows (totals and subtotals)
   - Calculate derived metrics (incidents per 100k population)
   - Cleaned data is stored in `data/db.sqlite` (table `cleaned_*`)

3. **Data Visualization**: Cleaned data is loaded and presented through interactive charts

### Data Tables Used

- **Table 1**: Bias Motivations (by type and category)
- **Table 2**: Offense Types
- **Table 9**: Offender Demographics (race)
- **Table 10**: Incident Locations
- **Table 12**: Geographic Distribution (by state)

### Database

The project uses SQLite for local data persistence:
- Location: `data/db.sqlite`
- Tables: `raw_*` (original data) and `cleaned_*` (processed data)
- Enables offline dashboard operation after initial data load

## Developer Guide

### Architecture

The project follows a modular architecture separating concerns into distinct layers:

```
main.py
  |
  +-- src/utils/get_data.py        (Data retrieval)
  |     |
  |     v
  +-- src/utils/clean_data.py      (Data processing)
  |     |
  |     v
  +-- src/dash_app/app.py          (Dash application)
  |     |
  |     +-- src/dash_app/callbacks.py (Interactivity)
  |     |
  |     v
  +-- src/pages/home.py            (Page layouts)
  |     |
  |     +-- src/components/        (UI components)
  |     |     |-- header.py
  |     |     |-- navbar.py
  |     |     |-- footer.py
  |     |     |-- bias_chart.py
  |     |     |-- offense_chart.py
  |     |     |-- offenders.py
  |     |
  |     +-- src/pages/*/           (Page-specific layouts)
  |           |-- geographic_analysis/layout.py
```

### Project Structure

```
projet_dash/
  |-- config.py                          Configuration (database, colors, etc.)
  |-- main.py                            Application entry point
  |-- pyproject.toml                     Dependency specification
  |-- README.md                          This file
  |-- data/
  |   |-- db.sqlite                      Local SQLite database
  |   |-- hate_crime_2024/              Raw data storage
  |-- src/
  |   |-- components/                    Reusable UI components
  |   |   |-- bias_chart.py             Bias motivation visualizations
  |   |   |-- offense_chart.py          Offense type visualizations
  |   |   |-- header.py                 Dashboard header
  |   |   |-- navbar.py                 Navigation tabs
  |   |   |-- footer.py                 Dashboard footer
  |   |-- dash_app/
  |   |   |-- app.py                    Dash application instance
  |   |   |-- callbacks.py              Interactive callbacks
  |   |-- pages/
  |   |   |-- home.py                   Main layout builder
  |   |   |-- offenders.py              Offender demographics
  |   |   |-- summary.py                Console output utilities
  |   |   |-- state_chart.py            State-level analysis
  |   |   |-- geographic_analysis/
  |   |       |-- layout.py             Geographic visualizations
  |   |-- utils/
  |   |   |-- get_data.py               Data retrieval functions
  |   |   |-- clean_data.py             Data cleaning functions
  |   |   |-- common_functions.py       Shared utilities
  |-- tests/                             Unit tests (reserved)
```

### Code Organization

**Data Pipeline**: Separation of concerns for data handling
- `get_data.py`: Retrieves data from external sources
- `clean_data.py`: Transforms and validates data
- `config.py`: Centralized configuration

**UI Layer**: Component-based architecture
- Components are reusable, self-contained UI elements
- Pages compose components into complete views
- Callbacks connect UI interactions to data updates

**Styling**: Consistent design through Bootstrap
- `dbc.themes.FLATLY`: Base Bootstrap theme
- Color palette defined in `config.py`

### Adding a New Page

1. Create a new file in `src/pages/`:
```python
from dash import html, dcc
import dash_bootstrap_components as dbc

def build_tab_example() -> html.Div:
    """Build the example tab layout."""
    return html.Div([
        dbc.Row([
            dbc.Col(dcc.Graph(id="graph-example"), md=12)
        ])
    ])
```

2. Import the page in `src/pages/home.py`:
```python
from src.pages.example_page import build_tab_example
```

3. Add a tab to `src/components/navbar.py`:
```python
dbc.Tab(label="Example", tab_id="tab-example"),
```

4. Add routing logic in `src/dash_app/callbacks.py`:
```python
if active_tab == "tab-example":
    return build_tab_example()
```

5. Add callbacks in `src/dash_app/callbacks.py` to update visualizations

### Adding a New Chart

1. Create a visualization function in `src/components/` or `src/pages/`:
```python
import plotly.graph_objects as go

def make_example_chart(data: pd.DataFrame) -> go.Figure:
    """Create example chart."""
    fig = go.Figure(data=[...])
    fig.update_layout(title="Example", height=400)
    return fig
```

2. Add to layout in the appropriate page:
```python
dcc.Graph(id="graph-example")
```

3. Create a callback in `src/dash_app/callbacks.py`:
```python
@app.callback(
    Output("graph-example", "figure"),
    Input("filter-id", "value"),
)
def update_example_chart(filter_val):
    return make_example_chart(data["dataframe"])
```

### Configuration

Key settings in `config.py`:
- `DB_PATH`: SQLite database location
- `DASH_HOST`, `DASH_PORT`: Server configuration
- `COLORS`: Visualization color palette
- `NUM_AGENCIES`, `POP_COVERED`: Summary statistics

### Dependencies

Main packages:
- `dash`: Web framework for interactive applications
- `plotly`: Interactive visualization library
- `pandas`: Data manipulation and analysis
- `dash-bootstrap-components`: Bootstrap styling for Dash
- `sqlite3`: Local database storage

Full dependency list in `pyproject.toml`

## Analysis Report

### Key Findings

1. **Incident Volume**: The 2024 data covers incidents reported by participating agencies across all 50 states and the District of Columbia, representing the most comprehensive hate crime statistics available.

2. **Bias Motivations**: Hate crimes in 2024 are predominantly motivated by race/ethnicity, followed by religious bias. Sexual orientation continues to be a significant bias motivation.

3. **Geographic Variation**: Hate crime rates per capita vary significantly by state. Some states report rates 3-4x higher than the national average, indicating regional disparities in either incident frequency or reporting practices.

4. **Offense Types**: The most frequently reported offenses in hate crime incidents are simple assaults and intimidation, though violent offenses (aggravated assault, robbery, rape) account for a substantial portion.

5. **Offender Demographics**: Where known, offender data reveals patterns in the demographic characteristics of individuals perpetrating hate crimes.

### Interpretation Guidelines

- **Per Capita Rates**: The 100,000 population normalization allows fair comparison across states of different sizes
- **Underreporting**: Actual hate crime incidence may exceed reported statistics due to underreporting
- **Data Quality**: Variation in reporting practices across agencies may affect geographic comparisons
- **Year-over-Year Trends**: Single-year data should be interpreted as a snapshot; multi-year analysis reveals trends

### Limitations

- Data reflects only reported incidents
- Participation by agencies varies by year
- Offense and suspect data may be incomplete
- Jurisdictional reporting differences affect geographic comparisons

---

**Version**: 1.0  
**Last Updated**: 2025-06-14  
**Status**: Complete and ready for evaluation
