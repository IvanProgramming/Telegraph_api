from pydantic import BaseModel

from telegraph_api.models import Node

ALLOWED_EXTENSIONS = ['gif', 'jpg', 'jpe', 'jpeg', 'jfif', 'png', 'mp4', 'm4v', 'mp4v']


class UploadedFile(BaseModel):
    """ Pydantic model for Uploaded to server File """
    src: str
    """ Path to telegra.ph file """
    @property
    def extension(self) -> str:
        """ Extension of file """
        return self.src.split(".")[-1]

    def to_node(self, caption: str = "") -> Node:
        """
        Converts uploaded file object to Node, that can be pasted into Node tree

        :param caption: Captions for video or image
        :return: Node object
        """
        # Pictures
        if self.extension in ['gif', 'jpg', 'jpeg', 'jfif', 'png']:
            return Node(
                tag="figure",
                children=[
                    Node(tag="img", attrs={"src": self.src}),
                    Node(tag="figcaption", children=[caption])
                ]
            )
        # Videos
        else:
            return Node(
                tag="figure",
                children=[
                    Node(tag="video", attrs={"src": self.src}),
                    Node(tag="figcaption", children=[caption])
                ]
            )


