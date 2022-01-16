from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_bootstrap_components as dbc
from vega_datasets import data              # pip install vega-datasets

import altair as alt                        # pip install altair

import matplotlib.pyplot as plt             # pip install matplotlib
import mpld3                                # pip install mpld3

from bokeh.plotting import figure           # pip install Bokeh
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource


# bring data into app
cars = data.cars()
# print(cars.columns)

# Set up Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up the page layout
app.layout = dbc.Container([
    html.H1("Creating Interactive Altair, Matplotlib, Bokeh Visualizations with Dash"),

    html.Iframe(
        id='scatterplots',
        srcDoc=None, # here is where we will put the graph we make
        style={'border-width': '5', 'width': '100%', 'height': '500px'}),

    html.H5("Select Y column for graph", className='mt-2'),
    dcc.Dropdown(
        id='mydropdown',
        value='Horsepower',
        options=[{'label': col, 'value': col} for col in cars.columns])
])

# Create interactivity between dropdown and graph
@app.callback(
    Output(component_id='scatterplots', component_property='srcDoc'),
    Input(component_id='mydropdown', component_property='value'))
def plot_data(selected_ycol):
    print(f"User Seleceted this dropdown value: {selected_ycol}")

    # Altair graphing library----------------------------------------------
    chart = alt.Chart(cars).mark_circle().encode(
        x='Displacement',
        y=selected_ycol,
        tooltip=selected_ycol).interactive()
    html_altair = chart.to_html()

    # Matplotlib graphing library------------------------------------------
    # colvalue = cars[selected_ycol]
    # fig, ax = plt.subplots()
    # ax.scatter(x=cars.Displacement, y=colvalue)
    # ax.set_xlabel("Displacement")
    # ax.set_ylabel(selected_ycol)
    # ax.grid(color='lightgray', alpha=0.7)
    # html_matplotlib = mpld3.fig_to_html(fig)

    # Bokeh graphing library-----------------------------------------------
    # sourcedata = ColumnDataSource(cars.copy())
    # plot = figure(x_axis_label='Displacement', y_axis_label=selected_ycol)
    # plot.scatter(x='Displacement', y=selected_ycol, source=sourcedata)
    # html_bokeh = file_html(plot, CDN)

    return html_altair

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)
