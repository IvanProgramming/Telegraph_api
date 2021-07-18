from typing import Optional, List, ForwardRef, Union

from pydantic import BaseModel

Node = ForwardRef("Node")


class Node(BaseModel):
    tag: str
    attrs: Optional[dict]
    children: Optional[List[Union[str, Node]]]


Node.update_forward_refs()
