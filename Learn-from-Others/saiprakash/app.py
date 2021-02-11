import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd

#Initialize the dash app
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

server=app.server


center={
  'display': 'block',
  'width': '50%',
  'margin-left':'auto',
  'margin-right':'auto',
  'height': '40%'
}


tab_style = {
    'borderBottom': '1px solid #212F3C',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #212F3C',
    'borderBottom': '1px solid #212F3C',
    'backgroundColor': '#F7DC6F',
    #F1C40F',
    'color': 'black',
    'padding': '6px',
    'fontWeight':'bold'
}


""" 1. Data Cleaning"""

#Load the data from multiple sheets of provided excel sheet
df_2019=pd.read_excel("Socialgood.xlsx",'2019',index_col=0)
df_2018=pd.read_excel("Socialgood.xlsx",'2018',index_col=0)


#Transpose the data
df_2019=df_2019.T
df_2018=df_2018.T


#Reset Index
df_2019=df_2019.reset_index()
df_2018=df_2018.reset_index()


#Rename Columns
df_2019=df_2019.rename(columns={'index':'African Country'})
df_2018=df_2018.rename(columns={'index':'African Country'})


#Replacing the duplicate values with the actual names

df_2019['African Country']=df_2019['African Country'].replace(['Benin.1','Benin.2','Benin.3','Benin.4','Benin.5'],'Benin')
df_2019['African Country']=df_2019['African Country'].replace(['Burkina Faso''Burkina Faso.1','Burkina Faso.2','Burkina Faso.3'],'Burkina_Faso')
df_2019['African Country']=df_2019['African Country'].replace(['Ivory Coast.1','Ivory Coast'],'Ivory_Coast')
#df_2019['African Country']=df_2019['African Country'].replace(['Burkina Faso.1','Burkina Faso.2','Burkina Faso.3'],'Burkina Faso')
#df_2019['African Country']=df_2019['African Country'].replace('Ivory Coast.1','Ivory Coast')
df_2019['African Country']=df_2019['African Country'].replace(['Mali.1','Mali.2','Mali.3'],'Mali')
df_2019['African Country']=df_2019['African Country'].replace(['Central African Republic.1','Central African Republic'],'Central_African_Republic')
df_2019['African Country']=df_2019['African Country'].replace('Togo.1','Togo')
df_2019['African Country']=df_2019['African Country'].replace('Guinea-Conakry','Guinea_Conakry')
df_2019['African Country']=df_2019['African Country'].replace('Democratic Republic of the Congo','Democratic_Republic_of_the_Congo')



#Replacing the duplicate values with the actual names
df_2018['African Country']=df_2018['African Country'].replace(['Benin.1','Benin.2','Benin.3','Benin.4','Benin.5'],'Benin')
df_2018['African Country']=df_2018['African Country'].replace(['Burkina Faso''Burkina Faso.1','Burkina Faso.2','Burkina Faso.3'],'Burkina_Faso')
df_2018['African Country']=df_2018['African Country'].replace(['Ivory Coast.1','Ivory Coast'],'Ivory_Coast')
#df_2018['African Country']=df_2018['African Country'].replace(['Burkina Faso.1','Burkina Faso.2','Burkina Faso.3'],'Burkina Faso')
#df_2018['African Country']=df_2018['African Country'].replace('Ivory Coast.1','Ivory Coast')
df_2018['African Country']=df_2018['African Country'].replace(['Mali.1','Mali.2','Mali.3'],'Mali')
df_2018['African Country']=df_2018['African Country'].replace(['Central African Republic.1','Central African Republic'],'Central_African_Republic')
df_2018['African Country']=df_2018['African Country'].replace('Togo.1','Togo')
df_2018['African Country']=df_2018['African Country'].replace('Guinea-Conakry','Guinea_Conakry')
df_2018['African Country']=df_2018['African Country'].replace('Democratic Republic of the Congo','Democratic_Republic_of_the_Congo')


#Getting the Project Counts for each country in 2019
project_count_2019=pd.DataFrame(columns=['Country','Project Count'])
for i in df_2019['African Country'].unique():
    new_df_2019=df_2019[df_2019['African Country']==i]
    x=len(new_df_2019['Project title'].unique())
    project_count_2019=project_count_2019.append({'Country':i,'Project Count':x},ignore_index=True)


#Getting the Project Counts for each country in 2018
project_count_2018=pd.DataFrame(columns=['Country','Project Count'])
for i in df_2018['African Country'].unique():
    new_df_2018=df_2018[df_2018['African Country']==i]
    x=len(new_df_2018['Project title'].unique())
    project_count_2018=project_count_2018.append({'Country':i,'Project Count':x},ignore_index=True)


#Getting the Project Category for each country in 2019
category_count_2019=pd.DataFrame(columns=['Country','Category Name','Category Count'])
for i in df_2019['African Country'].unique():
    new_df_2019=df_2019[df_2019['African Country']==i]
    x=len(new_df_2019['Axis of intervention'].unique())
    category_name=new_df_2019['Axis of intervention'].unique()
    category_count_2019=category_count_2019.append({'Country':i,'Category Name':category_name,'Category Count':x},ignore_index=True)


#Getting the Project Category for each country in 2018
category_count_2018=pd.DataFrame(columns=['Country','Category Name','Category Count'])
for i in df_2018['African Country'].unique():
    new_df_2018=df_2018[df_2018['African Country']==i]
    x=len(new_df_2018['Axis of intervention'].unique())
    category_name=new_df_2018['Axis of intervention'].unique()
    category_count_2018=category_count_2018.append({'Country':i,'Category Name':category_name,'Category Count':x},ignore_index=True)

#Getting the Project names and each project information for all countries for Tabs in Modal for year 2018
countries=['Benin', 'Burkina_Faso', 'Ivory_Coast', 'Guinea_Conakry',
           'Madagascar', 'Mali', 'Central_African_Republic',
           'Democratic_Republic_of_the_Congo', 'Togo']
grouped_country=df_2018.groupby('African Country')
for i in countries:
    globals()['project_group_2018_{}'.format(i)]=grouped_country.get_group(i)
    globals()['project_name_2018_{}'.format(i)]=[]
    globals()['category_name_2018_{}'.format(i)]=[]
    globals()['Direct_Benefits_2018_{}'.format(i)]=[]
    globals()['Indirect_Benefits_2018_{}'.format(i)]=[]
    globals()['Region_2018_{}'.format(i)]=[]
    globals()['Local_partner_2018_{}'.format(i)]=[]
    globals()['project_share_2018_{}'.format(i)]=[]
    globals()['country_share_2018_{}'.format(i)]=[]
    globals()['country_budget_2018_{}'.format(i)]=[]
    for j in globals()['project_group_2018_{}'.format(i)]['Project title']:
        globals()['project_name_2018_{}'.format(i)].append(j)
    for k in globals()['project_group_2018_{}'.format(i)]['Axis of intervention']:
        globals()['category_name_2018_{}'.format(i)].append(k)
    for l in globals()['project_group_2018_{}'.format(i)]['Direct beneficiaries']:
        globals()['Direct_Benefits_2018_{}'.format(i)].append(l)
    for m in globals()['project_group_2018_{}'.format(i)]['Indirect beneficiaries']:
        globals()['Indirect_Benefits_2018_{}'.format(i)].append(m)
    for n in globals()['project_group_2018_{}'.format(i)]['Region']:
        globals()['Region_2018_{}'.format(i)].append(n)
    for o in globals()['project_group_2018_{}'.format(i)]['Local partner']:
        globals()['Local_partner_2018_{}'.format(i)].append(o)
    for p in globals()['project_group_2018_{}'.format(i)]['Project share % out of all budget']:
        globals()['project_share_2018_{}'.format(i)].append(p)
    for q in globals()['project_group_2018_{}'.format(i)]['Country share % out of all budget']:
        globals()['country_share_2018_{}'.format(i)].append(q)
    for r in globals()['project_group_2018_{}'.format(i)]['Voted 2018 country budget €']:
        globals()['country_budget_2018_{}'.format(i)].append(r)


#Getting the Project names and each project information for all countries for Tabs in Modal for year 2019
countries=['Benin', 'Burkina_Faso', 'Ivory_Coast', 'Guinea_Conakry',
           'Madagascar', 'Mali', 'Central_African_Republic',
           'Democratic_Republic_of_the_Congo', 'Togo']
grouped_country=df_2019.groupby('African Country')
for i in countries:
    globals()['project_group_{}'.format(i)]=grouped_country.get_group(i)
    globals()['project_name_{}'.format(i)]=[]
    globals()['category_name_{}'.format(i)]=[]
    globals()['Direct_Benefits_{}'.format(i)]=[]
    globals()['Indirect_Benefits_{}'.format(i)]=[]
    globals()['Region_{}'.format(i)]=[]
    globals()['Local_partner_{}'.format(i)]=[]
    globals()['project_share_{}'.format(i)]=[]
    globals()['country_share_{}'.format(i)]=[]
    globals()['country_budget_{}'.format(i)]=[]
    for j in globals()['project_group_{}'.format(i)]['Project title']:
        globals()['project_name_{}'.format(i)].append(j)
    for k in globals()['project_group_{}'.format(i)]['Axis of intervention']:
        globals()['category_name_{}'.format(i)].append(k)
    for l in globals()['project_group_{}'.format(i)]['Direct beneficiaries']:
        globals()['Direct_Benefits_{}'.format(i)].append(l)
    for m in globals()['project_group_{}'.format(i)]['Indirect beneficiaries']:
        globals()['Indirect_Benefits_{}'.format(i)].append(m)
    for n in globals()['project_group_{}'.format(i)]['Region']:
        globals()['Region_{}'.format(i)].append(n)
    for o in globals()['project_group_{}'.format(i)]['Local partner']:
        globals()['Local_partner_{}'.format(i)].append(o)
    for p in globals()['project_group_{}'.format(i)]['Project share % out of all budget']:
        globals()['project_share_{}'.format(i)].append(p)
    for q in globals()['project_group_{}'.format(i)]['Country share % out of all budget']:
        globals()['country_share_{}'.format(i)].append(q)
    for r in globals()['project_group_{}'.format(i)]['Voted 2019 country budget €']:
        globals()['country_budget_{}'.format(i)].append(r)


#Building a modals for year 2018
modal_benin_2018=html.Div([
                dbc.Button("Click for Insights",id="open_benin_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[0]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-benin_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-1_2018",
                                        label=project_name_2018_Benin[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: More than 50 children benefited from psychological and health care!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-2_2018",
                                        label=project_name_2018_Benin[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 27 apprentices out of 28 (14 in sewing and 14 in building work) completed their training successfully and obtained their professionnal qualification certificate!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-3_2018",
                                        label=project_name_2018_Benin[2],
                                        value="tab-3",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 32 awareness raising sessions and 192 educational talks were organised in the 16 villages within the area!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project3_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-4_2018",
                                        label=project_name_2018_Benin[3],
                                        value="tab-4",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_2018_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_2018_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Result: Hospitalisation at the center in Allada was required for 22 of the positively screened buruli ulcer cases!!",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project4_2018',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-5_2018",
                                        label=project_name_2018_Benin[4],
                                        value="tab-5",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_2018_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_2018_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Result: 127 women gave birth in the right conditions!!",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-02:3302 people were sensitized about HIV/AIDS",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-03:209 malnourished children were cared for",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-04:1206 children under one year old were vaccinated in Zè ",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-05:1 new healthcare center in Lokpodji for 35.000 inhabitants in the area",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project5_2018',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'
                                               }
                                        ),

                                    ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-6_2018",
                                        label=project_name_2018_Benin[5],
                                        value="tab-6",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_2018_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_2018_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Result:See Togo",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project6_2018',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    )
                                ]
                        )
                ],
                is_open=False,
                id="modal_benin_2018",
                size="xl",
                backdrop=True,
                scrollable=True,
                centered=True,
                fade=True
                )
])

modal_burkina_faso_2018=html.Div([
                dbc.Button("Click for Insights",id="open_burkina_faso_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[1]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-Burkina_Faso_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-7_2018",
                                        label=project_name_2018_Burkina_Faso[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 40 young people were taken care of and trained at the center jeunes pris en charge et formés au centre",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Burkina_Faso1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-8_2018",
                                        label=project_name_2018_Burkina_Faso[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 53 villages benefited from the awareness raising campaigns and reached 7.362 people!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Burkina_Faso2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_burkina_faso_2018",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_ivory_coast_2018=html.Div([
                dbc.Button("Click for Insights",id="open_ivory_coast_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[2]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-ivory-coast_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-9_2018",
                                        label=project_name_2018_Ivory_Coast[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 30 girls benefited from adapted care at the center, from a medical, nutritional, sanitary, psychological and educational perspective!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Ivory_Coast1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-10_2018",
                                        label=project_name_2018_Ivory_Coast[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 110 young people benefited from adapted care at the center, from a medical, nutritional, sanitary, psychological and educational perspective!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Ivory_Coast2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_ivory_coast_2018",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_guinea_conakry_2018=html.Div([
                dbc.Button("Click for Insights",id="open_guinea_conakry_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[3]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-guinea-conakry_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-11_2018",
                                        label=project_name_2018_Guinea_Conakry[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 70 community health agents were trained about understanding, preventing and treating the Buruli ulcer!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Guinea_Conakry1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Guinea_Conakry_2018",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )

                                        ])

modal_madagascar_2018=html.Div([
                dbc.Button("Click for Insights",id="open_madagascar_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[4] + str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-madagascar_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-12_2018",
                                        label=project_name_2018_Madagascar[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 16 mass check-ups and 59 awareness raising activities were organised",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Madagascar1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Madagascar_2018",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )
])

modal_mali_2018=html.Div([
                dbc.Button("Click for Insights",id="open_mali_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[5]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-mali_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-13_2018",
                                        label=project_name_2018_Mali[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 398 educational talks and 70 information and awareness sessions, led by former excisers",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-14_2018",
                                        label=project_name_2018_Mali[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 113.850 people were sensitized to the good hygiene pratices, to the importance of medical follow-up and family planning!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-15_2018",
                                        label=project_name_2018_Mali[2],
                                        value="tab-3",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 88 street rounds were realised enabling to identify 378 children!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project3_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-16_2018",
                                        label=project_name_2018_Mali[3],
                                        value="tab-4",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_2018_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_2018_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Result: 2 new centers were equipped in Safolo and Tassona!!",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Mali_project4_2018',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Mali_2018",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_car_2018=html.Div([
                dbc.Button("Click for Insights",id="open_car_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[6]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-car_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-17_2018",
                                        label=project_name_2018_Central_African_Republic[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 1,553 Women received parental checks and 4991 Akas were vaccined",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Central_African_Republic1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-18_2018",
                                        label=project_name_2018_Central_African_Republic[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 38 health structures supported by the project!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Central_African_Republic2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Central_African_Republic_2018",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_drc_2018=html.Div([
                dbc.Button("Click for Insights",id="open_drc_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[7] + str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-drc_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-19_2018",
                                        label=project_name_2018_Democratic_Republic_of_the_Congo[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 8,362 patients had a check-up at the polyclinic!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Democratic_Republic_of_the_Congo1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Democratic_Republic_of_the_Congo_2018",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )
])

modal_togo_2018=html.Div([
                dbc.Button("Click for Insights",id="open_togo_2018",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[8]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-togo_2018",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-20_2018",
                                        label=project_name_2018_Togo[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: Since 2011, more than 3200 coordinators were installed in 280 schools, to benefit around 40,000 children!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Togo1_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-21_2018",
                                        label=project_name_2018_Togo[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_2018_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_2018_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_2018_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_2018_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_2018_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 2 new peripheral care units made operational!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Togo2_2018',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Togo_2018",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

#Building a modals for year 2019
modal_benin=html.Div([
                dbc.Button("Click for Insights",id="open_benin",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[0]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-benin",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-1",
                                        label=project_name_Benin[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 80 handicaped or vulnerable children were cared for",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-2",
                                        label=project_name_Benin[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result:49 students from 16 to 23 years old undertook their training: 17 in woodworking (4 girls), 16 in masonry (1 girl), 16 in sewing (4 boys)",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-3",
                                        label=project_name_Benin[2],
                                        value="tab-3",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Result:133 children from 3 to 16 years old, including 41 girls, were cared for",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Benin_project3',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-4",
                                        label=project_name_Benin[3],
                                        value="tab-4",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Result:174 new patients were treated during the 1 trimester",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project4',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-5",
                                        label=project_name_Benin[4],
                                        value="tab-5",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[4]),className="font-weight-bold"),
                                        dbc.ModalBody("Result-01:169 women gave birth in the right conditions",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-02:3302 people were sensitized about HIV/AIDS",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-03:209 malnourished children were cared for",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-04:1206 children under one year old were vaccinated in Zè ",className="font-weight-bold"),
                                        #dbc.ModalBody("Result-05:1 new healthcare center in Lokpodji for 35.000 inhabitants in the area",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project5',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center',
                                               'overflow-y':'scroll'}
                                        ),

                                    ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-6",
                                        label=project_name_Benin[5],
                                        value="tab-6",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Benin[5]),className="font-weight-bold"),
                                        dbc.ModalBody("Result:See Togo",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Benin_project6',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    )
                                ]
                        )
                ],
                className="modal-dialog-scrollable",
                is_open=False,
                id="modal_benin",
                size="xl",
                backdrop=True,
                scrollable=True,
                centered=True,
                fade=True
                )
])

modal_burkina_faso=html.Div([
                dbc.Button("Click for Insights",id="open_burkina_faso",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[1]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-Burkina_Faso",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-7",
                                        label=project_name_Burkina_Faso[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Burkina_Faso[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 36 young people in the center completed their training",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Burkina_Faso1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-8",
                                        label=project_name_Burkina_Faso[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Burkina_Faso[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 79 women suffering from the consequences of FGM were medically and psychologically cared for",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Burkina_Faso2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_burkina_faso",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_ivory_coast=html.Div([
                dbc.Button("Click for Insights",id="open_ivory_coast",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[2]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-ivory-coast",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-9",
                                        label=project_name_Ivory_Coast[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Ivory_Coast[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 41 girls followed a training, including 15 teenage-mothers",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Ivory_Coast1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-10",
                                        label=project_name_Ivory_Coast[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Ivory_Coast[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 77 children from 6 to 22 years old welcomed to the Maison de l'Enfance de Bouaké",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Ivory_Coast2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_ivory_coast",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_guinea_conakry=html.Div([
                dbc.Button("Click for Insights",id="open_guinea_conakry",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[3]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-guinea-conakry",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-11",
                                        label=project_name_Guinea_Conakry[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Guinea_Conakry[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 6000 people sensitized during the mass awareness-raising campaigns",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Guinea_Conakry1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Guinea_Conakry",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )

                                        ])

modal_madagascar=html.Div([
                dbc.Button("Click for Insights",id="open_madagascar",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[4] + str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-madagascar",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-12",
                                        label=project_name_Madagascar[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Madagascar[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 2516 medical checks were registered",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Madagascar1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Madagascar",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )
])

modal_mali=html.Div([
                dbc.Button("Click for Insights",id="open_mali",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[5]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-mali",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-13",
                                        label=project_name_Mali[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Mali[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 17,308 people were reached by the activities within this project, amongst which 5180 men so one third of the people",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-14",
                                        label=project_name_Mali[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Mali[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 7000 malians from Diouman have access to drinking water",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-15",
                                        label=project_name_Mali[2],
                                        value="tab-3",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Mali[2]),className="font-weight-bold"),
                                            dbc.ModalBody("Result:90 street rounds were done!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Mali_project3',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    dcc.Tab(
                                        id="project-16",
                                        label=project_name_Mali[3],
                                        value="tab-4",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                        dbc.ModalBody("Local Partner: "+str(Local_partner_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Category: " +str(category_name_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Region: "+str(Region_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Mali[3]),className="font-weight-bold"),
                                        dbc.ModalBody("Result: 27555 medical checks, 43603 vaccinations, 2896 baby deliveries are successfully completed!!",className="font-weight-bold"),
                                        html.Div([
                                        dcc.Graph(
                                        id='Mali_project4',
                                        figure={},
                                        style={'padding-left':'60px',
                                               'padding-bottom':'10px',
                                               'align':'center'}
                                        ),

                                    ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Mali",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_car=html.Div([
                dbc.Button("Click for Insights",id="open_car",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[6]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-car",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-17",
                                        label=project_name_Central_African_Republic[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Central_African_Republic[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 3309 baby deliveries including 63 C-sections.",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Central_African_Republic1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-18",
                                        label=project_name_Central_African_Republic[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Central_African_Republic[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 38 healthcare structures supported!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Central_African_Republic2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Central_African_Republic",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])

modal_drc=html.Div([
                dbc.Button("Click for Insights",id="open_drc",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[7] + str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-drc",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-19",
                                        label=project_name_Democratic_Republic_of_the_Congo[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Democratic_Republic_of_the_Congo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 5615 patients seen for medical checks!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Democratic_Republic_of_the_Congo1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),
                                            ])
                                            ])
                                            )])
                                            ],
                                            className="modal-dialog-scrollable",
                                            is_open=False,
                                            id="modal_Democratic_Republic_of_the_Congo",
                                            size="xl",
                                            backdrop=True,
                                            scrollable=True,
                                            centered=True,
                                            fade=True
                                            )
])

modal_togo=html.Div([
                dbc.Button("Click for Insights",id="open_togo",color='primary',outline=True),
                dbc.Modal([
                        dbc.ModalHeader(countries[8]+ str("-Projects list")),
                        dcc.Tabs(
                                id="tabs-togo",
                                value="data-view",
                                children=[
                                    dcc.Tab(
                                        id="project-20",
                                        label=project_name_Togo[0],
                                        value="tab-1",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Togo[0]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: Since 2011, more 3200 computers were installed in 280 schools to benefit a total of 40000 children!!",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Togo1',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                    ])),
                                    dcc.Tab(
                                        id="project-21",
                                        label=project_name_Togo[1],
                                        value="tab-2",
                                        style=tab_style,
                                        selected_style=tab_selected_style,
                                        children=html.Div([
                                            dbc.ModalBody("Local Partner: "+str(Local_partner_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Category: " +str(category_name_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Region: "+str(Region_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Direct Benefit: "+str(Direct_Benefits_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("In-direct Benefit: "+str(Indirect_Benefits_Togo[1]),className="font-weight-bold"),
                                            dbc.ModalBody("Result: 210young mothers gave birth in the right conditions and benefited with a newborn kit",className="font-weight-bold"),
                                            html.Div([
                                            dcc.Graph(
                                            id='Togo2',
                                            figure={},
                                            style={'padding-left':'60px',
                                                   'padding-bottom':'10px',
                                                   'align':'center'}
                                            ),

                                        ])
                                        ])
                                    ),
                                    ])
                                    ],
                                    className="modal-dialog-scrollable",
                                    is_open=False,
                                    id="modal_Togo",
                                    size="xl",
                                    backdrop=True,
                                    scrollable=True,
                                    centered=True,
                                    fade=True
                                    )
])


#Model Selection function for year 2018

def modal_selection_2018(i):
    #Extracting the Project Count and Caetgroy names for each country
    countries=['Benin', 'Burkina_Faso', 'Ivory_Coast', 'Guinea_Conakry',
           'Madagascar', 'Mali', 'Central_African_Republic',
           'Democratic_Republic_of_the_Congo', 'Togo']
    if (i==countries[0]):
        return modal_benin_2018
    elif (i==countries[1]):
        return modal_burkina_faso_2018
    elif (i==countries[2]):
        return modal_ivory_coast_2018
    elif (i==countries[3]):
        return modal_guinea_conakry_2018
    elif (i==countries[4]):
        return modal_madagascar_2018
    elif (i==countries[5]):
        return modal_mali_2018
    elif (i==countries[6]):
        return modal_car_2018
    elif (i==countries[7]):
        return modal_drc_2018
    else:
        return modal_togo_2018

#Model Selection function for year 2019
def modal_selection(i):
    #Extracting the Project Count and Caetgroy names for each country
    countries=['Benin', 'Burkina_Faso', 'Ivory_Coast', 'Guinea_Conakry',
           'Madagascar', 'Mali', 'Central_African_Republic',
           'Democratic_Republic_of_the_Congo', 'Togo']
    if (i==countries[0]):
        return modal_benin
    elif (i==countries[1]):
        return modal_burkina_faso
    elif (i==countries[2]):
        return modal_ivory_coast
    elif (i==countries[3]):
        return modal_guinea_conakry
    elif (i==countries[4]):
        return modal_madagascar
    elif (i==countries[5]):
        return modal_mali
    elif (i==countries[6]):
        return modal_car
    elif (i==countries[7]):
        return modal_drc
    else:
        return modal_togo



#Card creations for app layout for year 2018
for i in df_2018['African Country'].unique():
    a=pd.Series()
    a=project_count_2018[project_count_2018['Country']==i]
    b=pd.Series()
    b=category_count_2018[category_count_2018['Country']==i]
    globals()['card_content_2018_{}'.format(i)]=[
                dbc.CardHeader(i,className='card-title'),
                dbc.CardBody(
                [
                html.H5("Project Count: " +str(a['Project Count'].item()), className="card-title"),
                html.P(
                "The Categories covered in this year: " +str(b['Category Name'].item()),
                className="card-text",
                ),
                modal_selection_2018(i)
                ]
                ),
                ]

#Card creations for app layout for year 2019
for i in df_2019['African Country'].unique():
    a=pd.Series()
    a=project_count_2019[project_count_2019['Country']==i]
    b=pd.Series()
    b=category_count_2019[category_count_2019['Country']==i]
    globals()['card_content_{}'.format(i)]=[
                dbc.CardHeader(i),
                dbc.CardBody(
                [
                html.H5("Project Count: " +str(a['Project Count'].item()), className="card-title"),
                html.P(
                "The Categories covered in this year: " +str(b['Category Name'].item()),
                className="card-text",
                ),
                modal_selection(i)
                ]
                ),
                ]

#Creating a graph card for year 2018
graphcard_2018=html.Div([
                html.H4("2018 Project Results",className='text-center text-primary mb-4'),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_2018_Benin,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Burkina_Faso,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Ivory_Coast,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_2018_Guinea_Conakry,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Madagascar,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Mali,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_2018_Central_African_Republic,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Democratic_Republic_of_the_Congo,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_2018_Togo,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dcc.Markdown('''Developed by **A.V. Sai Prakash**''',className='text-right text-primary mb-4',style={'padding-right':'50px'})


])

#Creating a graph card for year df_2019
graphcard_2019=html.Div([
                html.H4("2019 Project Results",className='text-center text-primary mb-4'),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_Benin,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Burkina_Faso,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Ivory_Coast,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_Guinea_Conakry,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Madagascar,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Mali,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dbc.Row(
                        [
                        dbc.Col(dbc.Card(card_content_Central_African_Republic,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Democratic_Republic_of_the_Congo,color='light',inverse=True,outline=True),width=3),
                        dbc.Col(dbc.Card(card_content_Togo,color='light',inverse=True,outline=True),width=3)
                        ],
                        no_gutters=False,justify='around'
                ),
                html.Br(),
                dcc.Markdown('''Developed by **A.V. Sai Prakash**''',className='text-right text-primary mb-4',style={'padding-right':'50px'})
])


#Layout Section:dash_bootstrap
app.layout=html.Div([
                    dbc.Row([
                        dbc.Col(html.H1("Fondation Follereau Luxembourg (FFL)",
                                        className='text-center text-primary mb-4'), #Space has to be defined when mutliple parameters need to be assigned
                                        width=12)]),

                    html.Div(id="slideshow-container", children=[
                        html.Div(id="image"),
                        dcc.Interval(id='interval', interval=3000)
                    ],style={'padding-bottom':'10px'}),

                    html.Br(),

                    dbc.Row([
                        dbc.Col(html.H4("Select a Year to track the Project Achievements!!",
                                        className='text-center text-primary mb-4'), #Space has to be defined when mutliple parameters need to be assigned
                                        width=4),
                        dbc.Col([],width=0.1),
                        dbc.Col([dbc.Button("2018",id="2018",color='primary',outline=True)],width=1),
                        dbc.Col([],width=0.1),
                        dbc.Col([dbc.Button("2019",id="2019",color='primary',outline=True)

                        ],width=1)
                    ],style={'padding-left':'20px','padding-bottom':'5px'}),
                    #dbc.Row([
                    #        dbc.Col(
                    #        html.Label(['Year-Selection',dcc.Dropdown(id='mydpdn',multi=False,
                    #                    options=[{'label':2018,'value':2018},
                    #                             {'label':2019,'value':2019}],style={'padding-left':'5px'})]),width=4
                    #)]),
                    #html.Div(id='display-cards_2018',style={'padding-bottom':'20px'}),
                    html.Div(id='display-cards',style={'padding-bottom':'20px'})

                            #graphcard_2019),

])



################################################Callback for Slideshow#####################################
@app.callback(Output('image', 'children'),
              [Input('interval', 'n_intervals')])
def display_image(n):
    if n == None or n % 5 == 1:
        img = html.Img(src=app.get_asset_url('471B6384.JPG'),style=center)
    elif n % 5 == 2:
        img = html.Img(src=app.get_asset_url('2.JPG'),style=center)
    elif n % 5 == 3:
        img = html.Img(src=app.get_asset_url('FASO4192.JPG'),style=center)
    elif n % 5 == 4:
        img = html.Img(src=app.get_asset_url('3.JPG'),style=center)
    elif n % 5 == 0:
        img = html.Img(src=app.get_asset_url('5.JPG'),style=center)
    else:
        img = "None"
    return img


#################################################callback for year 2018##############################################
@app.callback(
Output("display-cards","children"),
[Input("2018","n_clicks"),
Input("2019","n_clicks")])

def main_function_1(n_clicks,n_clicks1):
    ctx=dash.callback_context
    if (n_clicks==0) & (n_clicks1==0):
        return ''
    else:
        x = ctx.triggered[0]['prop_id'].split('.')[0]
        if x == '2018':
            return graphcard_2018
        elif x =='2019':
            return graphcard_2019

#def update_output(value):
#    if (value==2019):
#        return graphcard_2019
#    else:
#        pass

"""callbacks for 2018"""
#Modal callback for Benin Country for 2019 data
@app.callback(
    Output("modal_benin_2018","is_open"),
    [Input("open_benin_2018","n_clicks")],
    [State("modal_benin_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

k=3

#Benin Card Table Callbacks insode Modal
@app.callback(
    Output("Benin_project1_2018","figure"),
    [Input("project-1_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[0]*100,k),round(country_share_2018_Benin[0]*100,k),country_budget_2018_Benin[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project2_2018","figure"),
    [Input("project-2_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[1]*100,k),round(country_share_2018_Benin[1]*100,k),country_budget_2018_Benin[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project3_2018","figure"),
    [Input("project-3_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[2]*100,k),round(country_share_2018_Benin[2]*100,k),country_budget_2018_Benin[2]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project4_2018","figure"),
    [Input("project-4_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[3]*100,k),round(country_share_2018_Benin[3]*100,k),country_budget_2018_Benin[3]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project5_2018","figure"),
    [Input("project-5_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[4]*100,k),round(country_share_2018_Benin[4]*100,k),country_budget_2018_Benin[4]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project6_2018","figure"),
    [Input("project-6_2018","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Benin[5]*100,k),round(country_share_2018_Benin[5]*100,k),country_budget_2018_Benin[5]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Burkina Faso Country for 2018 data
@app.callback(
    Output("modal_burkina_faso_2018","is_open"),
    [Input("open_burkina_faso_2018","n_clicks")],
    [State("modal_burkina_faso_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Burkina-Faso callbacks inside Modal
@app.callback(
    Output("Burkina_Faso1_2018","figure"),
    [Input("project-7_2018","children")]
)
def Burkina_Faso_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Burkina_Faso[0]*100,k),round(country_share_2018_Burkina_Faso[0]*100,k),country_budget_2018_Burkina_Faso[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Burkina_Faso2_2018","figure"),
    [Input("project-8_2018","children")]
)
def Burkina_Faso_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Burkina_Faso[1]*100,k),round(country_share_2018_Burkina_Faso[1]*100,k),country_budget_2018_Burkina_Faso[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Ivory Coast Country for 2018 data
@app.callback(
    Output("modal_ivory_coast_2018","is_open"),
    [Input("open_ivory_coast_2018","n_clicks")],
    [State("modal_ivory_coast_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Ivory Coast callbacks inside Modal
@app.callback(
    Output("Ivory_Coast1_2018","figure"),
    [Input("project-9_2018","children")]
)
def Ivory_Coast_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Ivory_Coast[0]*100,k),round(country_share_2018_Ivory_Coast[0]*100,k),country_budget_2018_Ivory_Coast[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Ivory_Coast2_2018","figure"),
    [Input("project-10_2018","children")]
)
def Ivory_Coast_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Ivory_Coast[1]*100,k),round(country_share_2018_Ivory_Coast[1]*100,k),country_budget_2018_Ivory_Coast[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Guinea_Conakry Country for 2019 data
@app.callback(
    Output("modal_Guinea_Conakry_2018","is_open"),
    [Input("open_guinea_conakry_2018","n_clicks")],
    [State("modal_Guinea_Conakry_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Guinea_Conakry callbacks inside Modal
@app.callback(
    Output("Guinea_Conakry1_2018","figure"),
    [Input("project-11_2018","children")]
)
def Guinea_Conakry_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Guinea_Conakry[0]*100,k),round(country_share_2018_Guinea_Conakry[0]*100,k),country_budget_2018_Guinea_Conakry[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Madagascar Country for 2018 data
@app.callback(
    Output("modal_Madagascar_2018","is_open"),
    [Input("open_madagascar_2018","n_clicks")],
    [State("modal_Madagascar_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Madagascar callbacks inside Modal
@app.callback(
    Output("Madagascar1_2018","figure"),
    [Input("project-12_2018","children")]
)
def Madagascar_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Madagascar[0]*100,k),round(country_share_2018_Madagascar[0]*100,k),country_budget_2018_Madagascar[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Mali Country for 2018 data
@app.callback(
    Output("modal_Mali_2018","is_open"),
    [Input("open_mali_2018","n_clicks")],
    [State("modal_Mali_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#Mali Card Table Callbacks insode Modal
@app.callback(
    Output("Mali_project1_2018","figure"),
    [Input("project-13_2018","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Mali[0]*100,k),round(country_share_2018_Mali[0]*100,k),country_budget_2018_Mali[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project2_2018","figure"),
    [Input("project-14_2018","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Mali[1]*100,k),round(country_share_2018_Mali[1]*100,k),country_budget_2018_Mali[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project3_2018","figure"),
    [Input("project-15_2018","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Mali[2]*100,k),round(country_share_2018_Mali[2]*100,k),country_budget_2018_Mali[2]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project4_2018","figure"),
    [Input("project-16_2018","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Mali[3]*100,k),round(country_share_2018_Mali[3]*100,k),country_budget_2018_Mali[3]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for CAR Country for 2018 data
@app.callback(
    Output("modal_Central_African_Republic_2018","is_open"),
    [Input("open_car_2018","n_clicks")],
    [State("modal_Central_African_Republic_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#car Card Table Callbacks insode Modal
@app.callback(
    Output("Central_African_Republic1_2018","figure"),
    [Input("project-17_2018","children")]
)
def car_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Central_African_Republic[0]*100,k),round(country_share_2018_Central_African_Republic[0]*100,k),country_budget_2018_Central_African_Republic[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Central_African_Republic2_2018","figure"),
    [Input("project-18_2018","children")]
)
def car_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Central_African_Republic[1]*100,k),round(country_share_2018_Central_African_Republic[1]*100,k),country_budget_2018_Central_African_Republic[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for drc Country for 2018 data
@app.callback(
    Output("modal_Democratic_Republic_of_the_Congo_2018","is_open"),
    [Input("open_drc_2018","n_clicks")],
    [State("modal_Democratic_Republic_of_the_Congo_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#drc Card Table Callbacks insode Modal
@app.callback(
    Output("Democratic_Republic_of_the_Congo1_2018","figure"),
    [Input("project-19_2018","children")]
)
def drc_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Democratic_Republic_of_the_Congo[0]*100,k),round(country_share_2018_Democratic_Republic_of_the_Congo[0]*100,k),country_budget_2018_Democratic_Republic_of_the_Congo[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Togo Country for 2018 data
@app.callback(
    Output("modal_Togo_2018","is_open"),
    [Input("open_togo_2018","n_clicks")],
    [State("modal_Togo_2018","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Togo callbacks inside Modal
@app.callback(
    Output("Togo1_2018","figure"),
    [Input("project-20_2018","children")]
)
def Togo_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Togo[0]*100,k),round(country_share_2018_Togo[0]*100,k),country_budget_2018_Togo[0]]]
    #colorscale = [[.0, '#F7DC6F']]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Togo2_2018","figure"),
    [Input("project-21_2018","children")]
)
def Togo_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_2018_Togo[1]*100,k),round(country_share_2018_Togo[1]*100,k),country_budget_2018_Togo[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig



#################################################callback for year 2019##############################################
#@app.callback(
#Output("display-cards","children"),
#[Input("2019","n_clicks")])

#def main_function_1(n_clicks):
#    if n_clicks is None:
#        pass
#    elif (n_clicks>=1):
#        return graphcard_2019

#def update_output(value):
#    if (value==2019):
#        return graphcard_2019
#    else:
#        pass

"""callbacks for 2019"""
#Modal callback for Benin Country for 2019 data
@app.callback(
    Output("modal_benin","is_open"),
    [Input("open_benin","n_clicks")],
    [State("modal_benin","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

k=3

#Benin Card Table Callbacks insode Modal
@app.callback(
    Output("Benin_project1","figure"),
    [Input("project-1","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[0]*100,k),round(country_share_Benin[0]*100,k),country_budget_Benin[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project2","figure"),
    [Input("project-2","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[1]*100,k),round(country_share_Benin[1]*100,k),country_budget_Benin[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project3","figure"),
    [Input("project-3","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[2]*100,k),round(country_share_Benin[2]*100,k),country_budget_Benin[2]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project4","figure"),
    [Input("project-4","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[3]*100,k),round(country_share_Benin[3]*100,k),country_budget_Benin[3]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project5","figure"),
    [Input("project-5","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[4]*100,k),round(country_share_Benin[4]*100,k),country_budget_Benin[4]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Benin_project6","figure"),
    [Input("project-6","children")]
)
def Benin_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Benin[5]*100,k),round(country_share_Benin[5]*100,k),country_budget_Benin[5]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Burkina Faso Country for 2019 data
@app.callback(
    Output("modal_burkina_faso","is_open"),
    [Input("open_burkina_faso","n_clicks")],
    [State("modal_burkina_faso","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Burkina-Faso callbacks inside Modal
@app.callback(
    Output("Burkina_Faso1","figure"),
    [Input("project-7","children")]
)
def Burkina_Faso_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Burkina_Faso[0]*100,k),round(country_share_Burkina_Faso[0]*100,k),country_budget_Burkina_Faso[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Burkina_Faso2","figure"),
    [Input("project-8","children")]
)
def Burkina_Faso_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Burkina_Faso[1]*100,k),round(country_share_Burkina_Faso[1]*100,k),country_budget_Burkina_Faso[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Ivory Coast Country for 2019 data
@app.callback(
    Output("modal_ivory_coast","is_open"),
    [Input("open_ivory_coast","n_clicks")],
    [State("modal_ivory_coast","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Ivory Coast callbacks inside Modal
@app.callback(
    Output("Ivory_Coast1","figure"),
    [Input("project-9","children")]
)
def Ivory_Coast_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Ivory_Coast[0]*100,k),round(country_share_Ivory_Coast[0]*100,k),country_budget_Ivory_Coast[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Ivory_Coast2","figure"),
    [Input("project-10","children")]
)
def Ivory_Coast_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Ivory_Coast[1]*100,k),round(country_share_Ivory_Coast[1]*100,k),country_budget_Ivory_Coast[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Guinea_Conakry Country for 2019 data
@app.callback(
    Output("modal_Guinea_Conakry","is_open"),
    [Input("open_guinea_conakry","n_clicks")],
    [State("modal_Guinea_Conakry","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Guinea_Conakry callbacks inside Modal
@app.callback(
    Output("Guinea_Conakry1","figure"),
    [Input("project-11","children")]
)
def Guinea_Conakry_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Guinea_Conakry[0]*100,k),round(country_share_Guinea_Conakry[0]*100,k),country_budget_Guinea_Conakry[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Madagascar Country for 2019 data
@app.callback(
    Output("modal_Madagascar","is_open"),
    [Input("open_madagascar","n_clicks")],
    [State("modal_Madagascar","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Madagascar callbacks inside Modal
@app.callback(
    Output("Madagascar1","figure"),
    [Input("project-12","children")]
)
def Madagascar_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Madagascar[0]*100,k),round(country_share_Madagascar[0]*100,k),country_budget_Madagascar[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Mali Country for 2019 data
@app.callback(
    Output("modal_Mali","is_open"),
    [Input("open_mali","n_clicks")],
    [State("modal_Mali","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#Mali Card Table Callbacks insode Modal
@app.callback(
    Output("Mali_project1","figure"),
    [Input("project-13","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Mali[0]*100,k),round(country_share_Mali[0]*100,k),country_budget_Mali[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project2","figure"),
    [Input("project-14","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Mali[1]*100,k),round(country_share_Mali[1]*100,k),country_budget_Mali[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project3","figure"),
    [Input("project-15","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Mali[2]*100,k),round(country_share_Mali[2]*100,k),country_budget_Mali[2]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Mali_project4","figure"),
    [Input("project-16","children")]
)
def Mali_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Mali[3]*100,k),round(country_share_Mali[3]*100,k),country_budget_Mali[3]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for CAR Country for 2019 data
@app.callback(
    Output("modal_Central_African_Republic","is_open"),
    [Input("open_car","n_clicks")],
    [State("modal_Central_African_Republic","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#car Card Table Callbacks insode Modal
@app.callback(
    Output("Central_African_Republic1","figure"),
    [Input("project-17","children")]
)
def car_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Central_African_Republic[0]*100,k),round(country_share_Central_African_Republic[0]*100,k),country_budget_Central_African_Republic[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Central_African_Republic2","figure"),
    [Input("project-18","children")]
)
def car_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Central_African_Republic[1]*100,k),round(country_share_Central_African_Republic[1]*100,k),country_budget_Central_African_Republic[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for drc Country for 2019 data
@app.callback(
    Output("modal_Democratic_Republic_of_the_Congo","is_open"),
    [Input("open_drc","n_clicks")],
    [State("modal_Democratic_Republic_of_the_Congo","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open

#drc Card Table Callbacks insode Modal
@app.callback(
    Output("Democratic_Republic_of_the_Congo1","figure"),
    [Input("project-19","children")]
)
def drc_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Democratic_Republic_of_the_Congo[0]*100,k),round(country_share_Democratic_Republic_of_the_Congo[0]*100,k),country_budget_Democratic_Republic_of_the_Congo[0]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

#Modal callback for Togo Country for 2019 data
@app.callback(
    Output("modal_Togo","is_open"),
    [Input("open_togo","n_clicks")],
    [State("modal_Togo","is_open")],
)
def toggle_modal(n1,is_open):
    if n1:
        return not is_open
    else:
        return is_open


# Togo callbacks inside Modal
@app.callback(
    Output("Togo1","figure"),
    [Input("project-20","children")]
)
def Togo_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Togo[0]*100,k),round(country_share_Togo[0]*100,k),country_budget_Togo[0]]]
    #colorscale = [[.0, '#F7DC6F']]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

@app.callback(
    Output("Togo2","figure"),
    [Input("project-21","children")]
)
def Togo_project_table(children):
    data_matrix= [['Project share %','Country share %','Country budget €'],
                [round(project_share_Togo[1]*100,k),round(country_share_Togo[1]*100,k),country_budget_Togo[1]]]
    fig = ff.create_table(data_matrix,height_constant=6)
    fig.layout.width=1000
    return fig

if __name__=='__main__':
    app.run_server(debug=False,dev_tools_hot_reload_interval=60000)
