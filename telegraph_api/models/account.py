from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    """ Represents Account type """
    short_name: str
    author_name: str
    author_url: str
    access_token: Optional[str]
    auth_url: Optional[str]
    page_count: Optional[int]
