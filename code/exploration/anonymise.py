import pandas as pd
import os

# This script provides functions that will anonymise a dataset based on 
# the existing user id and give them a new id

# FOR TESTING #
def main():
    #change working directory to access folder with data
    os.chdir("D:/Honours Project Data")

    # use sample dataset that was created for initial demonstration
    df_updates = pd.read_csv("/sample_data/updates_sample.csv")
    df_users = pd.read_csv("sample_data/users_sample.csv")

    #run the function with these sample datasets to return the anonymised dataset
    df_users_anon, df_updates_anon = anonymise(df_users, df_updates)

    print(df_users_anon)
    print(df_updates_anon)

def anonymise(df_users, df_updates):
    # for each user, make an object and assign an index
    users = set(df_users['osu_id'])
    mapping = {user : index for index, user in enumerate(users)}

    # map users table and sort
    df_users_anon = map(df_users, "osu_id", mapping, True)
    #map updates table and don't sort
    df_updates_anon = map(df_updates, "user", mapping, False)

    return df_users_anon, df_updates_anon

def map(df, old, mapping, sort):
    #assign the new id as a new field in the dataset and sort by this new id
    df['anon_id'] = df[old].map(mapping)

    #if you want to sort by new id
    if sort:
        df = df.sort_values('anon_id')
    else:
        pass

    return df

# FOR TESTING #
"""
if __name__ == "__main__":
    main()
"""
