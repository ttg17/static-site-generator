import os
import shutil
import sys

from blocks import markdown_to_html_node


def copy_recursive(src: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_recursive(src_path, dest_path)



def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
            
    raise Exception("No H1 header found in markdown document")  # noqa: TRY002


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    html_content = html_content.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(file_path):
            generate_page(file_path, template_path, dest_path[:-2]+'html', basepath)
        else:
            generate_pages_recursive(file_path, template_path, dest_path, basepath)



def main():
    # copy the files from static to docs
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_recursive("static", "docs")

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    generate_pages_recursive("content/", "template.html", "docs/", basepath)
    

main()
