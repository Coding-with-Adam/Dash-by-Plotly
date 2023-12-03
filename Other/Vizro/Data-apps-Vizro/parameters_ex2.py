import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.tables import dash_data_table

df = px.data.gapminder().query("year == 2007")

page = vm.Page(
    title="Example of a Dash DataTable",
    components=[
        vm.Table(id="table", title="Dash DataTable", figure=dash_data_table(data_frame=df, editable=True)),
    ],
    controls=[
        vm.Parameter(selector=vm.Dropdown(options=[{"label":"True", "value":True},
                                                   {"label":"False", "value":False}],
                                          multi=False,
                                          value=True,
                                          title="Editable Cells"),
                     targets=["table.editable"]),
              ],
)
dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
