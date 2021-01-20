import os
import pandas as pd

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
merged_data = merged_data.drop("child_mortality", axis=1)

# Export clean data
merged_data.to_pickle("data/clean_data.pkl")
merged_data.to_csv("data/clean_data.csv")