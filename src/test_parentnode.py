import unittest
from parentnode import ParentNode
from leafnode import  LeafNode

class TestParentNodeToHtml(unittest.TestCase):
    """Tests for parentNode.to_html()."""

    def setUp(self) -> None:
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        self.parent_node = ParentNode(
            "span",
            children,
        )
        self.no_children = ParentNode(
             "span",
             children=None,
        )
        self.empty_children = ParentNode(
            "span",
            children=[],
        )
        self.no_tag = ParentNode(
            None,
            children,
        )
        self.grandparent_node = ParentNode(
            "div",
            [self.parent_node],
        )
        self.with_props = ParentNode(
            "a",
            [LeafNode("b", "Bold text")],
            {"href": "https://www.google.com"},
        )

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError) as cm:
            self.no_children.to_html()
        self.assertEqual(str(cm.exception), "All parent nodes must have children.")

    def test_to_html_empty_children(self):
        self.assertEqual(
            self.empty_children.to_html(),
            "<span></span>"
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError) as cm:
            self.no_tag.to_html()
        self.assertEqual(str(cm.exception), "All parent nodes must have a tag.")  

    def test_to_html_with_children(self):
        self.assertEqual(
            self.parent_node.to_html(),
            '<span><b>Bold text</b>Normal text<i>italic text</i>Normal text</span>'
        )

    def test_to_html_with_grandchildren(self):
        self.assertEqual(
            self.grandparent_node.to_html(),
            '<div><span><b>Bold text</b>Normal text<i>italic text</i>Normal text</span></div>'
        )

    def test_to_html_with_props(self):
        self.assertEqual(
            self.with_props.to_html(),
            '<a href="https://www.google.com"><b>Bold text</b></a>',
        )