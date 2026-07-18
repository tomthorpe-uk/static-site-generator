from __future__ import annotations

class HTMLNode():
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict[str,str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        output = ""
        for prop, value in self.props.items():
            output += f' {prop}="{value}"'
        return output
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: dict[str,str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value and self.tag != "img":
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str,str] = None):
        super().__init__(tag, None,children, props)

    def to_html(self):
        if self.children == []:
            raise ValueError("ParentNode must have children")
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        return f"<{self.tag}{self.props_to_html()}>" + "".join([child.to_html() for child in self.children]) + f"</{self.tag}>"
    
