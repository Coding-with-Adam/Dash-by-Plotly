import os
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
from google.oauth2 import service_account
import pandas_gbq
credentials = service_account.Credentials.from_service_account_file('C:/Users/13474/heroku/My_Dash/Youtube/Sandbox/hattie/assets\mynewproject.json')

new_date = '2021-01-01'

df_sql = f"""SELECT 
date(creation_date) as creation_date,
count(distinct id) as num_comments 
FROM `bigquery-public-data.stackoverflow.comments`
where text like '%python%'
and date(creation_date)>='{new_date}'
group by 1
"""
project_id = 'arboreal-totem-307806'
df= pd.read_gbq(df_sql, project_id=project_id, dialect='standard', credentials=credentials)
print(df.head())
