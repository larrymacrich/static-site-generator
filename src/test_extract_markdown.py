import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class test_extract_markdown_images(unittest.TestCase):
    """Tests for inline_markdown.extract_markdown_images()"""
    def test_extract_markdown_images_with_image_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_images_with_link_text(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            []
        )

    def test_extract_markdown_images_with_no_images(self):
        text = "This is plain text with no images at all."
        self.assertEqual(
            extract_markdown_images(text),
            []
        )

    def test_extract_markdown_images_with_multiple_images(self):
        text = "![first](https://example.com/1.png) some text ![second](https://example.com/2.png) more text ![third](https://example.com/3.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("first", "https://example.com/1.png"),
                ("second", "https://example.com/2.png"),
                ("third", "https://example.com/3.png"),
            ]
        )

class test_extract_markdown_links(unittest.TestCase):
    """Tests for inline_markdown.extract_markdown_links()"""
    def test_extract_markdown_links_with_link_text(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_markdown_links_with_image_text(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_links(text),
            []
        )
    def test_extract_markdown_links_with_no_links(self):
        text = "This is plain text with no links at all."
        self.assertEqual(
            extract_markdown_links(text),
            []
        )

    def test_extract_markdown_links_with_multiple_links(self):
        text = "[first](https://example.com/1) some text [second](https://example.com/2) more text [third](https://example.com/3)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("first", "https://example.com/1"),
                ("second", "https://example.com/2"),
                ("third", "https://example.com/3"),
            ]
        )

class TestTextNodeSplitNodesDelimiter(unittest.TestCase):
    """Tests for inline_markdown.split_nodes_delimiter()"""

    def test_empty_list(self):
        node = []
        self.assertEqual(
            [node],
            [[]]
    )
        
    def test_code_type(self):
        node = TextNode("This is text with a `code block word`", TextType.CODE)
        self.assertEqual(
            [node],
            [TextNode("This is text with a `code block word`", TextType.CODE)]
        )

    def test_delimiter_open(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(cm.exception), 
            f"No closing of given delimter in:\n{node}"
        )  

    def test_delimiter_enclosed(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_beginning(self):
        node = TextNode("`This is` text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is", TextType.CODE),
            TextNode(" text with a code block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_end(self):
        node = TextNode("This is text with a code `block word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a code ", TextType.TEXT),
            TextNode("block word", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_empty_delimiter_(self):
        node = TextNode("This is text with a `` code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode(" code block word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_delimiter_in_one_text(self):
        node = TextNode("This has `code one` and `code two` in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("code two", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

class TestTextNodeSplitNodesImage(unittest.TestCase):
    """Tests for inline_markdown.split_nodes_image()"""

    def test_split_images_with_one_image_at_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This is text with an ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an ", TextType.TEXT),
            ],
        )

    def test_split_images_with_one_image_inbetween(self):
        node = TextNode(
            "This is text ![image](https://i.imgur.com/zjjcJKZ.png) with an ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" with an ", TextType.TEXT),
            ],
        )

    def test_split_images_with_one_image_at_end(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_images_with_two_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_split_images_with_mixed_image_and_link(self):
        node = TextNode(
            "Here is ![img](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
    )

    def test_split_images_with_multiple_nodes(self):
        node1 = TextNode("This is a text with no images", TextType.TEXT)
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with no images", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [node],
        )

    def test_split_images_with_text(self):
        node = TextNode(
            "This is a text ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [node],
        )

class TestTextNodeSplitNodesLink(unittest.TestCase):
    """Tests for inline_markdown.split_nodes_link()"""

    def test_split_link_with_one_link_at_beginning(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) This is text with an ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" This is text with an ", TextType.TEXT),
            ],
        )

    def test_split_link_with_one_link_inbetween(self):
        node = TextNode(
            "This is text [link](https://i.imgur.com/zjjcJKZ.png) with an ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" with an ", TextType.TEXT),
            ],
        )

    def test_split_link_with_one_link_at_end(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_link_with_two_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
        )

    def test_split_link_with_mixed_image_and_link(self):
        node = TextNode(
            "Here is ![img](https://i.imgur.com/zjjcJKZ.png) and a [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here is ![img](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
    )

    def test_split_link_with_multiple_nodes(self):
        node1 = TextNode("This is a text with no images", TextType.TEXT)
        node2 = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with no images", TextType.TEXT),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_split_link_with_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [node],
        )

    def test_split_link_with_text(self):
        node = TextNode(
            "This is a text ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [node],
        )