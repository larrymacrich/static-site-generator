from enum import Enum
from leafnode import LeafNode

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
             f"{type(self).__name__}(text={self.text!r}, text_type={self.text_type.value!r}, "
             f"url={self.url!r})"
        )

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None,value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a",value=text_node.text, props={"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img",value="", props={"src" : text_node.url, "alt": text_node.text})
        case _:
            raise TypeError(
                f"{text_node.text_type} type is not supported"
                f"for {type(text_node).__name__}"
            )    

def split_nodes_delimiter(
        old_nodes: list[TextNode], 
        delimiter: str, 
        text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections  = old_node.text.split(delimiter)
        if len(sections ) % 2 == 0:
            raise ValueError(f"No closing of given delimter in:\n{old_node}")

        for i, section in enumerate(sections):
            if section == "":
                continue
            section_type = TextType.TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(text = section, text_type = section_type))
    return new_nodes