import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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

class TestTextNodeToHTML(unittest.TestCase):
    """Tests for TextNode.text_node_to_html_node()"""

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self):
        node = TextNode("An alt description", TextType.IMAGE, "https://boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/image.png", "alt": "An alt description"})

    def test_invalid_type_raises(self):
        node = TextNode("Bad type", "not_a_real_type")
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()