class HTMLNode():

    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            children: list[HTMLNode] | None = None, 
            props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("WIP")

    def props_to_html(self) -> str:
        props_str = ''
        if self.props is not None:
            for prop_k, prop_v in self.props.items():
                props_str += f' {prop_k}="{prop_v}"'
        return props_str

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )