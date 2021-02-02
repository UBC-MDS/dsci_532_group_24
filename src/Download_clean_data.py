import os
import pandas as pd
import plotly.express as px

# Download files
## Key variables from 1800

core_data = pd.read_csv(
    "https://raw.githubusercontent.com/UofTCoders/workshops-dc-py/master/data/processed/world-data-gapminder.csv"
)

core_data.to_csv("data/raw/core.csv", header=True, index=False)

# Read in data
## Metadata
metadata = pd.read_csv("data/metadata.csv")

## Core data
core_data = pd.read_csv("data/raw/core.csv")

## Other data files
data_files = {}

for file_name, variable_name in zip(metadata["File_name"], metadata["Variable_name"]):
    data_files[variable_name] = pd.read_csv(os.path.join("data", "raw", file_name))

# Clean data
merged_data = core_data

for variable_name in metadata["Variable_name"]:
    ## Reshape data files into long form
    df_to_merge = data_files[variable_name]

    df_to_merge_melted = pd.melt(
        df_to_merge,
        id_vars=["country"],
        var_name="year",
        value_name=variable_name,
    )

    df_to_merge_melted["year"] = df_to_merge_melted["year"].astype(int)

    ## Merge with core_data
    merged_data = merged_data.merge(
        df_to_merge_melted,
        left_on=["country", "year"],
        right_on=["country", "year"],
        how="left",
    )

## Get data for Africa
merged_data = merged_data.loc[
    merged_data["region"] == "Africa",
]

## Get data after 1990, when child death data is available
merged_data = merged_data.loc[
    merged_data["year"] >= 1990,
]

## Remove `child_mortality` column, which is duplicated
clean_data = merged_data.drop("child_mortality", axis=1)

# Create datasets for analyses and visualizations

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
    "total_child_deaths",
]

disease_count_data = pd.melt(
    disease_count_data,
    id_vars=["country", "year", "sub_region"],
    var_name="disease",
    value_name="count",
)

## Define per-child data
pc_data = clean_data[["country", "year", "number_of_under_five_years_children"]]

pc_data.columns = ["country", "year", "ncu5"]

disease_count_data_pc = pd.merge(
    disease_count_data, pc_data, on=["country", "year"], how="left"
)
disease_count_data_pc["count_pkc"] = (
    1000 * disease_count_data_pc["count"] / disease_count_data_pc["ncu5"]
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

# Export pre-processed datasets
clean_data.to_pickle("data/clean_data.pkl", protocol=4)
clean_data.to_csv("data/clean_data.csv")

disease_count_data.to_pickle("data/disease_count_data.pkl", protocol=4)
disease_count_data.to_csv("data/disease_count_data.csv")

disease_count_data_pc.to_pickle("data/disease_count_data_pc.pkl", protocol=4)
disease_count_data_pc.to_csv("data/disease_count_data_pc.csv")

disease_count_map_data.to_pickle("data/disease_count_map_data.pkl", protocol=4)
disease_count_map_data.to_csv("data/disease_count_map_data.csv")
