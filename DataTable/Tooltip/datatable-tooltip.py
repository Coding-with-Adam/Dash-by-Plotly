import dash
import dash_table
import pandas as pd

df = pd.read_csv("medical_supplies_tooltip.csv")

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),

    # Overflow into ellipsis
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
    },

    tooltip_delay=0, # 1000
    tooltip_duration=None, # 2000
    # *********************************************************************
    # for all individual cells
    # tooltip_data=[
    #     {
    #         column: {'value': str(value), 'type': 'markdown'}
    #         for column, value in row.items()
    #     } for row in df.to_dict('records')
    # ],
    # *********************************************************************
    # column headers
    tooltip_header={
        'Part description': 'Part description',
        'Origin supplier': 'Suppliers since 1994',
    },
    # *********************************************************************
    # single tooltip for entire column
    # tooltip={i:
    #     {
    #         'value': i,
    #         'use_with': 'both'  # both refers to header & data cell
    #     } for i in df.columns
    # },
    # *********************************************************************
    # conditional content in cells
    tooltip_data=[{
        'Machines A': {
            'value': 'There are **{} {}** A machines than B machines'.format(
                str(abs(row['Machines A'] - row['Machines B'])),
                'more' if row['Machines A'] > row['Machines B'] else 'fewer'
            ),
            'type': 'markdown'
        },
        'Elapsed Days': {
            'value': 'The shipment is {}'.format(
                '![Markdown Logo is here.](https://media.giphy.com/media/1xjX6EOQZnS5ouhU5k/giphy.gif)'
                if row['Elapsed Days'] >=18
                else '![Markdown Logo is here.](https://media.giphy.com/media/7SIdExk63rTPXhbbbt/giphy.gif)'
            ),
            'type': 'markdown'
        }
    } for row in df.to_dict('records')],
    # *********************************************************************
    # conditional content
    # tooltip_conditional=[
    #     {
    #         'if': {
    #             'filter_query': '{Country} eq "Canada"'
    #         },
    #         'type': 'markdown',
    #         'value': 'Canada row.'
    #     }
    # ],
    # *********************************************************************
    # styling the tooltip
    # css=[{
    #     'selector': '.dash-table-tooltip',
    #     'rule': 'background-color: purple; color: yellow;'
    # }],

)

if __name__=='__main__':
    app.run_server(debug=True)
