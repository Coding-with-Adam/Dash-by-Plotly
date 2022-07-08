from dash import Dash, dcc, html, Output, Input, State, callback
import plotly.express as px

df = px.data.tips()
print(df.head())

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=px.histogram(df, x='day', y='tip'), id='bar-graph'),
    dcc.Graph(figure={}, id='my-graph')
])

# Plot a pie chart based on the selected day of the bar chart
@callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='bar-graph', component_property='clickData'),
    prevent_initial_call=True
)
def update_text(chosen_data):  # the function argument comes from the component property of the Input
    print(chosen_data)
    print(type(chosen_data))
    extract_day = chosen_data['points'][0]['x']
    print(extract_day)
    dff = df[df.day==extract_day]
    print(dff.head())
    fig = px.pie(dff, names='smoker', values='total_bill',  title=f'total bill by smoker on {extract_day}')
    return fig  # the returned objects are assigned to the component properties of the Outputs


if __name__=='__main__':
    app.run(port=8005)