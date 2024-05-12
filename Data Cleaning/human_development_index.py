import pandas as pd
import matplotlib.pyplot as plt
from os import path

in_path = path.relpath('data/unclean/')
out_path = path.relpath('data/clean/')

# Load in DataFrame using pyarrow engine
base_df = pd.read_csv(path.join(in_path, 'Human Development Index.csv'), engine='pyarrow')

# Convert to long form to be able to manipulate column names
df_melted = pd.melt(base_df, id_vars=['ISO3', 'Country'], var_name='variable_year', value_name='Value')

# Extract column names and years using regular expressions
df_melted[['columns', 'Year']] = df_melted['variable_year'].str.extract(r'^(.*?)\s*(?:\((\d{4})\))?$')
# Drop the combined variable_year column
df_melted.drop('variable_year', axis=1, inplace=True)

# Separate data with no year attached for clarity, then drop year column
df_no_year_formatted = df_melted[df_melted['Year'].isna()].set_index('Country').drop('Year', axis=1)

# Separate data with year
df_with_year_formatted = df_melted[df_melted['Year'].notna()]
# Parse year as number object
df_with_year_formatted.loc[:,'Year'] = pd.to_numeric(df_with_year_formatted.loc[:,'Year'], downcast='integer')
# Set Year and Country as MultiIndex
df_with_year_formatted.set_index(['Country', 'Year'], inplace=True)

# Pivot column names back into columns to produce short form data
df_no_year_formatted = df_no_year_formatted.pivot(columns='columns', values='Value')
df_with_year_formatted = df_with_year_formatted.pivot(columns='columns', values='Value')

# Fill all NAs using previous year
df_with_year_formatted.bfill(inplace=True)

# Output files
df_no_year_formatted.to_csv(path.join(out_path, "Human Development Index.csv"))
df_with_year_formatted.to_csv(path.join(out_path, "Human Development Index (years).csv"))

print(f"Data cleaned! You can find it at '{out_path}/Human Development Index (years).csv' and '{out_path}/Human Development Index.csv'")

df_no_year_formatted.info()
df_with_year_formatted.info()
