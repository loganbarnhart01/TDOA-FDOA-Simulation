# How to run basic UI
* `python user_interface/app.py`


# File Breakdown    
# __init__.py
    - allows other python files to be treated like a package (ie..globe.py & globe_rendering_utils)


# app.py
    - flask import app that controls end point logic and what URL renders an HTML file.
    each / (insert string) renders a different HTML file


# globe_rendering_utils.py
    - utilies to take data and convert it to an actual globe in HTML


# globe.py
    - TBD