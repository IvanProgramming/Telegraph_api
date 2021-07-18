from typing import Optional, List, Union

from pydantic import BaseModel

from telegraph_api.models import Node


class Page(BaseModel):
    """ PyDantic model for telegra.ph Page """
    path: str
    url: str
    title: str
    description: str
    author_name: Optional[str]
    author_url: Optional[str]
    image_url: Optional[str]
    content: Optional[List[Union[Node, str]]]
    views: int
    can_edit: Optional[bool]

