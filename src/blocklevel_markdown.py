from enum import Enum
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