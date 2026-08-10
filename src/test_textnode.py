import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    # Test __eq___
    def test_eq_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a code node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("docs", TextType.LINK, "https://a.example")
        node2 = TextNode("docs", TextType.LINK, "https://b.example")
        self.assertNotEqual(node1, node2)

    def test_image_node(self):
        node1 = TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png")
        node2 = TextNode("diagram", TextType.IMAGE, "https://example.com/diagram.png")
        self.assertEqual(node1, node2)

    # Test __repr__
    def test_repr(self):
        node = TextNode(
            "This is some link text", 
            TextType.LINK, 
            "https://www.boot.dev"
        )
        self.assertEqual(
            repr(node), 
            "TextNode(This is some link text, link, https://www.boot.dev)"
        )

    
    

if __name__ == "__main__":
    unittest.main()