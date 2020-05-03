import dash             #(version 1.11.0) pip install dash==1.11.0
import dash_table
import pandas as pd
from collections import OrderedDict
# (all code is from https://dash.plotly.com/datatable/style)

app = dash.Dash(__name__)

#-----------------------------------------------------------------------------
# Create Fake Dataframes
data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(data)

#-----------------------------------------------------------------------------
app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
#----------------------------------------------------------------
# Column Alignment
#----------------------------------------------------------------
    style_cell={'textAlign': 'left'},
    # style_cell_conditional=[            # style_cell_c. refers to the whole table
    #     {
    #         'if': {'column_id': c},
    #         'textAlign': 'left'
    #     } for c in ['Date', 'Region']
    # ],

#----------------------------------------------------------------
# Table as list (without vertical grid lines)
#----------------------------------------------------------------
    # style_as_list_view=True,

#----------------------------------------------------------------
# Styling Table Header
#----------------------------------------------------------------
    # style_as_list_view=True,
    # style_cell={'padding': '5px'},   # style_cell refers to the whole table
    # style_header={
    #     'backgroundColor': 'white',
    #     'fontWeight': 'bold',
    #     'border': '1px solid black'
    # },

#----------------------------------------------------------------
# Striped Rows
#----------------------------------------------------------------
    # style_header={
    #     'backgroundColor': 'rgb(230, 230, 230)',
    #     'fontWeight': 'bold'
    # },
    # style_data_conditional=[        # style_data.c refers only to data rows
    #     {
    #         'if': {'row_index': 'odd'},
    #         'backgroundColor': 'rgb(248, 248, 248)'
    #     }
    # ],

#----------------------------------------------------------------
# Dark Theme with Cells
#----------------------------------------------------------------
    # style_header={'backgroundColor': 'rgb(30, 30, 30)'},
    # style_cell={
    #     'backgroundColor': 'rgb(50, 50, 50)',
    #     'color': 'white'
    # },

#----------------------------------------------------------------
# Highlighting Certain Rows
#----------------------------------------------------------------
    # style_data_conditional=[{
    #     "if": {"row_index": 4},
    #     "backgroundColor": "#3D9970",
    #     'color': 'white',
    #     "fontWeight": "bold"
    # }]

#----------------------------------------------------------------
# Highlighting Certain Columns
#----------------------------------------------------------------
    # style_data_conditional=[{
    #     'if': {'column_id': 'Temperature'},
    #     'backgroundColor': '#3D9970',
    #     'color': 'white',
    # }]
#----------------------------------------------------------------
# Highlighting Certain Cells
#----------------------------------------------------------------
    # style_data_conditional=[
    #     {
    #         'if': {
    #             'column_id': 'Region',
    #             'filter_query': '{Region} eq "Montreal"'
    #         },
    #         'backgroundColor': '#3D9970',
    #         'color': 'white',
    #     },
    #     {
    #         'if': {
    #             'column_id': 'Humidity',
    #             'filter_query': '{Humidity} eq 20'
    #         },
    #         'backgroundColor': '#3D9970',
    #         'color': 'white',
    #     },
    #     {
    #         'if': {
    #             'column_id': 'Temperature',
    #             'filter_query': '{Temperature} > 3.9'
    #         },
    #         'backgroundColor': '#3D9970',
    #         'color': 'white',
    #     },
    # ],

#----------------------------------------------------------------
# Adding Borders
#----------------------------------------------------------------
    # style_data={ 'border': '1px solid red' },
    # style_header={ 'border': '1px solid black' },

#----------------------------------------------------------------
# Multi-Headers
#----------------------------------------------------------------
    # columns=[
    #     {"name": ["", "Year"], "id": "year"},
    #     {"name": ["City", "Montreal"], "id": "montreal"},
    #     {"name": ["City", "Toronto"], "id": "toronto"},
    #     {"name": ["City", "Ottawa"], "id": "ottawa"},
    #     {"name": ["City", "Vancouver"], "id": "vancouver"},
    #     {"name": ["Climate", "Temperature"], "id": "temp"},
    #     {"name": ["Climate", "Humidity"], "id": "humidity"},
    # ],
    # data=[
    #     {
    #         "year": i,
    #         "montreal": i * 10,
    #         "toronto": i * 100,
    #         "ottawa": i * -1,
    #         "vancouver": i * -10,
    #         "temp": i * -100,
    #         "humidity": i * 5,
    #     }
    #     for i in range(10)
    # ],
    # merge_duplicate_headers=True,

#----------------------------------------------------------------
# Styling Editable Columns
#----------------------------------------------------------------
    # data=df.to_dict('records'),
    # columns=[
    #     {'id': c, 'name': c, 'editable': (c == 'Humidity')}
    #     for c in df.columns
    # ],
    # style_data_conditional=[{           # style_data refers only to data rows
    #     'if': {'column_editable': False},
    #     'backgroundColor': 'rgb(30, 30, 30)',
    #     'color': 'white'
    # }],
    # style_header_conditional=[{         # style_header refers only to Header
    #     'if': {'column_editable': False},
    #     'backgroundColor': 'rgb(30, 30, 30)',
    #     'color': 'white'
    # }],

#----------------------------------------------------------------
# Styles Priority
#----------------------------------------------------------------
# There is a specific order of priority for the style_* properties. If there are
# multiple style_* props, the one with higher priority will take precedence.
# Within each prop, rules for higher indices will be prioritized over those for lower indices.
# Previously applied styles of equal priority win over later ones (applied top to bottom, left to right).
#
# These are the priorities of style_* props, in decreasing order:
#
# 1. style_data_conditional
# 2. style_data
# 3. style_filter_conditional
# 4. style_filter
# 5. style_header_conditional
# 6. style_header
# 7. style_cell_conditional
# 8. style_cell


#----------------------------------------------------------------
)

if __name__ == '__main__':
    app.run_server(debug=True)
