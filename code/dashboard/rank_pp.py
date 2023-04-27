import pandas as pd

class RankPP:

    def __init__(this, path):
        this.path = path
        this.df = pd.read_csv(path / "final_data/monthly_avgs.csv", index_col=0)

    def graph_data(this):
        #return graph data as-is
        return this.df