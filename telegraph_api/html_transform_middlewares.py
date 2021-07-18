import re

from bs4 import BeautifulSoup
from urllib3.util import parse_url


def handle_youtube_tags(html: str):
    """ Middleware for youtube iframes """
    bs_object = BeautifulSoup(html, features="html.parser")
    regex = r"https:\/\/w?w?w?\.?youtube\.com\/embed\/"
    all_iframes = bs_object.find_all("iframe")
    for tag_index in range(len(all_iframes)):
        tag = all_iframes[tag_index]
        if re.search(regex, tag["src"]):
            # Last part form embed url
            video_id = parse_url(tag["src"]).path.split[:-1]
            telegraph_embed_src = f"/embed/youtube?url=https://youtube.com/watch?v={video_id}"
            tag["src"] = telegraph_embed_src
            tag["width"] = "640"
            tag["height"] = "360"
            tag["allow_transparency"] = "true"
            tag["allow_fullscreen"] = "true"
            if tag.next_sibling.name != "figcaption":
                tag.insert_after("<figcaption></figcaption>")
            if tag.parent.name != "figure":
                tag.wrap(bs_object.new_tag("figure"))
    return str(bs_object)


def remove_unsupported_tags(html: str):
    """ Middleware, that removes unsupported by telegraph tags. Runs at the end transformation"""
    SUPPORTED_TAGS = ["a", "aside", "b", "blockquote", "br", "code", "em", "figcaption", "figure", "h3", "h4", "hr",
                      "i", "iframe", "img", "li", "ol", "p", "pre", "s", "strong", "u", "ul", "video"]
    bs_object = BeautifulSoup(html, features="html.parser")
    for tag in bs_object.find_all():
        if tag.name not in SUPPORTED_TAGS:
            tag.unwrap()
    return str(bs_object)


def remove_unsupported_attrs(html: str):
    """ Middleware, that removes unsupported by telegraph API attrs. Runs at the end of transformation"""
    SUPPORTED_ATTRS = ["href", "src"]
    bs_object = BeautifulSoup(html, features="html.parser")
    for tag in bs_object.find_all():
        for attr in tag.attrs:
            if attr not in SUPPORTED_ATTRS:
                del tag[attr]
    return str(bs_object)
