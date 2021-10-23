import pytest
from flask import current_app
from logger.app import create_app


@pytest.fixture(scope="module")
def client():
    if not current_app:
        app = create_app()
    else:
        app = current_app
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize(
    "endpoint,expected",
    [
        ("/search/browser/philippines", 8),
        ("/search/IE/philippines", 31),
    ],
)
def test_simple_search(client, endpoint, expected):
    res = client.get(endpoint)
    assert len(res.json) == expected


queries = [
    (
        {"CONTAINS": {"message": "error"}},
        0,
    ),
    ({"IS": {"browser": "chrome"}}, 0),
    (
        {"NOT": {"IS": {"country": "Brazil"}}},
        95,
    ),
    (
        {
            "AND": [
                {"IS": {"browser": "Firefox"}},
                {"IS": {"country": "Philippines"}},
            ]
        },
        3,
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
        85,
    ),
]


@pytest.mark.parametrize(
    "test_input,expected",
    queries,
)
def test_query_logger(client, test_input, expected):
    response = client.get("/search/query", json=test_input)
    assert len(response.json) == expected


@pytest.mark.parametrize(
    "test_input",
    [
        {"OPERATION_DOES_NOT_EXISTS": {"message": "error"}},
        {"CONTAINS": {"random_column": "error"}},
        {"AND": {"message": "error"}},
        {"AND": [{"message": "error"}]},
        {"AND": []},
        {"OR": {"browser": "Safari"}},
        {"OR": [{"browser": "Safari"}]},
        {"OR": []},
        {"NOT": {"NOT": {"country": "Brazil"}}},
        {"NOT": [{"IS": {"browser": "Safari"}}, {"IS": {"country": "Sweden"}}]},
    ],
)
def test_query_validation(client, test_input):
    response = client.get("/search/query", json=test_input)
    assert response.status_code == 400
