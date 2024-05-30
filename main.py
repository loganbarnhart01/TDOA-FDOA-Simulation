from plotly import graph_objects as go

fig = go.Figure(go.Scattergeo(lat = [39.849312 , 39.5795], lon = [-104.673828, -104.84929], text = ["KDEN","KAPA"]))

#customize these?
# fig.update_traces(marker_size=20, line=dict(color="Purple"))
fig.update_traces(
    marker_size=10,
    marker_symbol="hash-open",
    line=dict(color="Pink")
)

fig.update_geos(projection_type="orthographic")
fig.update_layout(width=800, height=800, margin={"r":0,"t":0,"l":0,"b":0})

fig.show()