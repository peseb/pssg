import os
import shutil
import sys

from util.extract_title import extract_title
from util.markdown_to_html_node import markdown_to_html_node

def generate_pages_recursive(basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.isfile(dir_path_content):
        path = os.path.join(dest_dir_path.replace(".md", ".html"))
        generate_page(basepath, dir_path_content, template_path, path)
    else:
        dir = os.listdir(dir_path_content)
        for entry in dir:
            content_path = os.path.join(dir_path_content, entry)
            dest_path = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(basepath, content_path, template_path, dest_path)

def generate_page(basepath: str, from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    markdown = f.read()
    f.close()
    f = open(template_path)
    template = f.read()
    f.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")

    dirname = os.path.dirname(dest_path)
    
    os.makedirs(dirname, 511, True)
    f = open(dest_path, "x")
    f.write(template)

def copy_to_public():
    destination = "docs"
    src_dir = "static"
    public_exists = os.path.exists(destination)
    if public_exists:
        shutil.rmtree(destination)
    
    shutil.copytree(src_dir, destination)



def main():
    basepath = "/"
    args = sys.argv
    print(args)
    if len(args) > 1:
        basepath = args[1]

    copy_to_public()
    generate_pages_recursive(basepath, "content", "template.html", "docs")

main()