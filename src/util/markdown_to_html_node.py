from enums.blocktype import BlockType
from htmlnode import HTMLNode
from parentnode import ParentNode
from util.block_to_blocktype import block_to_blocktype
from util.util import markdown_to_blocks, text_node_to_html_node, text_to_textnodes

def get_block_type(blocktype: BlockType, block: str):
    match blocktype:
        case BlockType.Heading: return f"h{block.count("#", 0, 6)}"
        case BlockType.Code: return "pre"
        case BlockType.UnorderedList: return f"ul"
        case BlockType.OrderedList: return f"ol"
        case BlockType.Quote: return f"blockquote"
        case _: pass
    return "p"

def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_blocktype(block)
        surrounding_block = ParentNode(get_block_type(block_type, block), [])
        parent_node.children.append(surrounding_block) # type: ignore

        
        if block_type == BlockType.UnorderedList or block_type == BlockType.OrderedList:
            items = list(filter(lambda x: x, block.split("- ")))
            for item in items:
                text_nodes = text_to_textnodes(item)
                list_item_node = ParentNode("li", [])
                for text in text_nodes:
                    html_node = text_node_to_html_node(text)
                    list_item_node.children.append(html_node) # type: ignore
                    
                surrounding_block.children.append(list_item_node) # type: ignore
        else:
            print("ELSE")
            text_nodes = text_to_textnodes(block)
            for text in text_nodes:
                html_node = text_node_to_html_node(text)
                surrounding_block.children.append(html_node) # type: ignore
    
    return parent_node

