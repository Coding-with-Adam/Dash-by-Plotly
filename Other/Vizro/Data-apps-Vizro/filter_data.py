import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm

df = px.data.iris()
print(df.head())

page = vm.Page(
    title="My first dashboard",
    components=[
        vm.Graph(id="scatter_chart", figure=px.scatter(df, x="sepal_length", y="petal_width", color="species")),
        vm.Graph(id="hist_chart", figure=px.histogram(df, x="sepal_width", color="species")),
    ],
    controls=[
        # filter the dataframe (df) of the histogram, by column sepal_width, using the dropdown
        vm.Filter(column="sepal_width", selector=vm.Dropdown(), targets=["hist_chart"]),
    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
