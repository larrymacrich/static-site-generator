from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        new_block = block.strip()
        if new_block:
            new_blocks.append(new_block)
    return new_blocks

def block_to_block_type(markdown: str) -> BlockType:
    block_type = BlockType.PARAGRAPH # deafult
    valid_heading = markdown.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### '))
    valid_code =  markdown.startswith('```\n') and markdown.endswith('```')
    if valid_heading: 
        block_type = BlockType.HEADING
    elif valid_code:
        block_type = BlockType.CODE
    lines = markdown.split("\n")
    valid_quote = all(
        line.startswith(('>')) 
        for line in lines
    )
    valid_unorderd_list = all(
        line.startswith('- ') 
        for line in lines
    )
    valid_ordered_list = all(
        line.startswith(f'{index}. ')
        for index, line in enumerate(lines, start=1)
    )
    if valid_quote:
        block_type = BlockType.QUOTE
    elif valid_unorderd_list: 
        block_type = BlockType.UNORDERED_LIST
    elif valid_ordered_list:
        block_type = BlockType.ORDERED_LIST
    return block_type

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block_type, block)
        children.append(block_node)
    tag = 'div'
    parent = ParentNode(
        tag,
        children
    )
    return parent

def block_to_html_node(block_type: BlockType, block: str) -> HTMLNode:
    match block_type:
        case BlockType.HEADING:
            hashes, text = block.split(maxsplit=1)
            hash_tag = f'h{hashes.count('#')}'
            children = text_to_children(text)
            block_node = ParentNode(
                hash_tag,
                children,
            )
        case BlockType.CODE:
            text = '\n'.join(block.split('\n')[1:-1])+'\n'
            child_tag = 'code'
            child = LeafNode(
                child_tag,
                text, 
            )
            parent_tag = 'pre'
            block_node = ParentNode(
                parent_tag,
                [child],
            )
        case BlockType.QUOTE:
            quote_tag = 'blockquote'
            text = ' '.join(
                line[1:].strip() for line in block.split('\n')
            )
            children = text_to_children(text)
            block_node = ParentNode(
                quote_tag,
                children, 
            )
        case BlockType.UNORDERED_LIST:
            child_tag = 'li'
            children = [
                ParentNode(
                    child_tag,
                    text_to_children(line[1:].strip()),
                ) for line in block.split('\n')
            ]
            parent_tag = 'ul'
            block_node = ParentNode(
                parent_tag,
                children,
            )
        case BlockType.ORDERED_LIST:
            child_tag = 'li'
            children = [
                ParentNode(
                    child_tag,
                    text_to_children(line.split('.', maxsplit=1)[1].strip()),
                ) for line in block.split('\n')
            ]
            parent_tag = 'ol'
            block_node = ParentNode(
                parent_tag,
                children,
            )
        case _: # paragraph
            tag = 'p'
            text = ' '.join(block.split('\n'))
            children = text_to_children(text)
            block_node = ParentNode(
                tag,
                children,
            )
    return block_node

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes