import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import pytest

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
from request_handler import RequestHandler
from config import API_DOMAIN

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "URL Shortener"

app.layout = html.Div(
    [
        dcc.Store(id="store-history", storage_type="local"),
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
                    width=1,
                ),
                dbc.Col(
                    [
                        dmc.Button(
                            "Clear History",
                            id="btn-clear-history",
                            leftIcon=DashIconify(icon="clarity:trash-line", width=20),
                            variant="outline",
                            color="red",
                        ),
                    ],
                    width=2,
                ),
            ],
            justify="center",
            align="end",
            style={"margin": "24px 0px 0px 24px"},
        ),
        dbc.Row(
            dbc.Col(
                [
                    dash_table.DataTable(
                        style_table={
                            "height": "400px",
                            "overflowY": "auto",
                            "border": "1px solid #E3E9F3",  # Light border to match the theme
                        },
                        fixed_rows={"headers": True},
                        style_header={
                            "backgroundColor": "#E3E9F3",  # Header background color
                            "fontWeight": "bold",
                            "color": "#1A1B1D",  # Header text color
                            "border": "none",  # Remove border for a cleaner look
                        },
                        style_data={
                            "whiteSpace": "nowrap",  # Prevent text wrapping in data cells
                            "overflow": "hidden",  # Hide overflow content
                            "textOverflow": "ellipsis",  # Show ellipsis for overflow text
                            "color": "#1A1B1D",  # Data text color
                            "border": "1px solid #E3E9F3",  # Light border to match the theme
                        },
                        style_cell={
                            "overflow": "hidden",  # Hide overflow content
                            "textOverflow": "ellipsis",  # Show ellipsis for overflow text
                            "maxWidth": "200px",  # Set a maximum width for the cell
                            "whiteSpace": "nowrap",  # Prevent text from wrapping to the next line
                            "textAlign": "left",  # Align text to the left
                        },
                        style_cell_conditional=[
                            {"if": {"column_id": "id"}, "width": "5%"},
                            {"if": {"column_id": "Long URL"}, "width": "60%"},
                        ],
                        style_data_conditional=[
                            {
                                "if": {"row_index": "odd"},
                                "backgroundColor": "#F8F9FA",  # Light gray background for odd rows
                            },
                            {
                                "if": {"row_index": "even"},
                                "backgroundColor": "white",  # White background for even rows
                            },
                            {
                                "if": {"state": "active"},
                                "backgroundColor": "#D1E7FF",  # Light blue background for active row
                            },
                        ],
                        css=[
                            {
                                "selector": ".dash-table-tooltip",
                                "rule": """
                                    background-color: #e7f5ff !important;  /* Light blue background */
                                    color: #1c7ed6 !important;  /* Darker blue text color */
                                    width: 600px !important;
                                    max-width: 600px !important;
                                    padding: 8px !important;  /* Adds space within tooltip */
                                    border: 1px solid #1971c2 !important;  /* Dark blue border */
                                    border-radius: 5px !important;  /* Rounded corners */
                                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1) !important;  /* Light shadow */
                                    word-wrap: break-word !important;
                                    white-space: normal !important;
                                """,
                            }
                        ],
                        id="table-history",
                    )
                ],
                width=10,
            ),
            justify="center",
            style={
                "margin": "24px 0px 0px 0px",
            },
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
    Output("text-input-long-url", "value"),
    Output("store-history", "data"),
    Input("btn-shorten", "n_clicks"),
    State("text-input-long-url", "value"),
    State("store-history", "data"),
    prevent_initial_call=True,
)
def shorten_long_url(_nclicks: int, long_url: str, history_data):
    request_handler = RequestHandler()
    response = request_handler.shorten_url(long_url)
    complete_short_url = f"{API_DOMAIN}/fetch/{response['short_url']}"

    # Update the history data with the new entry
    if history_data is None:
        history_data = []
    new_entry = {
        "id": len(history_data) + 1,
        "Long URL": long_url,
        "Short URL": complete_short_url,
    }
    updated_history = history_data + [new_entry]

    return complete_short_url, "", updated_history


@app.callback(
    Output("store-history", "data", allow_duplicate=True),
    Input("btn-clear-history", "n_clicks"),
    prevent_initial_call=True,
)
def on_click_clear_history(_nclicks):
    return []


@app.callback(
    Output("table-history", "data"),
    Output("table-history", "tooltip_data"),
    Input("store-history", "data"),
    prevent_initial_call=True,
)
def update_table(history_data):

    if history_data is None:
        raise PreventUpdate

    tooltip_data = [
        {
            column: {"value": str(value), "type": "markdown"}
            for column, value in row.items()
        }
        for row in history_data
    ]

    # Update the table with the history data
    return history_data, tooltip_data


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
