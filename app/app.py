import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html
from dash.dependencies import Input, Output, State

from request_handler import RequestHandler
from config import API_DOMAIN

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "URL Shortener"

app.layout = html.Div(
    [
        dcc.Store(id="history"),
        dbc.Row(
            html.H1("URL SHORTENER", style={"text-align": "center"}),
            justify="center",
            style={"margin": "200px 0px 12px 0px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dmc.TextInput(
                        label="Long URL:", id="text-input-long-url", w="100%"
                    ),
                    width=6,
                ),
                dbc.Col(
                    dmc.Button("Shorten", id="btn-shorten"),
                    width=2,
                ),
            ],
            justify="center",
            align="end",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dmc.TextInput(
                            id="text-input-short-url",
                            label="Short URL:",
                            w="100%",
                            disabled=True,
                        ),
                    ],
                    width=5,
                ),
                dbc.Col(
                    [
                        dmc.Button(
                            "Copy",
                            id="btn-copy",
                            leftIcon=dcc.Clipboard(
                                id="clipboard-copy",
                                style={
                                    "display": "inline-block",
                                    "fontSize": 20,
                                    "verticalAlign": "top",
                                },
                            ),
                            variant="outline",
                        ),
                    ],
                    width=2,
                ),
            ],
            justify="center",
            align="end",
            style={"margin": "24px 0px 0px 24px"},
        ),
        html.Div(id="output-container"),
    ]
)


@app.callback(
    Output("clipboard-copy", "n_clicks"),
    Input("btn-copy", "n_clicks"),
    State("clipboard-copy", "n_clicks"),
    prevent_initial_call=True,
)
def on_click_btn_copy(_nclicks, n_clicks):
    return 1 if not n_clicks else n_clicks + 1


@app.callback(
    Output("clipboard-copy", "content"),
    Input("clipboard-copy", "n_clicks"),
    State("text-input-short-url", "value"),
    prevent_initial_call=True,
)
def copy_short_url(_nclicks: int, short_url: str):
    return short_url


@app.callback(
    Output("text-input-short-url", "value"),
    Input("btn-shorten", "n_clicks"),
    State("text-input-long-url", "value"),
    prevent_initial_call=True,
)
def shorten_long_url(_nclicks: int, long_url: str):
    request_handler = RequestHandler()
    response = request_handler.shorten_url(long_url)
    complete_short_url = f"{API_DOMAIN}/fetch/{response['short_url']}"
    return complete_short_url


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
