from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str,  props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, [], props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        
        value = self.value
        if self.tag == "p":
            value = self.value.replace("\n", "")

        props = self.props_to_html()
        return f"<{self.tag}{f" {props}" if len(props) > 0 else ""}>{value}</{self.tag}>"