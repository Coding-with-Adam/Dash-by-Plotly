import dash  # (version 1.11.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__)

# ------------------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='my_txt_input',
            type='text',
            debounce=True,           # changes to input are sent to Dash server only on enter or losing focus
            pattern=r"^[A-Za-z].*",  # Regex: string must start with letters only
            spellCheck=True,
            inputMode='latin',       # provides a hint to browser on type of data that might be entered by the user.
            name='text',             # the name of the control, which is submitted with the form data
            list='browser',          # identifies a list of pre-defined options to suggest to the user
            n_submit=0,              # number of times the Enter key was pressed while the input had focus
            n_submit_timestamp=-1,   # last time that Enter was pressed
            autoFocus=True,          # the element should be automatically focused after the page loaded
            n_blur=0,                # number of times the input lost focus
            n_blur_timestamp=-1,     # last time the input lost focus.
            # selectionDirection='', # the direction in which selection occurred
            # selectionStart='',     # the offset into the element's text content of the first selected character
            # selectionEnd='',       # the offset into the element's text content of the last selected character
        ),
    ]),

    html.Datalist(id='browser', children=[
        html.Option(value="blue"),
        html.Option(value="yellow"),
        html.Option(value="green")
    ]),

    html.Br(),
    html.Br(),

    html.Div(id='div_output'),

    html.P(['------------------------']),

    html.P(['Enter clicked:']),
    html.Div(id='div_enter_clicked'),

    html.P(['Enter clicked timestamp:']),
    html.Div(id='div_sub_tmstp'),

    html.P(['------------------------']),

    html.P(['Input lost focus:']),
    html.Div(id='div_lost_foc'),

    html.P(['Lost focus timestamp:']),
    html.Div(id='div_lst_foc_tmstp'),

])

# ------------------------------------------------------------------------
@app.callback(
    [Output(component_id='div_output', component_property='children'),
     Output(component_id='div_enter_clicked', component_property='children'),
     Output(component_id='div_sub_tmstp', component_property='children'),
     Output(component_id='div_lost_foc', component_property='children'),
     Output(component_id='div_lst_foc_tmstp', component_property='children')],
    [Input(component_id='my_txt_input', component_property='value'),
     Input(component_id='my_txt_input', component_property='n_submit'),
     Input(component_id='my_txt_input', component_property='n_submit_timestamp'),
     Input(component_id='my_txt_input', component_property='n_blur'),
     Input(component_id='my_txt_input', component_property='n_blur_timestamp')]
)
def update_graph(txt_inserted, num_submit, sub_tmstp, lost_foc, lst_foc_tmstp):
    if sub_tmstp == -1:
        submited_dt = sub_tmstp
    else:
        submited_dt = datetime.datetime.fromtimestamp(int(sub_tmstp) / 1000)  # using the local timezone
        submited_dt = submited_dt.strftime("%Y-%m-%d %H:%M:%S")

    if lst_foc_tmstp == -1:
        lost_foc_dt = lst_foc_tmstp
    else:
        lost_foc_dt = datetime.datetime.fromtimestamp(int(lst_foc_tmstp) / 1000)  # using the local timezone
        lost_foc_dt = lost_foc_dt.strftime("%Y-%m-%d %H:%M:%S")

    return txt_inserted, num_submit, submited_dt, lost_foc, lost_foc_dt


# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
