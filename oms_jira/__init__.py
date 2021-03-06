# pylint: disable=too-few-public-methods

"""Flask recommender factory"""

import os

from flask import Flask

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from oms_jira.extensions import db, migrate, celery
from oms_jira.api import api
from oms_jira.services.mp import MPClient
from settings import config_by_name
from .commands import blueprint


def create_app():
    """Creates the flask app, initializes config in
    the proper ENV and initializes flask-restx"""

    init_sentry_flask()

    app = Flask(__name__)
    app.config.from_object(config_by_name[os.environ["FLASK_ENV"]])

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    init_celery(app)
    init_blueprints(app)

    return app


def init_celery(app: Flask = None):
    """Initializes celery"""

    app = app or create_app()

    if os.environ["FLASK_ENV"] == "testing":
        celery.conf.update(task_always_eager=True)
    else:
        celery.conf.update(
            broker_url=app.config["REDIS_HOST"],
            result_backend=app.config["REDIS_HOST"],
        )

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask recommender context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def init_sentry_flask():
    """Initializes sentry-flask integration"""

    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
    )


def init_sentry_celery():
    """Initializes sentry-celery integration"""

    sentry_sdk.init(
        integrations=[CeleryIntegration(), RedisIntegration()],
        traces_sample_rate=1.0,
    )


def init_blueprints(app: Flask):
    app.register_blueprint(blueprint)
