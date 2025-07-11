import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="Home")

layout = html.Div([
    html.H2("Welcome to the Circular Functions App"),
    dcc.Markdown("""
This app helps you understand how angles on the unit circle define the sine and cosine functions.

Use the sidebar to navigate:
- 🎯 **Unit Circle**: Explore angles, sine, and cosine on the unit circle
- (More pages coming soon!)
    """)
])
