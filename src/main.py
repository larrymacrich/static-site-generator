from sys import argv
from copystatic import copystatic
from gencontent import generate_pages

def main(argv):
    if len(argv) > 1:
        basepath = argv[1]
    else:
        basepath = '/'
    copystatic()
    generate_pages(basepath)


if __name__ == "__main__":
    main(argv)