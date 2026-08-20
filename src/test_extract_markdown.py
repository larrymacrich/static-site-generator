import unittest
from extract_markdown import extract_markdown_images, extract_markdown_links


class test_extract_markdown_images(unittest.TestCase):
    """Tests for extract_markdown_images()"""
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
    """Tests for extract_markdown_links()"""
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