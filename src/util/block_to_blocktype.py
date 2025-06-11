from typing import List
from enums.blocktype import BlockType

def is_ordered_list(lines: List[str]) -> bool:
    for index, line in enumerate(lines):
        line_number = index + 1
        if not line.startswith(f"{line_number}. "):
            return False

    return True

def is_heading(block: str):
    if "# " not in block:
        return False
    
    return block.startswith("#") and block.index("# ") < 6

def block_to_blocktype(block_markdown: str) -> BlockType:
    if is_heading(block_markdown): return BlockType.Heading
    if block_markdown.startswith("```") and block_markdown.endswith("```"): return BlockType.Code

    lines = block_markdown.split("\n")
    quotes = list(filter(lambda x: x.startswith("> "), lines))
    if len(quotes) == len(lines):
        return BlockType.Quote
    
    unordered_list = list(filter(lambda x: x.startswith("- "), lines))
    if len(unordered_list) == len(lines):
        return BlockType.UnorderedList
    
    if is_ordered_list(lines):
        return BlockType.OrderedList

    return BlockType.Paragraph