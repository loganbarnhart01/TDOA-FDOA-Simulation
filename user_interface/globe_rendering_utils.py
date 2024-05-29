from plotly import graph_objects as go

def render_plot(data):
    """
    Renders globe for given data:

    args:
        data (dict): dictionary with all desired plotly scattergeo arguments, 
        e.g.: {'lat' : [1, 2, 3], 'long' : [1, 2, 3], ...}
    
    returns:
        html for plotly globe with template
    """
    fig = go.Figure(go.Scattergeo(**data))

    #customize these?
    fig.update_traces(marker_size=20, line=dict(color="Red"))
    fig.update_geos(projection_type="orthographic")
    fig.update_layout(width=800, height=800, margin={"r":0,"t":0,"l":0,"b":0})
    html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return html


    
def format_globe_html(globe_html, template_path, completed_path):    
    with open(template_path, 'r') as file:
        template_html = file.read()
    
    combined_html = template_html.replace("{{ plotly_placeholder }}", globe_html)

    with open(completed_path, 'w') as file:
        file.write(combined_html)

