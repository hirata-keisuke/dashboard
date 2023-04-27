import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dateutil.relativedelta import relativedelta
from data.fetch import fetch_from_db
from view.artist import drow_technicals

dash.register_page(__name__, path_template="/analysis/<code>")

def layout(code):
    name, st = fetch_from_db(code)
    latest = st.loc[st.index[-1]]
    st = st[st["Date"]>latest["Date"]-relativedelta(years=3)]
    visualized_technicals = drow_technicals(st, 5, 20, 60, 20, 10)

    return html.Div([
        html.Div([
            dbc.Card(dbc.CardBody(
                children=name, id="stock-name"), className="header-item"
            ),
            dbc.Card(dbc.CardBody(
                children=f'{latest["Close"]:.2f}円', id="stock-price"
            ), className="header-item"),
            dbc.Card(dbc.CardBody(
                children=f'{latest["Volume"]:,d}株', id="stock-volume"
            ), className="header-item")
        ], className="header"),
        html.Div([
            dcc.Graph(id="technicals", figure=visualized_technicals),
        ], className="technicals-graphs"),
        dbc.Button("戻る", color="primary", outline=True, href=f"/", className="button-back")
    ])