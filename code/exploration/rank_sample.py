import pandas as pd
from pathlib import Path

#this script is for generating a random sample of updates for each rank range

#list of dicts containing each rank range to be evaluated
ranges = [
            {"from": 100000, "to": 200000, "name": "100,000 - 200,000"},
            {"from": 50000, "to": 99999, "name": "50,000 - 99,999"},
            {"from": 25000, "to": 49999, "name": "25,000 - 49,999"},
            {"from": 10000, "to": 24999, "name": "10,000 - 24,999"},
            {"from": 5000, "to": 9999, "name": "5,000 - 9,999"},
            {"from": 1000, "to": 4999, "name": "1,000 - 4,999"},
            {"from": 500, "to": 999, "name": "500 - 999"},
            {"from": 100, "to": 499, "name": "100 - 499"}]

def main():
    #open the dataset
    path = Path(__file__).parent.parent.parent.absolute()
    df_updates = pd.read_csv(path / "original_data/updates.csv", index_col=0)
    df_users = pd.read_csv(path / "original_data/users.csv")

    frames = []

    print("Do you want to sample the data before adding range? (y/n)")
    inp = input()

    #iterate through samples in list and create a dataset for each
    for i in ranges:
        rng = i
        #get range
        df_range = df_updates[(df_updates['pp_rank'] >= rng['from']) & (df_updates['pp_rank'] <= rng['to']) & (df_updates['mode'] == 0)]

        if inp == "y":
            #get list of unique users in the range, then create a filtered df containing all those users
            unique_users = df_range['user'].unique()
            df_users_unique = df_users.loc[df_users['osu_id'].isin(unique_users)]

            #sample the users table and use this to filter the updates dataset
            df_users_sample = df_users_unique.sample(50)
            unique_users_sample = df_users_sample['osu_id'].unique()
            df_updates_sample = df_range.loc[df_range['user'].isin(unique_users_sample)]

            #add a field to the dataframe that will apply the current sample name to all records
            df_updates_sample['range'] = i['name']
            frames.append(df_updates_sample) #append to list of dataframes to be concatenated

        elif inp == "n":
            df_range['range'] = i['name']
            frames.append(df_range)

    # concatenate into one dataset
    if inp == "y":
        df_sampled_updates = pd.concat(frames)
        df_sampled_updates.to_csv(path / 'final_data/sampled_updates.csv', index=False)
    elif inp == "n":
        df_range_updates = pd.concat(frames)
        df_range_updates.to_csv(path / 'final_data/range_updates.csv')

if __name__ == "__main__":
    main()