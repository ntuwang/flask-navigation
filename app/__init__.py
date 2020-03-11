from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from logging.config import dictConfig
import datetime
import os

db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in ('base', 'navigation',):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def configure_logs(app):
    baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logDir = os.path.join(baseDir, "logs")
    if not os.path.exists(logDir):
        os.makedirs(logDir)  # 创建路径

    logDict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
            'standard': {
                'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
            },
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },

            "default": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "simple",
                "filename": 'logs/navigation-{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")),
                'mode': 'w+',
                "maxBytes": 1024 * 1024 * 5,  # 5 MB
                "backupCount": 20,
                "encoding": "utf8"
            },
        },

        "loggers": {
            "app_name": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": "no"
            }
        },

        "root": {
            'handlers': ['default'],
            'level': "INFO",
            'propagate': False
        }
    }

    dictConfig(logDict)
    logger = getLogger()
    logger.addHandler(StreamHandler())


def create_app(config, selenium=False):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config)
    if selenium:
        app.config['LOGIN_DISABLED'] = True
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    configure_logs(app)
    return app
