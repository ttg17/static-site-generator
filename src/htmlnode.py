
class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('to_html method not implemented')

    def props_to_html(self):
        result = ''
        if self.props:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        elif not self.tag:
            return self.value
        else:
            result = f'<{self.tag}'
            if self.props:
                for prop in self.props:
                    result += f' {prop}="{self.props[prop]}"'
            result += f'>{self.value}</{self.tag}>'
            return result

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"



class ParentNode(HTMLNode):
    def __init__(self, tag: str | None, children: list[HTMLNode] | None, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag provided.")
        elif not self.children:
            raise ValueError("No children provided.")
        else:
            result = f'<{self.tag}>'
            for child in self.children:
                result += child.to_html()
            result += f'</{self.tag}>'
            return result