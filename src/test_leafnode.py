import unittest
from leafnode import LeafNode


class TestLeafNodeToHtml(unittest.TestCase):
    """Tests for LeafNode.to_html()."""

    def setUp(self) -> None:
        self.value = LeafNode(None,"This is a paragraph of text.")
        self.value_tag = LeafNode(
            "p", 
            "This is a paragraph of text."
        )
        self.value_tag_prop = LeafNode(
            "a", 
            "Click me!", 
            {"href": "https://www.google.com"}
        )
        self.no_value = LeafNode(
            "a",
            None
        )

    def test_to_html_onlyValue(self):
        self.assertEqual(
            self.value.to_html(), 
            'This is a paragraph of text.'
        )

    def test_to_html_duo(self):
        self.assertEqual(
            self.value_tag.to_html(),
            '<p>This is a paragraph of text.</p>',
        )

    def test_to_html_triple(self):
        self.assertEqual(
            self.value_tag_prop.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_to_html_no_value(self):
        with self.assertRaises(ValueError) as cm:
            self.no_value.to_html()
        self.assertEqual(str(cm.exception), "All leaf nodes must have a value.")  

class TestLeafNodeRepresentation(unittest.TestCase):
    """Tests for LeafNode.__repr__()."""

    def setUp(self) -> None:
        self.value = LeafNode(None,"This is a paragraph of text.")
        self.value_tag = LeafNode(
            "p", 
            "This is a paragraph of text."
        )
        self.value_tag_prop = LeafNode(
            "a", 
            "Click me!", 
            {"href": "https://www.google.com"}
        )
        self.noValue = LeafNode(
            "a",
            None
        )

    def test_repr_noValue(self):
        self.assertEqual(
            repr(self.noValue),
            "LeafNode(tag='a', value=None, props=None)"
        )

    def test_repr_onlyValue(self):
        self.assertEqual(
            repr(self.value), 
            "LeafNode(tag=None, value='This is a paragraph of text.', props=None)"
        )
    
    def test_repr_duo(self):
        self.assertEqual(
            repr(self.value_tag),
            "LeafNode(tag='p', value='This is a paragraph of text.', props=None)"
        )
    
    def test_repr_triple(self):
        expected_repr = (
            "LeafNode(tag='a', value='Click me!', "
            "props={'href': 'https://www.google.com'})"
        )
        self.assertEqual(repr(self.value_tag_prop), expected_repr)


if __name__ == "__main__":
    unittest.main()