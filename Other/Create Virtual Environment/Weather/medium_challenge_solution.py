# Solution to update your web app with city of New Delhi, and show only temperature and observation time
# changes made to line 4,8

categories=["observation_time","temperature"]

def update_weather():
    weather_requests = requests.get(
        "http://api.weatherstack.com/current?access_key=88ffb416536794b25ea52f6e9a6c6c28&query=New%20Delhi"
    )
    json_data = weather_requests.json()
    df = pd.DataFrame(json_data)
    return([
            html.Table(
                className='table-weather',
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    name+": "+str(data)
                                ]
                            )
                        ]
                    )
            for name,data in zip(categories,df['current'][categories])
        ])
    ])
