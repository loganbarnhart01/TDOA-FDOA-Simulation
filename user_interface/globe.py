from globe_rendering_utils import render_plot, format_globe_html

data = {'lat' : [45.5231, 12.1234], 'lon' : [122.6765, 23.4567], 'mode' : 'markers'}

globe_html = render_plot(data)

render_html = format_globe_html(globe_html, 'user_interface/templates/live.html', 'user_interface/templates/live_completed.html')