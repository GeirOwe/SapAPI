# To complete the application, you need to have a Python script at the 
#top-level that defines the Flask application instance. Let's call this 
# script main.py, and define it as a single line that imports the 
# application instance

# Here you can see both together in the same sentence. The Flask application instance 
# is called app and is a member of the app package. The from app import app statement 
# imports the app variable that is a member of the app package.

# Flask needs to be told how to import it, by setting the FLASK_APP environment variable:
# (venv) $ export FLASK_APP=main.py

from app import app
