import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm

df = px.data.iris()
dff = px.data.gapminder()

page = vm.Page(
    title="My first dashboard",
    components=[
        vm.Graph(id="scatter_chart", figure=px.scatter(df, x="sepal_length", y="petal_width", color="species")),
        vm.Graph(id="hist_chart", figure=px.histogram(dff, x="continent", y="gdpPercap", range_y=[0,5000000])),
    ],
    controls=[
        # use the dropown to update (target) the x attribute of the scatter chart
        # scatter chart attributes: https://plotly.com/python-api-reference/generated/plotly.express.scatter.html#plotly.express.scatter
        vm.Parameter(selector=vm.Dropdown(options=["sepal_length","petal_length"],
                                          multi=False,
                                          value="sepal_length",
                                          title="X axis"),
                     targets=["scatter_chart.x"]),
        # use the rangeSlider to update (target) the range_y attribute of the histogram
        # histogram attributes: https://plotly.com/python-api-reference/generated/plotly.express.histogram.html#plotly.express.histogram
        vm.Parameter(selector=vm.RangeSlider(min=0,
                                             max=9000000,
                                             value=[0,5000000],
                                             step=1000000,
                                             title="Y axis Range"),
                     targets=["hist_chart.range_y"])
    ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
