import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro

gapminder = px.data.gapminder().query("year == 2007")
df = px.data.iris()

page1 = vm.Page(
    title="Page 1",
    components=[
        vm.Card(text="""This data app will explore the consequences of..."""),
        vm.Graph(id="scatter_chart", figure=px.scatter(df, x="sepal_length", y="petal_width", color="species")),
        vm.Graph(id="hist_chart", figure=px.histogram(df, x="sepal_width", color="species")),
    ],
    controls=[
        vm.Filter(column="species", selector=vm.Dropdown(value=["ALL"])),
    ],
)


page2 = vm.Page(
    title="Page 2",
    path="world-order",
    components=[
        vm.Graph(
            id="sunburst", figure=px.sunburst(gapminder, path=["continent", "country"], values="pop", color="lifeExp")
        )
    ],
    controls=[
        vm.Filter(column="continent", targets=["sunburst"]),
        vm.Parameter(targets=["sunburst.color"], selector=vm.RadioItems(options=["lifeExp", "pop"], title="Color")),
    ],
)

dashboard = vm.Dashboard(pages=[page1, page2])

Vizro().build(dashboard).run()
