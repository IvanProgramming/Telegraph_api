from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    """ Represents Account type """
    short_name: str
    """ Account name, helps users with several accounts remember which they are currently using. """
    author_name: str
    """ Default author name used when creating new articles. """
    author_url: str
    """ Profile link, opened when users click on the author's name below the title. """
    access_token: Optional[str]
    """ Optional. Only returned by the createAccount and revokeAccessToken method. Access token of the Telegraph 
    account. """
    auth_url: Optional[str]
    """ Optional. URL to authorize a browser on telegra.ph and connect it to a Telegraph account. """
    page_count: Optional[int]
    """ Optional. Number of pages belonging to the Telegraph account. """
