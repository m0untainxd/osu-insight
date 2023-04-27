import pandas as pd
from pathlib import Path
import numpy as np
from tqdm import tqdm

path = Path.cwd().absolute()
df_data = pd.read_csv(path / "final_data/progression_data.csv", index_col=0,)
df_filtered = pd.read_csv(path / "final_data/progression_filtered.csv")

#list of years to append to dataset
months = []

#convert to dict for iteration
df_dict = df_data.to_dict('records')

#iterate through rows 
for row in tqdm(df_dict):
    ids = str(row["ids"]) #get the string of ids
    row_ids = ids.split(", ") #convert to list
    #convert list to int
    if "nan" in row_ids:
        pass
    else:
        int_ids = list(map(int, row_ids))

    #find out what year corresponds to each day range
    df_this_range = df_filtered[df_filtered["id"].isin(int_ids)]

    #get last value to see when the user completed the range
    row = df_this_range.tail(1)
    date = str(row["date"].iloc[0])
    year = date[:4] #get year
    month = date[5:7]
    month_str = "{m}-{y}".format(m=month, y=year)

    months.append(month_str)

df_data['year'] = months

df_data.to_csv(path / "final_data/progression_data_years.csv")