import numpy as np
from plotly import graph_objects as go

def render_plot(data):
    """
    Renders globe for given data:

    args:
        data (dict): dictionary with latitude and longitude info and scattergeo kwargs
            each list should contain a list with the lat/long info for one line segment. 
        e.g.: {'lat' : [[1, 2, 3], ...] 'long' : [[1, 2, 3], ...], **kwargs}
    
    returns:
        html for plotly globe with template
    """
    latitude = data['lat']
    longitude = data['lon']

    fig = go.Figure()

    #Line customization    
    marker = dict(
        size = 20,
        color = '#ffc300',
    )
    line = dict(
        width = 3,
        color = '#ffc300'
    )

    for lat, lon in zip(latitude, longitude):
        # plot lines
        fig.add_trace(go.Scattergeo(
            lat=lat,
            lon=lon,
            mode='lines',
            line=line
        ))

        bearing = calculate_bearing(lat, lon)
        direction = triangle_orientation(bearing)
        marker['symbol'] = 'triangle' + direction


        fig.add_trace(go.Scattergeo(
            lat=[lat[-1]],
            lon=[lon[-1]],
            mode='markers',
            marker=marker,
        ))


    # fig.update_geos(projection_type="orthographic", showcountries=True)
    fig.update_geos(
        fitbounds=False
    )
    fig.update_layout(width=750, 
                      height=750, 
                      margin={"r":0,"t":0,"l":0,"b":0},
                      uirevision='constant',
                      geo=dict(
                          projection_type='orthographic',
                          showland=True,
                          landcolor='#1e1e2e',
                          showocean=True,
                          oceancolor='#cdd6f4',
                          showlakes=True,
                          lakecolor='#cdd6f4',
                          showcountries=True,
                          countrycolor='#cdd6f4',
                          bgcolor='#1e1e2e'
                        ),
                      showlegend=False
                      )
    
    fig_json = fig.to_json()
    return fig_json


def calculate_bearing(lat, lon):
    lat1 = lat[-1]
    lat2 = lat[-2]
    lon1 = lon[-1]
    lon2 = lon[-2]

    lat1, lat2, lon1, lon2 = map(np.radians, [lat1, lat2, lon1, lon2])

    dlon = lon2 - lon1
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(dlon))

    initial_bearing = np.degrees(np.arctan2(x, y))

    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def triangle_orientation(bearing):
    if 335.7 <= bearing < 22.5:
        return '-down'
    elif 22.5 <= bearing < 67.5:
        return '-sw'
    elif 67.5 <= bearing < 112.5:
        return '-left'
    elif 112.5 <= bearing < 157.5:
        return '-nw'
    elif 157.5 <= bearing < 202.5:
        return '-up'
    elif 202.5 <= bearing < 247.5:
        return '-ne'
    elif 247.5 <= bearing < 292.5:
        return '-right'
    elif 292.5 <= bearing < 335.7:
        return '-se'
    else:
        return '-up' # default
    
