from flask import Flask
from app.blueprints.page import page

def create_app(settings_override=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object('config.settings')
  app.config.from_pyfile('settings.py', silent=True)
  if settings_override:
    app.config.update(settings_override)
  app.register_blueprint(page)
  return app

myapp = create_app()