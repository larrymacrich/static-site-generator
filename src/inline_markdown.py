import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)

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
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)
        if not images:
            new_nodes.append(old_node)
            continue

        for image_alt, image_url in images:
            text, remaining_text = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)
        if not links:
            new_nodes.append(old_node)
            continue

        for link_alt, link_url in links:
            text, remaining_text = remaining_text.split(f"[{link_alt}]({link_url})", 1)
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes