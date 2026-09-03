````markdown
# Static Site Generator

A lightweight static site generator built with Python. It converts Markdown files into styled HTML pages using reusable templates and static assets.

## Features

- Markdown-to-HTML conversion
- Reusable HTML templates
- Custom CSS styling
- Code block syntax highlighting
- Static asset copying
- Automatic output directory generation
- Support for nested content pages

## Requirements

- Python 3.10 or newer
- Git

## Getting Started

Clone the repository:

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
````

Generate the website:

```bash
python3 src/main.py
```

Generated files are placed in the `public/` directory.

## Preview the Website

Start a local web server:

```bash
python3 -m http.server 8888 --directory public
```

Open [http://localhost:8888](http://localhost:8888/) in your browser.

## Project Structure

```text
.
├── content/       # Markdown source files
├── doc/        # Generated HTML files
├── src/           # Python source code
├── static/        # CSS and other static assets
├── template.html  # HTML page template
└── README.md      # Project documentation
```

## Customization

- Add or edit Markdown files in `content/`.
- Update styles in `static/`.
- Modify `template.html` to change page layouts.
- Extend the generator inside `src/`.

## Rebuilding the Website

```bash
rm -rf public/*
python3 src/main.py
```

## Learning Goals

This project practices file handling, directory management, Markdown parsing, HTML generation, static asset management, and Python application design.

## Credits

Built as part of the [Boot.dev Build a Static Site Generator in Python](https://www.boot.dev/courses/build-static-site-generator-python) course.

## License

This project is available for educational and personal use.
