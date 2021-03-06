from flask import Flask
from app.blueprints.page import page
from celery import Celery
from app.blueprints.contact import contact
from app.extensions import debug_toolbar, mail, csrf
from app.extensions import debug_toolbar
 
CELERY_TASK_LIST = [
    'app.blueprints.contact.tasks',
]


def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.

    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def extensions(app):
  debug_toolbar.init_app(app)
  mail.init_app(app)
  csrf.init_app(app)
  return None

def create_app(settings_override=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object('config.settings')
  app.config.from_pyfile('settings.py', silent=True)
  if settings_override:
    app.config.update(settings_override)
  app.register_blueprint(page)
  app.register_blueprint(contact)
  extensions(app)
  return app 

myapp = create_app()


