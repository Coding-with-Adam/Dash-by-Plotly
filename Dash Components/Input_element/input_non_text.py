import dash  # (version 1.11.0)
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px     # (version 4.6.0)
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------
# Import and filter data into pandas data frame
df = pd.read_csv("dup_bees.csv")
df['Value'] = pd.to_numeric(df['Value'])
mapping = {'HONEY, BEE COLONIES, AFFECTED BY DISEASE - INVENTORY, MEASURED IN PCT OF COLONIES': 'Disease',
           'HONEY, BEE COLONIES, AFFECTED BY OTHER CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Other',
           'HONEY, BEE COLONIES, AFFECTED BY PESTICIDES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Pesticides',
           'HONEY, BEE COLONIES, AFFECTED BY PESTS ((EXCL VARROA MITES)) - INVENTORY, MEASURED IN PCT OF COLONIES': 'Pests_excl_Varroa',
           'HONEY, BEE COLONIES, AFFECTED BY UNKNOWN CAUSES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Unknown',
           'HONEY, BEE COLONIES, AFFECTED BY VARROA MITES - INVENTORY, MEASURED IN PCT OF COLONIES': 'Varroa_mites'}
df['Data Item'] = df['Data Item'].map(mapping)
df.rename(columns={'Data Item': 'Affected by', 'Value': 'Percent of Colonies Impacted'}, inplace=True)

state_codes = {
    'District of Columbia': 'dc', 'Mississippi': 'MS', 'Oklahoma': 'OK',
    'Delaware': 'DE', 'Minnesota': 'MN', 'Illinois': 'IL', 'Arkansas': 'AR',
    'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 'Louisiana': 'LA',
    'Idaho': 'ID', 'Wyoming': 'WY', 'Tennessee': 'TN', 'Arizona': 'AZ',
    'Iowa': 'IA', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT',
    'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 'Montana': 'MT',
    'California': 'CA', 'Massachusetts': 'MA', 'West Virginia': 'WV',
    'South Carolina': 'SC', 'New Hampshire': 'NH', 'Wisconsin': 'WI',
    'Vermont': 'VT', 'Georgia': 'GA', 'North Dakota': 'ND',
    'Pennsylvania': 'PA', 'Florida': 'FL', 'Alaska': 'AK', 'Kentucky': 'KY',
    'Hawaii': 'HI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH',
    'Alabama': 'AL', 'Rhode Island': 'RI', 'South Dakota': 'SD',
    'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA',
    'North Carolina': 'NC', 'New York': 'NY', 'Texas': 'TX',
    'Nevada': 'NV', 'Maine': 'ME'}
df['state_code'] = df['State'].apply(lambda x: state_codes[x])

df = df.groupby(['State', 'State ANSI', 'Affected by', 'Year', 'state_code'])[['Percent of Colonies Impacted']].mean()
df.reset_index(inplace=True)

# ------------------------------------------------------------------------

input_types = ['number', 'password', 'text', 'tel', 'email', 'url', 'search', 'hidden']

app.layout = html.Div([
    html.Div([
        dcc.Input(
            id='my_{}'.format(x),
            type=x,
            placeholder="insert {}".format(x),  # A hint to the user of what can be entered in the control
            debounce=True,                      # Changes to input are sent to Dash server only on enter or losing focus
            min=2015, max=2019, step=1,         # Ranges of numeric value. Step refers to increments
            minLength=0, maxLength=50,          # Ranges for character length inside input box
            autoComplete='on',
            disabled=False,                     # Disable input box
            readOnly=False,                     # Make input box read only
            required=False,                     # Require user to insert something into input box
            size="20",                          # Number of characters that will be visible inside box
            # style={'':''}                     # Define styles for dropdown (Dropdown video: 13:05)
            # className='',                     # Define style from separate CSS document (Dropdown video: 13:05)
            # persistence='',                   # Stores user's dropdown changes in memory (Dropdown video: 16:20)
            # persistence_type='',              # Stores user's dropdown changes in memory (Dropdown video: 16:20)
        ) for x in input_types
    ]),

    html.Br(),

    dcc.Graph(id="mymap"),

])


# ------------------------------------------------------------------------
@app.callback(
    Output(component_id='mymap', component_property='figure'),
    [Input(component_id='my_{}'.format(x), component_property='value')
     for x in input_types
     ],
)
def update_graph(num_year, pwd_state, txt_state, tel_state, email_, url_, search_disease, hidden_input):
    if tel_state:
        tel_state = tel_state
    elif tel_state is None or len(tel_state) == 0:
        tel_state = 10

    if search_disease:
        search_disease = search_disease
    elif search_disease is None or len(search_disease) == 0:
        search_disease = "Disease"

    dff = df.copy()

    dff = dff[dff['Year'] == num_year]
    dff = dff[dff['State'] != pwd_state]
    dff = dff[dff['State'] != txt_state]
    dff = dff[dff['State ANSI'] != int(tel_state)]
    dff = dff[dff['Affected by'] == search_disease]

    print("number: " + str(num_year))
    print("password: " + str(pwd_state))
    print("text: " + str(txt_state))
    print("telephone: " + str(tel_state))
    print("hidden: " + str(hidden_input))
    print("email: " + str(email_))
    print("url: " + str(url_))
    print("search: " + str(search_disease))
    print("---------------")

    beemap = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Percent of Colonies Impacted',
        hover_data=['State', 'Percent of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title='Bees affected by {}'.format(search_disease),
        template='plotly_dark',
        labels={'Percent of Colonies Impacted': '% of Bee Colonies'}
    )

    beemap.update_layout(title={'x': 0.5, 'xanchor': 'center', 'font': {'size': 20}})

    beemap.update_traces(hovertemplate=
                         "<b>%{customdata[0]}</b><br><br>" +
                         "Percent of Colonies Impacted: %{customdata[1]:.3s}" +
                         "<extra></extra>",
                         )
    return (beemap)

# ------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
