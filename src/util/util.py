import re
from typing import List, Tuple
from htmlnode import HTMLNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from util.block_to_blocktype import block_to_blocktype

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes: List[TextNode]):
    result: List[TextNode] = []
    for node in old_nodes:
        nodes = get_nodes(node, TextType.Link)
        result.extend(nodes)

    return result

def split_nodes_image(old_nodes: List[TextNode]):
    result: List[TextNode] = []
    for node in old_nodes:
        nodes = get_nodes(node, TextType.Image)
        result.extend(nodes)

    return result

def get_nodes(node: TextNode, text_type: TextType):
    valid_text_types = [TextType.Image, TextType.Link]
    if text_type not in valid_text_types:
        raise ValueError(f"TextType must be one of {valid_text_types}")
    
    text = node.text
    get_matches = extract_markdown_images if text_type is TextType.Image else extract_markdown_links
    matches = get_matches(text)
    result: List[TextNode] = []
    if len(matches) == 0:
        result.append(node)
    else:
        for match in matches:
            prefix = "!" if text_type is TextType.Image else ""
            image_start_index = text.index(f"{prefix}[{match[0]}]")
            text_upto_image = text[:image_start_index]

            result.append(TextNode(text_upto_image, TextType.Text))
            image_text = match[0]
            image_url = match[1]
            result.append(TextNode(image_text, text_type, image_url))

            image_url_end = f"{image_url})"
            image_end_index = text.index(image_url_end) + len(image_url_end)
            text = text[image_end_index:]
        if len(text) > 0:
            result.append(TextNode(text, TextType.Text))
        
    return result

def text_node_to_html_node(textnode: TextNode) -> HTMLNode:
    text = textnode.text.removeprefix("\n")
    match textnode.text_type:
        case TextType.Text:
            return LeafNode(None, text.replace("\n", " "))
        case TextType.Bold:
            return LeafNode("b", text)
        case TextType.Italic:
            return LeafNode("i", text)
        case TextType.Link:
            return LeafNode("a", text)
        case TextType.Code:
            return LeafNode("code", text)
        case TextType.Image:
            src = textnode.url if textnode.url != None else ""
            return LeafNode("img", "", {"alt": text, "src": src})
        case _: pass
    
    raise Exception(f"Invalid TextType: {textnode.text_type}")


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    result: List[TextNode] = []
    for node in old_nodes:
        text = node.text
        if node.text_type == TextType.Code:
            result.append(node)
            continue
        if delimiter not in text:
            result.append(node)
            continue

        while delimiter in text:
            next_delimiter = text.index(delimiter)
            is_even_delimiter_count = text.count(delimiter) % 2 == 0  
            current_text_type = TextType.Text if is_even_delimiter_count else text_type

            current_text = text[:next_delimiter]
            if len(current_text) > 0:
                result.append(TextNode(current_text, current_text_type))

            text = text[next_delimiter + len(delimiter):]

        if len(text) > 0:
            result.append(TextNode(text, TextType.Text))
    
    return result

def text_to_textnodes(text: str) -> List[TextNode]:
    old_nodes: List[TextNode] = []
    new_nodes: List[TextNode] = [TextNode(text, TextType.Text)]
    while len(old_nodes) != len(new_nodes):
        old_nodes = new_nodes.copy()
        generated_nodes: List[TextNode] = []

        generated_nodes = split_nodes_delimiter(old_nodes, "```", TextType.Code)
        generated_nodes = split_nodes_delimiter(generated_nodes, "`", TextType.Code)
        generated_nodes = split_nodes_delimiter(generated_nodes, "_", TextType.Italic)
        generated_nodes = split_nodes_delimiter(generated_nodes, "**", TextType.Bold)
        generated_nodes = split_nodes_image(generated_nodes)
        generated_nodes = split_nodes_link(generated_nodes)

        new_nodes = (generated_nodes).copy()


    return new_nodes

def strip_block(block: str):
    return "\n".join(list(filter(lambda x: x != "", map(lambda x: x.strip(), block.split("\n")))))

def markdown_to_blocks(markdown: str):
    return list(filter(lambda x: x != "", list(map(strip_block, markdown.split("\n\n")))))