from flask import Flask

from logger.extensions import api, db
from logger.views import search


def create_app(config_object="logger.config"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_api_resources(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(search.bp)
    return None


def register_api_resources(app):
    api.init_app(search.bp)
    api.add_resource(search.LogSimpleSearch, "/<string:browser>/<string:country>")
    api.add_resource(search.LogQuery, "/query")
    return None
