from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
from fractions import Fraction


# Global cache for last used unit to persist between animations
_last_unit = {"value": "degrees"}

def format_angle_label(angle_deg, unit="degrees"):
    if unit == "degrees":
        return f"θ = {angle_deg}°"
    else:
        frac = Fraction(angle_deg, 180).limit_denominator(12)
        if frac.numerator == 0:
            return "θ = 0"
        elif frac == 1:
            return "θ = π"
        elif frac.denominator == 1:
            return f"θ = {frac.numerator}π"
        else:
            return f"θ = {frac.numerator}π/{frac.denominator}"

def format_slider_ticks(degrees_list, unit):
    return [format_angle_label(deg, unit).replace("θ = ", "") for deg in degrees_list]

def angle_deg_to_unit(angle_deg, unit):
    return angle_deg if unit == "degrees" else np.radians(angle_deg)

def get_axis_tickvals(unit):
    if unit == "degrees":
        return list(range(0, 361, 30)), list(map(str, range(0, 361, 30)))
    else:
        degs = list(range(0, 361, 30))
        vals = [round(np.radians(d), 6) for d in degs]
        labels = [format_angle_label(d, "radians").replace("θ = ", "") for d in degs]
        return vals, labels

def create_circular_function_figure(unit="degrees", plot_template="plotly_white"):
    _last_unit["value"] = unit  # persist current unit to avoid reset on animation end

    theta = np.linspace(0, 2 * np.pi, 500)
    circle_x = np.cos(theta)
    circle_y = np.sin(theta)

    angle_degrees = np.arange(0, 361, 1)
    angle_units = np.array([angle_deg_to_unit(deg, unit) for deg in angle_degrees])
    angle_radians = np.radians(angle_degrees)
    cos_vals = np.cos(angle_radians)
    sin_vals = np.sin(angle_radians)

    tick_angles = [15*i for i in range(0,25)]
    tick_labels = format_slider_ticks(tick_angles, unit)

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"rowspan": 2}, {}], [None, {}]],
        column_widths=[0.6, 0.4],
        horizontal_spacing=0.1,
        vertical_spacing=0.3,
        subplot_titles=("Unit Circle", "cos(θ)", "sin(θ)")
    )

    frames = []
    for deg, angle_val, cos_val, sin_val in zip(angle_degrees, angle_units, cos_vals, sin_vals):
        label = format_angle_label(deg, unit)
        rad = np.radians(deg)
        arc_theta = np.linspace(0, rad, 100)
        arc_x = 0.3 * np.cos(arc_theta)
        arc_y = 0.3 * np.sin(arc_theta)
        label_r = 0.6
        label_x = label_r * np.cos(rad / 2)
        label_y = label_r * np.sin(rad / 2)

        frames.append(go.Frame(
            name=str(deg),
            data=[
                go.Scatter(x=circle_x, y=circle_y, mode="lines", line=dict(color="black"), showlegend=False, xaxis="x1", yaxis="y1"),
                go.Scatter(x=angle_units, y=cos_vals, mode="lines", line=dict(color="blue"), showlegend=False, xaxis="x2", yaxis="y2"),
                go.Scatter(x=angle_units, y=sin_vals, mode="lines", line=dict(color="red"), showlegend=False, xaxis="x3", yaxis="y3"),
                go.Scatter(x=[0] + list(arc_x) + [0], y=[0] + list(arc_y) + [0], fill='toself', fillcolor='rgba(0,100,255,0.2)', line=dict(color='rgba(0,0,0,0)'), mode='lines', showlegend=False, xaxis="x1", yaxis="y1"),
                go.Scatter(x=[0, np.cos(rad)], y=[0, np.sin(rad)], mode='lines+markers', line=dict(color='green'), showlegend=False, xaxis="x1", yaxis="y1"),
                go.Scatter(x=[np.cos(rad)], y=[np.sin(rad)], mode='markers+text', text=[f"(<span style='color:blue'>{cos_val:.2f}</span>, <span style='color:red'>{sin_val:.2f}</span>)"], textposition='top right', textfont=dict(size=14), marker=dict(color='black', size=8), showlegend=False, xaxis="x1", yaxis="y1", hoverinfo="skip", texttemplate="%{text}"),
                go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color='green', dash='dash'), showlegend=False, xaxis="x1", yaxis="y1"),
                go.Scatter(x=[label_x], y=[label_y], mode='text', text=[label], textfont=dict(size=14, color='darkblue'), showlegend=False, xaxis="x1", yaxis="y1"),
                go.Scatter(x=[angle_val], y=[cos_val], mode='markers+text', text=[f"{cos_val:.2f}"], textposition="top center", marker=dict(color='blue', size=10), showlegend=False, xaxis="x2", yaxis="y2"),
                go.Scatter(x=[angle_val], y=[sin_val], mode='markers+text', text=[f"{sin_val:.2f}"], textposition="top center", marker=dict(color='red', size=10), showlegend=False, xaxis="x3", yaxis="y3")
            ]
        ))

    fig.frames = frames 
    fig.add_traces(frames[0].data)

    x_title = "θ (degrees)" if unit == "degrees" else "θ (radians)"
    x_range = [0, 385] if unit == "degrees" else [0, 2.1 * np.pi]
    tickvals, ticktext = get_axis_tickvals(unit)

    fig.update_layout(
        template=plot_template,
        width=1200,
        height=750,
        margin=dict(t=100, b=80),
        xaxis=dict(domain=[0, 0.55], range=[-1.5, 1.5], scaleanchor='y'),
        yaxis=dict(domain=[0, 1], range=[-1.5, 1.5]),
        xaxis2=dict(domain=[0.65, 1], anchor='y2', title=x_title, range=x_range, tickvals=tickvals, ticktext=ticktext, title_standoff=20, tickangle=-45),
        yaxis2=dict(domain=[0.6, 1], range=[-1.3, 1.3]),
        xaxis3=dict(domain=[0.65, 1], anchor='y3', title=x_title, range=x_range, tickvals=tickvals, ticktext=ticktext, title_standoff=20, tickangle=-45),
        yaxis3=dict(domain=[0, 0.35], range=[-1.3, 1.3]),
        sliders=[{
            "steps": [{
                "label": label,
                "method": "animate",
                "args": [[str(deg)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
            } for deg, label in zip(tick_angles, tick_labels)],
            "transition": {"duration": 0},
            "x": 0.05,
            "y": -0.07,
            "len": 0.9
        }],
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [
                {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]},
                {"label": "Pause", "method": "animate", "args": [[None], {"mode": "immediate"}]}
            ],
            "x": 0.03,
            "y": -0.08
        }]
    )

    return fig





# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import numpy as np
# from fractions import Fraction


# def format_angle_label(angle_deg, unit="degrees"):
#     if unit == "degrees":
#         return f"θ = {angle_deg}°"
#     else:
#         frac = Fraction(angle_deg, 180).limit_denominator(12)
#         if frac.numerator == 0:
#             return "θ = 0"
#         elif frac == 1:
#             return "θ = π"
#         elif frac.denominator == 1:
#             return f"θ = {frac.numerator}π"
#         else:
#             return f"θ = {frac.numerator}π/{frac.denominator}"


# def format_slider_ticks(degrees_list, unit):
#     return [format_angle_label(deg, unit).replace("θ = ", "") for deg in degrees_list]


# def angle_deg_to_unit(angle_deg, unit):
#     return angle_deg if unit == "degrees" else np.radians(angle_deg)


# def get_axis_tickvals(unit):
#     if unit == "degrees":
#         return list(range(0, 361, 30)), list(map(str, range(0, 361, 30)))
#     else:
#         degs = list(range(0, 361, 30))
#         vals = [round(np.radians(d), 6) for d in degs]
#         labels = [format_angle_label(d, "radians").replace("θ = ", "") for d in degs]
#         return vals, labels


# def create_circular_function_figure(unit="degrees", plot_template="plotly_white"):
#     theta = np.linspace(0, 2 * np.pi, 500)
#     circle_x = np.cos(theta)
#     circle_y = np.sin(theta)

#     angle_degrees = np.arange(0, 361, 15)
#     angle_units = np.array([angle_deg_to_unit(deg, unit) for deg in angle_degrees])
#     angle_radians = np.radians(angle_degrees)
#     cos_vals = np.cos(angle_radians)
#     sin_vals = np.sin(angle_radians)

#     tick_angles = angle_degrees.tolist()
#     tick_labels = format_slider_ticks(tick_angles, unit)

#     fig = make_subplots(
#         rows=2, cols=2,
#         specs=[[{"rowspan": 2}, {}], [None, {}]],
#         column_widths=[0.6, 0.4],
#         horizontal_spacing=0.1,
#         vertical_spacing=0.2,
#         subplot_titles=("Unit Circle", "cos(θ)", "sin(θ)")
#     )

#     frames = []
#     for deg, angle_val, cos_val, sin_val in zip(angle_degrees, angle_units, cos_vals, sin_vals):
#         label = format_angle_label(deg, unit)
#         rad = np.radians(deg)
#         arc_theta = np.linspace(0, rad, 100)
#         arc_x = 0.3 * np.cos(arc_theta)
#         arc_y = 0.3 * np.sin(arc_theta)
#         label_r = 0.6
#         label_x = label_r * np.cos(rad / 2)
#         label_y = label_r * np.sin(rad / 2)

#         frames.append(go.Frame(
#             name=str(deg),
#             data=[
#                 go.Scatter(x=circle_x, y=circle_y, mode="lines", line=dict(color="black"), showlegend=False, xaxis="x1", yaxis="y1"),
#                 go.Scatter(x=angle_units, y=cos_vals, mode="lines", line=dict(color="blue"), showlegend=False, xaxis="x2", yaxis="y2"),
#                 go.Scatter(x=angle_units, y=sin_vals, mode="lines", line=dict(color="red"), showlegend=False, xaxis="x3", yaxis="y3"),
#                 go.Scatter(x=[0] + list(arc_x) + [0], y=[0] + list(arc_y) + [0], fill='toself', fillcolor='rgba(0,100,255,0.2)', line=dict(color='rgba(0,0,0,0)'), mode='lines', showlegend=False, xaxis="x1", yaxis="y1"),
#                 go.Scatter(x=[0, np.cos(rad)], y=[0, np.sin(rad)], mode='lines+markers', line=dict(color='red'), showlegend=False, xaxis="x1", yaxis="y1"),
#                 go.Scatter(x=[np.cos(rad)], y=[np.sin(rad)], mode='markers+text', text=[f"(<span style='color:blue'>{cos_val:.2f}</span>, <span style='color:red'>{sin_val:.2f}</span>)"], textposition='top right', textfont=dict(size=14), marker=dict(color='black', size=8), showlegend=False, xaxis="x1", yaxis="y1", hoverinfo="skip", texttemplate="%{text}"),
#                 go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color='green', dash='dash'), showlegend=False, xaxis="x1", yaxis="y1"),
#                 go.Scatter(x=[label_x], y=[label_y], mode='text', text=[label], textfont=dict(size=14, color='darkblue'), showlegend=False, xaxis="x1", yaxis="y1"),
#                 go.Scatter(x=[angle_val], y=[cos_val], mode='markers+text', text=[f"{cos_val:.2f}"], textposition="bottom right", marker=dict(color='blue', size=10), showlegend=False, xaxis="x2", yaxis="y2"),
#                 go.Scatter(x=[angle_val], y=[sin_val], mode='markers+text', text=[f"{sin_val:.2f}"], textposition="bottom right", marker=dict(color='red', size=10), showlegend=False, xaxis="x3", yaxis="y3")
#             ]
#         ))


#     fig.frames = frames
#     fig.add_traces(frames[0].data)

#     x_title = "θ (degrees)" if unit == "degrees" else "θ (radians)"
#     x_range = [0, 360] if unit == "degrees" else [0, 2 * np.pi]
#     tickvals, ticktext = get_axis_tickvals(unit)

#     fig.update_layout(
#         template=plot_template,
#         width=1200,
#         height=750,
#         margin=dict(t=100, b=80),
#         xaxis=dict(domain=[0, 0.55], range=[-1.8, 1.8], scaleanchor='y'),
#         yaxis=dict(domain=[0, 1], range=[-1.5, 1.5]),
#         xaxis2=dict(domain=[0.65, 1], anchor='y2', title=x_title, range=x_range, tickvals=tickvals, ticktext=ticktext, title_standoff=2, tickangle=-45),
#         yaxis2=dict(domain=[0.55, 1], range=[-1.1, 1.1]),
#         xaxis3=dict(domain=[0.65, 1], anchor='y3', title=x_title, range=x_range, tickvals=tickvals, ticktext=ticktext, title_standoff=2, tickangle=-45),
#         yaxis3=dict(domain=[0, 0.45], range=[-1.1, 1.1]),
#         sliders=[{
#             "steps": [{
#                 "label": label,
#                 "method": "animate",
#                 "args": [[str(deg)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
#             } for deg, label in zip(tick_angles, tick_labels)],
#             "transition": {"duration": 0},
#             "x": 0.05,
#             "y": -0.07,
#             "len": 0.9
#         }],
#         updatemenus=[{
#             "type": "buttons",
#             "showactive": False,
#             "buttons": [
#                 {"label": "Play", "method": "animate", "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]},
#                 {"label": "Pause", "method": "animate", "args": [[None], {"mode": "immediate"}]}
#             ],
#             "x": 0.03,
#             "y": -0.09
#         }]
#     )

#     return fig

# from plotly.subplots import make_subplots
# import plotly.graph_objects as go
# import numpy as np
# from fractions import Fraction


# def format_angle_label(angle_deg, unit="degrees"):
#     if unit == "degrees":
#         return f"θ = {angle_deg}°"
#     else:
#         frac = Fraction(angle_deg, 180).limit_denominator(12)
#         if frac.numerator == 0:
#             return "θ = 0"
#         elif frac == 1:
#             return "θ = π"
#         elif frac.denominator == 1:
#             return f"θ = {frac.numerator}π"
#         else:
#             return f"θ = {frac.numerator}π/{frac.denominator}"


# def format_slider_ticks(degrees_list, unit):
#     return [format_angle_label(deg, unit).replace("θ = ", "") for deg in degrees_list]


# def create_circular_function_figure(unit="degrees", plot_template="plotly_white"):
#     theta = np.linspace(0, 2 * np.pi, 500)
#     circle_x = np.cos(theta)
#     circle_y = np.sin(theta)

#     angle_degrees = np.arange(0, 361, 1)
#     angle_radians = np.radians(angle_degrees)
#     cos_vals = np.cos(angle_radians)
#     sin_vals = np.sin(angle_radians)

#     tick_angles = [i*15 for i in range(0,25)]
#     print(tick_angles)
#     tick_labels = format_slider_ticks(tick_angles, unit)

#     fig = make_subplots(
#         rows=2, cols=2,
#         specs=[[{"rowspan": 2}, {}], [None, {}]],
#         column_widths=[0.6, 0.4],
#         horizontal_spacing=0.1,
#         vertical_spacing=0.15,
#         subplot_titles=("Unit Circle", "cos(θ)", "sin(θ)")
#     )

#     frames = []
#     for deg, rad, cos_val, sin_val in zip(angle_degrees, angle_radians, cos_vals, sin_vals):
#         label = format_angle_label(deg, unit)
#         arc_theta = np.linspace(0, rad, 100)
#         arc_x = 0.3 * np.cos(arc_theta)
#         arc_y = 0.3 * np.sin(arc_theta)
#         label_r = 0.6
#         label_x = label_r * np.cos(rad / 2)
#         label_y = label_r * np.sin(rad / 2)

#         frames.append(go.Frame(
#             name=str(deg),
#             data=[
#                 # Unit circle
#                 go.Scatter(x=np.cos(theta), y=np.sin(theta), mode="lines",
#                            line=dict(color="black"), showlegend=False,
#                            xaxis="x1", yaxis="y1"),
#                 # cos(θ)
#                 go.Scatter(x=angle_degrees, y=cos_vals, mode="lines",
#                            line=dict(color="blue"), showlegend=False,
#                            xaxis="x2", yaxis="y2"),
#                 # sin(θ)
#                 go.Scatter(x=angle_degrees, y=sin_vals, mode="lines",
#                            line=dict(color="green"), showlegend=False,
#                            xaxis="x3", yaxis="y3"),
#                 # Arc fill
#                 go.Scatter(x=[0] + list(arc_x) + [0], y=[0] + list(arc_y) + [0],
#                            fill='toself', fillcolor='rgba(0,100,255,0.2)',
#                            line=dict(color='rgba(0,0,0,0)'), mode='lines', showlegend=False,
#                            xaxis="x1", yaxis="y1"),
#                 # Radius line
#                 go.Scatter(x=[0, cos_val], y=[0, sin_val], mode='lines+markers',
#                            line=dict(color='red'), showlegend=False,
#                            xaxis="x1", yaxis="y1"),
#                 # Point on circle
#                 go.Scatter(
#                         x=[cos_val], y=[sin_val],
#                         mode='markers+text',
#                         text=[
#                             f"(<span style='color:blue'>{cos_val:.2f}</span>, <span style='color:green'>{sin_val:.2f}</span>)"
#                         ],
#                         textposition='top right',
#                         textfont=dict(size=14),
#                         marker=dict(color='black', size=8),
#                         showlegend=False,
#                         xaxis="x1", yaxis="y1",
#                         hoverinfo="skip",
#                         texttemplate="%{text}"
#                     ),
#                 # Arc outline
#                 go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color='green', dash='dash'),
#                            showlegend=False, xaxis="x1", yaxis="y1"),
#                 # Angle label
#                 go.Scatter(x=[label_x], y=[label_y], mode='text', text=[label],
#                            textfont=dict(size=14, color='darkblue'), showlegend=False,
#                            xaxis="x1", yaxis="y1"),
#                 # Moving point on cos(θ)
#                 go.Scatter(x=[deg], y=[cos_val], mode='markers+text',
#                            text=[f"{cos_val:.2f}"], textposition="bottom right",
#                            marker=dict(color='blue', size=10), showlegend=False,
#                            xaxis="x2", yaxis="y2"),
#                 # Moving point on sin(θ)
#                 go.Scatter(x=[deg], y=[sin_val], mode='markers+text',
#                            text=[f"{sin_val:.2f}"], textposition="bottom right",
#                            marker=dict(color='green', size=10), showlegend=False,
#                            xaxis="x3", yaxis="y3")
#             ]
#         ))


#     fig.frames = frames
#     fig.add_traces(frames[0].data)

#     fig.update_layout(
#         template=plot_template,
#         width=1000,
#         height=700,
#         margin=dict(t=60, b=30),
#         xaxis=dict(domain=[0, 0.55], range=[-2, 2], scaleanchor='y'),
#         yaxis=dict(domain=[0, 1], range=[-1.5, 1.5]),
#         xaxis2=dict(domain=[0.65, 1], anchor='y2', title="θ (degrees)", range=[0, 390]),
#         yaxis2=dict(domain=[0.55, 1], range=[-1.1, 1.1]),
#         xaxis3=dict(domain=[0.65, 1], anchor='y3', title="θ (degrees)", range=[0, 390]),
#         yaxis3=dict(domain=[0, 0.45], range=[-1.1, 1.1]),
#         sliders=[{
#             "steps": [{
#                 "label": label,
#                 "method": "animate",
#                 "args": [[str(deg)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
#             } for deg, label in zip(tick_angles, tick_labels)],
#             "transition": {"duration": 0},
#             "x": 0.05,
#             "len": 0.9
#         }],
#         updatemenus=[{
#             "type": "buttons",
#             "showactive": False,
#             "buttons": [
#                 {"label": "Play", "method": "animate",
#                  "args": [None, {"frame": {"duration": 15, "redraw": True}, "fromcurrent": True}]},
#                 {"label": "Pause", "method": "animate",
#                  "args": [[None], {"mode": "immediate"}]}
#             ],
#             "x": 0.05,
#             "y": -0.07
#         }]
#     )

#     return fig





import dash
from dash import html, dcc, callback, Output, Input
dash.register_page(__name__, path="/circ_func_defs", name="Circular Function Definitions")

# from circ_func_defs_plot import create_circular_function_figure  # if using a separate file

layout = html.Div([
    dcc.Store(id="theme-store", storage_type="session"),
    dcc.Store(id="angle-unit-store", storage_type="session", data="degrees"),

    html.Div([
        html.Label("Angle Units:", style={"marginRight": "0.5rem"}),
        dcc.RadioItems(
            id="angle-unit-toggle",
            options=[
                {"label": "Degrees", "value": "degrees"},
                {"label": "Radians", "value": "radians"}
            ],
            value="degrees",
            labelStyle={"display": "inline-block", "marginRight": "1rem"}
        )
    ], style={"marginBottom": "1rem"}),

    html.Div(id="unit-circle-content")
])

@callback(
    Output("unit-circle-content", "children"),
    Input("theme-store", "data"),
    Input("angle-unit-toggle", "value")
)
def render_combined_plot(theme, unit):
    template = "plotly_dark" if theme == "dark" else "plotly_white"
    fig = create_circular_function_figure(unit=unit, plot_template=template)
    return dcc.Graph(figure=fig)


# import dash
# from dash import html, dcc, callback, Input, Output
# import plotly.graph_objects as go

# dash.register_page(__name__, path="/circ_func_defs", name="Circular Function Defintions")



# layout = html.Div([
#     dcc.Store(id="theme-store", storage_type="session"),
#     html.Div(id="unit-circle-content")
# ])

# @callback(
#     Output("unit-circle-content", "children"),
#     Input("theme-store", "data")
# )
# def render_plot(theme):
#     import numpy as np  # Make sure this is available
#     plot_template = "plotly_dark" if theme == "dark" else "plotly_white"

#     # === Precompute static unit circle ===
#     theta = np.linspace(0, 2 * np.pi, 500)
#     circle_x = np.cos(theta)
#     circle_y = np.sin(theta)

#     # === Precompute animation frames ===
#     angles = np.arange(0, 361, 2)
#     frames = []

#     for angle in angles:
#         rad = np.radians(angle)
#         x, y = np.cos(rad), np.sin(rad)

#         # Arc outline for angle sector
#         arc_theta = np.linspace(0, rad, 100)
#         arc_radius = 0.3
#         arc_x = arc_radius * np.cos(arc_theta)
#         arc_y = arc_radius * np.sin(arc_theta)

#         # Angle label position (midpoint of arc)
#         label_angle = rad / 2
#         label_x = 0.4 * np.cos(label_angle)
#         label_y = 0.4 * np.sin(label_angle)

#         frames.append(go.Frame(
#             data=[
#                 # 0: Unit circle
#                 go.Scatter(x=circle_x, y=circle_y, mode='lines', line=dict(color='black'), name='Unit Circle'),

#                 # 1: Filled angle sector
#                 go.Scatter(
#                     x=[0] + list(arc_x) + [0],  # close the sector
#                     y=[0] + list(arc_y) + [0],
#                     fill='toself',
#                     mode='lines',
#                     fillcolor='rgba(0, 100, 255, 0.2)',
#                     line=dict(color='rgba(0,0,0,0)'),
#                     showlegend=False
#                 ),

#                 # 2: Radius line
#                 go.Scatter(x=[0, x], y=[0, y], mode='lines+markers', line=dict(color='red'), showlegend=False),

#                 # 3: Point on circle
#                 go.Scatter(x=[x], y=[y], mode='markers+text',
#                         text=[f"({x:.2f}, {y:.2f})"],
#                         textposition='top right',
#                         marker=dict(color='blue', size=8), showlegend=False),

#                 # 4: Arc outline
#                 go.Scatter(x=arc_x, y=arc_y, mode='lines', line=dict(color='green', dash='dash'), showlegend=False),

#                 # 5: Angle label
#                 go.Scatter(x=[label_x], y=[label_y], mode='text',
#                         text=[f"θ = {angle}°"], textposition='middle right',
#                         textfont=dict(size=14, color='darkblue'), showlegend=False)
#             ],
#             name=str(angle)
#         ))

#     # === Initial figure (from first frame) ===
#     fig = go.Figure(
#         data=frames[0].data,
#         frames=frames
#     )

#     # === Layout ===
#     fig.update_layout(
#         template=plot_template,
#         title="Interactive Unit Circle — Angle and Coordinates",
#         xaxis=dict(scaleanchor='y', range=[-1.5, 1.5], zeroline=True),
#         yaxis=dict(range=[-1.5, 1.5], zeroline=True),
#         width=None,
#         autosize=True,
#         margin=dict(t=40, b=10),
#         sliders=[{
#             "steps": [{
#                 "method": "animate",
#                 "label": str(angle),
#                 "args": [[str(angle)], {"mode": "immediate", "frame": {"duration": 0, "redraw": True}}],
#             } for angle in angles],
#             "transition": {"duration": 0},
#             "x": 0.1,
#             "len": 0.9
#         }],
#         updatemenus=[{
#             "type": "buttons",
#             "showactive": False,
#             "buttons": [
#                 {"label": "Play", "method": "animate",
#                  "args": [None, {"frame": {"duration": 30, "redraw": True}, "fromcurrent": True}]},
#                 {"label": "Pause", "method": "animate",
#                  "args": [[None], {"mode": "immediate"}]}
#             ],
#             "x": 0.1,
#             "y": -0.1
#         }]
#     )

#     return html.Div([
#         html.H2("Unit Circle"),
#         dcc.Graph(figure=fig)
#     ])
