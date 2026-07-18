from __future__ import annotations

from enum import Enum, auto
import re
from utils import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
from htmlnode import ParentNode, LeafNode


class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()
    

def block_to_block_type(block: str) -> BlockType:
    heading_regex = r"^#{1,6} "
    code_regex = r"^```[\s\S]*```$"
    
    # Check the first line for structural prefixes
    lines = block.split("\n")
    first_line = lines[0]

    if re.match(heading_regex, first_line):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if first_line.startswith(">"):
        return BlockType.QUOTE
    if first_line.startswith("- ") or first_line.startswith("* "):
        return BlockType.UNORDERED_LIST
    if re.match(r"^\d+\. ", first_line):
        return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            cleaned_blocks.append(stripped)
    return cleaned_blocks


def markdown_to_html_node(markdown: str) -> ParentNode:
    html_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        match block_type:
            case BlockType.PARAGRAPH:
                block_nodes.append(to_paragraph(block))
            case BlockType.HEADING:
                block_nodes.append(to_heading(block))
            case BlockType.CODE:
                block_nodes.append(to_code(block))
            case BlockType.QUOTE:
                block_nodes.append(to_quote(block))
            case BlockType.UNORDERED_LIST:
                block_nodes.append(to_unordered_list(block))
            case BlockType.ORDERED_LIST:
                block_nodes.append(to_ordered_list(block))
                
    html_node.children = block_nodes
    return html_node


def to_paragraph(block: str) -> ParentNode:
    clean_text = " ".join(block.split())
    block_text_nodes = text_to_textnodes(clean_text)
    html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
    return ParentNode("p", html_nodes)


def to_heading(block: str) -> ParentNode:
    level = len(block) - len(block.lstrip('#'))
    text_content = block[level:].strip()
    
    clean_text = " ".join(text_content.split())
    block_text_nodes = text_to_textnodes(clean_text)
    html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
    return ParentNode(f"h{level}", html_nodes)


def to_code(block: str) -> ParentNode:
    lines = block.split("\n")
    if lines and lines[0].startswith("```"):
        lines.pop(0)
    if lines and lines[-1].endswith("```"):
        lines.pop()
    cleaned_lines = [line.strip() for line in lines]
    block_text = "\n".join(cleaned_lines) + "\n"

    block_text_nodes = [TextNode(block_text, TextType.TEXT)]
    html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
    return ParentNode("pre", [ParentNode("code", html_nodes)])


def to_quote(block: str) -> ParentNode:
    # Strip '>' character from every line of a multi-line quote block
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        if line.startswith(">"):
            cleaned_lines.append(line[1:].strip())
        else:
            cleaned_lines.append(line.strip())
            
    clean_text = " ".join(" ".join(cleaned_lines).split())
    block_text_nodes = text_to_textnodes(clean_text)
    html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
    return ParentNode("blockquote", html_nodes)


def to_unordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Match list syntax markers
        text_content = re.sub(r"^[-*]\s+", "", line).strip()
        block_text_nodes = text_to_textnodes(text_content)
        html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
        li_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ul", li_nodes)


def to_ordered_list(block: str) -> ParentNode:
    lines = block.split("\n")
    li_nodes = []
    for line in lines:
        # Strip digits followed by period and space
        text_content = re.sub(r"^\d+\.\s+", "", line).strip()
        block_text_nodes = text_to_textnodes(text_content)
        html_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
        li_nodes.append(ParentNode("li", html_nodes))
    return ParentNode("ol", li_nodes)