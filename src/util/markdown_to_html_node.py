from enums.blocktype import BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from util.block_to_blocktype import block_to_blocktype
from util.util import markdown_to_blocks, text_node_to_html_node, text_to_textnodes

def get_block_type(blocktype: BlockType):
    match blocktype:
        case BlockType.Code: return "code"
        case _: pass
    return "p"

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_blocktype(block)
        current_block = ParentNode(get_block_type(block_type), [])
        text_nodes = text_to_textnodes(block)
        for text in text_nodes:
            html_node = text_node_to_html_node(text)
            current_block.children.append(html_node) # type: ignore
        
        parent_node.children.append(current_block) # type: ignore
    
    print("Returning: ", parent_node)
    return parent_node

