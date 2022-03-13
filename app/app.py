from flask import Flask
from app.blueprints.page import page
from app.extensions import debug_toolbar
def create_app(settings_override=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object('config.settings')
  app.config.from_pyfile('settings.py', silent=True)
  if settings_override:
    app.config.update(settings_override)
  app.register_blueprint(page)
  extensions(app)
  return app

myapp = create_app()


def extensions(app):
  debug_toolbar.init_app(app)

  return None
