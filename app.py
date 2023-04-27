import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(
    title="テクニカル分析-入門",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True
)

app.layout = html.Div([dash.page_container
])

if __name__ == "__main__":
    app.run_server(debug=True)