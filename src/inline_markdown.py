import re
from typing import Callable
from textnode import TextNode, TextType

def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [
        ('**',TextType.BOLD),
        ('_', TextType.ITALIC),
        ('`', TextType.CODE),
    ]
    for text_delimiter, text_type in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, text_delimiter, text_type)

    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    
    return new_nodes


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, 
        extract_markdown_images, 
        lambda alt, url: f"![{alt}]({url})", 
        TextType.IMAGE
    )

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes_by_pattern(
        old_nodes, 
        extract_markdown_links, 
        lambda alt, url: f"[{alt}]({url})", 
        TextType.LINK
    )

def _split_nodes_by_pattern(
    old_nodes: list[TextNode], 
    extract_matches: Callable[[str], list[tuple[str, str]]],
    build_delimiter: Callable[[str, str], str], 
    text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        matches = extract_matches(remaining_text)
        if not matches:
            new_nodes.append(old_node)
            continue

        for alt, url in matches:
            text, remaining_text = remaining_text.split(build_delimiter(alt, url), 1)
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(alt, text_type, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)