from textnode import TextNode, TextType


def main():
    textNode = TextNode("Random text", TextType.Link, "https://cool.dev")
    print(textNode)

main()