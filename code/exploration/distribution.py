import pandas as pd
import plotly.express as px
from pathlib import Path

def main():
    #set path and open dataset
    path = Path(__file__).parent.parent.parent.absolute() / "final_data/range_updates.csv"
    print(path)
    df = pd.read_csv(path)

    #new dataset with only rank and range
    df_rank = df.filter(["pp_rank", "range"], axis=1)

    #plot the data per 1000 ranks
    fig_1000 = px.histogram(df_rank, nbins=200, title='Rank Distribution', color='range')
    #lables
    fig_1000.update_xaxes(title_text='Rank').update_yaxes(title_text='Count')

    #create plot showing the count of updates for each range
    ranges = df_rank['range'].unique().tolist() #get all range types
    counts = [] #init array to store counts

    #iterate through ranges to get counts
    for i in ranges:
        count = len(df[df["range"] == i])
        counts.append(count)

    #plot the data for range counts
    fig_ranges = px.histogram(x=ranges, y=counts, title='Count of updates per Range')
    #lables
    fig_ranges.update_xaxes(title_text='Rank Ranges').update_yaxes(title_text='Count')

    #show plots
    fig_1000.show()
    fig_ranges.show()


if __name__ == "__main__":
    main()