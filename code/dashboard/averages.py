import pandas as pd

#initialise class so dataframe can be initialised and run alongside the dashboard
#this allows the data returned to be changed easily
class Averages:

    def __init__(this, path):
        #open dataset with data for last month
        this.path = path
        this.df = pd.read_csv(path / "final_data/avg_last_month.csv")
        this.ranges = this.df["range"].unique()

    #get general averages data
    def general(this):
        #drop unneeded columns
        df_averages = this.df[['count300', 'count100', 'count50', 'playcount', 'ranked_score', 'total_score', 'pp_rank', 'level', 'pp_raw', 'accuracy']].copy()

        #init dict for columns and averages
        avgs = {}

        #iterate through columns to get avg for each
        for name, values in df_averages.iteritems():
            avg = values.median().astype(str)
            avgs.update({name: avg})

        return avgs
    
    #get ranged averages data
    def range(this, range):
        #drop unneeded columns
        df_averages_range = this.df[['count300', 'count100', 'count50', 'playcount', 'ranked_score', 'total_score', 'pp_rank', 'level', 'pp_raw', 'accuracy', 'range']].copy()

        #filter for range
        df_this = df_averages_range[df_averages_range["range"] == range]
        df_this.reset_index(drop=True)

        #drop range field to prevent error with iteration
        df_this.drop("range", axis=1, inplace=True)

        #init dict for columns and averages
        avgs = {}
    
        #iterate through columns to get avg for each
        for name, values in df_this.iteritems():
            avg = str(values.median())
            avgs.update({name: avg})
        
        return avgs
