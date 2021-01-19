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
country_list = list(clean_data["country"].unique())
disease_list = [
    "HIV",
    "Malaria",
    "Measles",
    "Meningitis",
    "NCD",
    "Total deaths",
]

## Define new dataset to present disease
disease_count_data = clean_data[
    [
        "country",
        "year",
        "sub_region",
        "hiv_deaths_in_children_1_59_months_total_deaths",
        "malaria_deaths_in_children_1_59_months_total_deaths",
        "measles_deaths_in_children_1_59_months_total_deaths",
        "meningitis_deaths_in_children_1_59_months_total_deaths",
        "ncd_deaths_in_children_1_59_months_total_deaths",
        "number_of_child_deaths",
    ]
]

disease_count_data.columns = [
    "country",
    "year",
    "sub_region",
    "HIV",
    "Malaria",
    "Measles",
    "Meningitis",
    "NCD",
    "Total",
]

disease_count_data = pd.melt(
    disease_count_data,
    id_vars=["country", "year", "sub_region"],
    var_name="disease",
    value_name="count",
)

## Define map data
country_iso = (
    px.data.gapminder()
    .query("continent=='Africa'")[["country", "iso_alpha"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

### Add South Sudan and Seychelles
country_iso = country_iso.append(
    pd.DataFrame(
        {"country": ["South Sudan", "Seychelles"], "iso_alpha": ["SSD", "SYC"]}
    )
)

disease_count_map_data = pd.DataFrame.merge(
    disease_count_data, country_iso, on="country", how="left"
)

# Define three controllers
year_controller = html.Div(
    [
        "Year",
        dcc.RangeSlider(
            id="year_widget",
            min=1990,
            max=2019,
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

country_controller = html.Div(
    [
        "Country",
        dcc.Dropdown(
            id="country_widget",
            value=["Angola"],
            placeholder="Select a country...",
            options=[{"label": country, "value": country} for country in country_list],
            multi=True,
        ),
    ]
)

disease_controller = html.Div(
    [
        "Disease",
        dcc.Dropdown(
            id="disease_widget",
            value=["HIV"],
            placeholder="Select a disease...",
            options=[{"label": disease, "value": disease} for disease in disease_list],
            multi=True,
        ),
    ]
)

# Define app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Causes of Child Mortality in Africa, since 1990"),
        html.P("App Developed by Junghoo Kim, Mark Wang and Zhenrui (Eric) Yu"),
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(year_controller),
                        dbc.Col(country_controller),
                        dbc.Col(disease_controller),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Iframe(
                                id="country_chart",
                                style={
                                    "border-width": "0",
                                    "width": "20vw",
                                    "height": "50vh",
                                },
                            )
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id="map",
                                style={
                                    "border-width": "0",
                                    "width": "20vw",
                                    "height": "50vh",
                                },
                            )
                        ),
                        dbc.Col(
                            html.Iframe(
                                id="disease_chart",
                                style={
                                    "border-width": "0",
                                    "width": "20vw",
                                    "height": "50vh",
                                },
                            )
                        ),
                    ]
                ),
            ]
        ),
    ]
)

# Define charts
## chart by country
@app.callback(
    Output("country_chart", "srcDoc"),
    Input("year_widget", "value"),
    Input("country_widget", "value"),
    Input("disease_widget", "value"),
)
def plot_country(year_range, countries, diseases):
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
        .configure_legend(orient="top")
    )
    return year_chart.to_html()


## Chart by disease
@app.callback(
    Output("disease_chart", "srcDoc"),
    Input("year_widget", "value"),
    Input("country_widget", "value"),
    Input("disease_widget", "value"),
)
def plot_disease(year_range, countries, diseases):
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
        .configure_legend(orient="top")
    )
    return year_chart.to_html()


# Define map


@app.callback(
    Output("map", "figure"),
    Input("year_widget", "value"),
    Input("country_widget", "value"),
    Input("disease_widget", "value"),
)
def display_choropleth(year_range, countries, diseases):
    df = disease_count_map_data[
        (disease_count_data["year"] >= year_range[0])
        & (disease_count_data["year"] <= year_range[1])
        & (disease_count_data["disease"].isin(diseases))
    ]
    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="count",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_layout(
        height=300,
        width=300,
        geo_scope="africa",
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, b=0, t=10),
    )
    return fig


# Run server
if __name__ == "__main__":
    app.run_server(debug=True)