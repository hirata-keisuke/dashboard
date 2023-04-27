import dash_bootstrap_components as dbc
from dash import html, dcc

from data.fetch import fetch_from_db
from logic.sma import find_GC_or_DC
from logic.stochastics import calc_stochastics, assess

def create_card(code):
    code = code.rstrip()

    name, st = fetch_from_db(code)

    max_idx = st["Date"].idxmax()
    price = st.loc[max_idx, "Close"]
    volume = st.loc[max_idx, "Volume"]

    GC_or_DC = find_GC_or_DC(st, 5, 20)
    GCDC_font_color = "blue" if GC_or_DC=="GC" else "red" if GC_or_DC=="DC" else "black"
    sto_k, sto_d = calc_stochastics(st, 3, 5)
    stochastics_assessment = assess(sto_k[-1], sto_d[-1])

    return dbc.Card(dbc.CardBody([
        html.H5(name),
        html.Div([html.Span(f"{price:.2f}円  "+f"  {volume:,d}株")]),
        html.Div([
            "ゴールデンクロス/デッドクロス:",html.Span(GC_or_DC, style={"color":GCDC_font_color})
        ]),
        html.P("ストキャスティクス:"+stochastics_assessment),
        dbc.Button(
            "詳しく見る", color="primary", outline=True, href=f"/analysis/{code}"
        )
    ]),)