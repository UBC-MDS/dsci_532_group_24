import altair as alt
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import nbformat
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import os

# Import data
clean_data = pd.read_pickle("data/clean_data.pkl")
disease_count_data = pd.read_pickle("data/disease_count_data.pkl")
disease_count_data_pc = pd.read_pickle("data/disease_count_data_pc.pkl")
disease_count_map_data = pd.read_pickle("data/disease_count_map_data.pkl")
disease_count_map_data_pc = pd.read_pickle("data/disease_count_map_data_pc.pkl")

## Make country and disease lists
country_list = list(clean_data["country"].unique())

disease_list = [
    "HIV",
    "Malaria",
    "Measles",
    "Meningitis",
    "NCD",
]

default_country_list = [
    "Nigeria",
    "Congo, Dem, Rep.",
    "Niger",
    "Burkina Faso",
    "Mali",
    "South Africa",
    "Ethiopia",
    "Mozambique",
    "Sierra Leone",
    "South Sudan",
    "Central African Republic",
    "Chad",
    "Guinea",
]
# Define elements

## Trend tab
### Statatistic type controller
stat_type_controller_trend = html.Div(
    [
        dcc.RadioItems(
            id="stat_type_widget_trend",
            options=[
                {"label": "Raw number of deaths", "value": "raw_stats"},
                {"label": "Deaths per thousand 0-4 year-olds", "value": "pc_k"},
            ],
            value="raw_stats",
            labelStyle={"display": "block"},
        ),
    ]
)

### Year range controller
year_range_controller_trend = html.Div(
    [
        dcc.RangeSlider(
            id="year_range_widget_trend",
            min=1990,
            max=2015,
            value=[2000, 2010],
            marks={
                1990: "1990",
                1995: "1995",
                2000: "2000",
                2005: "2005",
                2010: "2010",
                2015: "2015",
            },
        ),
    ]
)

### Country controller
country_controller_trend = html.Div(
    [
        dcc.Dropdown(
            id="country_widget_trend",
            value=default_country_list,
            placeholder="Select a country...",
            options=[{"label": country, "value": country} for country in country_list],
            multi=True,
        ),
    ]
)

### Disease controller
disease_controller_trend = html.Div(
    [
        dcc.Dropdown(
            id="disease_widget_trend",
            value=disease_list,
            placeholder="Select a disease...",
            options=[{"label": disease, "value": disease} for disease in disease_list],
            multi=True,
        ),
    ]
)

## Snapshot tab
###Statistic type controller
stat_type_controller_snapshot = html.Div(
    [
        dcc.RadioItems(
            id="stat_type_widget_snapshot",
            options=[
                {"label": "Raw number of deaths", "value": "raw_stats"},
                {"label": "Deaths per thousand 0-4 year-olds", "value": "pc_k"},
            ],
            value="raw_stats",
            labelStyle={"display": "block"},
        ),
    ]
)

### Year controller
year_controller_snapshot = html.Div(
    [
        dcc.Slider(
            id="year_widget_snapshot",
            min=1990,
            max=2015,
            value=2005,
            marks={
                1990: "1990",
                1995: "1995",
                2000: "2000",
                2005: "2005",
                2010: "2010",
                2015: "2015",
            },
            included=False,
        ),
    ]
)

### Country controller
country_controller_snapshot = html.Div(
    [
        dcc.Dropdown(
            id="country_widget_snapshot",
            value=default_country_list,
            placeholder="Select a country...",
            options=[{"label": country, "value": country} for country in country_list],
            multi=True,
        ),
    ]
)

### Disease controller
disease_controller_snapshot = html.Div(
    [
        dcc.Dropdown(
            id="disease_widget_snapshot",
            value=disease_list,
            placeholder="Select a disease...",
            options=[{"label": disease, "value": disease} for disease in disease_list],
            multi=True,
        ),
    ]
)

### Default number selector
default_number_selector_snapshot = html.Div(
    [
        html.Div(
            [
                html.H6(
                    """Select maximum number of countries to show""",
                    style={"margin-right": "1em"},
                )
            ],
        ),
        dcc.Dropdown(
            id="default_number_widget_snapshot",
            options=[{"label": str(n), "value": n} for n in range(3, 11)],
            value=8,
            style=dict(width="40%", verticalAlign="middle"),
        ),
    ],
    style=dict(display="flex"),
)

## information tab
table_header = [html.Thead(html.Tr([html.Th("Variable"), html.Th("Source")]))]

row1 = html.Tr(
    [
        html.Td("The total number of children dying before age 5"),
        html.Td(
            html.A(
                "World Health Organization",
                href="https://www.who.int/data/maternal-newborn-child-adolescent-ageing/child-data",
            )
        ),
    ]
)
row2 = html.Tr(
    [
        html.Td(
            "HIV, malaria, measles, meningitis and NCD (non-communicable disease) deaths in children 1-59 months"
        ),
        html.Td(
            html.A(
                "World Health Organization",
                href="https://www.who.int/data/maternal-newborn-child-adolescent-ageing/child-data",
            )
        ),
    ]
)
row3 = html.Tr(
    [
        html.Td("Population aged from 0 to 4 year-olds by country"),
        html.Td(
            html.A(
                "The United Nations, 2019 Revision of World Population Prospects",
                href="https://population.un.org/wpp/",
            )
        ),
    ]
)

table_body = [html.Tbody([row1, row2, row3])]

information_tab = [
    html.Br(),
    html.P(
        """
        This app is developed as part of DSCI 532's coursework. We intend to provide information to staff and volunteers at an international charity whose work focuses on healthcare and medication to children in Africa.
        The underlying dataset of this app is obtained from Gapminder, an independent Swedish foundation, with a mission to fight misconceptions and promotes a fact-based worldview.
        The table below summarizes the key data sources used in the app. 
        """
    ),
    html.Br(),
    dbc.Table(table_header + table_body, bordered=True, size=3),
]

# Define app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        html.H1(
                            "Trends of Child Diseases and Mortality in Africa, 1990 - 2015"
                        ),
                        html.P(
                            "App Developed by Junghoo Kim, Mark Wang and Zhenrui (Eric) Yu"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Select statistic type: "),
                                                stat_type_controller_trend,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Filter Country: "),
                                                country_controller_trend,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Filter Year: "),
                                                year_range_controller_trend,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Filter Disease: "),
                                                disease_controller_trend,
                                            ]
                                        ),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Col(
                                            [
                                                html.Iframe(
                                                    id="country_chart_trend",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "100%",
                                                        "height": "50vh",
                                                    },
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Iframe(
                                                    id="disease_chart_trend",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "100%",
                                                        "height": "50vh",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    label="Trend",
                ),
                dbc.Tab(
                    [
                        html.H1("Child Diseases and Mortality in Africa, 1990 - 2015"),
                        html.P(
                            "App Developed by Junghoo Kim, Mark Wang and Zhenrui (Eric) Yu"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Select statistic type: "),
                                                stat_type_controller_snapshot,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Filter Country: "),
                                                country_controller_snapshot,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Select Year: "),
                                                year_controller_snapshot,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.Label("Filter Disease: "),
                                                disease_controller_snapshot,
                                            ]
                                        ),
                                    ],
                                    md=3,
                                ),
                                dbc.Col(
                                    [
                                        default_number_selector_snapshot,
                                        html.Iframe(
                                            id="country_chart_snapshot",
                                            style={
                                                "border-width": "0",
                                                "width": "120%",
                                                "height": "100%",
                                            },
                                        ),
                                        "Diseases by Number of Deaths",
                                        html.Iframe(
                                            id="disease_chart_snapshot",
                                            style={
                                                "border-width": "0",
                                                "width": "120%",
                                                "height": "100%",
                                            },
                                        ),
                                    ],
                                    md=4.5,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dcc.Graph(
                                                    id="map_snapshot",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "0vh",
                                                        "height": "0vh",
                                                    },
                                                )
                                            ]
                                        )
                                    ],
                                    md=4.5,
                                ),
                            ]
                        ),
                    ],
                    label="Snapshot",
                ),
                dbc.Tab(information_tab, label="Data Source and Explanation"),
            ]
        )
    ],
    fluid=True,
)

# Define charts
## Trend Tab
###  Line chart by country
@app.callback(
    Output("country_chart_trend", "srcDoc"),
    Input("year_range_widget_trend", "value"),
    Input("country_widget_trend", "value"),
    Input("disease_widget_trend", "value"),
    Input("stat_type_widget_trend", "value"),
)
def plot_country(year_range, countries, diseases, stat_type):
    if stat_type == "raw_stats":
        year_chart = (
            alt.Chart(
                disease_count_data[
                    (disease_count_data["year"] >= year_range[0])
                    & (disease_count_data["year"] <= year_range[1])
                    & (disease_count_data["country"].isin(countries))
                    & (disease_count_data["disease"].isin(diseases))
                ]
            )
            .mark_line()
            .encode(
                x=alt.X(
                    "year",
                    scale=alt.Scale(zero=False),
                    title="Year",
                    axis=alt.Axis(format="d"),
                ),
                y=alt.Y(
                    field="count",
                    aggregate="sum",
                    type="quantitative",
                    title="Number of deaths",
                ),
                color=alt.Color("country", title="Country"),
            )
        )
    else:
        year_chart = (
            alt.Chart(
                disease_count_data_pc[
                    (disease_count_data_pc["year"] >= year_range[0])
                    & (disease_count_data_pc["year"] <= year_range[1])
                    & (disease_count_data_pc["country"].isin(countries))
                    & (disease_count_data_pc["disease"].isin(diseases))
                ]
            )
            .mark_line()
            .encode(
                x=alt.X(
                    "year",
                    scale=alt.Scale(zero=False),
                    title="Year",
                    axis=alt.Axis(format="d"),
                ),
                y=alt.Y(
                    field="count_pkc",
                    aggregate="sum",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
                color=alt.Color("country", title="Country"),
            )
        )
    return (
        year_chart.properties(width=700, height=300)
        .configure_axis(labelFontSize=15, titleFontSize=20)
        .configure_legend(orient="right", labelFontSize=15, titleFontSize=20)
        .interactive()
        .to_html()
    )


### Line chart by disease
@app.callback(
    Output("disease_chart_trend", "srcDoc"),
    Input("year_range_widget_trend", "value"),
    Input("country_widget_trend", "value"),
    Input("disease_widget_trend", "value"),
    Input("stat_type_widget_trend", "value"),
)
def plot_disease(year_range, countries, diseases, stat_type):
    if stat_type == "raw_stats":
        year_chart = (
            alt.Chart(
                disease_count_data[
                    (disease_count_data["year"] >= year_range[0])
                    & (disease_count_data["year"] <= year_range[1])
                    & (disease_count_data["country"].isin(countries))
                    & (disease_count_data["disease"].isin(diseases))
                ]
            )
            .mark_line()
            .encode(
                x=alt.X(
                    "year",
                    scale=alt.Scale(zero=False),
                    title="Year",
                    axis=alt.Axis(format="d"),
                ),
                y=alt.Y(
                    field="count",
                    aggregate="sum",
                    type="quantitative",
                    title="Number of deaths",
                ),
                color=alt.Color(
                    "disease", title="Disease", scale=alt.Scale(scheme="cividis")
                ),
            )
        )
    else:
        year_chart = (
            alt.Chart(
                disease_count_data_pc[
                    (disease_count_data_pc["year"] >= year_range[0])
                    & (disease_count_data_pc["year"] <= year_range[1])
                    & (disease_count_data_pc["country"].isin(countries))
                    & (disease_count_data_pc["disease"].isin(diseases))
                ]
            )
            .mark_line()
            .encode(
                x=alt.X(
                    "year",
                    scale=alt.Scale(zero=False),
                    title="Year",
                    axis=alt.Axis(format="d"),
                ),
                y=alt.Y(
                    field="count_pkc",
                    aggregate="sum",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
                color=alt.Color(
                    "disease", title="Disease", scale=alt.Scale(scheme="cividis")
                ),
            )
        )
    return (
        year_chart.properties(width=700, height=300)
        .configure_axis(labelFontSize=15, titleFontSize=20)
        .configure_legend(orient="right", labelFontSize=15, titleFontSize=20)
        .interactive()
        .to_html()
    )


## Snapshot Tab
### chart by country
@app.callback(
    Output("country_chart_snapshot", "srcDoc"),
    Input("year_widget_snapshot", "value"),
    Input("country_widget_snapshot", "value"),
    Input("disease_widget_snapshot", "value"),
    Input("stat_type_widget_snapshot", "value"),
    Input("default_number_widget_snapshot", "value"),
)
def plot_country(year, countries, diseases, stat_type, number_default_countries):
    if stat_type == "raw_stats":
        country_count = (
            disease_count_data[
                (disease_count_data["year"] == year)
                & (disease_count_data["country"].isin(countries))
                & (disease_count_data["disease"].isin(diseases))
            ]
            .groupby(by="country")
            .sum()
            .reset_index()
        )
        min_count = list(country_count["count"].sort_values(ascending=False))[-1]
        max_count = list(country_count["count"].sort_values(ascending=False))[0]
        country_chart = (
            alt.Chart(country_count)
            .mark_bar()
            .encode(
                x=alt.X(
                    field="count",
                    type="quantitative",
                    title="Number of deaths",
                ),
                y=alt.Y(
                    field="country",
                    type="nominal",
                    scale=alt.Scale(zero=False),
                    sort="-x",
                    title="",
                ),
                color=alt.Color(
                    field="count",
                    type="quantitative",
                    title="Count",
                    sort="-x",
                    legend=None,
                    scale=alt.Scale(scheme="plasma", domain=[min_count, max_count]),
                ),
                tooltip=alt.Tooltip(
                    field="count",
                    type="quantitative",
                    title="Number of deaths",
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count", "order": "descending"}],
            )
            .transform_filter("datum.rank <= " + str(number_default_countries))
        )
    else:
        country_count_pc = (
            disease_count_data_pc[
                (disease_count_data_pc["year"] == year)
                & (disease_count_data_pc["country"].isin(countries))
                & (disease_count_data_pc["disease"].isin(diseases))
            ]
            .groupby(by="country")
            .sum()
            .reset_index()
        )
        min_count_pc = list(country_count_pc["count_pkc"].sort_values(ascending=False))[
            -1
        ]
        max_count_pc = list(country_count_pc["count_pkc"].sort_values(ascending=False))[
            0
        ]
        country_chart = (
            alt.Chart(country_count_pc)
            .mark_bar()
            .encode(
                x=alt.X(
                    field="count_pkc",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
                y=alt.Y(
                    field="country",
                    type="nominal",
                    scale=alt.Scale(zero=False),
                    sort="-x",
                    title="",
                ),
                color=alt.Color(
                    field="count_pkc",
                    type="quantitative",
                    title="Count per thousand",
                    sort="-x",
                    legend=None,
                    scale=alt.Scale(
                        scheme="plasma", domain=[min_count_pc, max_count_pc]
                    ),
                ),
                tooltip=alt.Tooltip(
                    field="count_pkc",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count_pkc", "order": "descending"}],
            )
            .transform_filter("datum.rank <= " + str(number_default_countries))
        )
    return (
        country_chart.properties(width=400, height=300)
        .configure_axis(labelFontSize=15, titleFontSize=20)
        .interactive()
        .to_html()
    )


### Chart by disease
@app.callback(
    Output("disease_chart_snapshot", "srcDoc"),
    Input("year_widget_snapshot", "value"),
    Input("country_widget_snapshot", "value"),
    Input("disease_widget_snapshot", "value"),
    Input("stat_type_widget_snapshot", "value"),
)
def plot_disease(year, countries, diseases, stat_type):
    if stat_type == "raw_stats":
        disease_count = (
            disease_count_data[
                (disease_count_data["year"] == year)
                & (disease_count_data["country"].isin(countries))
                & (disease_count_data["disease"].isin(diseases))
            ]
            .groupby(by="disease")
            .sum()
            .reset_index()
        )

        disease_chart = (
            alt.Chart(disease_count)
            .mark_bar()
            .encode(
                x=alt.X(
                    field="count",
                    type="quantitative",
                    title="Number of deaths",
                ),
                y=alt.Y(
                    field="disease",
                    type="nominal",
                    scale=alt.Scale(zero=False),
                    title="",
                    sort="-x",
                ),
                color=alt.value("grey"),
                tooltip=alt.Tooltip(
                    field="count", type="quantitative", title="Number of deaths"
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count", "order": "descending"}],
            )
            .transform_filter("datum.rank <= 5")
        )
    else:
        disease_count_pc = (
            disease_count_data_pc[
                (disease_count_data["year"] == year)
                & (disease_count_data["country"].isin(countries))
                & (disease_count_data["disease"].isin(diseases))
            ]
            .groupby(by="disease")
            .sum()
            .reset_index()
        )

        disease_chart = (
            alt.Chart(disease_count_pc)
            .mark_bar()
            .encode(
                x=alt.X(
                    field="count_pkc",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
                y=alt.Y(
                    field="disease",
                    type="nominal",
                    scale=alt.Scale(zero=False),
                    title="",
                    sort="-x",
                ),
                color=alt.value("grey"),
                tooltip=alt.Tooltip(
                    field="count_pkc",
                    type="quantitative",
                    title="Deaths per thousand 0-4-year-olds",
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count_pkc", "order": "descending"}],
            )
            .transform_filter("datum.rank <= 5")
        )
    return (
        disease_chart.properties(width=400, height=300)
        .configure_axis(labelFontSize=15, titleFontSize=20)
        .interactive()
        .to_html()
    )


### Map
@app.callback(
    Output("map_snapshot", "figure"),
    Input("year_widget_snapshot", "value"),
    Input("country_widget_snapshot", "value"),
    Input("disease_widget_snapshot", "value"),
    Input("stat_type_widget_snapshot", "value"),
)
def display_choropleth(year, countries, diseases, stat_type):
    if stat_type == "raw_stats":
        df = (
            disease_count_map_data[
                (disease_count_data["year"] == year)
                & (disease_count_data["country"].isin(countries))
                & (disease_count_data["disease"].isin(diseases))
            ]
            .groupby(["country", "iso_alpha"])
            .agg(total_deaths=pd.NamedAgg(column="count", aggfunc="sum"))
            .reset_index()
        )
        fig = px.choropleth(
            df,
            locations="iso_alpha",
            color="total_deaths",
            hover_name="country",
            hover_data={"iso_alpha": False, "total_deaths": ":.0f"},
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout(
            height=800,
            width=700,
            geo_scope="africa",
            margin=dict(l=0, r=0, b=0, t=0),
            coloraxis_colorbar=dict(
                title="Total deaths",
                thicknessmode="pixels",
                thickness=20,
                lenmode="pixels",
                len=300,
            ),
        )
    else:
        df_pc = (
            disease_count_map_data_pc[
                (disease_count_data["year"] == year)
                & (disease_count_data["country"].isin(countries))
                & (disease_count_data["disease"].isin(diseases))
            ]
            .groupby(["country", "iso_alpha"])
            .agg(deaths_pkc=pd.NamedAgg(column="count_pkc", aggfunc="sum"))
            .reset_index()
        )
        fig = px.choropleth(
            df_pc,
            locations="iso_alpha",
            color="deaths_pkc",
            hover_name="country",
            hover_data={"iso_alpha": False, "deaths_pkc": ":.2f"},
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout(
            height=800,
            width=700,
            geo_scope="africa",
            margin=dict(l=0, r=0, b=0, t=0),
            coloraxis_colorbar=dict(
                title="Deaths per 1,000<br>0-4-year-olds",
                thicknessmode="pixels",
                thickness=20,
                lenmode="pixels",
                len=300,
            ),
        )
    return fig


# Run server
if __name__ == "__main__":
    app.run_server(debug=True)