from typing import Optional, List, ForwardRef, Union

from pydantic import BaseModel

Node = ForwardRef("Node")


class Node(BaseModel):
    """ This abstract object represents a DOM Node. """
    tag: str
    """ Name of the DOM element. """
    attrs: Optional[dict]
    """ Optional. Attributes of the DOM element """
    children: Optional[List[Union[str, Node]]]
    """ Optional. List of child nodes for the DOM element. """


Node.update_forward_refs()
