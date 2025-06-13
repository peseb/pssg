import os
import shutil
from textnode import TextNode, TextType

def copy_to_public():
    destination = "public"
    src_dir = "static"
    public_exists = os.path.exists(destination)
    if public_exists:
        shutil.rmtree(destination)
    
    shutil.copytree(src_dir, destination)

def main():
    copy_to_public()
    textNode = TextNode("Random text", TextType.Link, "https://cool.dev")
    print(textNode)

main()