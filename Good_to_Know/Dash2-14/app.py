from dash import Dash, Input, html, dcc, page_container
import plotly.express as px
df = px.data.iris().to_dict()

app = Dash(
   __name__,
   use_pages=True,
   routing_callback_inputs={
       # The language will be passed as a keyword argument to pages' layout functions
       "language_chosen": Input("language", "value"),
       "stored_data": Input("our-data", "data")
   },
)
app.layout = html.Div(
   [
       html.Div(
           [
               "My app",
               html.Div(
                   [
                       dcc.Link("Home", href="/"),
                       dcc.Link("Page 1", href="/page-1"),
                       dcc.Dropdown(
                           id="language",
                           options=[
                               {"label": "English", "value": "en"},
                               {"label": "Français", "value": "fr"},
                           ],
                           value="en",
                           clearable=False
                       ),
                       dcc.Store(data=df, id="our-data")
                   ],
                   style={"marginLeft": "auto", "display": "flex", "gap": 10}
               )
           ],
           style={"background": "#CCC", "padding": 10, "marginBottom": 20, "display": "flex"},
       ),
       page_container,
   ]
)

if __name__ == '__main__':
    app.run(debug=True)
