from flask import Flask
#from config import Config
import config

app = Flask(__name__)
#app.config.from_object(Config)
app.config.from_object(config)

#from app import routes
from app import gettoken