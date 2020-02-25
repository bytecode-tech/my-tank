import os
import logging
from flask import Flask, make_response, request
from flask_api import FlaskAPI
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client.core import REGISTRY
from . import config as Config

from .modules.dht_sensor import temp_controller
from .modules.soil_temp import soil_temp_controller
from .modules.schedule import schedule_controller
from .modules.admin import admin_controller
from .modules.sensor_collector import sensor_collector
from .modules.devices import device_controller
from .modules.wifi import wifi_controller

# For import *
__all__ = ['create_app']


DEFAULT_BLUEPRINTS = [
    temp_controller,
    wifi_controller,
    soil_temp_controller,
    schedule_controller,
    admin_controller,
    device_controller
]

def create_app(config=None, app_name=None, blueprints=None):
   """Create a Flask app."""

   blueprints = DEFAULT_BLUEPRINTS

   app = FlaskAPI("zero_controller")
   CORS(app)
   configure_app(app, config)   
   configure_blueprints(app, blueprints)

   REGISTRY.register(sensor_collector.SensorCollector())

   if app.debug:
      print('running in debug mode')
   else:
      print('NOT running in debug mode')

   app = DispatcherMiddleware(app, {
      '/metrics': make_wsgi_app()
   })

   return app

def configure_app(app, config=None):
   """Different ways of configurations."""

   # http://flask.pocoo.org/docs/api/#configuration
   app.config.from_object(Config.DefaultConfig)

   if config:
      app.config.from_object(config)
      return

   MODE = os.getenv('APPLICATION_MODE', 'DEV')

   print("Running in %s mode" % MODE)

   app.config.from_object(Config.get_config(MODE))

def configure_blueprints(app, blueprints):
   """Configure blueprints in views."""

   for blueprint in blueprints:
      app.register_blueprint(blueprint)
