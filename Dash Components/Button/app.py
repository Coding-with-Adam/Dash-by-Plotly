################## Dash HTML Button component #############################

from dash import Dash, html

app = Dash(__name__)

button = html.Button("Enter")

app.layout = html.Div(button)

if __name__ == "__main__":
    app.run(debug=True, port=8001)


# -------------------------------------------------------------------------
#################### Dash Bootstrap Button ################################

# from dash import Dash, html
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) #CYBORG https://dashcheatsheet.pythonanywhere.com/
#
# buttons = html.Div(
#     [
#         dbc.Button("Primary", color="primary", className="me-1" ),
#         dbc.Button("Secondary", color="secondary", className="me-1"),
#         dbc.Button("Success", color="success", className="me-1"),
#         dbc.Button("Warning", color="warning", className="me-1"),
#         dbc.Button("Danger", color="danger", className="me-1"),
#         dbc.Button("Info", color="info"),
#     ], className= "m-4"
# )
#
# app.layout = dbc.Container(buttons)
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8002)


# -------------------------------------------------------------------------
########## Dash Bootstrap Button with different styles ####################

# from dash import Dash, html
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# buttons = html.Div(
#     [
#         dbc.Button("Regular", className="me-1"),
#         dbc.Button("Outline", outline=True, color="primary", className="me-1"),
#         dbc.Button("Disabled", disabled=True, className="me-1"),
#         dbc.Button("Large", size="lg", className="me-1"),
#         dbc.Button("Small", size="sm", className="me-1"),
#         dbc.Button("Link", color="link"),
#
#     ], className= "m-4"
# )
#
# app.layout = dbc.Container(buttons)
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8003)


# -------------------------------------------------------------------------
#################### Dash Bootstrap Button with Icons #####################

# from dash import Dash, html
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])
#
# FA_icon = html.I(className="fa-solid fa-cloud-arrow-down me-2")
# FA_button =  dbc.Button([FA_icon, "Download"], className="me-2")
#
# BS_icon = html.I(className="bi bi-cloud-arrow-down-fill me-2")
# BS_button = dbc.Button([BS_icon, "Download"])
#
# app.layout = dbc.Container([FA_button, BS_button])
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8004)


# -------------------------------------------------------------------------
#################### Dash Bootstrap Button with Iconify ###################

# from dash import Dash
# import dash_bootstrap_components as dbc
# from dash_iconify import DashIconify
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# download_icon = DashIconify(icon="bi:cloud-download", style={"marginRight": 5})
# download_button =  dbc.Button([download_icon, "Download"], className="me-2")
#
# settings_icon = DashIconify(icon="carbon:settings-check", style={"marginRight": 5})
# settings_button = dbc.Button([settings_icon, "Settings"])
#
# app.layout = dbc.Container([download_button, settings_button])
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8005)


# -------------------------------------------------------------------------
#################### Dash Mantine Component Button ########################

# from dash import Dash
# import dash_mantine_components as dmc
# from dash_iconify import DashIconify
#
# app = Dash(__name__)
#
# buttons = dmc.Group(
#     [
#         dmc.Button("Default"),
#         dmc.Button("Subtle", variant="subtle"),
#         dmc.Button("Gradient", variant="gradient"),
#         dmc.Button("Light", variant="light"),
#         dmc.Button("Outline", variant="outline"),
#         dmc.Button("Radius- lg", radius="lg"),
#         dmc.Button("Compact", compact=True),
#         dmc.Button("Icon", leftIcon=[DashIconify(icon="fluent:settings-32-regular")],
#         ),
#     ]
# )
#
# app.layout = dmc.Container(buttons)
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8006)


# -------------------------------------------------------------------------
################# Mantine Button Connected to a Form ######################

# from dash import Dash, html, Input, Output, State
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
#
# form = dbc.FormFloating(
#     [
#         dbc.Input(id="username"),
#         dbc.Label("Enter username"),
#     ]
# )
# button = dbc.Button("Submit")
# output_container = html.Div(className="mt-4")
#
# app.layout = dbc.Container([form, button, output_container], fluid=True)
#
#
# @app.callback(
#     Output(output_container, "children"),
#     Input(button, "n_clicks"),
#     State("username", "value"),
#     prevent_initial_call=True,
# )
# def greet(_, name):
#     return f"Welcome {name}!" if name else "Please enter username"
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8007)


# -------------------------------------------------------------------------
################# Mantine Button Connected to a Form ######################

# from dash import Dash, html, Input, Output, State, ctx
# import dash_bootstrap_components as dbc
#
# app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])
#
# app.layout = dbc.Container([
#     dbc.FormFloating(
#         [
#             dbc.Input(id="username"),
#             dbc.Label("Enter username"),
#         ]
#     ),
#     dbc.Button(id="button1", children="Register Name"),
#     dbc.Button(id="button2", children="Submit Application", className="ms-2"),
#     html.Div(id="output_container", className="mt-4")
# ], fluid=True)
#
#
# @app.callback(
#     Output("output_container", "children"),
#     Input("button1", "n_clicks"),
#     Input("button2", "n_clicks"),
#     State("username", "value"),
#     prevent_initial_call=True,
# )
# def greet(_, __, name):
#     button_clicked = ctx.triggered_id
#     if button_clicked == 'button1':
#         return f"Welcome {name}!" if name else "Please enter username"
#     elif button_clicked == 'button2':
#         return "Your application has been submitted." if name else "Please enter username"
#
#
# if __name__ == "__main__":
#     app.run_server(debug=True, port=8008)
