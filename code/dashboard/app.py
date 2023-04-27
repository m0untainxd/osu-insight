# general imports
import os
from pathlib import Path
import requests
import dotenv
import flask
from datetime import datetime

# graph imports
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# dash imports
import dash
import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# class imports
from averages import Averages
from progression import Progression
from rank_pp import RankPP

# load .env file and get params
dotenv.load_dotenv()
API_KEY = os.getenv('api_key')

# initialise app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
path = Path.cwd().parent.parent.absolute()

# initialise classes
avg = Averages(path)
prg = Progression(path)
rnkpp = RankPP(path)

# get general avg data
gen_avgs = avg.general()

# get data for rank and pp
df_rank_pp = rnkpp.graph_data()

# construct graphs
graph = go.Figure()
y1 = px.line(df_rank_pp, x="month", y="avg_rank")
y1.update_layout(yaxis_range=[10000,80000])
y2 = px.line(df_rank_pp, x="month", y="avg_pp")

graph.add_trace(y1.data[0])
graph.add_trace(y2.data[0])

# --------------- App Layout --------------- #

app.layout = dbc.Container([

    dcc.Location(id="url", refresh=False),

    html.H1("osu!insights", style={'text-align': 'center'}),

    html.H3("Average Rank and PP over time"),

    dcc.Graph(id="avg_graph", figure=graph),
    html.Br(),

    dcc.Dropdown(id="slct_range",
                 options=[
                     {"label": "General", "value": "general"},
                     {"label": "100,000-200,000", "value": "100,000 - 200,000"},
                     {"label": "50,000-100,000", "value": "50,000 - 99,999"},
                     {"label": "25,000-50,000", "value": "25,000 - 49,999"},
                     {"label": "10,000-25,000", "value": "10,000 - 24,999"},
                     {"label": "5,000-10,000", "value": "5,000 - 9,999"},
                     {"label": "1000-5000", "value": "1,000 - 4,999"},
                     {"label": "500-1000", "value": "500 - 999"},
                     {"label": "100-500", "value": "100 - 499"},
                 ],
                 multi=False,
                 value="general",
                 style={"width": "40%"}),

    html.Div(children=[], id="user_rng"),
    html.Br(),
    html.H3("OR"),
    html.Br(),
    dcc.Input(id="user", type="text", placeholder="Enter username"),
    dbc.Button("Find user", id="user_btn", color="dark", className="me-1", n_clicks=0),

    # averages
    html.Div(children=["Average Values for General"], className="h3 d-flex align-items-center justify-content-center",
             id="avg_header"),

    dbc.Card([
        dbc.CardBody([
            html.H5("300 Count", className="card-title"),
            html.Div(id="cnt_300", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_300", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("100 Count", className="card-title"),
            html.Div(id="cnt_100", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_100", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("50 Count", className="card-title"),
            html.Div(id="cnt_50", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_50", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Play Count", className="card-title"),
            html.Div(id="playcount", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_playcount", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Ranked Score", className="card-title"),
            html.Div(id="rnk_score", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_rnk_score", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Total Score", className="card-title"),
            html.Div(id="ttl_score", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_ttl_score", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Rank", className="card-title"),
            html.Div(id="rank", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_rank", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("PP", className="card-title"),
            html.Div(id="pp", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_pp", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Level", className="card-title"),
            html.Div(id="lvl", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_lvl", className="card-text")
        ])
    ]),

    dbc.Card([
        dbc.CardBody([
            html.H5("Accuracy", className="card-title"),
            html.Div(id="acc", className="card-text"),
            html.Br(),
            # for user data
            html.H5("Your data", className="card-title"),
            html.Div("Not logged in", id="user_acc", className="card-text")
        ])
    ]),

    html.Div(id="prog_div", style={"display": "none"},
             children=[
                 html.H3("Progression", style={'text-align': 'center'}),
                 html.Br(),
                 html.Div(children=["Average time taken to progress through "], id="prog_dur_header"),
                 html.Div(id="prog_dur"),
                 html.Br(),
                 dcc.Graph(id="prog_graph", figure={})
             ])
])


# callback for range selection
@app.callback(
    [Output(component_id="avg_header", component_property="children"),
     Output(component_id="cnt_300", component_property="children"),
     Output(component_id="cnt_100", component_property="children"),
     Output(component_id="cnt_50", component_property="children"),
     Output(component_id="playcount", component_property="children"),
     Output(component_id="rnk_score", component_property="children"),
     Output(component_id="ttl_score", component_property="children"),
     Output(component_id="rank", component_property="children"),
     Output(component_id="pp", component_property="children"),
     Output(component_id="lvl", component_property="children"),
     Output(component_id="acc", component_property="children"),
     Output(component_id="prog_div", component_property="style"),
     Output(component_id="prog_dur_header", component_property="children"),
     Output(component_id="prog_dur", component_property="children"),
     Output(component_id="prog_graph", component_property="figure")],
    [Input(component_id="slct_range", component_property="value")]
)
def update(selected_val):
    if selected_val == "general":

        avgs = gen_avgs

        # average values
        avg_header = f"Average Values for {selected_val}"
        cnt_300 = avgs["count300"]
        cnt_100 = avgs["count100"]
        cnt_50 = avgs["count50"]
        playcount = avgs["playcount"]
        rnk_score = avgs["ranked_score"]
        ttl_score = avgs["total_score"]
        rank = avgs["pp_rank"]
        pp = avgs["pp_raw"]
        lvl = avgs["level"]
        acc = avgs["accuracy"]

        # hide prog graph
        prog_div = {"display": "none"}
        prog_dur_header = ""
        prog_dur = ""

        prog_graph = {}

        return avg_header, cnt_300, cnt_100, cnt_50, playcount, rnk_score, ttl_score, rank, pp, lvl, acc, prog_div, \
            prog_dur_header, prog_dur, prog_graph

    else:

        # get values for range
        avgs = avg.range(selected_val)

        # average values
        avg_header = f"Average Values for {selected_val}"
        cnt_300 = avgs["count300"]
        cnt_100 = avgs["count100"]
        cnt_50 = avgs["count50"]
        playcount = avgs["playcount"]
        rnk_score = avgs["ranked_score"]
        ttl_score = avgs["total_score"]
        rank = avgs["pp_rank"]
        pp = avgs["pp_raw"]
        lvl = avgs["level"]
        acc = avgs["accuracy"]

        # build prog section
        prog_div = {"display": "block"}
        prog_dur_header = f"Average time taken to progress through {selected_val}"
        prog_dur_val = prg.avg_days(selected_val)  # get val for avg days
        prog_dur = prog_dur_val

        # get data for graph
        df_dict = prg.graph_data(selected_val)
        df = pd.DataFrame(df_dict)

        # data manipulation
        df.drop(['ids'], inplace=True, axis=1)
        df['year'] = pd.to_datetime(df['year'])

        # create the graph
        prog_graph = px.scatter(df,
                                x='year',
                                y='days',
                                trendline="lowess",
                                trendline_color_override="purple",
                                title=f"Time taken to progress through rank range {selected_val}")

        return avg_header, cnt_300, cnt_100, cnt_50, playcount, rnk_score, ttl_score, rank, pp, lvl, acc, prog_div, \
            prog_dur_header, prog_dur, prog_graph


# server route for getting user data
@app.server.route("/user")
def redirect():
    return flask.redirect(f"https://osu.ppy.sh/oauth/authorize?redirect_uri=http%3A%2F%2F127%2E0%2E0%2E1%3A8050%2F")


@app.callback(
    [Output(component_id="user_300", component_property="children"),
     Output(component_id="user_100", component_property="children"),
     Output(component_id="user_50", component_property="children"),
     Output(component_id="user_playcount", component_property="children"),
     Output(component_id="user_rnk_score", component_property="children"),
     Output(component_id="user_ttl_score", component_property="children"),
     Output(component_id="user_rank", component_property="children"),
     Output(component_id="user_pp", component_property="children"),
     Output(component_id="user_lvl", component_property="children"),
     Output(component_id="user_acc", component_property="children")],
    Input(component_id="user_btn", component_property="n_clicks"),
    State(component_id="user", component_property="value"),)
def update_user(_, username):
    # get the user details from api
    if _ >= 1:
        user_json = requests.get(f"https://osu.ppy.sh/api/get_user?k={API_KEY}&u={username}&mode=0")
        if user_json.status_code == 200:
            user_str = user_json.json()
            user = user_str[0]

            # update on ui
            cnt_300 = user["count300"]
            cnt_100 = user["count100"]
            cnt_50 = user["count50"]
            playcount = user["playcount"]
            rnk_score = user["ranked_score"]
            ttl_score = user["total_score"]
            rank = user["pp_rank"]
            pp = user["pp_raw"]
            lvl = user["level"]
            acc = user["accuracy"]

            return cnt_300, cnt_100, cnt_50, playcount, rnk_score, ttl_score, rank, pp, lvl, acc
        else:
            print(user_json.status_code)
            raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True)
