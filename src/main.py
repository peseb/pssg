from util.util import copy_to_public, generate_pages_recursive



def main():
    copy_to_public()
    generate_pages_recursive("content", "template.html", "public")

main()