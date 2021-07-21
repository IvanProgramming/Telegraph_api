import asyncio
import logging
import tempfile
import unittest
from random import choice
from string import ascii_letters

from pydantic import ValidationError

from telegraph_api import Telegraph
from telegraph_api.models import Node

logging.basicConfig(level=logging.WARNING)
logging.getLogger("Telegraph").level = logging.DEBUG


def generate_random_str(length: int):
    result = ""
    for _ in range(length):
        result += choice(ascii_letters)
    return result


def run_async(future):
    if asyncio.get_event_loop().is_closed():
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(future)
    else:
        current_loop = asyncio.get_event_loop()
        return current_loop.run_until_complete(future)


class APITestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.telegraph = Telegraph()
        run_async(cls.telegraph.create_account(generate_random_str(10)))

    def test_account_creation(self):
        short_name = generate_random_str(5)
        name = "Test Account"
        new_account = run_async(self.telegraph.create_account(
            short_name=short_name,
            author_name=name,
            renew_token=False
        ))
        self.assertEqual(name, new_account.author_name)
        self.assertEqual(short_name, new_account.short_name)

    def test_page_view(self):
        try:
            path = "Already-Created-Article-07-18"
            page = run_async(self.telegraph.get_page(path, return_content=True))
            self.assertEqual("Already Created Article", page.title)
            self.assertEqual([Node(tag="p", attrs=None, children=["HA HA HA HA HA"])], page.content)
        except ValidationError as e:
            print(e.json())

    def test_page_creation(self):
        created_page = run_async(self.telegraph.create_page(
            title="Test Article!",
            author_name="Test Bot",
            content=[Node(tag="p", attrs={}, children=["This is my test article"])]
        ))
        path = created_page.path
        viewed_page = run_async(self.telegraph.get_page(path))
        self.assertEqual("Test Article!", viewed_page.title)

    def test_page_creation_from_html(self):
        source_html = """
            <p>This is first paragraph</p>
            <p>This is second paragraph with <strong>Bold</strong> text</p>
            <p>And this Paragraph contains <blink>restricted</blink> tag</p>
        """
        source_as_tree = [
            Node(tag="p", children=["This is first paragraph"]),
            Node(tag="p", children=["This is second paragraph with ", Node(tag="strong", children=["Bold"]), " text"]),
            Node(tag="p", children=["And this Paragraph contains restricted tag"])
        ]
        created_page = run_async(self.telegraph.create_page(
            title="Test Article, but from html!",
            author_name="Test Bot",
            content_html=source_html,
            return_content=True
        ))
        self.assertEqual(source_as_tree, created_page.content)

    def test_page_edition(self):
        created_page = run_async(self.telegraph.create_page(
            title="Test article and it will be edited!",
            author_name="Test Bot",
            content=[Node(tag="p", children=["2+2=5"])]
        ))
        path = created_page.path
        run_async(self.telegraph.edit_page(
            path,
            title="Test article and it has been already edited!",
            content=[Node(tag="p", children=["2+2=4"])]
        ))
        edited_page = run_async(self.telegraph.get_page(path, return_content=True))
        self.assertEqual("Test article and it has been already edited!", edited_page.title)
        self.assertEqual([Node(tag="p", children=["2+2=4"])], edited_page.content)

    def test_account_view(self):
        new_telegraph = Telegraph()
        name = generate_random_str(5)
        run_async(new_telegraph.create_account(name, author_name="TestBot"))
        account_data = run_async(new_telegraph.get_account_info(fields=["short_name", "author_name"]))
        self.assertEqual(name, account_data["short_name"])
        self.assertEqual("TestBot", account_data["author_name"])

    def test_account_edition(self):
        new_telegraph = Telegraph()
        run_async(new_telegraph.create_account(generate_random_str(6), author_name="Bot Test"))
        run_async(new_telegraph.edit_account_info(author_name="Test Bot"))
        new_name = run_async(new_telegraph.get_account_info(fields=["author_name"]))
        self.assertEqual(new_name["author_name"], "Test Bot")

    def test_token_revoke(self):
        old_token = self.telegraph.access_token
        run_async(self.telegraph.revoke_access_token())
        new_token = self.telegraph.access_token
        self.assertNotEqual(old_token, new_token)

    def test_file_upload(self):
        file_path = ""
        if not file_path:
            self.skipTest("File path is not specified!")
        file = run_async(self.telegraph.upload_file())
        self.assertIsNotNone(file)


if __name__ == '__main__':
    unittest.main()
