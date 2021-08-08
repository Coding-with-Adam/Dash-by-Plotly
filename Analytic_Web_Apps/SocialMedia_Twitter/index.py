import dash_bootstrap_components as dbc
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import twitter  # pip install python-twitter
from app import app, api

# Connect to the layout and callbacks of each tab
from mentions import mentions_layout
from trends import trends_layout
from other import other_layout


# our app's Tabs *********************************************************
app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Mentions", tab_id="tab-mentions", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Trends", tab_id="tab-trends", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
                dbc.Tab(label="Other", tab_id="tab-other", labelClassName="text-success font-weight-bold", activeLabelClassName="text-danger"),
            ],
            id="tabs",
            active_tab="tab-mentions",
        ),
    ], className="mt-3"
)

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Twitter Analytics Dashboard Live",
                            style={"textAlign": "center"}), width=12)),
    html.Hr(),
    dbc.Row(dbc.Col(app_tabs, width=12), className="mb-3"),
    html.Div(id='content', children=[])

])

@app.callback(
    Output("content", "children"),
    [Input("tabs", "active_tab")]
)
def switch_tab(tab_chosen):
    if tab_chosen == "tab-mentions":
        return mentions_layout
    elif tab_chosen == "tab-trends":
        return trends_layout
    elif tab_chosen == "tab-other":
        return other_layout
    return html.P("This shouldn't be displayed for now...")



if __name__=='__main__':
    app.run_server(debug=True)
