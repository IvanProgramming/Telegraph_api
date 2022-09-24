from typing import Optional, List, Union

from pydantic import BaseModel

from telegraph_api.models import Node


class Page(BaseModel):
    """ PyDantic model for telegra.ph Page """
    path: str
    """ Path to the page. """
    url: str
    """ URL of the page. """
    title: str
    """ Title of the page. """
    description: str
    """ Description of the page. """
    author_name: Optional[str]
    """ Optional. Name of the author, displayed below the title. """
    author_url: Optional[str]
    """ Optional. Profile link, opened when users click on the author's name below the title.
      Can be any link, not necessarily to a Telegram profile or channel. """
    image_url: Optional[str]
    """ Optional. Image URL of the page. """
    content: Optional[List[Union[Node, str]]]
    """ Optional. Content of the page. """
    views: int
    """ Number of page views for the page. """
    can_edit: Optional[bool]
    """ Optional. Only returned if access_token passed. True, if the target Telegraph account can edit the page. """


class PagesList(BaseModel):
    """ PyDantic model for telegra.ph PagesList """
    total_count: int
    """ Total number of pages belonging to the target Telegraph account. """
    pages: List[Page]
    """ List of pages belonging to the target Telegraph account. """
