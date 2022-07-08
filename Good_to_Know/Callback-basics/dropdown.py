from dash import Dash, dcc, html, Output, Input, State, callback
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(options=['Texas','Florida','New York'], value='Texas', clearable=True, id='our-States'),
    dcc.RadioItems(options=['Dallas','Arlington','Austin'], id='my-radio-btn'),
])

# Display options of cities based on chosen US state
@callback(
    Output(component_id='my-radio-btn', component_property='options'),
    Input(component_id='our-States', component_property='value')
)
def update_text(chosen_state):  # the function argument comes from the component property of the Input
    print(chosen_state)
    print(type(chosen_state))
    if chosen_state == 'Texas':
        return ['Dallas','Arlington','Austin']
    elif chosen_state == 'Florida':
        return ['Polk City','Pinecrest','Orlando']
    elif chosen_state == 'New York':
        return ['Troy','Buffalo','Batavia']
    else:
        return []  # the returned objects are assigned to the component properties of the Outputs


if __name__=='__main__':
    app.run(port=8004)