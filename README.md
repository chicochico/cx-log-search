# Logs Querying

## Exercise

### User Story

As a user, I want to be able to search for error logs using advanced filters.

#### Background

The objective of this user story is to implement an API endpoint for an existing log storage service written in Python.

Error logs are stored in a database table with the following structure:


| Field name | Type     |
|------------|----------|
| id         | Integer  |
| created    | DateTime |
| browser    | String   |
| page_url   | String   |
| country    | String   |
| message    | String   |

An **endpoint**, allowing for searches by browser or country, already exists.

- The functionality must be implemented as an endpoint separate from the existing simple search endpoint.
- The endpoint must accept a search expression represented by a json tree
    - The tree has three types of inner nodes:
        - grouping nodes (labelled as 'AND', 'OR')
            - a grouping node is used to combine multiple operation and control operation priorities
                - the AND node only allows a log message if it's allowed by all its children
                - the OR node only allows a log message if it's allowed by at least one of its children
            - a grouping node can have an arbitrary number of children (>1) and children can be of any type
        - negating nodes (labelled as 'NOT')
            - a negating node has only one child. The child can either be a grouping node or an operation node
            - a negating node only allows a log message if it's not allowed by its child
        - operation nodes (labelled as 'IS', 'CONTAIN')
            - operation nodes are the only parents for leaf nodes. The left leaf of an operation node is a field name. The right leaf is a value
            - operation nodes allow all log messages for which the result of applying the operation on the 'field' with the 'value' is true
- Search tree examples:
```
    - {"CONTAINS":{"message": "error"}}
        - returns all records with the field "message" containing the word "error"
    - {"IS":{"browser": "chrome"}}
        - returns all records with the field "browser" being exactly the word "chrome"
    - {"NOT":{"IS":{"country": "Italy"}}}
        - returns all records with the field "country" NOT exactly equal to the word "Italy"
    - {"NOT": {"OR": [{"AND": [{"IS": {"browser": "safari"}},{"IS": {"country": "Germany"}}]},{"CONTAINS": {"message": "stacktrace"}}]}}
        - returns all records that DO NOT match one or both of these conditions:
            - the field "message" contains the word "stacktrace"
            - the field "browser" is the word "safari" AND the field "country" is the word "Germany"
```
- The endpoint must return a JSON list of all records matching the search expression.
- The existing code must be refactored using software development principles that are adequate to the size and nature of the project


## Exercise solution notes

The complex search endpoint is implemented as a `GET` method, where the query is sent as a json in the request body.

### Endpoints
```
GET /search/{browser}/{country}
GET /search/query
```

curl examples:
```
curl http://localhost:5000/search/browser/philippines

curl -i -X GET localhost:5000/search/query \
    -H "Content-Type: application/json" \
    -d '{"NOT": {"IS": {"country": "Brazil"}}}'
```

### Assumptions
In no particular order:
- flask is mandatory
- CONTAINS is case insensitive

### Further possible improvements for the future
- add authentication
- add pagination for the search endpoints
- add a swagger document page

### Toughts
For my own reasoning:
- ~~boolean algebra seems to be where the solution may lay?~~
- a tree represent the query
    - root: logical nodes
        - exception: when there is only one node the root must be a operating node
    - internal: logical nodes
    - leafs operating nodes
- ~~is there a library that can translate arbitraryly nested structures like this into a sql query?~~
- tree operations means recursion might be in the map
    - recursively travese the tree depth first building the sql filter statements
- raw sql statements risk of sql injection
    - [x] use some sqlalchemy filter function instead
- validations for the input query?
    - [x] validations for valid operations: NOT, OR, AND, IS and CONTAINS
    - [x] OR and AND must have more than one operand
    - [x] NOT can not contains a NOT child (no double negations)
