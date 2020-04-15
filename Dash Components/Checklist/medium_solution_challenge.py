        html.Div([
            dcc.Checklist(
                id='my_checklist',                    
                options=[
                         {'label': x, 'value': x, 'disabled':True}
                         if x=='March' else {'label': x, 'value': x, 'disabled':False}
                         for x in df['Month Call Made'].unique()
                ]
            )
        ])
