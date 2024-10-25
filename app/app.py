import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(
    [
        html.H1("Dash App Template"),
        html.Div("This is a basic template for a Dash app."),
        # Dropdown for user input
        dcc.Dropdown(
            id="example-dropdown",
            options=[
                {"label": "Option 1", "value": "OPT1"},
                {"label": "Option 2", "value": "OPT2"},
                {"label": "Option 3", "value": "OPT3"},
            ],
            value="OPT1",  # Default value
        ),
        # Div for displaying output
        html.Div(id="output-container"),
    ]
)


# Define callback to update the output based on dropdown selection
@app.callback(
    Output("output-container", "children"), Input("example-dropdown", "value")
)
def update_output(selected_value):
    return f"You have selected: {selected_value}"


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
