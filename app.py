# app.py
import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        # Sidebar
        dbc.Col([
            html.H2("Circular Functions", className="mt-4"),
            html.Hr(),
            dbc.Nav([
                dbc.NavLink("Definitions", href="/circ_func_defs", active="exact"),
                dbc.NavLink("Trig & Circle", href="/trig_connection", active="exact"),
            ], vertical=True, pills=True),
        ], width=3, style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "1rem"}),

        # Main content
        dbc.Col([
            dash.page_container
        ], width=9, style={"padding": "2rem"})
    ])
], fluid=True)

# from dash import ClientsideFunction

# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='store_current_angle'
#     ),
#     Output('current-angle-store', 'data'),
#     Input('trig-connection-graph', 'relayoutData'),
#     prevent_initial_call=True
# )



if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
