from __future__ import annotations

from textnode import TextNode
import re
from enums import TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    output: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        new_nodes = split_node(node.text, delimiter, text_type)
        output.extend(new_nodes)
    return output


def split_node(text: str, delimiter: str, text_type: TextType):
    output = []
    split = text.split(delimiter)
    if len(split) % 2 == 0:
        raise ValueError("No matching delimiter")
    
    for i in range(0, len(split)):
        if i % 2 == 0:
            output.append(TextNode(split[i], TextType.TEXT))
        else:
            output.append(TextNode(split[i], text_type))
    return output

def extract_markdown_images(text: str) ->list[tuple[str, str]]:
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_regex, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)


def split_nodes_image(old_nodes: list[TextNode]):
    output = []
    full_image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
            
        text_segments = re.split(full_image_regex, node.text)
        image_data = extract_markdown_images(node.text) 
        
        for i in range(len(image_data)):
            if text_segments[i]: 
                output.append(TextNode(text_segments[i], TextType.TEXT))    
            alt, url = image_data[i]
            output.append(TextNode(alt, TextType.IMAGE, url))
            
        if text_segments[-1]:
            output.append(TextNode(text_segments[-1], TextType.TEXT))
            
    return output
    
def split_nodes_link(old_nodes: list[TextNode]):
    output = []
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
            
        text_segments = re.split(link_regex, node.text)
        link_data = extract_markdown_links(node.text) 
        
        for i in range(len(link_data)):
            if text_segments[i]: 
                output.append(TextNode(text_segments[i], TextType.TEXT))    
            alt, url = link_data[i]
            output.append(TextNode(alt, TextType.LINK, url))
       
        if text_segments[-1]:
            output.append(TextNode(text_segments[-1], TextType.TEXT))
            
    return output    

def text_to_textnodes(text: str):
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in delimiters.items():
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes