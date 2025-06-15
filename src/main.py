import sys
from util.util import copy_to_public, generate_pages_recursive



def main():
    basepath = "/"
    args = sys.argv
    if len(args) > 0:
        basepath = args[0]
    

    copy_to_public()
    generate_pages_recursive(basepath, "content", "template.html", "public")

main()