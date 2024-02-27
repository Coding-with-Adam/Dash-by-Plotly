# Code written by Sébastien Didier
# Insert code (with micropip) in WasmDash to run app: https://wasmdash.vercel.app/
# import micropip
# await micropip.install("dash_ag_grid")
import dash_ag_grid as dag
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd

app = Dash()

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/ag-grid/olympic-winners.csv"
)

columnDefs = [
    {"field": 'athlete', "minWidth": 180},
    {"field": 'age', "filter": 'agNumberColumnFilter', "maxWidth": 80},
    {"field": 'country'},
    {"field": 'year', "maxWidth": 90},
    {
        "field": 'date',
        "filter": 'agDateColumnFilter',
        "filterParams": {
            "comparator": {"function": "dateFilterComparator"},
        },
    },
]

filter_function = {
    'below25': "params.data.age < 25",
    'between25and50': "params.data.age >= 25 && params.data.age <= 50",
    'above50': "params.data.age > 50",
    'everyone': "true"
}

app.layout = html.Div(
    [
        dcc.RadioItems(
            id='external-filter-radio',
            options={
                'everyone': 'Everyone',
                'below25': 'Below 25',
                'between25and50': 'Between 25 and 50',
                'above50': 'Above 50',
            },
            value='everyone',
            inline=False,
            style={'margin': '10px'}
        ),
        dag.AgGrid(
            id="external-filter-example",
            rowData=df.to_dict("records"),
            columnDefs=columnDefs,
            defaultColDef={"flex": 1},
            # dashGridOptions={"isExternalFilterPresent":{"function":"true"},
            #                  "doesExternalFilterPass": {"function": filter_function['below25']}}
        ),
    ]
)


@callback(
    Output("external-filter-example", "dashGridOptions"),
    Input("external-filter-radio", "value"),
    prevent_initial_call=True,
)
def update_external_filter(filter_value):
    return {
        # if filter_value is not 'everyone', then we will start filtering
        "isExternalFilterPresent": {"function": "true" if filter_value != 'everyone' else "false"},
        "doesExternalFilterPass": {"function": filter_function[filter_value]}
    }


if __name__ == "__main__":
    app.run(debug=True)
