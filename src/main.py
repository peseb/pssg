import os
import shutil
from util.extract_title import extract_title
from util.markdown_to_html_node import markdown_to_html_node

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    markdown = f.read()
    f.close()
    f = open(template_path)
    template = f.read()
    f.close()

    html = markdown_to_html_node(markdown).to_html()
    print("HTML: ", html)
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dirname = os.path.dirname(dest_path)
    
    os.makedirs(dirname, 511, True)
    f = open(dest_path, "x")
    f.write(template)




def copy_to_public():
    destination = "public"
    src_dir = "static"
    public_exists = os.path.exists(destination)
    if public_exists:
        shutil.rmtree(destination)
    
    shutil.copytree(src_dir, destination)

def main():
    copy_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

main()