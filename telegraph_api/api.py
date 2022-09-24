import logging
from json import dumps
from typing import List

import aiohttp
from aiohttp import ContentTypeError
from pydantic import parse_obj_as
from typing.io import IO

from telegraph_api.exceptions import MethodIsNotAllowed, TelegraphError, FileIsNotPresented, InvalidFileExtension
from telegraph_api.html_transform import html2nodes
from telegraph_api.models import Account, Page
from telegraph_api.models import Node
from telegraph_api.models.page import PagesList
from telegraph_api.models.uploaded_file import UploadedFile
from telegraph_api.utils import normalize_locals, serialize_nodes


class APIEndpoints:
    """Class with endpoints of telegraph api"""

    base_uri = "https://api.telegra.ph"
    CREATE_ACCOUNT = f"{base_uri}/createAccount"
    CREATE_PAGE = f"{base_uri}/createPage"
    EDIT_ACCOUNT_INFO = f"{base_uri}/editAccountInfo"
    GET_ACCOUNT_INFO = f"{base_uri}/getAccountInfo"
    GET_PAGE_LIST = f"{base_uri}/getPageList"
    REVOKE_ACCESS_TOKEN = f"{base_uri}/revokeAccessToken"
    UPLOAD = f"https://telegra.ph/upload"

    @staticmethod
    def edit_page(page_name: str):
        return f"{APIEndpoints.base_uri}/editPage/{page_name}"

    @staticmethod
    def get_page(page_name: str):
        return f"{APIEndpoints.base_uri}/getPage/{page_name}"

    @staticmethod
    def get_views(page_name: str):
        return f"{APIEndpoints.base_uri}/getViews/{page_name}"


class Telegraph:
    """Telegraph API class"""

    def __init__(self, access_token=None):
        """
        Constructor of Class

        :param access_token: Access token. If not specified, limited quanity of methods will be availible, until you create account
        """
        self.access_token = access_token
        self.logger = logging.getLogger("Telegraph")

    async def create_account(self, short_name: str, author_name: str = None, author_url: str = None,
                             renew_token: bool = True):
        """
        Method for Creating new Account.

        :param short_name: Account name, helps users with several accounts remember which they are currently using
        :param author_name: Default author name used when creating new articles.
        :param author_url: Profile link, opened when users click on the author's name below the title.
        :param renew_token: Specifies, should be Telegraph object token renewed on method execution
        :return: Account object with access_token field
        """
        account: Account = await self.make_request(APIEndpoints.CREATE_ACCOUNT,
                                                   normalize_locals(locals(), "renew_token"),
                                                   model=Account)
        if renew_token:
            self.logger.debug(f"Token changed from {self.access_token} to {account.access_token}")
            self.access_token = account.access_token
        return account

    async def create_page(self, title: str, content: List[Node] = None, author_name: str = None, author_url: str = None,
                          return_content: bool = False, content_html: str = None) -> Page:
        """
        Create new telegraph page

        :param title: Page title
        :param content: Content of the page
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on the author's name below the title
        :param return_content: If true, content will be returned in content field
        :param content_html: Html Content, that will be converted into list of nodes
        :return: Page object, contains content if return_content is set to True
        """
        if content_html:
            content_json = serialize_nodes(html2nodes(content_html))
        elif not content:
            content_json = [""]
        else:
            content_json = serialize_nodes(content)

        params = normalize_locals(locals(), "content", "content_html", "content_json")
        params["content"] = dumps(content_json)
        page: Page = await self.make_request(APIEndpoints.CREATE_PAGE, json=params, method="post", model=Page)
        return page

    async def edit_page(self, path: str, title: str, content: List[Node] = None, content_html: str = None,
                        author_name: str = None, author_url: str = None, return_content: bool = False) -> Page:
        """
        Edit existing telegraph page

        :param path: Path to page
        :param title: Page title
        :param content: Content of the page
        :param author_name: Author name, displayed below the article's title
        :param author_url: Profile link, opened when users click on the author's name below the title
        :param return_content: If true, content will be returned in content field
        :param content_html: Html Content, that will be converted into list of nodes
        :return: Page object, contains content if return_content is set to True
        """
        if content_html:
            content_json = serialize_nodes(html2nodes(content_html))
        elif not content:
            content_json = [""]
        else:
            content_json = serialize_nodes(content)
        params = normalize_locals(locals(), "content", "content_html", "path")
        params["content"] = dumps(content_json)
        page: Page = await self.make_request(APIEndpoints.edit_page(path), json=params, method="post", model=Page)
        return page

    async def get_account_info(self, fields: List[str] = None):
        """
        Use this method to get information about a Telegraph account

        :param fields: List of account fields to return. Available fields: short_name, author_name, author_url, auth_url, page_count
        :return: an Account object
        """
        account_info = await self.make_request(APIEndpoints.GET_ACCOUNT_INFO, normalize_locals(locals()))
        return account_info

    async def revoke_access_token(self) -> dict:
        """
        Use this method to revoke access_token and generate a new one. Sets new access_token

        :return: Account object with access token field
        """
        account: dict = await self.make_request(APIEndpoints.REVOKE_ACCESS_TOKEN)
        self.logger.debug(f"Token changed from {self.access_token} to {account['access_token']}")
        self.access_token = account["access_token"]
        return account

    async def get_page(self, path: str, return_content: bool = False) -> Page:
        """
        Use this method to revoke access_token and generate a new one

        :param path: Path to the Telegraph page
        :param return_content: If true, content field will be returned
        :return: Page object
        """
        page: Page = await self.make_request(APIEndpoints.get_page(path), params=normalize_locals(locals(), "path"),
                                             model=Page)
        return page

    async def get_page_list(self, limit: int = 50, offset: int = 0) -> PagesList:
        """
        Use this method to get a list of pages belonging to a Telegraph account

        :param limit: Limits the number of pages to be retrieved
        :param offset: Sequential number of the first page to be returned
        :return: list of pages, sorted by most recently created pages first
        """
        pages: PagesList = await self.make_request(APIEndpoints.GET_PAGE_LIST, params=normalize_locals(locals()),
                                                   model=PagesList)
        return pages

    async def get_views(self, path: str, year: int = None, month: int = None, day: int = None, hour: int = None) -> int:
        """
        Use this method to get the number of views for a Telegraph article.

        :param path: Path to the Telegraph page
        :param year: Required if month is passed. If passed, the number of page views for the requested year will be returned.
        :param month: Required if day is passed. If passed, the number of page views for the requested month will be returned.
        :param day: Required if hour is passed. If passed, the number of page views for the requested day will be returned.
        :param hour: If passed, the number of page views for the requested hour will be returned.
        :return: By default, the total number of page views will be returned.
        """
        views_dict = await self.make_request(APIEndpoints.get_views(path), params=normalize_locals(locals(), "path"))
        return views_dict["views"]

    async def edit_account_info(self, short_name: str = None, author_name: str = None,
                                author_url: str = None) -> Account:
        """
        Use this method to update information about a Telegraph account.

        :param short_name: New account name
        :param author_name: New default author name used when creating new articles
        :param author_url: New default profile link, opened when users click on the author's name below the title
        :return: an Account object with the default fields
        """
        account = await self.make_request(APIEndpoints.EDIT_ACCOUNT_INFO, params=normalize_locals(locals()))
        return account

    async def upload_file(self, file_path: str = None, file_stream: IO = None):
        """
        Uploads file to telegra.ph servers
        (only gif, jpg, jpe, jpeg, jfif, png, mp4, m4v, mp4v files allowed)

        :param file_path: Path to file in local filesystem
        :param file_stream: IO object for example can be occurred from open() function
        :return: UploadedFile object
        :raises FileIsNotPresented: If no files were passed into function
        :raises InvalidFileExtension: If file extension is not supported by telegra.ph
        """
        if file_path:
            stream = open(file_path, "rb")
        elif file_stream:
            stream = file_stream
        else:
            raise FileIsNotPresented
        data = {"file": stream}
        self.logger.debug("Uploading file. ")
        try:
            response_text = await self.get(APIEndpoints.UPLOAD, data=data)
            stream.close()
            return parse_obj_as(UploadedFile, response_text)
        except ContentTypeError:
            raise InvalidFileExtension

    async def make_request(self, endpoint: str, params: dict = None, method: str = "get", model=None,
                           use_token: bool = True, json=None, **extra_params):
        """
        Function for making requests to API

        :param endpoint: Telegraph API endpoints
        :param params: Params for request queries
        :param method: Request Method. Only "get" or "post" are allowed
        :param model: PyDantic model for after request transformation
        :param use_token: Specifies, should token be passed in params, or not
        :param extra_params: Extra options, that will be passed into request function (e.g. file)
        :return: json dict, if model is not set, else BaseModel object
        :raises: MethodIsNotAllowed: if method param is invalid
        """
        # OMG this looks so scary, I think it should be fixed
        if params is None:
            params = {}

        if self.access_token and use_token:
            if json is not None:
                json["access_token"] = self.access_token
            else:
                params["access_token"] = self.access_token

        self.logger.debug(f"Making request to {endpoint}. Params - {params}")
        if method == "get":
            result = await self.get(endpoint, params=params, **extra_params)
        elif method == "post":
            result = await self.post(endpoint, params=params, json=json, **extra_params)
        else:
            raise MethodIsNotAllowed

        if not result["ok"]:
            raise TelegraphError(result["error"])

        data = result["result"]
        if model:
            return parse_obj_as(model, data)
        return data

    @staticmethod
    async def get(url: str, params: dict = None, raw=False, encoding="utf-8", **extra_params):
        """
        Make asynchronus GET request

        :param url: Request URL
        :param params: Query Params
        :param raw: Specifies should function return raw string, or use json parser
        :param encoding: (if raw is set to True) Specifies string encoding
        :param extra_params: Extra request params, passed into session.get function
        :return: Dict or Str, depending on raw flag
        """
        async with aiohttp.request("get", url, params=params, **extra_params) as response:
            if raw:
                return (await response.read()).decode(encoding=encoding)
            else:
                return await response.json()

    @staticmethod
    async def post(url: str, params: dict, raw=False, encoding="utf-8", **extra_params):
        """
        Make asynchronus POST request

        :param url: Request URL
        :param params: Query Params
        :param raw: Specifies should function return raw string, or use json parser
        :param encoding: (if raw is set to True) Specifies string encoding
        :param extra_params: Extra request params, passed into session.get function
        :return: Dict or Str, depending on raw flag
        """
        async with aiohttp.request("post", url, params=params, **extra_params) as response:
            if raw:
                return (await response.read()).decode(encoding=encoding)
            else:
                return await response.json()
