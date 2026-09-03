from os import makedirs, listdir, mkdir
from os.path import dirname, isfile, join
from blocklevel_markdown import markdown_to_html_node, extract_title

def generate_page(from_path: str, tmp_path: str, dst_path: str, basepath: str):
    print(f'Generating page from {from_path} to {dst_path} using {tmp_path}')
    with open(from_path, "r") as f:
        md_file = f.read()
    with open(tmp_path, "r") as f:
        tmp_file = f.read()
    md_content = markdown_to_html_node(md_file).to_html()
    md_title = extract_title(md_file)
    html_file = (
        tmp_file
        .replace('{{ Title }}', md_title)
        .replace('{{ Content }}', md_content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )
    dir_dst_path = dirname(dst_path)
    makedirs(dir_dst_path, exist_ok=True)
    with open(dst_path, "w") as f:
        f.write(html_file)

def generate_pages(basepath: str):
    target = 'docs'
    generate_pages_recursive('content', 'template.html', target, basepath)

def generate_pages_recursive(dir_path_content: str, tmp_path: str, dst_dir_path: str, basepath: str):
    entry_names = listdir(dir_path_content)
    for entry_name  in entry_names:
            dir_path = join(dir_path_content, entry_name )
            dst_path = join(dst_dir_path, entry_name )
            if isfile(dir_path):
                dst_path = dst_path.replace('.md', '.html')
                generate_page(dir_path, tmp_path, dst_path, basepath)
            else:
                print(f"Creating new directory: '{dst_path}'")
                mkdir(dst_path)
                generate_pages_recursive(dir_path, tmp_path ,dst_path, basepath)