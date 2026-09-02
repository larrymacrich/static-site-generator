from textnode import TextNode, TextType
from copystatic import copystatic
from gencontent import generate_page

def main():
    copystatic()
    generate_page(
        'content/index.md',
        'template.html',
        'public/index.html'
    )


if __name__ == "__main__":
    main()