# hashtag out the labelClassName and add opacity to labelStyle (line 18)

html.Div([
        dcc.Checklist(
            id='my_checklist',
            options=[
                     {'label': x, 'value': x, 'disabled':False}
                     for x in df['Month Call Made'].unique()
            ],
            value=['January','July','December'],
            className='my_box_container',
            inputClassName='my_box_input',

            # labelClassName='my_box_label',
            labelStyle={'background':'#A5D6A7',
                        'padding':'0.5rem 1rem',
                        'border-radius':'0.5rem',
                        'opacity':0.5},
        ),
    ]),
