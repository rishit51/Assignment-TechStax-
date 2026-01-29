from flask import Flask
from .extensions import mongo
from .webhook.routes import webhook
import os
import configparser
config = configparser.ConfigParser()
config.read("app/sample.ini")

# Setup MongoDB here
# Creating our flask app
def create_app():

    app = Flask(__name__)
    # registering all the blueprints
    app.register_blueprint(webhook)
    mongo.init_app(app,uri=config['TEST']['DB_URI'])
    return app
