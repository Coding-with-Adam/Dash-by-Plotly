import dash      #(version 1.9.1) pip install dash==1.9.1
import dash_table
import pandas as pd
from collections import OrderedDict

app = dash.Dash(__name__)
# (all code is from https://dash.plotly.com/datatable/width)
#------------------------------------------------------------------
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

election_data = OrderedDict(
    [
        (
            "Date",
            [
                "July 12th, 2013 - July 25th, 2013",
                "July 12th, 2013 - August 25th, 2013",
                "July 12th, 2014 - August 25th, 2014",
            ],
        ),
        (
            "Election Polling Organization",
            ["The New York Times", "Pew Research", "The Washington Post"],
        ),
        ("Rep", [1, -20, 3.512]),
        ("Dem", [10, 20, 30]),
        ("Ind", [2, 10924, 3912]),
        (
            "Region",
            [
                "Northern New York State to the Southern Appalachian Mountains",
                "Canada",
                "Southern Vermont",
            ],
        ),
    ]
)

df_election = pd.DataFrame(election_data)
df_long = pd.DataFrame(
    OrderedDict([(name, col_data * 10) for (name, col_data) in election_data.items()])
)

#----------------------------------------------------------------

app.layout = dash_table.DataTable(
    data=df_election.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df_election.columns],)  # Before running code at 03:45 in tutorial, delete this Parenthesis. 
#----------------------------------------------------------------
# Overflow cells' content into multiple lines
#----------------------------------------------------------------
    # style_data={
    #     'whiteSpace': 'normal',
    #     'height': 'auto'
    # })
#----------------------------------------------------------------
# Overflow cells' content into ellipses (...)
#----------------------------------------------------------------
    # style_data={
    #     'overflow': 'hidden',
    #     'textOverflow': 'ellipsis', #use 'clip' to hide content
    #     'maxWidth': 0,
    # })
#----------------------------------------------------------------
# Horizontal Scroll
#----------------------------------------------------------------
    # style_table={'overflowX': 'scroll'})
#----------------------------------------------------------------
# Combine horizontal scroll with fixed column width
#----------------------------------------------------------------
    # style_table={'overflowX': 'scroll'},
    # style_cell={
    #     'height': 'auto',
    #     # all three widths are needed
    #     'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
    #     'whiteSpace': 'normal'
    # })
#----------------------------------------------------------------
# Combine horizontal scroll, fixed columns width, & ellipses (...)
#----------------------------------------------------------------
    # style_table={'overflowX': 'scroll'},
    # style_cell={
    #     # all three widths are needed
    #     'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
    #     'overflow': 'hidden',
    #     'textOverflow': 'ellipsis',
    # })
#----------------------------------------------------------------
# Horizontal scroll by Freezing left column
#----------------------------------------------------------------
    # fixed_columns={ 'headers': True, 'data': 1 }) #digit = number of columns fixed
#----------------------------------------------------------------
# Horizontal scroll by Freezing left column, & ellipses (...)
#----------------------------------------------------------------
    # fixed_columns={ 'headers': True, 'data': 1 },
    # style_cell={
    #     # all three widths are needed
    #     'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
    #     'overflow': 'hidden',
    #     'textOverflow': 'ellipsis',
    # })
#----------------------------------------------------------------
# Individual Column Widths (percentages)
#----------------------------------------------------------------
    # data=df.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df.columns],

    # style_cell_conditional=[
    #     {'if': {'column_id': 'Date'},
    #      'width': '40%'},
    #     {'if': {'column_id': 'Region'},
    #      'width': '40%'},
    # ])
#----------------------------------------------------------------
# Individual Column Widths (pixels)
#----------------------------------------------------------------
    # style_cell_conditional=[
    #     {'if': {'column_id': 'Temperature'},
    #      'width': '230px'},
    #     {'if': {'column_id': 'Humidity'},
    #      'width': '230px'},
    #     {'if': {'column_id': 'Pressure'},
    #      'width': '230px'},
    # ])
#----------------------------------------------------------------
# Vertical Scrolling
#----------------------------------------------------------------
    # data=df_long.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df_long.columns],

    # style_table={
    #     'maxHeight': '300px',
    #     'overflowY': 'scroll'
    # })
#------------------------------------------------------------------
# Freeze Rows
#------------------------------------------------------------------
    # fixed_rows={ 'headers': True, 'data': 1 },  #digit represents number of rows frozen
    # style_cell={'width': '150px'})              #must set an explicit pixel-based width
#------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
