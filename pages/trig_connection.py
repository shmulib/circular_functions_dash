import dash
from dash import html, dcc, callback, Input, Output, State
# from .trig_connection_plot import create_trig_connection_figure

dash.register_page(__name__, path="/trig_connection", name="Trig & Circle")

layout = html.Div([
    html.H2("Connecting Trigonometry and the Unit Circle", style={"textAlign": "center"}),
    html.P("In the first quadrant, each angle θ on the unit circle defines a right triangle.", style={"textAlign": "center"}),

    html.Div([
        # Left: Plot
        html.Div(
            dcc.Graph(
                id="trig-connection-graph",
                style={"height": "700px", "width": "100%"}
            ),
            style={"flex": "2", "margin": "0", "padding": "0"}
        ),

        # Right: Controls
        html.Div([
            html.Label("Angle Unit:"),
            dcc.RadioItems(
                id="trig-angle-unit-toggle",
                options=[
                    {"label": "Degrees", "value": "degrees"},
                    {"label": "Radians", "value": "radians"},
                ],
                value="degrees",
                inline=False
            ),

            html.Br(),

            html.Label("Show symmetric points:"),
            dcc.Checklist(
                id="symmetry-toggle",
                options=[
                    {"label": "Q2 (−x, y)", "value": "Q2"},
                    {"label": "Q3 (−x, −y)", "value": "Q3"},
                    {"label": "Q4 (x, −y)", "value": "Q4"},
                ],
                value=[],
                inline=False
            ),

            html.Br(),

            html.Label("Angle:"),
            dcc.Slider(
                id="angle-slider",
                min=0, max=90, step=2, value=30,
                marks={i: str(i) for i in range(0, 91, 15)},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], style={
            "flex": "1",
            "margin": "0",
            "padding": "0",
            "minWidth": "250px",
            "justifyContent":"left"
        })
    ], style={
        "display": "flex",
        "alignItems": "flex-start",
        "justifyContent": "center",
        "gap": "0"  # explicitly kill all spacing
    })
])



@callback(
    Output("trig-connection-graph", "figure"),
    Input("angle-slider", "value"),
    Input("trig-angle-unit-toggle", "value"),
    Input("symmetry-toggle", "value")
)
def update_figure(angle, unit, symmetries):
    return create_trig_connection_figure(unit=unit, symmetries=symmetries, current_angle=str(angle))




import numpy as np
import plotly.graph_objects as go
from fractions import Fraction


def format_angle_label(angle_deg, unit="degrees"):
    if unit == "degrees":
        return f"{angle_deg}°"
    else:
        print("angle_deg", angle_deg)
        frac = Fraction(int(angle_deg), 180).limit_denominator(12)
        if frac.numerator == 0:
            return "0"
        elif frac == 1:
            return "π"
        elif frac.denominator == 1:
            return f"{frac.numerator}π"
        else:
            return f"{frac.numerator}π/{frac.denominator}"


def create_trig_connection_figure(unit="degrees", symmetries=[], current_angle="30"):
    print("unit", unit,  "current_angle", current_angle)
    angle_deg = float(current_angle)
    angle_rad = np.radians(angle_deg)
    x, y = np.cos(angle_rad), np.sin(angle_rad)
    arc_radius = 0.35 * x  # shrink arc as θ approaches 90°

    fig = go.Figure()
    points = {}

    def add_triangle(sign_x, sign_y):
        px, py = sign_x * x, sign_y * y
        base_x, base_y = 0, 0
        quadrant = f"Q{(2 if sign_x == -1 and sign_y == 1 else 1) if sign_y == 1 else (3 if sign_x == -1 else 4)}"
        points[quadrant] = (px, py)

        # Triangle sides
        fig.add_trace(go.Scatter(x=[base_x, px], y=[base_y, py], mode="lines",
                                 line=dict(color="gray", width=2), showlegend=False))
        fig.add_trace(go.Scatter(x=[base_x, px], y=[base_y, base_y], mode="lines",
                                 line=dict(color="blue", width=3, dash="dot"), showlegend=False))
        fig.add_trace(go.Scatter(x=[px, px], y=[base_y, py], mode="lines",
                                 line=dict(color="red", width=3, dash="dot"), showlegend=False))

        # Point marker and coordinate label
        fig.add_trace(go.Scatter(
            x=[px], y=[py], mode="markers+text",
            text=[f"(<span style='color:blue'>{px:.2f}</span>, <span style='color:red'>{py:.2f}</span>)"],
            textposition="top right",
            textfont=dict(size=12),
            marker=dict(color="black", size=7),
            showlegend=False,
            hoverinfo="skip"
))

  


        # Arc + angle label
        arc_theta = np.linspace(0, angle_rad, 100)
        arc_x = arc_radius * np.cos(arc_theta) * sign_x
        arc_y = arc_radius * np.sin(arc_theta) * sign_y
        label_theta = format_angle_label(angle_deg, unit)
        fig.add_trace(go.Scatter(x=arc_x, y=arc_y, mode="lines",
                                 line=dict(color="green", dash="dot"), showlegend=False))
        
        if (sign_x, sign_y) != (1, 1):
            fig.add_trace(go.Scatter(
                x=[arc_radius * 0.75 * np.cos(angle_rad / 2) * sign_x],
                y=[arc_radius * 0.75 * np.sin(angle_rad / 2) * sign_y],
                text=[label_theta], mode="text", textfont=dict(size=10,color="green"), showlegend=False
            ))


        # --- Compute full standard angle (from positive x-axis) ---

        # --- Arc coordinates from 0 to full angle ---
        r_factors = [1, 1.1,1.3,1.5]
        if (sign_x, sign_y) == (1, 1):     # Q1
            full_angle = angle_rad
            r_factor=1
        elif (sign_x, sign_y) == (-1, 1):  # Q2
            full_angle = np.pi - angle_rad
            arc_theta = np.linspace(0, full_angle, 100)
            r_factor = r_factors[1]
            arc_x = r_factor*arc_radius * np.cos(arc_theta)
            arc_y = r_factor*arc_radius * np.sin(arc_theta)
        elif (sign_x, sign_y) == (-1, -1): # Q3
            full_angle = np.pi + angle_rad
            arc_theta = np.linspace(0, full_angle, 100)
            r_factor = r_factors[2]
            arc_x = r_factor*arc_radius * np.cos(arc_theta)
            arc_y = r_factor*arc_radius * np.sin(arc_theta)
        elif (sign_x, sign_y) == (1, -1):  # Q4
            full_angle = 2 * np.pi - angle_rad
            arc_theta = np.linspace(0, full_angle, 100)
            r_factor = r_factors[3]
            arc_x = r_factor*arc_radius * np.cos(arc_theta)
            arc_y = r_factor*arc_radius * np.sin(arc_theta)

        # --- Determine full angle from positive x-axis ---
        if (sign_x, sign_y) == (1, 1):     # Q1
            full_angle = angle_rad
            arc_color = "green"
        elif (sign_x, sign_y) == (-1, 1):  # Q2
            full_angle = np.pi - angle_rad
            arc_color = "#000080"
        elif (sign_x, sign_y) == (-1, -1): # Q3
            full_angle = np.pi + angle_rad
            arc_color = "#9932CC"
        elif (sign_x, sign_y) == (1, -1):  # Q4
            full_angle = 2 * np.pi - angle_rad
            arc_color = "#DC143C"

        # # --- Arc from x-axis to full_angle ---
        # arc_theta = np.linspace(0, full_angle, 100)
        # arc_x = arc_radius * np.cos(arc_theta)
        # arc_y = arc_radius * np.sin(arc_theta)

        # --- Label: full angle (formatted) ---
        if unit == "degrees":
            label_full = f"<span style='color:{arc_color}'>{np.degrees(full_angle):.0f}°</span>"
        else:
            frac = Fraction(full_angle / np.pi).limit_denominator(12)
            if frac.numerator == 0:
                label_full = "0"
            elif frac.denominator == 1:
                label_full = f"<span style='color:{arc_color}'>{frac.numerator}π</span>"
            else:
                label_full = f"<span style='color:{arc_color}'>{frac.numerator}π/{frac.denominator}</span>"

        # --- Triangle angle label (black θ = …) ---
        label_triangle = f"θ = {angle_deg:.0f}°" if unit == "degrees" else f"θ = {format_angle_label(angle_rad, 'radians')}"

        # --- Add colored arc ---
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y, mode="lines",
            line=dict(color=arc_color, dash="dot"), showlegend=False
        ))

                # --- Add colored arc ---
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y, mode="lines",
            line=dict(color=arc_color, dash="dot"), showlegend=False
        ))

        # --- Add full angle label (outside arc, colored) ---
 
        fig.add_trace(go.Scatter(
                x=[arc_radius*r_factor * 1.2 * np.cos(full_angle- (angle_rad/2 ) )],
                y=[arc_radius *r_factor* 1.2 * np.sin(full_angle-(angle_rad/2 ) )],
                text=[label_full],
                mode="text", textfont=dict(size=14),
                showlegend=False
            ))
            






        # Side labels
        if  (sign_x, sign_y) == (1, 1): 
            fig.add_trace(go.Scatter(
                x=[(base_x + px)/2], y=[base_y - 0.05 * sign_y], mode="text",
                text=[f"<span style='color:blue'>A = {abs(x):.2f}</span>"],
                textfont=dict(size=13), showlegend=False))
            fig.add_trace(go.Scatter(
                x=[px + 0.05 * sign_x], y=[(base_y + py)/2], mode="text",
                text=[f"<span style='color:red'>O = {abs(y):.2f}</span>"],
                textfont=dict(size=13), showlegend=False))
            fig.add_trace(go.Scatter(
                x=[(base_x + px)/2 - 0.05 * sign_x], y=[(base_y + py)/2 + 0.05 * sign_y],
                mode="text", text=["1"], textfont=dict(size=13), showlegend=False))

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 500)
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines",
                             line=dict(color="black"), showlegend=False))

    # Q1 always shown
    add_triangle(1, 1)

    # Other quadrants
    signs = {"Q2": (-1, 1), "Q3": (-1, -1), "Q4": (1, -1)}
    for q, (sx, sy) in signs.items():
        if q in symmetries:
            add_triangle(sx, sy)

    # Horizontal lines if pairs present
    if "Q2" in symmetries:
        fig.add_trace(go.Scatter(
            x=[points["Q2"][0], points["Q1"][0]], y=[points["Q2"][1], points["Q1"][1]],
            mode="lines", line=dict(color="black", dash="dash"), showlegend=False))
    if "Q3" in symmetries and "Q4" in symmetries:
        fig.add_trace(go.Scatter(
            x=[points["Q3"][0], points["Q4"][0]], y=[points["Q3"][1], points["Q4"][1]],
            mode="lines", line=dict(color="black", dash="dash"), showlegend=False))

    # Grey out hidden quadrants
    if "Q2" not in symmetries:
        fig.add_shape(type="rect", x0=-1.4, y0=0, x1=0, y1=1.4, fillcolor="gray", opacity=0.3, line_width=0)
    if "Q3" not in symmetries:
        fig.add_shape(type="rect", x0=-1.4, y0=-1.4, x1=0, y1=0, fillcolor="gray", opacity=0.3, line_width=0)
    if "Q4" not in symmetries:
        fig.add_shape(type="rect", x0=0, y0=-1.4, x1=1.4, y1=0, fillcolor="gray", opacity=0.3, line_width=0)

    


    # === Add angle tick marks on the unit circle ===
    tick_degrees =list(set(range(0, 361, 30)).union(set(range(0,361,45))))
    tick_degrees.sort()
    tick_radius_outer = 1.02
    tick_radius_inner = 0.97

    for deg in tick_degrees:
        rad = np.radians(deg)
        x_outer = tick_radius_outer * np.cos(rad)
        y_outer = tick_radius_outer * np.sin(rad)
        x_inner = tick_radius_inner * np.cos(rad)
        y_inner = tick_radius_inner * np.sin(rad)

        # Tick mark line
        fig.add_trace(go.Scatter(
            x=[x_inner, x_outer], y=[y_inner, y_outer],
            mode="lines", line=dict(color="gray", width=1),
            showlegend=False, hoverinfo="skip"
        ))

        # Angle label
        if unit == "degrees":
            label = f"{deg}°"
        else:
           # label = f"{deg}°
            print('deg', deg)
            frac = Fraction(deg, 180).limit_denominator(12)
            if frac.numerator == 0:
                label = "0"
            elif frac == 1:
                label = "π"
            elif frac.denominator == 1:
                label = f"{frac.numerator}π"
            else:
                label = f"{frac.numerator}π/{frac.denominator}"

        label_x = 1.12 * np.cos(rad)
        label_y = 1.12 * np.sin(rad)

        fig.add_trace(go.Scatter(
            x=[label_x], y=[label_y],
            mode="text", text=[label],
            textfont=dict(size=10),
            showlegend=False, hoverinfo="skip"
        ))



    fig.update_layout(
        title="Trigonometric Triangles in All Quadrants",
        xaxis=dict(scaleanchor="y", range=[-1.4, 1.4], zeroline=True, showgrid=False),
        yaxis=dict(range=[-1.4, 1.4], zeroline=True, showgrid=False),
        margin=dict(t=40, b=10),
        width=800,
        height=700,
    )

    return fig

