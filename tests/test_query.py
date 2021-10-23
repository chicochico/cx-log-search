import pytest
from flask import current_app
from logger.app import create_app
from logger.models.logs import Log
from logger.models.logs_utils import query2sql
from sqlalchemy.sql.expression import and_, not_, or_

if not current_app:
    app = create_app()
    app.app_context().push()


queries = [
    (
        {"CONTAINS": {"message": "error"}},
        Log.query.filter(Log.message.ilike("%error%")),
    ),
    (
        {"IS": {"browser": "chrome"}},
        Log.query.filter(Log.browser == "chrome"),
    ),
    (
        {"NOT": {"IS": {"country": "Brazil"}}},
        Log.query.filter(not_(Log.country == "Brazil")),
    ),
    (
        {
            "AND": [
                {"IS": {"browser": "Firefox"}},
                {"IS": {"country": "Philippines"}},
            ]
        },
        Log.query.filter(and_(Log.browser == "Firefox", Log.country == "Philippines")),
    ),
    (
        {
            "NOT": {
                "OR": [
                    {
                        "AND": [
                            {"IS": {"browser": "Safari"}},
                            {"IS": {"country": "Sweden"}},
                        ]
                    },
                    {"CONTAINS": {"message": "Integer"}},
                ]
            }
        },
        Log.query.filter(
            (
                not_(
                    or_(
                        and_(Log.browser == "Safari", Log.country == "Sweden"),
                        Log.message.ilike("%Integer%"),
                    )
                )
            )
        ),
    ),
]


@pytest.mark.parametrize(
    "test_input,expected",
    queries,
)
def test_tree_to_sql(test_input, expected):
    sql = query2sql(test_input, Log)
    assert str(sql) == str(expected)
