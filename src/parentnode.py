from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):

    def __init__(
        self, 
        tag: str,
        children: list[HTMLNode], 
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if self.children is None:
            raise ValueError("All parent nodes must have children.")
        return (
            f'<{self.tag}{self.props_to_html()}>'
            f'{"".join([child.to_html() for child in self.children])}'
            f'</{self.tag}>'
        )