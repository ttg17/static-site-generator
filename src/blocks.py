import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split('\n\n')
    clean_blocks = [cleaned for x in blocks if (cleaned := x.strip())]
    return clean_blocks


def block_to_block_type(block: str) -> BlockType:
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    elif block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    elif block.startswith('>'):
        return BlockType.QUOTE
    elif block.startswith('- '):
        return BlockType.UNORDERED_LIST
    elif block.startswith('1. '):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH



def markdown_to_html_node(markdown: str) -> ParentNode:
    core_children: list[HTMLNode] = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            text = ' '.join(block.splitlines())
            core_children.append(ParentNode('p', text_to_children(text)))
        elif block_type == BlockType.HEADING:
            heading = re.match(r'^(#{1,6})\s+(.*)$', block, re.DOTALL)
            if heading is None:
                raise ValueError(f'Invalid heading block: {block}')
            tag = f'h{len(heading.group(1))}'
            core_children.append(ParentNode(tag, text_to_children(heading.group(2))))
        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            code_node = text_node_to_html_node(TextNode(code_text, TextType.CODE))
            core_children.append(ParentNode('pre', [code_node]))
        elif block_type == BlockType.QUOTE:
            quote_lines = [line[1:].lstrip() for line in block.splitlines()]
            quote_text = '\n'.join(quote_lines)
            core_children.append(ParentNode('blockquote', text_to_children(quote_text)))
        elif block_type == BlockType.UNORDERED_LIST:
            items: list[HTMLNode] = [
                ParentNode('li', text_to_children(line[2:]))
                for line in block.splitlines()
            ]
            core_children.append(ParentNode('ul', items))
        elif block_type == BlockType.ORDERED_LIST:
            items: list[HTMLNode] = []
            for line in block.splitlines():
                item_text = re.sub(r'^\d+\.\s+', '', line, count=1)
                items.append(ParentNode('li', text_to_children(item_text)))
            core_children.append(ParentNode('ol', items))

    return ParentNode('div', core_children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes


# def block_type_tag(block_text: str, block_type: BlockType):
#     if block_type == BlockType.HEADING:
#         for i in range(6, 0, -1):
#             if block_text.startswith('#' * i):
#                 tag = '#' * i
#                 return tag
#     elif block_type == BlockType.QUOTE:
#         return 'blockquote'
#     elif block_type == BlockType.UNORDERED_LIST:
#         return 'ul'