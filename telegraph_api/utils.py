from json import dumps
from typing import List, Union

from pydantic import BaseModel

from telegraph_api.models import Node


def normalize_locals(_locals: dict, *unnecessary_parameters) -> dict:
    """
    Normalizes locals() result, for sending it to telegra.ph API. Run str for all not strings and removes "self" and Empty params
    :param _locals: locals() function result
    :return: normalized locals
    """
    result = _locals.copy()
    for param, value in _locals.items():
        if value is None or value == "" or param in unnecessary_parameters:
            del result[param]
        elif type(value) != str:
            if type(value) == int or type(value) == float:
                result[param] = str(value)
            elif BaseModel in type(value).__bases__:
                result[param] = value.json()
            elif type(value) == list:
                result[param] = dumps(value)
            elif type(value) == bool:
                result[param] = "true" if value else "false"
            else:
                del result[param]
    return result


def serialize_nodes(nodes: List[Union[Node, str]]) -> List[Union[dict, str]]:
    """
    Converts list with Pydantic nodes into serializable list of dicts
    :param nodes:
    :return:
    """
    result_list = []
    for element in nodes:
        if type(element) == str:
            if element:
                result_list.append(element)
        elif type(element) == Node:
            result_list.append(element.dict())

    return result_list
