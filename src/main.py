from textnode import TextNode, TextType
from copystatic import copystatic
from gencontent import generate_page, generate_pages

def main():
    copystatic()
    generate_pages()


if __name__ == "__main__":
    main()