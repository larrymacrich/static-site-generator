import unittest
from htmlnode import HTMLNode


class TestHTMLNodeProps(unittest.TestCase):
    """Tests for HTMLNode.props_to_html()."""

    def setUp(self) -> None:
        self.props_empty = {}
        self.props_single = {"target": "_blank"}
        self.props_multi = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        self.node_props_empty = HTMLNode(props=self.props_empty)
        self.node_props_single = HTMLNode(props=self.props_single)
        self.node_props_multi = HTMLNode(props=self.props_multi)

    def test_props_to_html_empty(self):
        self.assertEqual(self.node_props_empty.props_to_html(), "")

    def test_props_to_html_single(self):
        self.assertEqual(
            self.node_props_single.props_to_html(),
            ' target="_blank"',
        )

    def test_props_to_html_multi(self):
        self.assertEqual(
            self.node_props_multi.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )


class TestHTMLNodeRepresentation(unittest.TestCase):
    """Tests for HTMLNode.__repr__()."""

    def setUp(self) -> None:
        self.props_single = {"target": "_blank"}
        self.props_multi = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

        self.node_empty = HTMLNode()
        self.node_tag = HTMLNode(tag="p")
        self.node_paragraph = HTMLNode(value="First Paragraph")

        self.tag_value_and_props_multi = HTMLNode(
            tag="p",
            value="First Paragraph",
            props=self.props_multi,
        )

        self.children_two_tag_value_and_props_multi = [
            self.tag_value_and_props_multi
        ]

        self.node_children = HTMLNode(
            tag="p",
            value="First Paragraph",
            props=self.props_single,
            children=self.children_two_tag_value_and_props_multi,
        )

    def test_repr_empty(self):
        self.assertEqual(
            repr(self.node_empty), 
            "HTMLNode(tag=None, value=None, children=None, props=None)"
        )

    def test_repr_tag(self):
        self.assertEqual(
            repr(self.node_tag), 
            "HTMLNode(tag='p', value=None, children=None, props=None)"
        )

    def test_repr_paragraph(self):
        self.assertEqual(
            repr(self.node_paragraph), 
            "HTMLNode(tag=None, value='First Paragraph', children=None, props=None)"
        )

    def test_repr_children(self):
        expected_repr = (
            "HTMLNode(tag='p', value='First Paragraph', "
            "children=[HTMLNode(tag='p', value='First Paragraph', children=None, props={'href': 'https://www.google.com', 'target': '_blank'})], "
            "props={'target': '_blank'})"
        )
        self.assertEqual(repr(self.node_children), expected_repr)


class TestHTMLNodeAttributes(unittest.TestCase):
    """Tests for direct HTMLNode attribute assignments and defaults."""

    def test_node_attributes(self):
        node = HTMLNode(
            tag="p",
            value="Hello world",
            children=[],
            props={"class": "main"},
        )
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello world")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "main"})

    def test_default_attributes_are_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()