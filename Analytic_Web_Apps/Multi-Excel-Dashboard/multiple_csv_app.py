import base64
import datetime
import io

from dash import Dash, dcc, html, dash_table, Input, Output, State, MATCH, no_update
import plotly.express as px
import pandas as pd

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1('Dashboard of Multiple Excel Sheets', style={'textAlign': 'center'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-data-upload', children=[]),
])

# Upload CSV and Excel sheets to the app and create the tables----------------------------------------------------------
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              State('output-data-upload', 'children'),
              prevent_initial_call=True
)
def update_output(contents, filename, date, children):
    # part of the code snippet is from https://dash.plotly.com/dash-core-components/upload
    if contents is not None:
        for i, (c, n, d) in enumerate(zip(contents, filename, date)):

            content_type, content_string = contents[i].split(',')

            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in filename[i]:
                    # Assume that the user uploaded a CSV file
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in filename[i]:
                    # Assume that the user uploaded an excel file
                    df = pd.read_excel(io.BytesIO(decoded))

                # Create the tables and empty graphs
                children.append(html.Div([
                    html.H5(filename[i]),

                    dash_table.DataTable(
                        df.to_dict('records'),
                        [{'name': i, 'id': i, 'selectable':True} for i in df.columns],
                        page_size=5,
                        filter_action='native',
                        column_selectable=False if filename[i]=='Toronto_temp.xlsx' else 'single',
                        selected_columns=[df.columns[4]], # preselect the 5th columns
                        style_table={'overflowX': 'auto'},
                        id={'type': 'dynamic-table',
                            'index': i},
                    ),

                    dcc.Graph(
                        id={
                            'type': 'dynamic-graph',
                            'index': i
                        },
                        figure={}
                    ),

                    # # For debugging
                    # html.Div('Raw Content'),
                    # html.Pre(contents[i][0:200] + '...', style={
                    #     'whiteSpace': 'pre-wrap',
                    #     'wordBreak': 'break-all'
                    # }),
                    html.Hr()
            ]))

            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])
        return children
    else:
        return ""


# Build the graphs from the filtered data in the Datatable--------------------------------------------------------------
@app.callback(Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
              Input({'type': 'dynamic-table', 'index': MATCH}, 'derived_virtual_indices'),
              Input({'type': 'dynamic-table', 'index': MATCH}, 'selected_columns'),
              State({'type': 'dynamic-table', 'index': MATCH}, 'data')
)
def create_graphs(filtered_data, selected_col, all_data):
    if filtered_data is not None:
        dff = pd.DataFrame(all_data)
        dff = dff[dff.index.isin(filtered_data)]

        # if first column of the dataset is Year, you are working with the NYC Central park table
        if list(dff.columns)[0] == 'Year':
            print(dff.head())
            if selected_col[0]=='Year': # if user selects the Year column, don't update graph
                return no_update
            else:
                dff = dff.groupby(['Year'])[selected_col[0]].mean().reset_index(name=selected_col[0])
                fig_climate = px.line(dff, x='Year', y=selected_col[0])
                return fig_climate

        # if first column of the dataset is STATION, you are working with the NYC Central park table
        elif list(dff.columns)[0] == 'STATION':
            if selected_col[0]=='DATE':  # if user selects the DATE column, don't update graph
                return no_update
            else:
                dff['DATE'] = pd.to_datetime(dff['DATE'])
                dff['year'] = dff['DATE'].dt.year
                dff = dff.groupby(['year'])[selected_col[0]].sum().reset_index(name=selected_col[0])
                fig_nyc = px.bar(dff, x='year', y=selected_col[0])
                return fig_nyc

        # if first column of the dataset is Date_Time, you are working with the Toronto table
        elif list(dff.columns)[0] == 'Date_Time':
            dff = dff.groupby(['year'])[['Mean Temp (C)', 'Max Temp (C)', 'Min Temp (C)']].mean().reset_index()
            fig_toronto = px.line(dff, x='year', y=['Mean Temp (C)', 'Max Temp (C)', 'Min Temp (C)'])
            return fig_toronto
    else:
        return {}



if __name__ == '__main__':
    app.run_server(debug=True)
