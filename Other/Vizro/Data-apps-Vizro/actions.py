import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.actions import filter_interaction

df_gapminder = px.data.gapminder().query("year == 2007")

dashboard = vm.Dashboard(
    pages=[
        vm.Page(
            title="Filter interaction",
            components=[
                vm.Graph(
                    id="bar_relation_2007",
                    figure=px.box(
                        df_gapminder,
                        x="continent",
                        y="lifeExp",
                        color="continent",
                        points="all",
                        custom_data=["continent"],
                    ),
                    # clicking the custom_data (continent) of box plot will filter (target)
                    # the dataframe (continent column) of gapminder_scatter graph
                    actions=[vm.Action(function=filter_interaction(targets=["gapminder_scatter"]))],
                ),
                vm.Graph(
                    id="gapminder_scatter",
                    figure=px.scatter(
                        df_gapminder,
                        x="gdpPercap",
                        y="lifeExp",
                        size="pop",
                        color="continent",
                    ),
                ),
            ],
        ),
    ]
)

Vizro().build(dashboard).run()
