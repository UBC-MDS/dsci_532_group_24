import altair as alt
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
    "Central African Republic",
    "Guinea",
]

colors = {"title": "#add8e6", "background": "#90ee90", "controls": "#f3ff94"}

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
            value="pc_k",
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="select_all_trend",
                            options=[{"label": "Select All", "value": 1}],
                            value=[],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="deselect_all_trend",
                            options=[{"label": "Deselect All", "value": 0}],
                            value=[],
                        )
                    ]
                ),
            ]
        ),
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
            value="pc_k",
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
            value=2015,
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="select_all_snapshot",
                            options=[{"label": "Select All", "value": 1}],
                            value=[],
                        )
                    ]
                ),
                dbc.Col(
                    [
                        dcc.Checklist(
                            id="deselect_all_snapshot",
                            options=[{"label": "Deselect All", "value": 0}],
                            value=[],
                        )
                    ]
                ),
            ]
        ),
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
            options=[{"label": str(n), "value": n} for n in range(5, 15)],
            value=10,
            style=dict(width="40%", verticalAlign="middle"),
        ),
    ],
    style=dict(display="flex"),
)

## information tab
table_header = [
    html.Thead(
        html.Tr(
            [
                html.Th("Dataset"),
                html.Th("Data Source"),
            ],
            style={"backgroundColor": "rgb(230, 230, 230)", "fontWeight": "bold"},
        )
    )
]

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
    dcc.Markdown(
        """
        Although there has been significant progress in reducing preventable child deaths between 1999 and 2019, [2020 WHO fact sheet on improving children survival and well-being](https://www.who.int/en/news-room/fact-sheets/detail/children-reducing-mortality) discusses the prevalence of child mortality that persists in Sub-Saharan Africa, which accounts for the highest child mortality rate in the world. 
        For example, in 2019, 86 out of 1000 newborns in The Democratic Republic of the Congo, a nation with 86.79 million people, do not make it to their fifth birthday. In Chad, the number is as high as 117. By contrast, about 99.6% (996 in 1000) of Canadian newborns are still alive when they are five years old. 
        As internal data analysts for an international non-governmental organization (INGO), we are dedicated to using data to understand infant and child mortality across the African continent. 
        """,
        style={
            "border-radius": 3,
        },
    ),
    html.Br(),
    dcc.Markdown(
        """
        This app is developed as part of DSCI 532's coursework. We intend to provide information to staff and volunteers at an international charity whose work focuses on healthcare and medication to children in Africa.
        The underlying dataset of this app is obtained from Gapminder, an independent Swedish foundation, with a mission to fight misconceptions and promotes a fact-based worldview.
        The table below summarizes the key data sources used in the app. 
        For the source code and detailed user guidance of this app, please visit our GitHub [repository](https://github.com/UBC-MDS/dsci_532_group_24), where you can also share with us your feedback. 
        """,
        style={
            "border-radius": 3,
        },
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
                            "Child Diseases and Mortality in Africa, 1990 - 2015",
                            style={
                                "backgroundColor": colors["title"],
                                "padding": 20,
                                "text-align": "center",
                                "border-radius": 3,
                            },
                        ),
                        html.P(
                            "App Developed by Junghoo Kim, Mark Wang and Zhenrui (Eric) Yu"
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Select statistic type: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                stat_type_controller_snapshot,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Select country: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                country_controller_snapshot,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ],
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader("Select year: "),
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    html.Div(
                                                                        id="year_display_snapshot",
                                                                        children="Selected year: ",
                                                                        style={
                                                                            "padding": 15,
                                                                            "border-radius": 3,
                                                                        },
                                                                    )
                                                                ),
                                                                year_controller_snapshot,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Filter disease: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                disease_controller_snapshot,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    style={
                                        "background-color": colors["controls"],
                                        "padding": 15,
                                        "border-radius": 3,
                                    },
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                default_number_selector_snapshot,
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                "",
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                "",
                                            ]
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Iframe(
                                                    id="country_chart_snapshot",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "100%",
                                                        "height": "60vh",
                                                    },
                                                ),
                                            ]
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                id="map_snapshot",
                                                style={
                                                    "border-width": "0",
                                                    "width": "100%",
                                                    "height": "50vh",
                                                },
                                            )
                                        ),
                                        dbc.Col(
                                            [
                                                "",
                                                html.Iframe(
                                                    id="disease_chart_snapshot",
                                                    style={
                                                        "border-width": "0",
                                                        "width": "100%",
                                                        "height": "60vh",
                                                    },
                                                ),
                                            ]
                                        ),
                                    ],
                                ),
                            ]
                        ),
                    ],
                    label="Snapshot",
                ),
                dbc.Tab(
                    [
                        html.H1(
                            "Trends of Child Diseases and Mortality in Africa, 1990 - 2015",
                            style={
                                "backgroundColor": colors["title"],
                                "padding": 20,
                                "text-align": "center",
                                "border-radius": 3,
                            },
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
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Select statistic type: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                stat_type_controller_trend,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Select country: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                country_controller_trend,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader("Select year: "),
                                                        dbc.CardBody(
                                                            [
                                                                dbc.Row(
                                                                    html.Div(
                                                                        id="year_display_trend",
                                                                        children="Selected year: ",
                                                                        style={
                                                                            "padding": 15,
                                                                            "border-radius": 3,
                                                                        },
                                                                    )
                                                                ),
                                                                year_range_controller_trend,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Col(
                                            [
                                                dbc.Card(
                                                    [
                                                        dbc.CardHeader(
                                                            "Filter disease: "
                                                        ),
                                                        dbc.CardBody(
                                                            [
                                                                disease_controller_trend,
                                                            ],
                                                        ),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    md=3,
                                    style={
                                        "background-color": colors["controls"],
                                        "padding": 15,
                                        "border-radius": 3,
                                    },
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
                dbc.Tab(information_tab, label="Data Source and Explanation"),
            ]
        )
    ],
    fluid=True,
    style={"max-width": "95%", "backgroundColor": colors["background"]},
)


@app.callback(
    Output("year_display_snapshot", "children"), Input("year_widget_snapshot", "value")
)
def selector_all_trend(selected):
    return f"Selected year: {selected}"


@app.callback(
    Output("year_display_trend", "children"), Input("year_range_widget_trend", "value")
)
def selector_all_trend(selected):
    return f"Selected year range: {selected}"


@app.callback(
    Output("country_widget_trend", "value"),
    Input("select_all_trend", "value"),
    Input("deselect_all_trend", "value"),
    State("country_widget_trend", "options"),
    State("country_widget_trend", "value"),
)
def selector_all_trend(selected, deselected, options, value):
    if 1 in selected:
        return [i["value"] for i in options]
    elif 0 in deselected:
        return []
    else:
        return value


@app.callback(
    Output("deselect_all_trend", "value"),
    Input("select_all_trend", "value"),
    Input("country_widget_trend", "value"),
    State("deselect_all_trend", "value"),
)
def update_deselector_all_trend(select_all, selected, deselect_all):
    if 1 in select_all or selected:
        return []
    else:
        return deselect_all


@app.callback(
    Output("select_all_trend", "value"),
    Input("deselect_all_trend", "value"),
    Input("country_widget_trend", "value"),
    State("select_all_trend", "value"),
)
def update_selector_all_trend(deselect_all, selected, select_all):
    if 0 in deselect_all or selected:
        return []
    else:
        return select_all


@app.callback(
    Output("country_widget_snapshot", "value"),
    Input("select_all_snapshot", "value"),
    Input("deselect_all_snapshot", "value"),
    State("country_widget_snapshot", "options"),
    State("country_widget_snapshot", "value"),
)
def selector_all_snapshot(selected, deselected, options, value):
    if 1 in selected:
        return [i["value"] for i in options]
    elif 0 in deselected:
        return []
    else:
        return value


@app.callback(
    Output("deselect_all_snapshot", "value"),
    Input("select_all_snapshot", "value"),
    Input("country_widget_snapshot", "value"),
    State("deselect_all_snapshot", "value"),
)
def update_deselector_all_snapshot(select_all, selected, deselect_all):
    if 1 in select_all or selected:
        return []
    else:
        return deselect_all


@app.callback(
    Output("select_all_snapshot", "value"),
    Input("deselect_all_snapshot", "value"),
    Input("country_widget_snapshot", "value"),
    State("select_all_snapshot", "value"),
)
def update_selector_all_snapshot(deselect_all, selected, select_all):
    if 0 in deselect_all or selected:
        return []
    else:
        return select_all


# Define charts
## Trend Tab
###  Line chart by country over the selected year range
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
                color=alt.Color("country", title="Country", sort="-y", legend=None),
                tooltip=[
                    alt.Tooltip(
                        field="country",
                        type="nominal",
                        title="Country",
                    ),
                    alt.Tooltip(
                        field="year",
                        type="quantitative",
                        title="Year",
                    ),
                    alt.Tooltip(
                        field="count",
                        aggregate="sum",
                        type="quantitative",
                        title="Number of deaths",
                    ),
                ],
            )
            .properties(
                title=[
                    f"Number of Children Deaths in Each Country between {year_range[0]} and {year_range[1]},",
                    f"from the Selected Diseases",
                ]
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
                color=alt.Color("country", title="Country", sort="-y", legend=None),
                tooltip=[
                    alt.Tooltip(
                        field="country",
                        type="nominal",
                        title="Country",
                    ),
                    alt.Tooltip(
                        field="year",
                        type="quantitative",
                        title="Year",
                    ),
                    alt.Tooltip(
                        field="count_pkc",
                        aggregate="sum",
                        type="quantitative",
                        title="Deaths per 1000 0-4-year-olds",
                        format=".2f",
                    ),
                ],
            )
            .properties(
                title=[
                    f"Deaths Per 1000 Children in Each Country between {year_range[0]} and {year_range[1]},",
                    f"from the Selected Diseases",
                ]
            )
        )
    return (
        (
            year_chart
            + year_chart.mark_point(size=50).encode(
                fill=alt.Fill("country", title="Country", sort="-y"),
            )
        )
        .properties(width=700, height=300)
        .configure_title(fontSize=20)
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
                color=alt.Color("disease", title="Disease", sort="-y", legend=None),
                tooltip=[
                    alt.Tooltip(
                        field="disease",
                        type="nominal",
                        title="Disease",
                    ),
                    alt.Tooltip(
                        field="year",
                        type="quantitative",
                        title="Year",
                    ),
                    alt.Tooltip(
                        field="count",
                        aggregate="sum",
                        type="quantitative",
                        title="Number of deaths",
                    ),
                ],
            )
            .properties(
                title=[
                    f"Number of Children Deaths from Each Disease between {year_range[0]} and {year_range[1]},",
                    f"in the Selected Countries",
                ]
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
                color=alt.Color("disease", title="Disease", sort="-y", legend=None),
                tooltip=[
                    alt.Tooltip(
                        field="disease",
                        type="nominal",
                        title="Disease",
                    ),
                    alt.Tooltip(
                        field="year",
                        type="quantitative",
                        title="Year",
                    ),
                    alt.Tooltip(
                        field="count_pkc",
                        aggregate="sum",
                        type="quantitative",
                        title="Deaths per 1000 0-4-year-olds",
                        format=".2f",
                    ),
                ],
            )
            .properties(
                title=[
                    f"Deaths Per 1000 Children from Each Disease between {year_range[0]} and {year_range[1]},",
                    f"in the Selected Countries",
                ]
            )
        )
    return (
        (
            year_chart
            + year_chart.mark_point(size=50).encode(
                fill=alt.Fill("disease", title="Disease", sort="-y"),
            )
        )
        .properties(width=700, height=300)
        .configure_title(fontSize=20)
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
    if not (number_default_countries):
        number_default_countries = 0

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
        ).properties(
            title=[
                f"{number_default_countries} Countries with Most Children Deaths in {year},",
                f"from the Selected Diseases",
            ]
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
        min_count_pc = (
            list(country_count_pc["count_pkc"].sort_values(ascending=False))[-1]
            if countries
            else None
        )
        max_count_pc = (
            list(country_count_pc["count_pkc"].sort_values(ascending=False))[0]
            if countries
            else None
        )
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
                    title="Deaths per 1000 0-4-year-olds",
                    format=".2f",
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count_pkc", "order": "descending"}],
            )
            .transform_filter("datum.rank <= " + str(number_default_countries))
            .properties(
                title=[
                    f"{number_default_countries} Countries with Most Deaths Per 1000 Children in {year},",
                    f"from the Selected Diseases",
                ]
            )
        )
    return (
        country_chart.properties(width=300, height=400)
        .configure_title(fontSize=15)
        .configure_axis(labelFontSize=12, titleFontSize=15)
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
            .properties(
                title=[
                    f"Diseases Causing Most Children Deaths in {year},",
                    f"in the Selected Countries",
                ]
            )
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
                    title="Deaths per 1000 0-4-year-olds",
                    format=".2f",
                ),
            )
            .transform_window(
                window=[{"op": "rank", "as": "rank"}],
                sort=[{"field": "count_pkc", "order": "descending"}],
            )
            .transform_filter("datum.rank <= 5")
            .properties(
                title=[
                    f"Diseases Causing Most Deaths Per 1000 Children in {year},",
                    f"in the Selected Countries",
                ]
            )
        )
    return (
        disease_chart.properties(width=300, height=400)
        .configure_title(fontSize=15)
        .configure_axis(labelFontSize=12, titleFontSize=15)
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
        df = df.rename(columns={"total_deaths": "Total deaths"})
        fig = px.choropleth(
            df,
            locations="iso_alpha",
            color="Total deaths",
            hover_name="country",
            hover_data={"iso_alpha": False, "Total deaths": ":.0f"},
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout(
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
        df_pc = df_pc.rename(columns={"deaths_pkc": "Deaths per 1000 0-4 year-olds"})
        fig = px.choropleth(
            df_pc,
            locations="iso_alpha",
            color="Deaths per 1000 0-4 year-olds",
            hover_name="country",
            hover_data={"iso_alpha": False, "Deaths per 1000 0-4 year-olds": ":.2f"},
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout(
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
    app.run_server()