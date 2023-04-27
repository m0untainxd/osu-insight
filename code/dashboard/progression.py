import pandas as pd

class Progression:
    
    def __init__(this, path):
        this.path = path
        this.df_data = pd.read_csv(path / "final_data/progression_data_years.csv")
        this.df_filtered = pd.read_csv(path / "final_data/progression_filtered.csv")
        this.ranges = [
                        {"from": 100000, "to": 200000, "name": "100,000 - 200,000"},
                        {"from": 50000, "to": 99999, "name": "50,000 - 99,999"},
                        {"from": 25000, "to": 49999, "name": "25,000 - 49,999"},
                        {"from": 10000, "to": 24999, "name": "10,000 - 24,999"},
                        {"from": 5000, "to": 9999, "name": "5,000 - 9,999"},
                        {"from": 1000, "to": 4999, "name": "1,000 - 4,999"},
                        {"from": 500, "to": 999, "name": "500 - 999"},
                        {"from": 100, "to": 499, "name": "100 - 499"}]
        
        #drop left over id column
        this.df_data.drop(columns=this.df_data.columns[0], axis=1, inplace=True)
        
    def avg_days(this, range):
        #for each range, get the corresponding day values and get median
        for i in this.ranges:
            if i["name"] == range:
                #get rows for the range
                df_this = this.df_data[this.df_data["ranges"] == range]
                df_this.reset_index(drop=True)

                #calc median day value and return
                avg_days = df_this["days"].median().astype(str)
                return avg_days

            else:
                pass

    def graph_data(this, range):
        #filter dataset for current range
        df_this = this.df_data[this.df_data["ranges"] == range]

        df_this["ids"].astype(str)

        return df_this.to_dict()


    def get_ranges(this, i):
        return this.ranges[i]