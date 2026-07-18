import shutil
import os
from blocks import markdown_to_html_node
from htmlnode import ParentNode

def main():
    copy_dir("static", "public")
    parse_dir_and_generate("content", "public")


def parse_dir_and_generate(dir: str, new_dir: str):
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            generate_page(os.path.join(dir, item), "template.html", os.path.join(new_dir, item.replace(".md", ".html")))
        else: 
            parse_dir_and_generate(os.path.join(dir, item),os.path.join(new_dir, item))


def copy_dir(src: str, dest: str):
    for item in os.listdir(dest):
        if os.path.isfile(os.path.join(dest, item)):
            os.remove(os.path.join(dest, item))
        elif os.path.isdir(os.path.join(dest, item)):
            shutil.rmtree(os.path.join(dest, item))
    shutil.copytree(src, dest, dirs_exist_ok=True)

def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()
    raise ValueError("No title found")

def generate_page(src, template, dest):
    print(f"Generating page from {src} to {dest}")
    with open(src, "r") as file:
        markdown = file.read()
    with open(template, "r") as file:
        template = file.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    
    if not os.path.exists(os.path.dirname(dest)):
        os.makedirs(os.path.dirname(dest))
    with open(dest, "w") as file:
        file.write(template)




if __name__ == "__main__":
    main()

