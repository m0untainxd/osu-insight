from progression import Progression
import pandas as pd
from pathlib import Path
import plotly.express as px
from timeit import default_timer as timer


# base variables
path = Path.cwd().parent.parent.absolute()


def main():
    start = timer()
    # initialise progression and give it the path
    prg = Progression(path)

    # get range from user
    print("What range would you like to use? (0-7)")
    rng = int(input())

    # get the range name
    rng_row = prg.get_ranges(rng)
    rng_name = rng_row["name"]

    # use the range name to get the data
    df_dict = prg.graph_data(rng_name)
    df = pd.DataFrame(df_dict)

    # manipulation
    df.drop(['ids'], inplace=True, axis=1)
    df['year'] = pd.to_datetime(df['year'])

    # create the graph
    sct = px.scatter(df,
                     x='year',
                     y='days',
                     trendline="lowess",
                     trendline_color_override="purple",
                     title=f"Time taken to progress through rank range {rng_name}")
    sct.update_traces(marker=dict(color='pink'))
    sct.show()
    end = timer()
    print(f"time taken to run program and render graph: {round(end-start)} seconds")


if __name__ == "__main__":
    main()
