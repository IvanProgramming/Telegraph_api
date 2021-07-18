from typing import List

from telegraph_api.html_transform_middlewares import *
from telegraph_api.models import Node

middlewares = [
    handle_youtube_tags,
    remove_unsupported_tags,
    remove_unsupported_attrs,
    str.strip
]


def html2nodes(html: str, use_middlewares: bool = True) -> List[Node]:
    """
    Converts html to list of nodes. Passes it through middlewares and converts
    :param use_middlewares: Flag, that shows, should I use middleware in this function
    :param html: Source html
    :return:  list of nodes, that is suitable for sending in telegraph api
    """
    result = []
    if use_middlewares:
        html = pass_through_middlewares(html)
    bs_object = BeautifulSoup(html, features="html.parser")
    for child in bs_object.contents:
        if child.name is None:
            result.append(str(child.string).strip("\n"))
        else:
            tag = Node(tag=child.name, attrs=child.attrs, children=html2nodes("".join(map(str, child.contents)), False))
            result.append(tag)
    return result


def pass_through_middlewares(html: str) -> str:
    """
    Passes html code through all special middlewares for normalizing it
    :param html: Source html
    :return: normalized html
    """
    for middleware in middlewares:
        html = middleware(html)
    return html
