import pandas as pd
import plotly.express as px
from pathlib import Path

def main():
    #set path and open dataset
    path = Path(__file__).parent.parent.parent.absolute() / "original_data/updates.csv"
    print(path)
    df = pd.read_csv(path)

    #filter dataset so it is 100-200,000 and standard mode
    df_range = df[(df['pp_rank'] >= 100) & (df['pp_rank'] <= 200000) & (df['mode'] == 0)]


    #get all of the rank updates as a list
    ranks = df_range["pp_rank"].tolist()

    #plot the data
    fig = px.histogram(ranks, nbins=200, title='Rank Distribution')

    #labels
    fig.update_xaxes(title_text='Rank')
    fig.update_yaxes(title_text='Count')

    # Show the plot
    fig.show()

if __name__ == "__main__":
    main()