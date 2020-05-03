import dash             #(version 1.11.0) pip install dash==1.11.0
import dash_table
import pandas as pd
from collections import OrderedDict
# (all code is from https://dash.plotly.com/datatable/height)

app = dash.Dash(__name__)

#-----------------------------------------------------------------------------
# Create Fake Dataframes
data = OrderedDict(
    [
        ("Date", ["2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15",
                  "2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15",
                  "2015-01-01", "2015-10-24", "2016-05-10", "2017-01-10", "2018-05-10", "2018-08-15"]),
        ("Region", ["Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London",
                    "Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London",
                    "Montreal", "Toronto", "New York City", "Miami", "San Francisco", "London"]),
        ("Temperature", [1, -20, 3.512, 4, 10423, -441.2,
                         1, -20, 3.512, 4, 10423, -441.2,
                         1, -20, 3.512, 4, 10423, -441.2]),
        ("Humidity", [10, 20, 30, 40, 50, 60,
                      10, 20, 30, 40, 50, 60,
                      10, 20, 30, 40, 50, 60]),
        ("Pressure", [2, 10924, 3912, -10, 3591.2, 15,
                      2, 10924, 3912, -10, 3591.2, 15,
                      2, 10924, 3912, -10, 3591.2, 15]),
    ]
)

df = pd.DataFrame(data)

data_numeric = pd.DataFrame(OrderedDict(
    [
        [
            'Column {}'.format(i + 1), list(range(30))
        ] for i in range(15)
    ]
))

df_numeric = pd.DataFrame(data_numeric)

#-----------------------------------------------------------------------------
app.layout = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
#-----------------------------------------------------------------------------
# Vertical Scroll (without Pagination)
#-----------------------------------------------------------------------------
    page_action='none',     # render all of the data at once
    style_table={'height': '300px', 'overflowY': 'auto'}

    # If you have more than 1000 rows, your browswer will slow down. Therefore,
    # for over 1000 rows, use pagination as per examples below or virtualization
    # as per last example.

#-----------------------------------------------------------------------------
# Fronent Pagination with Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',   # all data is passed to the table up-front
    # page_size=10,           # only 10 rows are displayed at a time
    # style_table={'height': '200px', 'overflowY': 'auto'}

#-----------------------------------------------------------------------------
# Fronent Pagination without Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',     # all data is passed to the table up-front
    # page_size=10,             # but only 10 rows are displayed at a time

    # If you have over 10,000 rows you should do pagination in the backend
    # to lower network costs and memory. See how with link below:
    # https://dash.plotly.com/datatable/callbacks

#-----------------------------------------------------------------------------
# Vertical Scroll With Fixed Headers
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_table={'height': 400}  # defaults to 500

    # By default and without wrapping, each row takes up 30px. So 10 rows with
    # one header would set the table to be 330px tall.
    # Since here we have 18 rows+header, that would equal 570px.

#-----------------------------------------------------------------------------
# Width of Headers (partial text)
#-----------------------------------------------------------------------------

    # If the headers are wider than the cells and the table's container isn't wide
    # enough to display all of the headers, then the column headers will be truncated

    # data=df_numeric.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df_numeric.columns],

    # fixed_rows={'headers': True}

#-----------------------------------------------------------------------------
# Width of Headers (full text)
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_cell={
    #     'minWidth': 95, 'maxWidth': 95, 'width': 95
    # }

#-----------------------------------------------------------------------------
# Vertical Scroll with Virtualization
#-----------------------------------------------------------------------------
    # virtualization=True,            # to use when you have over 1000 rows
    # fixed_rows={'headers': True},
    # style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95}, #set width when using virtualization
    # style_table={'height': 300}     # default is 500px

#----------------------------------------------------------------
)

if __name__ == '__main__':
    app.run_server(debug=True)
