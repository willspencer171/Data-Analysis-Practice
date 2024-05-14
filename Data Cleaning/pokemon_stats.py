import pandas as pd
from os import path

# Let's get to cleaning this thing
in_path = path.realpath(__file__ + "/../../data/unclean")
out_path = path.realpath(__file__ + "/../../data/clean")

pokemon_stats_raw = pd.read_csv(path.join(in_path, "Pokemon Stats.csv"), index_col="dexnum", engine="pyarrow")

# No null values where there shouldn't be any
for column in pokemon_stats_raw.columns:
    print(f"{column}: {pokemon_stats_raw[column].isna().any()}")

# Can confirm that all null-gender percentages are legitimate
genderless = pokemon_stats_raw.query("percent_male.isnull() & percent_female.isnull()")

# No aggregate columns that need separating. Maybe I picked a dataset that didn't need cleaning?
# Won't be adding any more columns for things like colour, nor building a database with images.
# Maybe I'll output as a .db so it can be SQL queried?

# Overall, not the most interesting dataset, maybe I'll pick things that need more thorough cleaning?
