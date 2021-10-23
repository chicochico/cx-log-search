import json

from flask import Blueprint, Response, request
from flask_restful import Resource
from logger.models.logs import Log
from logger.models.logs_utils import InvalidOperationError, query2sql
from sqlalchemy.sql.expression import or_

bp = Blueprint("search", __name__, url_prefix="/search")


class LogSimpleSearch(Resource):
    def get(self, browser, country):
        """
        Simple search endpoint that returns log messages
        filtered by browser and country
        """
        query_result = Log.query.filter(
            or_(Log.browser == browser, Log.country.ilike(country))
        ).all()
        return_result = [e.to_dict() for e in query_result]
        return return_result


class LogQuery(Resource):
    """
    Endpoint that allows querying the log with json search tree ex:

    {"NOT": {"IS": {"country": "Brazil"}}}
    """

    def get(self):
        query = request.json  # the json structure representing the query

        try:
            sql = query2sql(query, Log)
        except (InvalidOperationError, AttributeError) as e:
            return Response(
                json.dumps({"message": str(e)}),
                status=400,
                mimetype="application/json",
            )

        return_result = [e.to_dict() for e in sql.all()]
        return return_result
