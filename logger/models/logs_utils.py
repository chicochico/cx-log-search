from sqlalchemy.sql.expression import and_, not_, or_


class InvalidOperationError(Exception):
    pass


def unpack_node(node: dict):
    """
    Unpack a dictionary with a single key value pair
    """
    for key, val in node.items():
        return key, val


def operating_node2sql(operation: str, operand: dict, model):
    """
    Transform the operation statement in json
    format to a sqlalchemy filter statement
    """
    column, keyword = unpack_node(operand)
    if operation == "CONTAINS":
        return getattr(model, column).ilike(f"%{keyword}%")
    elif operation == "IS":
        return getattr(model, column) == keyword


def validate_operation(operation, operand):
    """
    Validate the operations
    """
    if operation in ["CONTAINS", "IS"]:
        return None
    elif operation == "NOT":
        if "NOT" in operand:
            raise InvalidOperationError("NOT cannot contain a NOT operand")
    elif operation == "OR":
        if len(operand) <= 1:
            raise InvalidOperationError("OR must have more than one operand")
    elif operation == "AND":
        if len(operand) <= 1:
            raise InvalidOperationError("AND must have more than one operand")
    else:
        raise InvalidOperationError(f"Operation {operation} is invalid.")


def node2sql(query: dict, model):
    """
    Recursively visit the nodes depth first and
    return for each node a sqlalchemy filter statement
    """
    operation, operand = unpack_node(query)

    validate_operation(operation, operand)

    if operation in ["CONTAINS", "IS"]:
        return operating_node2sql(operation, operand, model)
    elif operation == "NOT":
        return not_(node2sql(operand, model))
    elif operation == "OR":
        return or_(node2sql(op, model) for op in operand)
    elif operation == "AND":
        return and_(node2sql(op, model) for op in operand)


def query2sql(query: dict, model):
    """
    Transform a query in json format into a sqlalchemy
    query object
    """
    return model.query.filter(node2sql(query, model))
