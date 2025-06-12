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
        if (block_type == BlockType.Code):
            pre_tag = ParentNode("pre", [])
            pre_tag.children.append(current_block) # type: ignore
            parent_node.children.append(pre_tag) # type: ignore

        else:
            parent_node.children.append(current_block) # type: ignore

        print("BLOCK: ", block)
        text_nodes = text_to_textnodes(block)
        print("block: ", block)
        print("text_nodes: ", text_nodes)
        for text in text_nodes:
            html_node = text_node_to_html_node(text)
            print("HTML NODE: ", html_node)
            print("HTML NODE: tohtml", html_node.to_html())
            current_block.children.append(html_node) # type: ignore
        
        
    
    return parent_node

