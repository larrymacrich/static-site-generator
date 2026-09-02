from os import makedirs
from os.path import dirname
from blocklevel_markdown import markdown_to_html_node, extract_title

def generate_page(from_path: str, tmp_path: str, dst_path: str):
    print(f'Generating page from {from_path} to {dst_path} using {tmp_path}')
    with open(from_path, "r") as f:
        md_file = f.read()
    with open(tmp_path, "r") as f:
        tmp_file = f.read()
    md_content = markdown_to_html_node(md_file).to_html()
    md_title = extract_title(md_file)
    html_file = tmp_file.replace('{{ Title }}', md_title).replace('{{ Content }}', md_content)
    dir_dst_path = dirname(dst_path)
    makedirs(dir_dst_path, exist_ok=True)
    with open(dst_path, "w") as f:
        f.write(html_file)