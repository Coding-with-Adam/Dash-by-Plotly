import dash
from dash import html, dcc, Input, Output
import dash_pannellum

app = dash.Dash(__name__)

tour_config = {
    "default": {
        "firstScene": "street A",
        "sceneFadeDuration": 1000,
    },
    "scenes": {
        "street A": {
            "title": "Street A",
            "hfov": 100,
            "pitch": -1,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "/assets/street-A.jpg",  # insert image into assets folder
            "autoLoad": True,  # Add this line to each scene
            "hotSpots": [
                {
                    "pitch": -2.1,
                    "yaw": 2,
                    "type": "scene",
                    "text": "Between street A & B",
                    "sceneId": "street A-B"
                }
            ]
        },
        "street A-B": {
            "title": "Between street A & B",
            "hfov": 100,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "/assets/street-AB.jpg",  # insert image into assets folder
            "autoLoad": True,  # Add this line to each scene
            "hotSpots": [
                {
                    "pitch": 0,
                    "yaw": -1,
                    "type": "scene",
                    "text": "Street B",
                    "sceneId": "street B",
                    "targetPitch": 0,
                    "targetYaw": 0,
                },
                {
                    "pitch": 180,
                    "yaw": -1,
                    "type": "scene",
                    "text": "Street A",
                    "sceneId": "street A",
                    "targetYaw": 180,
                    "targetPitch": 0,
                }
            ]
        },
        "street B": {
            "title": "Street B",
            "hfov": 100,
            "yaw": 0,
            "type": "equirectangular",
            "panorama": "/assets/street-B.jpg",  # insert image into assets folder
            "autoLoad": True,  # Add this line to each scene
            "hotSpots": [
                {
                    "pitch": 0,
                    "yaw": 180,
                    "type": "scene",
                    "text": "Between street A & B",
                    "sceneId": "street A-B",
                    "targetYaw": 180,
                    "targetPitch": 0
                }
            ]
        }
    }
}



app.layout = html.Div([
    html.H1("Harlem Tour Example"),
    dash_pannellum.DashPannellum(
        id='tour-component',
        tour=tour_config,
        customControls=True,
        showCenterDot=True,
        width='100%',
        height='750px',
        autoLoad=True,
        compass=True,
        northOffset=90
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True, port='8051')
