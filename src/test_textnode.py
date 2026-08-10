import unittest
from textnode import TextNode, TextType


class TestTextNodeEquality(unittest.TestCase):
    """Tests covering equality (__eq__) logic across properties."""

    def test_eq_matching_nodes(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_explicit_none_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_matching_url(self):
        node1 = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_eq_image_node(self):
        node1 = TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png")
        node2 = TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png")
        self.assertEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a code node", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("docs", TextType.LINK, "https://a.example")
        node2 = TextNode("docs", TextType.LINK, "https://b.example")
        self.assertNotEqual(node1, node2)

    def test_not_eq_url_vs_none(self):
        node1 = TextNode("docs", TextType.LINK, "https://a.example")
        node2 = TextNode("docs", TextType.LINK, None)
        self.assertNotEqual(node1, node2)


class TestTextNodeRepresentation(unittest.TestCase):
    """Tests covering string representation (__repr__) logic."""

    def test_repr_with_url(self):
        node = TextNode(
            "This is some link text",
            TextType.LINK,
            "https://www.boot.dev",
        )
        self.assertEqual(
            repr(node),
            "TextNode(text='This is some link text', text_type='link', url='https://www.boot.dev')",
        )

    def test_repr_without_url(self):
        node = TextNode("Header text", TextType.TEXT)
        self.assertEqual(
            repr(node),
            "TextNode(text='Header text', text_type='text', url=None)",
        )


if __name__ == "__main__":
    unittest.main()