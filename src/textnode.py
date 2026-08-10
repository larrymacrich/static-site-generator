from enum import Enum


class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    ANCHOR_TEXT = "link"
    ALT_TEXT = "image"

class TextNode():

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        props = ["text", "text_type", "url"]
        for prop in props:
            if getattr(self, prop) != getattr(other, prop):
                    return False
        return True

    def __repr__(self) -> str:
        attr_str = f"TextNode({self.text}, {self.text_type.value})"
        if self.url is not None:
            attr_str = attr_str.replace(")", f", {self.url})")
        return attr_str