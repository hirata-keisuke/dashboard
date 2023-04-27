import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from view.creator import create_card

dash.register_page(__name__, "/")

with open("data/target.txt", "r") as f:
    targets=f.readlines()

layout = dbc.Container([
    dbc.Row([
        dbc.Col(create_card(targets[i])) for i in range(3)
    ], className="cards-row"),
    dbc.Row([
        dbc.Col(create_card(targets[i+3])) for i in range(3)
    ], className="cards-row"),
    dbc.Row([
        dbc.Col(create_card(targets[i+6])) for i in range(3)
    ], className="cards-row")
])