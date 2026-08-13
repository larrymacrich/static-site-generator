from textnode import TextNode, TextType


def main():
    text = "This is some anchor text"
    text_type =  TextType.LINK
    url = "https://www.boot.dev"
    t_node = TextNode(text, text_type, url)
    print(t_node)


if __name__ == "__main__":
    main()