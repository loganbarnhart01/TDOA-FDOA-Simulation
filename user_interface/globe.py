from globe_rendering_utils import render_plot, format_globe_html

data = {'lat' : [39.849312, 0], 'lon' : [0,-104.673828], 'mode' : 'markers'}

globe_html = render_plot(data)

render_html = format_globe_html(globe_html, 'user_interface/templates/live.html', 'user_interface/templates/live_completed.html')