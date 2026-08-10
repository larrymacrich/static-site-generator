from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False    
        props = ["text", "text_type", "url"]
        for prop in props:
            if getattr(self, prop) != getattr(other, prop):
                    return False
        return True

    def __repr__(self) -> str:
        return (
             f"TextNode(text={self.text!r}, text_type={self.text_type.value!r}, "
             f"url={self.url!r})"
        )